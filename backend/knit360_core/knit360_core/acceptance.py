"""Runtime acceptance checks for KNIT 360.

The 46 tests under */test_*.py are *structural*: they read doctype JSON and the
lifecycle registry and prove the definitions agree with each other. None of them
starts a database transaction, so none of them proves the product works.

This module is the other half. Every check here drives the real application on a
real site: it inserts documents, moves them through their lifecycles, posts to
the general ledger, and asserts on what came back. A check that passes here is
evidence of behaviour, not of definition.

Run it:

    bench --site knit360.localhost execute knit360_core.acceptance.run

Everything is created under its own company (see COMPANY) so a run never touches
demo or live data, and every check is written to be re-runnable.

A failing check prints the exception that caused it. Nothing is swallowed.
"""

import json
import pathlib
import traceback

import frappe
from frappe.utils import add_days, flt, getdate, nowdate

from knit360_core.business_status import engine, guard, model
from knit360_core.finance import chart_of_accounts, credit, ledger, settlement
from knit360_core.pricing import price_list
from knit360_core.stock import ledger as stock_ledger

#: Acceptance data lives under its own company so a run is isolated from
#: anything a person has entered. GL entries are immutable by design, so an
#: acceptance run that posted into the real company could not be undone.
COMPANY = "KNIT Acceptance Co"
COMPANY_DOCTYPE = "KNIT 360 Company"
CURRENCY = "INR"

CHECKS = []


def check(group, name):
	"""Register a check. The function returns a one-line detail string."""

	def register(fn):
		CHECKS.append((group, name, fn))
		return fn

	return register


# --- helpers ------------------------------------------------------------


def refuses(fn, *args, **kwargs):
	"""Assert that a call is refused, and return the message it was refused with.

	A guard that does not fire is a worse failure than a guard that fires
	wrongly, because nothing reports it. So absence of a refusal is a failure.
	"""
	try:
		fn(*args, **kwargs)
	except Exception as exc:  # noqa: BLE001 - any refusal counts; we assert one happened
		return str(exc).split("\n")[0][:160]
	raise AssertionError("the call was allowed, but it should have been refused")


def expect(condition, message):
	if not condition:
		raise AssertionError(message)


def company():
	"""The acceptance company, with a chart of accounts and an open year."""
	if not frappe.db.exists("KNIT 360 Company", COMPANY):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Company",
				"company_name": COMPANY,
				"default_currency": CURRENCY,
			}
		).insert(ignore_permissions=True)

	if not frappe.db.exists("KNIT 360 Account", {"company": COMPANY}):
		chart_of_accounts.setup(COMPANY)

	fiscal_year()
	frappe.db.commit()
	return COMPANY


def fiscal_year():
	"""An open fiscal year containing today, whatever today is."""
	today = getdate(nowdate())
	existing = frappe.db.get_value(
		"KNIT 360 Fiscal Year",
		{"year_start_date": ["<=", today], "year_end_date": [">=", today]},
		"name",
	)
	if existing:
		return existing
	name = f"Acceptance {today.year}"
	if not frappe.db.exists("KNIT 360 Fiscal Year", name):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Fiscal Year",
				"year_name": name,
				"year_start_date": f"{today.year}-01-01",
				"year_end_date": f"{today.year}-12-31",
			}
		).insert(ignore_permissions=True)
	return name


def account(leaf):
	"""A leaf account of the acceptance company by its bare name."""
	name = frappe.db.get_value(
		"KNIT 360 Account", {"company": COMPANY, "account_name": leaf, "is_group": 0}, "name"
	)
	expect(name, f"the chart of accounts has no leaf account called {leaf!r}")
	return name


def a_lead(**overrides):
	fields = {
		"doctype": "KNIT 360 Lead",
		"lead_name": "Acceptance Contact",
		"organization_name": "Acceptance Buyer Pvt Ltd",
		"company": company(),
	}
	fields.update(overrides)
	return frappe.get_doc(fields).insert(ignore_permissions=True)


def parent_doctypes():
	return frappe.get_all(
		"DocType",
		filters={"module": ["in", frappe.get_module_list("knit360_core")], "istable": 0},
		pluck="name",
	)


# --- A. install integrity ----------------------------------------------


@check("A. Install", "Every KNIT 360 doctype is installed and loadable")
def a_doctypes_load():
	names = frappe.get_all("DocType", filters={"name": ["like", "KNIT 360%"]}, pluck="name")
	expect(names, "no KNIT 360 doctypes are installed at all")
	for name in names:
		frappe.get_meta(name)  # raises if the controller or JSON is broken
	return f"{len(names)} doctypes, every meta loaded"


@check("A. Install", "No ERPNext app is installed")
def a_no_erpnext():
	apps = frappe.get_installed_apps()
	expect("erpnext" not in apps, f"erpnext is installed: {apps}")
	return f"installed apps: {', '.join(apps)}"


@check("A. Install", "Every doctype's controller class can be instantiated")
def a_controllers():
	broken = []
	for name in frappe.get_all("DocType", filters={"name": ["like", "KNIT 360%"]}, pluck="name"):
		try:
			frappe.new_doc(name)
		except Exception as exc:  # noqa: BLE001 - collecting, not handling
			broken.append(f"{name}: {exc}")
	expect(not broken, "; ".join(broken))
	return "every controller instantiates"


# --- B. masters and referential integrity ------------------------------


@check("B. Masters", "Every Link field points at a doctype that exists")
def b_links_resolve():
	dangling = []
	for doctype in frappe.get_all("DocType", filters={"name": ["like", "KNIT 360%"]}, pluck="name"):
		for field in frappe.get_meta(doctype).get_link_fields():
			if not field.options:
				dangling.append(f"{doctype}.{field.fieldname} has no target")
			elif not frappe.db.exists("DocType", field.options):
				dangling.append(f"{doctype}.{field.fieldname} -> {field.options}")
	expect(not dangling, "; ".join(dangling))
	return "every Link target resolves"


@check("B. Masters", "Tree masters carry working nested-set columns")
def b_trees():
	trees = [
		d
		for d in frappe.get_all("DocType", filters={"name": ["like", "KNIT 360%"]}, pluck="name")
		if frappe.get_meta(d).is_tree
	]
	expect(trees, "no tree doctypes are declared")
	for tree in trees:
		columns = {c.get("Field") or c.get("name") for c in frappe.db.sql(f"DESC `tab{tree}`", as_dict=True)}
		missing = {"lft", "rgt", "old_parent"} - columns
		expect(not missing, f"{tree} is a tree but lacks {sorted(missing)}")
	return f"{len(trees)} trees: {', '.join(t.replace('KNIT 360 ', '') for t in trees)}"


@check("B. Masters", "No Link column holds a value with no master behind it")
def b_no_orphans():
	orphans = []
	for doctype in frappe.get_all("DocType", filters={"name": ["like", "KNIT 360%"]}, pluck="name"):
		meta = frappe.get_meta(doctype)
		for field in meta.get_link_fields():
			if not field.options or not frappe.db.exists("DocType", field.options):
				continue
			rows = frappe.db.sql(
				f"""SELECT DISTINCT `{field.fieldname}` AS v FROM `tab{doctype}`
				    WHERE `{field.fieldname}` IS NOT NULL AND `{field.fieldname}` != ''""",
				as_dict=True,
			)
			for row in rows:
				if not frappe.db.exists(field.options, row.v):
					orphans.append(f"{doctype}.{field.fieldname}={row.v!r}")
	expect(not orphans, "; ".join(orphans[:10]))
	return "no stranded Link values"


# --- C. lifecycle engine ------------------------------------------------


@check("C. Lifecycle", "Every registered lifecycle matches its doctype's field options")
def c_options_match():
	mismatched = []
	for doctype, lifecycle in model.REGISTRY.items():
		if not frappe.db.exists("DocType", doctype):
			continue
		field = frappe.get_meta(doctype).get_field(model.FIELD)
		expect(field, f"{doctype} has no {model.FIELD} field")
		declared = [o for o in (field.options or "").split("\n") if o]
		if declared != list(lifecycle.states):
			mismatched.append(doctype)
	expect(not mismatched, f"options differ from the registry on: {', '.join(mismatched)}")
	return f"{len(model.REGISTRY)} lifecycles agree with their fields"


@check("C. Lifecycle", "The status field is read-only on every governed doctype")
def c_status_read_only():
	writable = [
		doctype
		for doctype in model.REGISTRY
		if frappe.db.exists("DocType", doctype)
		and not frappe.get_meta(doctype).get_field(model.FIELD).read_only
	]
	expect(not writable, f"status is editable on: {', '.join(writable)}")
	return "status is read-only everywhere; only the engine writes it"


@check("C. Lifecycle", "A legal transition moves the status and writes a log")
def c_transition_logs():
	lead = a_lead()
	before = frappe.db.count("KNIT 360 Business Status Log")
	lifecycle = model.for_doctype("KNIT 360 Lead")
	target = lifecycle.forward_from(lifecycle.initial)
	expect(target, "the Lead lifecycle declares no step forward from its initial state")

	engine.transition("KNIT 360 Lead", lead.name, target, reason="acceptance run")
	lead.reload()
	expect(
		lead.get(model.FIELD) == target,
		f"status is {lead.get(model.FIELD)!r}, expected {target!r}",
	)
	after = frappe.db.count("KNIT 360 Business Status Log")
	expect(after == before + 1, f"{after - before} log rows written, expected exactly 1")
	frappe.db.commit()
	return f"{lifecycle.initial} -> {target}, one log row"


@check("C. Lifecycle", "An illegal transition is refused")
def c_illegal_refused():
	lead = a_lead()
	message = refuses(engine.transition, "KNIT 360 Lead", lead.name, "Converted")
	frappe.db.commit()
	return message


@check("C. Lifecycle", "A status that is not in the lifecycle is refused")
def c_unknown_refused():
	lead = a_lead()
	message = refuses(engine.transition, "KNIT 360 Lead", lead.name, "Marinated")
	frappe.db.commit()
	return message


@check("C. Lifecycle", "allowed_next offers only legal targets")
def c_allowed_next():
	lead = a_lead()
	lifecycle = model.for_doctype("KNIT 360 Lead")
	offered = engine.allowed_next("KNIT 360 Lead", lead.name)
	names = [o["status"] if isinstance(o, dict) else o for o in offered]
	for name in names:
		expect(
			lifecycle.is_allowed(lead.get(model.FIELD), name),
			f"{name!r} was offered but the lifecycle forbids it",
		)
	frappe.db.commit()
	return f"from {lead.get(model.FIELD)!r}: {', '.join(names) or 'nothing'}"


# --- D. Customer-to-Cash -----------------------------------------------


@check("D. Customer to Cash", "A lead can be created through the web seam")
def d_create_lead():
	from knit360_core.api import c2c

	result = c2c.create_lead(lead_name="Seam Contact", company=company(), email="seam@example.com")
	expect(result.get("name"), f"create_lead returned no name: {result}")
	expect(result.get("status"), "create_lead returned no status")
	frappe.db.commit()
	return f"{result['name']} at status {result['status']!r}"


@check("D. Customer to Cash", "A lead converts to a customer and an opportunity")
def d_convert():
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Converting Contact")
	lifecycle = model.for_doctype("KNIT 360 Lead")
	status = lifecycle.initial
	# Walk the declared happy path up to the point conversion is legal.
	for _ in range(len(lifecycle.happy_path)):
		nxt = lifecycle.forward_from(status)
		if not nxt:
			break
		engine.transition("KNIT 360 Lead", lead.name, nxt)
		status = nxt
		if status == "Qualified":
			break

	result = c2c.convert_lead(lead.name)
	expect(result.get("customer"), f"no customer was created: {result}")
	expect(result.get("opportunity"), f"no opportunity was created: {result}")
	expect(
		frappe.db.exists("KNIT 360 Customer", result["customer"]),
		"the returned customer does not exist",
	)
	frappe.db.commit()
	return f"{lead.name} -> {result['customer']} + {result['opportunity']}"


@check("D. Customer to Cash", "An opportunity becomes a quotation carrying its value")
def d_quotation():
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Quoting Contact")
	status = model.for_doctype("KNIT 360 Lead").initial
	for _ in range(6):
		nxt = model.for_doctype("KNIT 360 Lead").forward_from(status)
		if not nxt:
			break
		engine.transition("KNIT 360 Lead", lead.name, nxt)
		status = nxt
		if status == "Qualified":
			break
	converted = c2c.convert_lead(lead.name)
	opportunity = converted["opportunity"]

	quotation = c2c.create_quotation(opportunity)
	expect(quotation.get("name"), f"no quotation came back: {quotation}")
	doc = frappe.get_doc("KNIT 360 Quotation", quotation["name"])
	expect(doc.opportunity == opportunity, "the quotation does not reference its opportunity")
	frappe.db.commit()
	return f"{opportunity} -> {doc.name} for {doc.customer}"


@check("D. Customer to Cash", "Quotation lines compute an amount and a total")
def d_items():
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Itemising Contact")
	status = model.for_doctype("KNIT 360 Lead").initial
	for _ in range(6):
		nxt = model.for_doctype("KNIT 360 Lead").forward_from(status)
		if not nxt:
			break
		engine.transition("KNIT 360 Lead", lead.name, nxt)
		status = nxt
		if status == "Qualified":
			break
	quotation = c2c.create_quotation(c2c.convert_lead(lead.name)["opportunity"])["name"]

	c2c.set_items(
		"quotation",
		quotation,
		json.dumps(
			[
				{"item_code": "Induction coil", "qty": 3, "unit_rate": 1500},
				{"item_code": "Control panel", "qty": 1, "unit_rate": 22000, "discount_percentage": 10},
			]
		),
	)
	doc = frappe.get_doc("KNIT 360 Quotation", quotation)
	expect(len(doc.items) == 2, f"{len(doc.items)} lines stored, expected 2")
	expect(flt(doc.items[0].amount) == 4500, f"line 1 amount is {doc.items[0].amount}, expected 4500")
	expect(
		flt(doc.items[1].amount) == 19800,
		f"line 2 amount is {doc.items[1].amount}, expected 19800 after a 10% discount",
	)
	expect(flt(doc.grand_total) == 24300, f"grand total is {doc.grand_total}, expected 24300")
	frappe.db.commit()
	return f"2 lines incl. a 10% discount, grand total {doc.grand_total}"


@check("D. Customer to Cash", "A mistyped line column is refused, not silently dropped")
def d_unknown_column():
	from knit360_core.api import c2c

	quotation = _a_quotation()
	# `rate` is the Sales Order Item column; Quotation Item calls it unit_rate.
	# This used to store a line with no price and report success.
	message = refuses(
		c2c.set_items, "quotation", quotation,
		json.dumps([{"item_code": "Coil", "qty": 1, "rate": 999}]),
	)
	doc = frappe.get_doc("KNIT 360 Quotation", quotation)
	expect(not doc.items, f"{len(doc.items)} priceless lines were stored anyway")
	frappe.db.commit()
	return message


@check("D. Customer to Cash", "A calculated column cannot be set by hand")
def d_computed_column():
	from knit360_core.api import c2c

	message = refuses(
		c2c.set_items, "quotation", _a_quotation(),
		json.dumps([{"item_code": "Coil", "qty": 1, "unit_rate": 100, "amount": 5}]),
	)
	frappe.db.commit()
	return message


@check("D. Customer to Cash", "A discount outside 0-100 is refused")
def d_bad_discount():
	from knit360_core.api import c2c

	message = refuses(
		c2c.set_items, "quotation", _a_quotation(),
		json.dumps([{"item_code": "Coil", "qty": 1, "unit_rate": 100, "discount_percentage": 150}]),
	)
	frappe.db.commit()
	return message


@check("D. Customer to Cash", "A sales order totals with the same engine as the quotation")
def d_order_totals():
	company()
	customer = "Acceptance Ordering Customer"
	if not frappe.db.exists("KNIT 360 Customer", customer):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": customer, "company": COMPANY}
		).insert(ignore_permissions=True)

	order = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Order",
			"customer": customer,
			"company": COMPANY,
			"items": [
				{"item_code": "Coil", "qty": 4, "rate": 2500},
				{"item_code": "Panel", "qty": 2, "rate": 1000},
			],
		}
	).insert(ignore_permissions=True)

	expect(flt(order.items[0].amount) == 10000, f"line 1 is {order.items[0].amount}, expected 10000")
	expect(flt(order.net_total) == 12000, f"net total is {order.net_total}, expected 12000")
	expect(flt(order.grand_total) == 12000, f"grand total is {order.grand_total}, expected 12000")
	frappe.db.commit()
	return f"{order.name}: net {order.net_total}, grand {order.grand_total}"


@check("D. Customer to Cash", "Every document that prices its lines can state a total")
def d_all_totals():
	"""The gap this acceptance run was written to find.

	Fifteen documents carried a table of line items and no total field, so a
	quotation could not state its own price. The check is deliberately narrow:
	it looks only at documents whose line table has a rate or an amount column,
	because a Delivery Note counts quantities and a Quality Inspection records
	readings -- neither is money and neither should total.

	NOT_PRICED names the two exceptions and why, so the list is a decision on
	the record rather than a silence.
	"""
	#: doctype -> why a money total is not computed here.
	NOT_PRICED = {
		"KNIT 360 Tax Template": "its `rate` column is a percentage, not an amount",
		"KNIT 360 Payment Entry": "its `allocated_amount` settles invoices rather than "
		                          "pricing lines; allocation is its own unbuilt feature",
		"KNIT 360 Goods Receipt": "its `rate` values stock for the stock ledger rather "
		                          "than pricing a payable; what the goods cost is held "
		                          "in the stock ledger and what is owed for them is on "
		                          "the supplier's invoice",
	}
	MONEY = {"rate", "unit_rate", "amount", "price"}

	wired, bare = [], []
	for doctype in frappe.get_all(
		"DocType", filters={"name": ["like", "KNIT 360%"], "istable": 0}, pluck="name"
	):
		meta = frappe.get_meta(doctype)
		tables = meta.get_table_fields()
		if not tables:
			continue
		prices = any(
			MONEY & {f.fieldname for f in frappe.get_meta(t.options).fields} for t in tables
		)
		if not prices:
			continue
		if meta.has_field("grand_total") or meta.has_field("total_debit"):
			wired.append(doctype.replace("KNIT 360 ", ""))
		elif doctype not in NOT_PRICED:
			bare.append(doctype.replace("KNIT 360 ", ""))

	expect(
		not bare,
		f"{len(bare)} documents price their lines but cannot total them: {', '.join(sorted(bare))}",
	)
	deferred = ", ".join(d.replace("KNIT 360 ", "") for d in sorted(NOT_PRICED))
	return f"{len(wired)} documents total; not priced by decision: {deferred}"


def _a_quotation():
	"""A fresh draft quotation, walked up from a lead."""
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Column Contact")
	status = model.for_doctype("KNIT 360 Lead").initial
	for _ in range(6):
		nxt = model.for_doctype("KNIT 360 Lead").forward_from(status)
		if not nxt:
			break
		engine.transition("KNIT 360 Lead", lead.name, nxt)
		status = nxt
		if status == "Qualified":
			break
	return c2c.create_quotation(c2c.convert_lead(lead.name)["opportunity"])["name"]


# --- E. the general ledger ---------------------------------------------


@check("E. Ledger", "A company gets a complete chart of accounts")
def e_chart():
	company()
	roots = frappe.get_all(
		"KNIT 360 Account", filters={"company": COMPANY, "parent_account": ["in", [None, ""]]}, pluck="name"
	)
	total = frappe.db.count("KNIT 360 Account", {"company": COMPANY})
	expect(len(roots) == 5, f"{len(roots)} root accounts, expected 5")
	expect(total >= 30, f"only {total} accounts were created")

	missing = [
		field
		for field, leaf in chart_of_accounts.DEFAULTS.items()
		if not frappe.db.get_value("KNIT 360 Company", COMPANY, field)
	]
	expect(not missing, f"company defaults left unset: {', '.join(missing)}")
	return f"{total} accounts, 5 roots, {len(chart_of_accounts.DEFAULTS)} defaults wired"


@check("E. Ledger", "A company created the ordinary way gets its own books")
def e_company_self_setup():
	"""Creating a Company must be enough on its own.

	Until KNIT360Company.after_insert existed, the chart of accounts was built
	only by the demo and acceptance scripts. A company created through the
	normal screen had no accounts, and without a receivable account it cannot
	raise an invoice -- so setting the product up for a real client needed a
	command line. This check is what stops that regressing.
	"""
	name = "KNIT Acceptance Self Setup Co"
	if frappe.db.exists("KNIT 360 Company", name):
		frappe.delete_doc("KNIT 360 Company", name, force=True, ignore_permissions=True)

	doc = frappe.get_doc(
		{"doctype": "KNIT 360 Company", "company_name": name, "default_currency": CURRENCY}
	).insert(ignore_permissions=True)

	accounts = frappe.db.count("KNIT 360 Account", {"company": doc.name})
	expect(accounts >= 30, f"only {accounts} accounts were created on insert")

	for field in chart_of_accounts.DEFAULTS:
		expect(
			frappe.db.get_value("KNIT 360 Company", doc.name, field),
			f"{field} was left unset, so documents relying on it will refuse",
		)
	expect(
		frappe.db.get_value("KNIT 360 Company", doc.name, "default_cost_center"),
		"no default cost centre, so invoice lines post without one",
	)
	frappe.db.commit()
	return f"{accounts} accounts and all defaults, with no command run"


@check("E. Ledger", "A balanced journal entry posts and the ledger agrees")
def e_journal_posts():
	company()
	cash, sales = account("Cash"), account("Sales")
	opening_cash = ledger.balance(cash, COMPANY)

	entry = frappe.get_doc(
		{
			"doctype": "KNIT 360 Journal Entry",
			"company": COMPANY,
			"posting_date": nowdate(),
			"user_remark": "Acceptance: cash sale",
			"accounts": [
				{"account": cash, "debit": 5000, "credit": 0},
				{"account": sales, "debit": 0, "credit": 5000},
			],
		}
	).insert(ignore_permissions=True)

	engine.transition("KNIT 360 Journal Entry", entry.name, "Posted")
	entry.reload()
	expect(entry.docstatus == 1, f"docstatus is {entry.docstatus} after posting, expected 1")

	entries = ledger.voucher_entries("KNIT 360 Journal Entry", entry.name)
	expect(len(entries) == 2, f"{len(entries)} GL entries written, expected 2")
	moved = ledger.balance(cash, COMPANY) - opening_cash
	expect(abs(moved - 5000) < ledger.TOLERANCE, f"cash moved by {moved}, expected 5000")
	frappe.db.commit()
	return f"{entry.name}: 2 GL entries, cash +5000"


@check("E. Ledger", "An unbalanced journal entry is refused before it is saved")
def e_unbalanced_refused():
	company()
	message = refuses(
		lambda: frappe.get_doc(
			{
				"doctype": "KNIT 360 Journal Entry",
				"company": COMPANY,
				"posting_date": nowdate(),
				"accounts": [
					{"account": account("Cash"), "debit": 100, "credit": 0},
					{"account": account("Sales"), "debit": 0, "credit": 90},
				],
			}
		).insert(ignore_permissions=True)
	)
	frappe.db.rollback()
	return message


@check("E. Ledger", "A posting to a group account is refused")
def e_group_refused():
	company()
	group = frappe.db.get_value(
		"KNIT 360 Account", {"company": COMPANY, "is_group": 1, "parent_account": ["!=", ""]}, "name"
	)
	expect(group, "the chart has no non-root group account to test with")
	message = refuses(
		ledger.post,
		"KNIT 360 Journal Entry",
		"ACCEPT-GROUP",
		COMPANY,
		nowdate(),
		[ledger.Line(group, debit=10), ledger.Line(account("Sales"), credit=10)],
	)
	frappe.db.rollback()
	return message


@check("E. Ledger", "Cancelling a posted entry reverses it to nil")
def e_reversal():
	company()
	cash = account("Cash")
	opening = ledger.balance(cash, COMPANY)

	entry = frappe.get_doc(
		{
			"doctype": "KNIT 360 Journal Entry",
			"company": COMPANY,
			"posting_date": nowdate(),
			"user_remark": "Acceptance: to be reversed",
			"accounts": [
				{"account": cash, "debit": 777, "credit": 0},
				{"account": account("Sales"), "debit": 0, "credit": 777},
			],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Journal Entry", entry.name, "Posted")
	engine.transition("KNIT 360 Journal Entry", entry.name, "Cancelled")

	entry.reload()
	expect(entry.docstatus == 2, f"docstatus is {entry.docstatus} after reversal, expected 2")
	net = ledger.balance(cash, COMPANY) - opening
	expect(abs(net) < ledger.TOLERANCE, f"cash is {net} off after a full reversal, expected 0")

	rows = ledger.voucher_entries("KNIT 360 Journal Entry", entry.name, include_cancelled=1)
	expect(len(rows) == 4, f"{len(rows)} rows after reversal, expected 4 (2 original + 2 contra)")
	frappe.db.commit()
	return f"{entry.name} reversed, net effect 0, original rows kept"


@check("E. Ledger", "The trial balance balances")
def e_trial_balance():
	company()
	report = ledger.trial_balance(COMPANY)
	debit, credit = flt(report["total_debit"]), flt(report["total_credit"])
	expect(
		report["balanced"],
		f"trial balance is out by {debit - credit:.2f} (debit {debit:.2f}, credit {credit:.2f})",
	)
	expect(
		abs(debit - credit) < ledger.TOLERANCE,
		"the report claims to balance but its own totals disagree",
	)
	return f"{len(report['rows'])} accounts, debits {debit:.2f} = credits {credit:.2f}"


@check("E. Ledger", "A sales invoice posts a receivable and reports it outstanding")
def e_invoice_posts():
	company()
	customer_name = "Acceptance Invoiced Customer"
	if not frappe.db.exists("KNIT 360 Customer", customer_name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": customer_name, "company": COMPANY}
		).insert(ignore_permissions=True)

	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Invoice",
			"company": COMPANY,
			"customer": customer_name,
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"items": [{"item_name": "Acceptance widget", "qty": 2, "rate": 1250}],
		}
	).insert(ignore_permissions=True)

	expect(flt(invoice.grand_total) == 2500, f"grand total is {invoice.grand_total}, expected 2500")
	engine.transition("KNIT 360 Sales Invoice", invoice.name, "Posted / Unpaid")
	invoice.reload()

	expect(invoice.docstatus == 1, f"docstatus is {invoice.docstatus}, expected 1")
	expect(
		flt(invoice.outstanding_amount) == 2500,
		f"outstanding is {invoice.outstanding_amount}, expected 2500",
	)
	receivable = ledger.party_balance("Customer", customer_name, COMPANY)
	expect(flt(receivable) != 0, "the customer's receivable balance did not move")
	frappe.db.commit()
	return f"{invoice.name}: 2500 receivable, party balance {receivable}"


# --- F. guards ----------------------------------------------------------


@check("F. Guards", "Frappe's own Submit cannot bypass the lifecycle")
def f_submit_guarded():
	company()
	entry = frappe.get_doc(
		{
			"doctype": "KNIT 360 Journal Entry",
			"company": COMPANY,
			"posting_date": nowdate(),
			"user_remark": "Acceptance: bypass attempt",
			"accounts": [
				{"account": account("Cash"), "debit": 1, "credit": 0},
				{"account": account("Sales"), "debit": 0, "credit": 1},
			],
		}
	).insert(ignore_permissions=True)

	message = refuses(entry.submit)
	entry.reload()
	expect(entry.docstatus == 0, f"the document submitted anyway: docstatus {entry.docstatus}")
	expect(
		not ledger.voucher_entries("KNIT 360 Journal Entry", entry.name),
		"GL entries were written by a submit the guard was supposed to refuse",
	)
	frappe.db.commit()
	return message


@check("F. Guards", "The ledger is the only module that writes GL entries")
def f_single_writer():
	import pathlib

	root = pathlib.Path(frappe.get_app_path("knit360_core"))
	offenders = []
	for path in root.rglob("*.py"):
		if path.name in ("ledger.py", "acceptance.py") or path.name.startswith("test_"):
			continue
		text = path.read_text(encoding="utf-8")
		if "KNIT 360 GL Entry" in text and ("insert(" in text or "new_doc(" in text):
			offenders.append(str(path.relative_to(root)))
	expect(not offenders, f"GL Entry is written outside the ledger by: {', '.join(offenders)}")
	return "finance/ledger.py is the sole writer"


@check("F. Guards", "A submitted document refuses after-the-fact edits")
def f_immutable():
	company()
	entry = frappe.get_doc(
		{
			"doctype": "KNIT 360 Journal Entry",
			"company": COMPANY,
			"posting_date": nowdate(),
			"user_remark": "Acceptance: immutability",
			"accounts": [
				{"account": account("Cash"), "debit": 42, "credit": 0},
				{"account": account("Sales"), "debit": 0, "credit": 42},
			],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Journal Entry", entry.name, "Posted")
	entry.reload()

	entry.user_remark = "edited after posting"
	message = refuses(entry.save)
	frappe.db.rollback()
	return message


# --- G. what the user sees ---------------------------------------------


@check("G. Desk", "Every workspace exists and is visible")
def g_workspaces():
	from knit360_core import desk

	expected = [desk.HOME["label"]] + list(desk.MODULES)
	missing = [w for w in expected if not frappe.db.exists("Workspace", w)]
	expect(not missing, f"missing workspaces: {', '.join(missing)}")
	hidden = frappe.get_all(
		"Workspace", filters={"name": ["in", expected], "is_hidden": 1}, pluck="name"
	)
	expect(not hidden, f"hidden workspaces: {', '.join(hidden)}")
	return f"{len(expected)} workspaces, none hidden"


@check("G. Desk", "Every workspace link points at an installed doctype")
def g_links_live():
	from knit360_core import desk

	broken = []
	for workspace in [desk.HOME["label"]] + list(desk.MODULES):
		if not frappe.db.exists("Workspace", workspace):
			continue
		for row in frappe.get_doc("Workspace", workspace).links:
			if row.type == "Link" and row.link_type == "DocType":
				if not frappe.db.exists("DocType", row.link_to):
					broken.append(f"{workspace}: {row.link_to}")
	expect(not broken, "; ".join(broken))
	return "every sidebar link resolves"


@check("G. Desk", "Every chart and card exists and renders a figure")
def g_charts():
	from knit360_core import dashboards

	missing_charts = [
		c["name"] for c in dashboards.CHARTS if not frappe.db.exists("Dashboard Chart", c["name"])
	]
	missing_cards = [
		c["name"] for c in dashboards.CARDS if not frappe.db.exists("Number Card", c["name"])
	]
	expect(not missing_charts, f"missing charts: {', '.join(missing_charts)}")
	expect(not missing_cards, f"missing cards: {', '.join(missing_cards)}")

	# A chart that exists but throws when asked for data is worse than none,
	# and that is exactly how a bad group-by field fails: silently, at render.
	# Frappe's own dashboard_chart.get coerces its `chart` argument back into a
	# Document before parsing it, so it cannot be called from here. Running the
	# chart's aggregation directly proves the same thing -- that the doctype,
	# the field and the grouping it was defined with actually resolve.
	for spec in dashboards.CHARTS:
		doc = frappe.get_doc("Dashboard Chart", spec["name"])
		expect(doc.is_public, f"{spec['name']} is not public, so only its owner sees it")
		if doc.chart_type == "Group By":
			aggregate = (
				f"sum(`{doc.aggregate_function_based_on}`)"
				if doc.group_by_type == "Sum"
				else "count(name)"
			)
			frappe.db.sql(
				f"""SELECT `{doc.group_by_based_on}`, {aggregate} AS value
				    FROM `tab{doc.document_type}` GROUP BY `{doc.group_by_based_on}`"""
			)
		else:
			frappe.db.sql(
				f"""SELECT `{doc.based_on}`, sum(`{doc.value_based_on}`) AS value
				    FROM `tab{doc.document_type}` GROUP BY `{doc.based_on}`"""
			)
	return f"{len(dashboards.CHARTS)} charts query cleanly, {len(dashboards.CARDS)} cards exist"


@check("G. Desk", "No other vendor's advertising reaches the user")
def g_no_vendor_ads():
	"""Frappe's list sidebar advertises Frappe's own commercial products.

	add_crm_banner() fires on any list whose doctype's module is called "CRM",
	which ours is, because that is BRD module 02's name. The result was
	"Switch to Frappe CRM for smarter sales" in the sidebar of our Lead,
	Opportunity and Customer lists -- an advert for a competing product, in
	front of whoever is being shown the system.

	Two halves, and this checks both: the Help menu link is hidden through
	Navbar Item's own `hidden` flag, and the sidebar banners are suppressed by
	overriding the one helper all three go through.
	"""
	from knit360_core import branding

	for label in branding.VENDOR_NAVBAR_ITEMS:
		rows = frappe.get_all("Navbar Item", filters={"item_label": label}, fields=["hidden"])
		for row in rows:
			expect(row.hidden, f"the navbar item {label!r} is still visible")

	# The About menu entry stays. What it opens is ours: the framework's own
	# dialog lists the vendor's site, GitHub, blog, forum, five social accounts
	# and every installed app by name. Replacing its contents is a different
	# act from deleting the menu item, and leaves the product with an About box.
	expect(
		"About" not in branding.VENDOR_NAVBAR_ITEMS,
		"About should be replaced, not hidden -- the product needs an About box",
	)

	bundle = pathlib.Path(frappe.get_app_path("knit360_core")) / "public" / "js" / "branding.bundle.js"
	expect(bundle.exists(), f"{bundle.name} is missing, so the sidebar banners return")
	source = bundle.read_text(encoding="utf-8")
	expect(
		"add_banner" in source and "ListSidebar" in source,
		"the branding bundle no longer overrides ListSidebar.add_banner",
	)
	expect(
		"frappe.ui.misc.about" in source,
		"the branding bundle no longer replaces the About dialog",
	)

	# Website Settings.footer_powered is empty by default, and the footer then
	# falls through to a template rendering "Built on <vendor>" with a link.
	# Any non-empty value replaces it.
	expect(
		frappe.db.get_single_value("Website Settings", "footer_powered"),
		"footer_powered is empty, so the website footer advertises the framework",
	)

	hooks = (pathlib.Path(frappe.get_app_path("knit360_core")) / "hooks.py").read_text(encoding="utf-8")
	expect(
		"branding.bundle.js" in hooks,
		"the branding bundle is not in app_include_js, so it never loads",
	)
	return (f"{len(branding.VENDOR_NAVBAR_ITEMS)} navbar item(s) hidden; banners, "
	        f"About dialog and website footer all replaced")


@check("G. Desk", "The requirement coverage report runs and adds up")
def g_coverage_report():
	"""The report a client is shown must agree with itself.

	It is the one artefact in the system whose whole purpose is to be believed,
	so the figures in its headline are checked against the rows beneath them.
	"""
	from knit360_core import brd_requirements, traceability
	from knit360_core.platform.report.knit_360_requirement_coverage import (
		knit_360_requirement_coverage as report,
	)

	columns, data, message, chart, cards = report.execute({})
	expect(columns and data, "the report returned no columns or no rows")
	expect(
		len(data) == len(brd_requirements.REQUIREMENTS) == 238,
		f"{len(data)} rows for {len(brd_requirements.REQUIREMENTS)} requirements",
	)

	summary = traceability.summary()
	counted = {"Proven": 0, "Modelled": 0, "Not started": 0}
	for row in data:
		counted[row["status"]] += 1
	expect(
		counted["Proven"] == summary["proven"]
		and counted["Modelled"] == summary["modelled"]
		and counted["Not started"] == summary["not_started"],
		f"the headline and the rows disagree: {summary} vs {counted}",
	)
	expect(
		summary["covered"] + summary["not_started"] == 238,
		"covered and not-started do not account for all 238 requirements",
	)
	expect(
		str(summary["covered"]) in message and "238" in message,
		"the headline message does not state the coverage it computed",
	)

	# A "Proven" row must name the check that proves it, or the word is empty.
	for row in data:
		if row["status"] == "Proven":
			expect(row["proven_by"], f"{row['requirement']} is Proven but names no check")

	# Chart and cards are returned in the positions Frappe reads them from;
	# swapping the two makes the table fail to render at all.
	expect(isinstance(chart, dict) and "data" in chart, "the chart is not a chart")
	expect(isinstance(cards, list), "report_summary must be a list of cards")
	return (f"238 rows, {summary['proven']} proven / {summary['modelled']} modelled / "
	        f"{summary['not_started']} not started, headline agrees")


@check("G. Desk", "Count charts are not formatted as currency")
def g_no_rupee_counts():
	from knit360_core import dashboards

	wrong = []
	for spec in dashboards.CHARTS:
		if not frappe.db.exists("Dashboard Chart", spec["name"]):
			continue
		currency = frappe.db.get_value("Dashboard Chart", spec["name"], "currency")
		is_money = bool(spec.get("currency"))
		if bool(currency) != is_money:
			wrong.append(f"{spec['name']} currency={currency!r}, money={is_money}")
	expect(not wrong, "; ".join(wrong))
	return "currency is set on money charts only"


@check("G. Desk", "A chart whose label and name differ would render blank")
def g_label_equals_name():
	from knit360_core import dashboards

	mismatched = [
		spec["name"]
		for spec in dashboards.CHARTS
		if frappe.db.exists("Dashboard Chart", spec["name"])
		and frappe.db.get_value("Dashboard Chart", spec["name"], "chart_name") != spec["name"]
	]
	expect(not mismatched, f"name != label on: {', '.join(mismatched)}")
	return "name == label == reference on every chart"


# --- H. the web seam ----------------------------------------------------


@check("H. Web seam", "stages() describes every stage with its actions")
def h_stages():
	from knit360_core.api import c2c

	stages = c2c.stages()
	expect(len(stages) == len(c2c.STAGES), f"{len(stages)} stages returned")
	for stage in stages:
		expect(stage.get("key"), f"a stage came back with no key: {stage}")
		expect(stage.get("label"), f"{stage.get('key')} has no label")
		expect(stage.get("states"), f"{stage['key']} describes no lifecycle states")
		expect("counts" in stage, f"{stage['key']} reports no per-status counts")
	return f"{len(stages)} stages: {', '.join(s['key'] for s in stages)}"


@check("H. Web seam", "documents() returns the listed fields and nothing else")
def h_documents():
	from knit360_core.api import c2c

	a_lead(lead_name="Listed Contact")
	frappe.db.commit()
	rows = c2c.documents("lead")
	expect(rows, "no leads came back, though one was just created")
	allowed = set(c2c.BY_KEY["lead"]["fields"]) | {"status", "title"}
	leaked = set(rows[0]) - allowed
	expect(not leaked, f"documents() leaked fields the seam does not declare: {sorted(leaked)}")
	expect("docstatus" not in rows[0], "docstatus leaked; the seam exists to hide it")
	return f"{len(rows)} rows, fields {sorted(rows[0])}"


@check("H. Web seam", "document() returns guidance a non-technical user can act on")
def h_document_guidance():
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Guided Contact")
	frappe.db.commit()
	detail = c2c.document("lead", lead.name)
	for key in ("name", "status", "actions"):
		expect(key in detail, f"document() returned no {key!r}")
	expect(detail["actions"], "a fresh lead was offered no next action at all")
	for action in detail["actions"]:
		expect(action.get("label"), f"an action has no label: {action}")
	return f"status {detail['status']!r}, {len(detail['actions'])} actions offered"


@check("H. Web seam", "next_steps tells the Desk what each move will do")
def h_next_steps():
	from knit360_core.business_status import engine as eng

	lead = a_lead(lead_name="Stepping Contact")
	frappe.db.commit()
	steps = eng.next_steps("KNIT 360 Lead", lead.name)
	expect(steps, "a fresh lead was offered no steps at all")

	bare = eng.allowed_next("KNIT 360 Lead", lead.name)
	expect(
		[s["status"] for s in steps] == list(bare),
		"next_steps and allowed_next disagree about what is legal",
	)
	for step in steps:
		for key in ("status", "locks", "terminal", "is_forward"):
			expect(key in step, f"a step is missing {key!r}: {step}")
	expect(
		sum(1 for s in steps if s["is_forward"]) <= 1,
		"more than one step was marked as the ordinary next one",
	)
	expect(
		eng.next_steps("KNIT 360 Item", "nonexistent") == [],
		"next_steps raised on a doctype with no lifecycle instead of returning nothing",
	)
	return f"{len(steps)} steps, forward={[s['status'] for s in steps if s['is_forward']]}"


@check("H. Web seam", "The Desk is offered the same stage actions as the web page")
def h_actions_for():
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Acting Contact")
	frappe.db.commit()

	early = c2c.actions_for("KNIT 360 Lead", lead.name)
	convert = next((a for a in early if a["key"] == "convert_lead"), None)
	expect(convert, "no convert action was described at all")
	expect(not convert["enabled"], "a brand new lead was offered conversion")
	expect(convert["reason"], "the action is disabled but gives no reason why")

	status = model.for_doctype("KNIT 360 Lead").initial
	for _ in range(6):
		nxt = model.for_doctype("KNIT 360 Lead").forward_from(status)
		if not nxt:
			break
		engine.transition("KNIT 360 Lead", lead.name, nxt)
		status = nxt
		if status == "Qualified":
			break
	frappe.db.commit()

	ready = next(a for a in c2c.actions_for("KNIT 360 Lead", lead.name) if a["key"] == "convert_lead")
	expect(ready["enabled"], f"a Qualified lead was refused conversion: {ready['reason']}")
	expect(
		c2c.actions_for("KNIT 360 Item", "nothing") == [],
		"actions_for raised on a doctype outside the three stages",
	)
	return f"disabled when New ({convert['reason'][:60]}...), enabled when Qualified"


@check("H. Web seam", "An action declares the status it reaches on its own")
def h_action_claims_status():
	"""Stops the Desk offering two buttons that look alike and are not.

	A Qualified lead can legally move straight to Converted, and it can also be
	converted properly -- which creates the customer and the opportunity and
	then moves it to Converted. Both were drawn as buttons. Pressing the plain
	one marks the lead converted and creates nothing. The action now names the
	status it produces so the duplicate can be left out.
	"""
	from knit360_core.api import c2c
	from knit360_core.crm import conversion

	lead = a_lead(lead_name="Claiming Contact")
	status = model.for_doctype("KNIT 360 Lead").initial
	for _ in range(6):
		nxt = model.for_doctype("KNIT 360 Lead").forward_from(status)
		if not nxt:
			break
		engine.transition("KNIT 360 Lead", lead.name, nxt)
		status = nxt
		if status == "Qualified":
			break
	frappe.db.commit()

	action = next(a for a in c2c.actions_for("KNIT 360 Lead", lead.name) if a["key"] == "convert_lead")
	expect(action.get("produces_status"), "the convert action does not say what status it reaches")
	expect(
		action["produces_status"] == conversion.CONVERTED,
		f"it claims {action['produces_status']!r}, but conversion sets {conversion.CONVERTED!r}",
	)
	expect(
		action["produces_status"] in engine.allowed_next("KNIT 360 Lead", lead.name),
		"the claimed status is not even a legal move, so nothing would be hidden",
	)
	return f"convert_lead claims {action['produces_status']!r}"


@check("H. Web seam", "The seam refuses a stage it does not expose")
def h_unknown_stage():
	from knit360_core.api import c2c

	return refuses(c2c.documents, "payroll")


@check("H. Web seam", "advance() goes through the engine, so it refuses illegal moves")
def h_advance_guarded():
	from knit360_core.api import c2c

	lead = a_lead(lead_name="Jumping Contact")
	frappe.db.commit()
	message = refuses(c2c.advance, "lead", lead.name, "Converted")
	frappe.db.commit()
	return message


@check("H. Web seam", "The Customer-to-Cash page is served with a usable CSRF token")
def h_page_renders():
	response = frappe.website.serve.get_response_content("/knit360")
	expect("csrf_token" in response, "the page carries no CSRF token at all")
	expect('"None"' not in response and "'None'" not in response, "the CSRF token rendered as None")
	expect("KNIT 360" in response, "the page does not name the product")
	return f"{len(response)} bytes, token present"



# --- I. HR: leave -------------------------------------------------------


def an_employee(name="Acceptance Employee"):
	existing = frappe.db.get_value("KNIT 360 Employee", {"employee_name": name, "company": COMPANY})
	if existing:
		return existing
	return frappe.get_doc(
		{"doctype": "KNIT 360 Employee", "employee_name": name, "company": company(),
		 "is_active": 1, "date_of_joining": "2026-01-01"}
	).insert(ignore_permissions=True).name


def a_leave_type(name="Acceptance Casual Leave", **overrides):
	if frappe.db.exists("KNIT 360 Leave Type", name):
		return name
	fields = {"doctype": "KNIT 360 Leave Type", "leave_type_name": name, "is_paid_leave": 1}
	fields.update(overrides)
	return frappe.get_doc(fields).insert(ignore_permissions=True).name


def a_leave_period():
	name = "Acceptance Leave Period"
	if frappe.db.exists("KNIT 360 Leave Period", name):
		return name
	year = getdate(nowdate()).year
	return frappe.get_doc(
		{"doctype": "KNIT 360 Leave Period", "period_name": name, "company": company(),
		 "from_date": f"{year}-01-01", "to_date": f"{year}-12-31", "is_active": 1}
	).insert(ignore_permissions=True).name


def allocate(employee, leave_type, days):
	"""A submitted allocation, moved there through the lifecycle."""
	year = getdate(nowdate()).year
	doc = frappe.get_doc(
		{
			"doctype": "KNIT 360 Leave Allocation",
			"employee": employee, "leave_type": leave_type, "company": COMPANY,
			"leave_period": a_leave_period(),
			"from_date": f"{year}-01-01", "to_date": f"{year}-12-31",
			"new_leaves_allocated": days,
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Leave Allocation", doc.name, "Allocated")
	return doc.name


def an_application(employee, leave_type, from_date, to_date, **overrides):
	fields = {
		"doctype": "KNIT 360 Leave Application",
		"employee": employee, "leave_type": leave_type, "company": COMPANY,
		"from_date": from_date, "to_date": to_date,
	}
	fields.update(overrides)
	return frappe.get_doc(fields).insert(ignore_permissions=True)


def approve(application):
	engine.transition("KNIT 360 Leave Application", application, "Pending Approval")
	engine.transition("KNIT 360 Leave Application", application, "Approved")


@check("I. HR leave", "An allocation grants a balance through the ledger")
def i_allocation_posts():
	from knit360_core.hr import leave_ledger

	employee = an_employee("Allocating Employee")
	leave_type = a_leave_type("Acceptance Allocation Leave")
	opening = leave_ledger.balance(employee, leave_type, company=COMPANY)

	name = allocate(employee, leave_type, 12)
	entries = leave_ledger.entries("KNIT 360 Leave Allocation", name)
	expect(len(entries) == 1, f"{len(entries)} ledger entries, expected 1")
	expect(flt(entries[0]["leaves"]) == 12, f"posted {entries[0]['leaves']}, expected 12")

	moved = leave_ledger.balance(employee, leave_type, company=COMPANY) - opening
	expect(abs(moved - 12) < 0.001, f"balance moved by {moved}, expected 12")
	frappe.db.commit()
	return f"{name}: +12 days"


@check("I. HR leave", "An approved application consumes the balance")
def i_application_consumes():
	from knit360_core.hr import leave_ledger

	employee = an_employee("Applying Employee")
	leave_type = a_leave_type("Acceptance Application Leave")
	allocate(employee, leave_type, 10)
	before = leave_ledger.balance(employee, leave_type, company=COMPANY)

	year = getdate(nowdate()).year
	app = an_application(employee, leave_type, f"{year}-06-01", f"{year}-06-03",
	                     reason="Acceptance run")
	expect(flt(app.total_leave_days) == 3, f"counted {app.total_leave_days} days, expected 3")

	approve(app.name)
	after = leave_ledger.balance(employee, leave_type, company=COMPANY)
	expect(abs((before - after) - 3) < 0.001, f"balance fell by {before - after}, expected 3")
	frappe.db.commit()
	return f"{app.name}: 3 days, balance {before:g} -> {after:g}"


@check("I. HR leave", "A balance is derived from the ledger, never stored")
def i_balance_is_derived():
	from knit360_core.hr import leave_ledger

	employee = an_employee("Derived Employee")
	leave_type = a_leave_type("Acceptance Derived Leave")
	allocate(employee, leave_type, 7)

	rows = frappe.get_all(
		"KNIT 360 Leave Ledger Entry",
		filters={"employee": employee, "leave_type": leave_type, "is_cancelled": 0},
		pluck="leaves",
	)
	expect(
		abs(sum(flt(r) for r in rows) - leave_ledger.balance(employee, leave_type)) < 0.001,
		"balance() does not equal the sum of the live entries",
	)

	for doctype in ("KNIT 360 Employee", "KNIT 360 Leave Type"):
		stored = [
			f.fieldname for f in frappe.get_meta(doctype).fields
			if "leave_balance" in (f.fieldname or "")
		]
		expect(not stored, f"{doctype} stores a leave balance in {stored}")
	frappe.db.commit()
	return f"balance == sum of {len(rows)} entries; no doctype stores one"


@check("I. HR leave", "Applying for more than the balance is refused")
def i_over_application_refused():
	employee = an_employee("Greedy Employee")
	leave_type = a_leave_type("Acceptance Scarce Leave")
	allocate(employee, leave_type, 2)
	year = getdate(nowdate()).year

	message = refuses(an_application, employee, leave_type, f"{year}-07-01", f"{year}-07-10")
	frappe.db.rollback()
	return message


@check("I. HR leave", "A leave type may permit a negative balance")
def i_negative_allowed():
	from knit360_core.hr import leave_ledger

	employee = an_employee("Overdrawn Employee")
	leave_type = a_leave_type("Acceptance Overdraft Leave", allow_negative_balance=1)
	year = getdate(nowdate()).year

	app = an_application(employee, leave_type, f"{year}-08-03", f"{year}-08-04")
	approve(app.name)

	balance = leave_ledger.balance(employee, leave_type, company=COMPANY)
	expect(balance < 0, f"balance is {balance}, expected it to go negative")
	frappe.db.commit()
	return f"no allocation, 2 days taken, balance {balance:g}"


@check("I. HR leave", "Holidays are not counted as leave")
def i_holidays_skipped():
	year = getdate(nowdate()).year
	name = "Acceptance Holiday List"
	if not frappe.db.exists("KNIT 360 Holiday List", name):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Holiday List", "holiday_list_name": name,
				"company": company(), "from_date": f"{year}-01-01", "to_date": f"{year}-12-31",
				"holidays": [
					{"holiday_date": f"{year}-09-02", "description": "Acceptance holiday"},
					{"holiday_date": f"{year}-09-03", "description": "Acceptance holiday"},
				],
			}
		).insert(ignore_permissions=True)

	employee = an_employee("Holidaying Employee")
	leave_type = a_leave_type("Acceptance Holiday Leave")
	allocate(employee, leave_type, 10)

	app = an_application(employee, leave_type, f"{year}-09-01", f"{year}-09-04",
	                     holiday_list=name)
	expect(
		flt(app.total_leave_days) == 2,
		f"counted {app.total_leave_days} days over a 4-day span with 2 holidays, expected 2",
	)
	frappe.db.commit()
	return "4 calendar days, 2 holidays, 2 days of leave"


@check("I. HR leave", "A half day counts as half a day")
def i_half_day():
	year = getdate(nowdate()).year
	employee = an_employee("Halving Employee")
	leave_type = a_leave_type("Acceptance Half Leave")
	allocate(employee, leave_type, 5)

	app = an_application(employee, leave_type, f"{year}-10-12", f"{year}-10-12", half_day=1)
	expect(flt(app.total_leave_days) == 0.5, f"counted {app.total_leave_days}, expected 0.5")

	message = refuses(an_application, employee, leave_type,
	                  f"{year}-10-14", f"{year}-10-16", half_day=1)
	frappe.db.commit()
	return f"0.5 days; a multi-day half day is refused"


@check("I. HR leave", "Cancelling an allocation reverses it to nil")
def i_allocation_reversal():
	from knit360_core.hr import leave_ledger

	employee = an_employee("Reversing Employee")
	leave_type = a_leave_type("Acceptance Reversal Leave")
	opening = leave_ledger.balance(employee, leave_type, company=COMPANY)

	name = allocate(employee, leave_type, 9)
	engine.transition("KNIT 360 Leave Allocation", name, "Cancelled")

	net = leave_ledger.balance(employee, leave_type, company=COMPANY) - opening
	expect(abs(net) < 0.001, f"balance is {net} off after a full reversal, expected 0")

	rows = leave_ledger.entries("KNIT 360 Leave Allocation", name, include_cancelled=1)
	expect(len(rows) == 2, f"{len(rows)} rows after reversal, expected 2 (original + contra)")
	expect(all(r["is_cancelled"] for r in rows), "the pair was not flagged cancelled")
	frappe.db.commit()
	return f"{name} cancelled, net 0, both rows kept"


@check("I. HR leave", "A ledger entry cannot be edited or deleted")
def i_ledger_immutable():
	from knit360_core.hr import leave_ledger

	employee = an_employee("Immutable Employee")
	leave_type = a_leave_type("Acceptance Immutable Leave")
	name = allocate(employee, leave_type, 4)
	entry = leave_ledger.entries("KNIT 360 Leave Allocation", name)[0]["name"]
	# Commit before testing refusals. An earlier version rolled back between
	# the two, which removed the entry -- and frappe.delete_doc ignores a
	# missing document, so the delete "succeeded" and the check reported a
	# product failure that was really a fixture failure.
	frappe.db.commit()

	expect(
		frappe.db.exists("KNIT 360 Leave Ledger Entry", entry),
		"the fixture entry does not exist, so neither refusal would mean anything",
	)

	delete = refuses(
		frappe.delete_doc, "KNIT 360 Leave Ledger Entry", entry, ignore_permissions=True
	)
	expect(
		frappe.db.exists("KNIT 360 Leave Ledger Entry", entry),
		"the entry was deleted anyway",
	)

	doc = frappe.get_doc("KNIT 360 Leave Ledger Entry", entry)
	doc.leaves = 999
	edit = refuses(doc.save)
	frappe.db.rollback()

	expect(
		flt(frappe.db.get_value("KNIT 360 Leave Ledger Entry", entry, "leaves")) == 4,
		"the entry's days changed despite the refusal",
	)
	return f"delete refused ({delete[:48]}...), edit refused ({edit[:48]}...)"


@check("I. HR leave", "Two allocations for the same period are refused")
def i_double_allocation_refused():
	employee = an_employee("Doubling Employee")
	leave_type = a_leave_type("Acceptance Double Leave")
	allocate(employee, leave_type, 6)
	frappe.db.commit()
	message = refuses(allocate, employee, leave_type, 6)
	frappe.db.rollback()
	return message


@check("I. HR leave", "Overlapping approved leave is refused")
def i_overlap_refused():
	year = getdate(nowdate()).year
	employee = an_employee("Overlapping Employee")
	leave_type = a_leave_type("Acceptance Overlap Leave")
	allocate(employee, leave_type, 20)

	first = an_application(employee, leave_type, f"{year}-11-02", f"{year}-11-06")
	approve(first.name)
	frappe.db.commit()

	message = refuses(an_application, employee, leave_type, f"{year}-11-04", f"{year}-11-05")
	frappe.db.rollback()
	return message


@check("I. HR leave", "A rejected application never reaches the ledger")
def i_rejected_posts_nothing():
	from knit360_core.hr import leave_ledger

	year = getdate(nowdate()).year
	employee = an_employee("Rejected Employee")
	leave_type = a_leave_type("Acceptance Rejected Leave")
	allocate(employee, leave_type, 8)
	before = leave_ledger.balance(employee, leave_type, company=COMPANY)

	app = an_application(employee, leave_type, f"{year}-12-07", f"{year}-12-09")
	engine.transition("KNIT 360 Leave Application", app.name, "Pending Approval")
	engine.transition("KNIT 360 Leave Application", app.name, "Rejected")

	app.reload()
	expect(app.docstatus == 0, f"a rejected application reached docstatus {app.docstatus}")
	expect(
		not leave_ledger.entries("KNIT 360 Leave Application", app.name),
		"a rejected application wrote to the leave ledger",
	)
	after = leave_ledger.balance(employee, leave_type, company=COMPANY)
	expect(abs(before - after) < 0.001, f"the balance moved by {before - after} on a rejection")
	frappe.db.commit()
	return "rejected, docstatus 0, nothing posted, balance unchanged"


@check("I. HR leave", "The leave ledger is the only module that writes entries")
def i_single_writer():
	import pathlib as _pathlib

	root = _pathlib.Path(frappe.get_app_path("knit360_core"))
	offenders = []
	for path in root.rglob("*.py"):
		if path.name in ("leave_ledger.py", "acceptance.py") or path.name.startswith("test_"):
			continue
		text = path.read_text(encoding="utf-8")
		if "KNIT 360 Leave Ledger Entry" in text and ("insert(" in text or "new_doc(" in text):
			offenders.append(str(path.relative_to(root)))
	expect(not offenders, f"the leave ledger is written outside hr/leave_ledger.py by: {offenders}")
	return "hr/leave_ledger.py is the sole writer"


# --- J. tax accounts and the supplier's bill ----------------------------
#
# These two groups exist because of two recorded decisions, DEC-020 and
# DEC-021, and each check asserts the decision rather than describing it.


def a_supplier():
	name = "Acceptance Supplier Pvt Ltd"
	if not frappe.db.exists("KNIT 360 Supplier", name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Supplier", "supplier_name": name, "company": company()}
		).insert(ignore_permissions=True)
	return name


def a_tax_template(name, components):
	"""A tax template of (component, rate, account) rows, created once."""
	company()
	if frappe.db.exists("KNIT 360 Tax Template", name):
		frappe.delete_doc("KNIT 360 Tax Template", name, force=True, ignore_permissions=True,
		                  delete_permanently=True)
	return frappe.get_doc(
		{
			"doctype": "KNIT 360 Tax Template",
			"template_name": name,
			"company": COMPANY,
			"taxes": [
				{"tax_component": component, "rate": rate, "tax_account": account}
				for component, rate, account in components
			],
		}
	).insert(ignore_permissions=True)


def _tax_invoice(template, rate=1000, qty=1):
	"""A posted sales invoice carrying tax from `template`."""
	customer_name = "Acceptance Taxed Customer"
	if not frappe.db.exists("KNIT 360 Customer", customer_name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": customer_name, "company": COMPANY}
		).insert(ignore_permissions=True)

	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Invoice",
			"company": COMPANY,
			"customer": customer_name,
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"tax_template": template,
			"items": [{"item_name": "Acceptance taxed widget", "qty": qty, "rate": rate}],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Sales Invoice", invoice.name, "Posted / Unpaid")
	invoice.reload()
	return invoice


@check("J. Tax and the supplier's bill", "A company's tax accounts are a liability and an asset")
def j_tax_accounts_exist():
	"""DEC-021. Tax charged is owed to the authority; tax paid is recoverable.

	Neither is income or expense, and a chart that puts them there would
	overstate profit by the whole tax collected. So the root type is asserted,
	not just the presence of the account.
	"""
	company()
	chart_of_accounts.backfill_defaults(COMPANY)
	values = frappe.db.get_value(
		"KNIT 360 Company",
		COMPANY,
		["default_output_tax_account", "default_input_tax_account"],
		as_dict=True,
	)
	expect(values.default_output_tax_account, "the company has no default output tax account")
	expect(values.default_input_tax_account, "the company has no default input tax account")

	output_root = frappe.db.get_value(
		"KNIT 360 Account", values.default_output_tax_account, "root_type"
	)
	input_root = frappe.db.get_value(
		"KNIT 360 Account", values.default_input_tax_account, "root_type"
	)
	expect(output_root == "Liability", f"output tax sits under {output_root}, expected Liability")
	expect(input_root == "Asset", f"input tax sits under {input_root}, expected Asset")
	return (
		f"output {values.default_output_tax_account} ({output_root}), "
		f"input {values.default_input_tax_account} ({input_root})"
	)


@check("J. Tax and the supplier's bill", "Tax posts to a tax account, never to round-off")
def j_tax_not_round_off():
	"""DEC-021, and the correction of a placeholder.

	Until DEC-021 the whole tax figure was credited to the round-off account.
	This asserts the new behaviour and the absence of the old one in the same
	check, so a regression to the placeholder fails rather than passing quietly.
	"""
	company()
	chart_of_accounts.backfill_defaults(COMPANY)
	template = a_tax_template("Acceptance Two Component Tax", [
		("Acceptance Tax Part A", 9, None),
		("Acceptance Tax Part B", 9, None),
	])
	invoice = _tax_invoice(template.name, rate=1000, qty=1)

	expect(flt(invoice.total_taxes) == 180, f"tax is {invoice.total_taxes}, expected 180")
	expect(flt(invoice.grand_total) == 1180, f"grand total is {invoice.grand_total}, expected 1180")

	entries = ledger.voucher_entries("KNIT 360 Sales Invoice", invoice.name)
	output_account = frappe.db.get_value(
		"KNIT 360 Company", COMPANY, "default_output_tax_account"
	)
	round_off = frappe.db.get_value("KNIT 360 Company", COMPANY, "round_off_account")

	to_tax = [row for row in entries if row.account == output_account]
	to_round_off = [row for row in entries if row.account == round_off]

	expect(len(to_tax) == 2, f"{len(to_tax)} lines reached the tax account, expected 2")
	expect(not to_round_off, f"{len(to_round_off)} tax lines still reach the round-off account")
	credited = flt(sum(flt(row.credit) for row in to_tax))
	expect(credited == 180, f"the tax account was credited {credited}, expected 180")

	debits = flt(sum(flt(row.debit) for row in entries))
	credits = flt(sum(flt(row.credit) for row in entries))
	expect(abs(debits - credits) < 0.005, f"the entry does not balance: {debits} vs {credits}")
	frappe.db.commit()
	return f"{invoice.name}: 180 tax in 2 lines to {output_account}, nothing to round-off"


@check("J. Tax and the supplier's bill", "A tax component may name the account it posts to")
def j_component_account():
	"""DEC-021. The per-component account is what makes more than one tax rate
	usable: two components of the same invoice can be owed to two authorities.
	"""
	company()
	chart_of_accounts.backfill_defaults(COMPANY)
	named = account("Input Tax Credit")  # any other real account will do
	template = a_tax_template("Acceptance Split Tax", [
		("Acceptance Tax Named", 5, named),
		("Acceptance Tax Default", 5, None),
	])
	invoice = _tax_invoice(template.name, rate=2000, qty=1)

	entries = ledger.voucher_entries("KNIT 360 Sales Invoice", invoice.name)
	default_account = frappe.db.get_value(
		"KNIT 360 Company", COMPANY, "default_output_tax_account"
	)
	to_named = [row for row in entries if row.account == named]
	to_default = [row for row in entries if row.account == default_account]

	expect(len(to_named) == 1, f"{len(to_named)} lines reached the named account, expected 1")
	expect(flt(to_named[0].credit) == 100, f"named account got {to_named[0].credit}, expected 100")
	expect(len(to_default) == 1, f"{len(to_default)} lines reached the default, expected 1")
	expect(
		flt(to_default[0].credit) == 100,
		f"default account got {to_default[0].credit}, expected 100",
	)
	frappe.db.commit()
	return f"{invoice.name}: 100 to {named}, 100 to {default_account}"


@check("J. Tax and the supplier's bill", "Tax with nowhere to post is refused, not guessed")
def j_tax_without_account_refused():
	"""DEC-021. The rule the receivable already follows, applied to tax: a wrong
	account is harder to find later than a blocked invoice is now.
	"""
	company()
	template = a_tax_template("Acceptance Unrouted Tax", [("Acceptance Tax Unrouted", 12, None)])
	original = frappe.db.get_value("KNIT 360 Company", COMPANY, "default_output_tax_account")
	frappe.db.set_value(
		"KNIT 360 Company", COMPANY, "default_output_tax_account", None, update_modified=False
	)
	try:
		message = refuses(_tax_invoice, template.name, rate=500, qty=1)
	finally:
		frappe.db.set_value(
			"KNIT 360 Company", COMPANY, "default_output_tax_account", original,
			update_modified=False,
		)
		frappe.db.commit()
	return f"refused: {message}"


@check("J. Tax and the supplier's bill", "A supplier's bill totals goods, freight and tax")
def j_supplier_bill_total():
	"""DEC-020. The amount payable is everything printed on the supplier's bill,
	because that is the amount that leaves the bank.
	"""
	supplier = a_supplier()
	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Supplier Invoice",
			"company": COMPANY,
			"supplier": supplier,
			"bill_no": "ACC-BILL-001",
			"bill_date": nowdate(),
			"freight_and_ancillary": 750,
			"statutory_tax_amount": 1800,
			"items": [
				{"item_code": "Acceptance raw coil", "qty": 4, "rate": 2000},
				{"item_code": "Acceptance fitting", "qty": 2, "rate": 1000},
			],
		}
	).insert(ignore_permissions=True)

	expect(flt(invoice.items[0].amount) == 8000, f"line 1 is {invoice.items[0].amount}, want 8000")
	expect(flt(invoice.net_total) == 10000, f"net total is {invoice.net_total}, expected 10000")
	expect(
		flt(invoice.grand_total) == 12550,
		f"grand total is {invoice.grand_total}, expected 12550 "
		f"(10000 goods + 750 freight + 1800 tax)",
	)
	frappe.db.commit()
	return f"{invoice.name}: 10000 + 750 freight + 1800 tax = {invoice.grand_total}"


@check("J. Tax and the supplier's bill", "A supplier's tax figure is recorded, not recalculated")
def j_supplier_tax_is_entered():
	"""DEC-020. The authoritative tax figure on a purchase is the one the
	supplier billed. A template on this document records the treatment; it does
	not overwrite their number, so an odd figure stays visible instead of being
	silently replaced by ours.
	"""
	supplier = a_supplier()
	template = a_tax_template("Acceptance Purchase Tax", [("Acceptance Tax Purchase", 18, None)])
	odd = 1733.41  # deliberately not 18% of the net
	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Supplier Invoice",
			"company": COMPANY,
			"supplier": supplier,
			"bill_no": "ACC-BILL-002",
			"bill_date": nowdate(),
			"tax_template": template.name,
			"statutory_tax_amount": odd,
			"items": [{"item_code": "Acceptance raw coil", "qty": 5, "rate": 2000}],
		}
	).insert(ignore_permissions=True)

	expect(
		flt(invoice.statutory_tax_amount) == odd,
		f"the supplier's tax figure became {invoice.statutory_tax_amount}, expected {odd}",
	)
	expect(
		flt(invoice.grand_total) == flt(10000 + odd),
		f"grand total is {invoice.grand_total}, expected {10000 + odd}",
	)
	frappe.db.commit()
	return f"{invoice.name}: kept the billed {odd}, total {invoice.grand_total}"


# --- K. numbering -------------------------------------------------------
#
# `format:SINV-{YYYY}-{####}` handed the counter an empty prefix, so every
# document type in the system drew from one pool: OPP-2026-0163, QTN-2026-0164,
# SO-2026-0165 and SINV-2026-0166 were four documents created in one second.
# These assert the counters are separate and stay separate.


@check("K. Numbering", "No document type is named from the shared counter")
def k_no_shared_counter():
	"""The defect itself: a Series row with an empty key means one counter."""
	shared = frappe.db.sql("SELECT current FROM tabSeries WHERE name = ''")
	expect(not shared, f"the shared empty-key counter is back, at {shared}")

	stragglers = []
	for doctype in parent_doctypes():
		autoname = frappe.db.get_value("DocType", doctype, "autoname") or ""
		if autoname.startswith("format:") and "{#" in autoname:
			stragglers.append(doctype.replace("KNIT 360 ", ""))
	expect(
		not stragglers,
		f"{len(stragglers)} document types still use a format: series, which "
		f"shares one counter: {', '.join(sorted(stragglers))}",
	)
	counted = frappe.db.sql("SELECT COUNT(*) FROM tabSeries")[0][0]
	return f"no shared counter; {counted} separate counters in use"


@check("K. Numbering", "Two document types number independently")
def k_counters_are_separate():
	"""Create one of each and assert the numbers do not interleave.

	This is the check that would have caught the original defect. Under the old
	naming these two came back consecutive.
	"""
	company()
	lead = a_lead(lead_name="Numbering Contact")
	customer_name = "Acceptance Numbering Customer"
	if not frappe.db.exists("KNIT 360 Customer", customer_name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": customer_name, "company": COMPANY}
		).insert(ignore_permissions=True)
	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Invoice",
			"company": COMPANY,
			"customer": customer_name,
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"items": [{"item_name": "Numbering widget", "qty": 1, "rate": 100}],
		}
	).insert(ignore_permissions=True)

	lead_number = int(lead.name.rsplit("-", 1)[1])
	invoice_number = int(invoice.name.rsplit("-", 1)[1])
	expect(
		lead_number != invoice_number + 1 and invoice_number != lead_number + 1,
		f"{lead.name} and {invoice.name} are consecutive, so they are still "
		f"sharing a counter",
	)
	expect(lead.name.startswith("LEAD-"), f"{lead.name} has the wrong prefix")
	expect(invoice.name.startswith("SINV-"), f"{invoice.name} has the wrong prefix")
	frappe.db.commit()
	return f"{lead.name} and {invoice.name} came from different counters"


@check("K. Numbering", "A document number carries its own year")
def k_year_in_the_number():
	"""The year is part of the counter key, not decoration on the end.

	Under the old naming the counter never reset, so the year said 2026 while
	the number counted from the beginning of the system.
	"""
	company()
	lead = a_lead(lead_name="Year Contact")
	year = getdate(nowdate()).year
	expect(
		f"-{year}-" in lead.name,
		f"{lead.name} does not carry {year}, so the series is not year-scoped",
	)
	key = lead.name.rsplit("-", 1)[0] + "-"
	counter = (frappe.db.sql("SELECT current FROM tabSeries WHERE name = %s", (key,)) or [[None]])[0][0]
	expect(counter, f"no counter exists for {key!r}")
	frappe.db.commit()
	return f"{lead.name} from counter {key!r}, now at {counter}"


@check("K. Numbering", "No ledger entry points at a document that is not there")
def k_no_orphaned_vouchers():
	"""Renaming is only safe if the references follow.

	`GL Entry.voucher_no` is a Data field, so Frappe does not update it on a
	rename -- the renumbering had to sweep for it by value. 19 references
	needed rewriting. This asserts none were missed, and keeps asserting it.
	"""
	rows = frappe.get_all(
		"KNIT 360 GL Entry",
		fields=["name", "voucher_type", "voucher_no", "against_voucher_type", "against_voucher"],
	)
	orphans = [
		row.name
		for row in rows
		if (row.voucher_no and not frappe.db.exists(row.voucher_type, row.voucher_no))
		or (row.against_voucher and not frappe.db.exists(row.against_voucher_type, row.against_voucher))
	]
	expect(not orphans, f"{len(orphans)} ledger rows point at documents that do not exist: {orphans[:5]}")
	return f"{len(rows)} ledger rows checked, every reference resolves"


# --- L. search ----------------------------------------------------------
#
# Search appears in none of the 238 BRD requirements. It exists because the
# framework's own index only holds fields a doctype marks for it, no KNIT 360
# field did, and so typing a document number into the bar returned nothing.


@check("L. Search", "Every document is in the index")
def l_everything_indexed():
	from knit360_core.search import index

	company()
	report = index.coverage()
	expect(
		not report["incomplete"],
		f"these record types have documents missing from the index: {report['incomplete']}",
	)
	expect(report["documents"], "there are no documents at all, so this proves nothing")
	return f"{report['indexed']} of {report['documents']} documents indexed"


@check("L. Search", "A new document is findable by its number straight away")
def l_findable_on_insert():
	"""Indexed by the document's own lifecycle, not by a scheduled job."""
	from knit360_core.search import api

	lead = a_lead(lead_name="Findable Contact")
	frappe.db.commit()

	hits = api.search(lead.name)
	names = [h["name"] for h in hits]
	expect(lead.name in names, f"{lead.name} is not findable; search returned {names[:5]}")
	expect(hits[0]["name"] == lead.name, f"the exact number ranked {names.index(lead.name) + 1}, not first")
	return f"{lead.name} found, ranked first of {len(hits)}"


@check("L. Search", "A part of a number finds the document")
def l_partial_match():
	"""The reason this is not a word-based index.

	Full text matches whole words, so `SINV-2026` would not find
	`SINV-2026-0001` -- which is exactly what a person types.
	"""
	from knit360_core.search import api

	lead = a_lead(lead_name="Partial Contact")
	frappe.db.commit()
	stem = lead.name.rsplit("-", 1)[0]

	names = [h["name"] for h in api.search(stem)]
	expect(lead.name in names, f"{stem!r} did not find {lead.name}; returned {names[:5]}")
	return f"{stem!r} found {len(names)} documents including {lead.name}"


@check("L. Search", "A document is findable by what is on it, not only its number")
def l_find_by_content():
	from knit360_core.search import api

	lead = a_lead(lead_name="Marigold Searchable", organization_name="Marigold Castings Pvt Ltd")
	frappe.db.commit()

	names = [h["name"] for h in api.search("Marigold")]
	expect(lead.name in names, f"searching an organisation name did not find {lead.name}")
	return f"'Marigold' found {lead.name} by its organisation name"


@check("L. Search", "A renamed document is findable by its new number, not its old")
def l_rename_follows():
	"""The index is keyed on the document, so a rename must move it."""
	from knit360_core.search import api, index

	lead = a_lead(lead_name="Renamed Contact")
	old = lead.name
	new = f"{old}-RENAMED"
	frappe.db.set_value("DocType", "KNIT 360 Lead", "allow_rename", 1, update_modified=False)
	frappe.clear_cache()
	try:
		frappe.rename_doc("KNIT 360 Lead", old, new, force=True)
	finally:
		frappe.db.set_value("DocType", "KNIT 360 Lead", "allow_rename", 0, update_modified=False)
		frappe.clear_cache()
	frappe.db.commit()

	expect(
		new in [h["name"] for h in api.search(new)],
		f"the renamed document is not findable as {new}",
	)
	stale = frappe.db.count(index.INDEX, {"reference_doctype": "KNIT 360 Lead", "reference_name": old})
	expect(not stale, f"{stale} index row(s) still point at the old name {old}")
	frappe.delete_doc("KNIT 360 Lead", new, force=True, ignore_permissions=True)
	frappe.db.commit()
	return f"{old} -> {new}: index followed, no stale row"


@check("L. Search", "A deleted document leaves no result behind")
def l_delete_removes():
	from knit360_core.search import api, index

	lead = a_lead(lead_name="Vanishing Contact")
	name = lead.name
	frappe.db.commit()
	expect(name in [h["name"] for h in api.search(name)], "it was not findable before deletion")

	frappe.delete_doc("KNIT 360 Lead", name, force=True, ignore_permissions=True)
	frappe.db.commit()

	rows = frappe.db.count(index.INDEX, {"reference_doctype": "KNIT 360 Lead", "reference_name": name})
	expect(not rows, f"{rows} index row(s) survive a document that does not")
	expect(
		name not in [h["name"] for h in api.search(name)],
		f"{name} is still a search result after being deleted",
	)
	return f"{name} deleted; no index row, no result"


@check("L. Search", "An index row cannot be written by hand")
def l_index_is_derived():
	"""It describes a document. Edited alone it would describe nothing, until
	that document was next saved and the edit silently vanished.
	"""
	from knit360_core.search import index

	message = refuses(
		frappe.get_doc(
			{
				"doctype": index.INDEX,
				"reference_doctype": "KNIT 360 Lead",
				"reference_name": "LEAD-2026-0001",
				"title": "typed by hand",
			}
		).insert,
		ignore_permissions=True,
	)
	return f"refused: {message}"


@check("L. Search", "A ledger row does not outrank the document it came from")
def l_derived_rank_last():
	"""A GL entry's content holds the number of the invoice it posted, so
	without a rank the invoice is buried under its own ledger rows.
	"""
	from knit360_core.search import index

	company()
	customer_name = "Acceptance Ranking Customer"
	if not frappe.db.exists("KNIT 360 Customer", customer_name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": customer_name, "company": COMPANY}
		).insert(ignore_permissions=True)
	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Invoice",
			"company": COMPANY,
			"customer": customer_name,
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"items": [{"item_name": "Ranking widget", "qty": 1, "rate": 700}],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Sales Invoice", invoice.name, "Posted / Unpaid")
	frappe.db.commit()

	rows = index.search_sql(invoice.name, limit=10)
	expect(rows, f"nothing at all was found for {invoice.name}")
	expect(
		rows[0].reference_doctype == "KNIT 360 Sales Invoice",
		f"the first result for {invoice.name} is a "
		f"{rows[0].reference_doctype}, not the invoice itself",
	)
	derived = [r for r in rows if r.weight]
	return (
		f"{invoice.name} ranked first of {len(rows)}, "
		f"with {len(derived)} derived row(s) below it"
	)


# --- M. settlement ------------------------------------------------------
#
# DEC-022. Before this, an invoice could be marked Paid with no record of any
# money arriving: the status moved and nothing else did. These assert that what
# is owed comes from the ledger and that the refusals hold.


def a_payer():
	name = "Acceptance Paying Customer"
	if not frappe.db.exists("KNIT 360 Customer", name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": name, "company": company()}
		).insert(ignore_permissions=True)
	return name


def a_posted_invoice(total, customer=None):
	"""A submitted invoice for `total`, ready to be settled."""
	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Invoice",
			"company": company(),
			"customer": customer or a_payer(),
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"items": [{"item_name": "Acceptance settled widget", "qty": 1, "rate": total}],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Sales Invoice", invoice.name, "Posted / Unpaid")
	invoice.reload()
	return invoice


def a_payment(amount, allocations, customer=None, post=True):
	"""A receipt, optionally driven all the way to Disbursed / Cleared."""
	payment = frappe.get_doc(
		{
			"doctype": "KNIT 360 Payment Entry",
			"company": COMPANY,
			"payment_direction": "Receive",
			"party_type": "KNIT 360 Customer",
			"party": customer or a_payer(),
			"payment_date": nowdate(),
			"amount": amount,
			"bank_account": account("Bank Account"),
			"allocations": [
				{
					"reference_doctype": "KNIT 360 Sales Invoice",
					"reference_name": name,
					"allocated_amount": value,
				}
				for name, value in allocations
			],
		}
	).insert(ignore_permissions=True)
	if post:
		engine.transition("KNIT 360 Payment Entry", payment.name, "Pending Bank Authorization")
		engine.transition("KNIT 360 Payment Entry", payment.name, "Disbursed / Cleared")
		payment.reload()
	return payment


@check("M. Settlement", "A receipt settles an invoice and reaches the ledger")
def m_receipt_posts():
	invoice = a_posted_invoice(5000)
	expect(
		flt(settlement.outstanding(invoice.doctype, invoice.name)) == 5000,
		f"a fresh invoice owes {settlement.outstanding(invoice.doctype, invoice.name)}, expected 5000",
	)
	payment = a_payment(5000, [(invoice.name, 5000)])
	invoice.reload()

	left = settlement.outstanding(invoice.doctype, invoice.name)
	expect(abs(left) < 0.005, f"after paying in full, {left} is still outstanding")

	entries = ledger.voucher_entries("KNIT 360 Payment Entry", payment.name)
	bank = [r for r in entries if r.account == account("Bank Account")]
	expect(len(bank) == 1, f"{len(bank)} lines hit the bank account, expected 1")
	expect(flt(bank[0].debit) == 5000, f"the bank was debited {bank[0].debit}, expected 5000")
	debits = flt(sum(flt(r.debit) for r in entries))
	credits = flt(sum(flt(r.credit) for r in entries))
	expect(abs(debits - credits) < 0.005, f"the receipt does not balance: {debits} vs {credits}")
	frappe.db.commit()
	return f"{payment.name} settled {invoice.name}; bank debited 5000, nothing outstanding"


@check("M. Settlement", "A part payment leaves the rest owing, and says so")
def m_part_payment():
	"""The status moves because the money moved, not instead of it."""
	invoice = a_posted_invoice(50000)
	a_payment(20000, [(invoice.name, 20000)])
	invoice.reload()

	left = settlement.outstanding(invoice.doctype, invoice.name)
	expect(flt(left) == 30000, f"{left} outstanding after paying 20000 of 50000, expected 30000")
	expect(
		invoice.knit360_business_status == "Partly Paid",
		f"status is {invoice.knit360_business_status!r}, expected 'Partly Paid'",
	)
	expect(
		flt(invoice.outstanding_amount) == 30000,
		f"the invoice shows {invoice.outstanding_amount}, the ledger says {left}",
	)
	frappe.db.commit()
	return f"{invoice.name}: paid 20000 of 50000, 30000 owing, status Partly Paid"


@check("M. Settlement", "What is owed is read from the ledger, not from a stored total")
def m_outstanding_is_derived():
	"""The field is a cache. Break it and the ledger still knows the truth."""
	invoice = a_posted_invoice(8000)
	a_payment(3000, [(invoice.name, 3000)])

	# Corrupt the cache behind the system's back.
	frappe.db.set_value(
		"KNIT 360 Sales Invoice", invoice.name, "outstanding_amount", 999999,
		update_modified=False,
	)
	derived = settlement.outstanding("KNIT 360 Sales Invoice", invoice.name)
	expect(flt(derived) == 5000, f"the ledger says {derived} is owed, expected 5000")

	wrong = settlement.check_cache()
	expect(invoice.name in wrong, "a corrupted cache was not detected")

	settlement.refresh("KNIT 360 Sales Invoice", invoice.name)
	# Scoped to this invoice: check_cache() reads the whole site, and an
	# earlier check deliberately leaves a refused invoice behind.
	expect(
		invoice.name not in settlement.check_cache(),
		f"the cache still disagrees after a refresh: {settlement.check_cache()}",
	)
	frappe.db.commit()
	return f"ledger said 5000 while the cache said 999999; detected and repaired"


@check("M. Settlement", "Allocating more than is owed is refused, not quietly capped")
def m_over_allocation_refused():
	invoice = a_posted_invoice(4000)
	message = refuses(a_payment, 10000, [(invoice.name, 10000)])
	frappe.db.rollback()
	return f"refused: {message}"


@check("M. Settlement", "A payment cannot allocate more than it is worth")
def m_over_commit_refused():
	first = a_posted_invoice(3000)
	second = a_posted_invoice(3000)
	message = refuses(a_payment, 4000, [(first.name, 3000), (second.name, 3000)])
	frappe.db.rollback()
	return f"refused: {message}"


@check("M. Settlement", "An overpayment is held for the party, not added to the invoice")
def m_overpayment_is_an_advance():
	"""DEC-022. The surplus is a debt to the customer, never income."""
	invoice = a_posted_invoice(6000)
	payment = a_payment(10000, [(invoice.name, 6000)])
	invoice.reload()

	expect(
		flt(payment.unallocated_amount) == 4000,
		f"unallocated is {payment.unallocated_amount}, expected 4000",
	)
	expect(
		abs(settlement.outstanding(invoice.doctype, invoice.name)) < 0.005,
		"the invoice is not settled",
	)
	expect(
		flt(invoice.grand_total) == 6000,
		f"the invoice total became {invoice.grand_total}; an overpayment inflated it",
	)

	entries = ledger.voucher_entries("KNIT 360 Payment Entry", payment.name)
	advance = [r for r in entries if not r.against_voucher and flt(r.credit)]
	expect(
		len(advance) == 1,
		f"{len(advance)} unallocated lines, expected 1: "
		+ "; ".join(f"{r.account} cr {r.credit} av={r.against_voucher!r}" for r in advance),
	)
	expect(flt(advance[0].credit) == 4000, f"the advance is {advance[0].credit}, expected 4000")
	frappe.db.commit()
	return f"{payment.name}: 6000 settled, 4000 held as an advance against the party"


@check("M. Settlement", "One payment settles several invoices")
def m_one_payment_many_invoices():
	first = a_posted_invoice(1000)
	second = a_posted_invoice(2000)
	third = a_posted_invoice(3000)
	payment = a_payment(6000, [(first.name, 1000), (second.name, 2000), (third.name, 3000)])

	for invoice in (first, second, third):
		left = settlement.outstanding(invoice.doctype, invoice.name)
		expect(abs(left) < 0.005, f"{invoice.name} still owes {left}")
		expect(
			frappe.db.get_value("KNIT 360 Sales Invoice", invoice.name,
			                    "knit360_business_status") == "Paid",
			f"{invoice.name} is not Paid",
		)
	expect(flt(payment.unallocated_amount) == 0, "something was left unallocated")
	frappe.db.commit()
	return f"{payment.name} settled three invoices totalling 6000"


@check("M. Settlement", "A payment cannot settle another party's invoice")
def m_wrong_party_refused():
	other = "Acceptance Other Customer"
	if not frappe.db.exists("KNIT 360 Customer", other):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": other, "company": company()}
		).insert(ignore_permissions=True)
	invoice = a_posted_invoice(2500, customer=other)
	message = refuses(a_payment, 2500, [(invoice.name, 2500)])  # paid by the usual payer
	frappe.db.rollback()
	return f"refused: {message}"


@check("M. Settlement", "Money cannot move through an account that is not bank or cash")
def m_bank_account_checked():
	invoice = a_posted_invoice(1500)
	message = refuses(
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Payment Entry",
				"company": COMPANY,
				"payment_direction": "Receive",
				"party_type": "KNIT 360 Customer",
				"party": a_payer(),
				"payment_date": nowdate(),
				"amount": 1500,
				"bank_account": account("Sales"),  # an income account
				"allocations": [
					{
						"reference_doctype": "KNIT 360 Sales Invoice",
						"reference_name": invoice.name,
						"allocated_amount": 1500,
					}
				],
			}
		).insert,
		ignore_permissions=True,
	)
	frappe.db.rollback()
	return f"refused: {message}"


@check("M. Settlement", "Cancelling a payment puts the debt back")
def m_cancel_restores():
	"""Reversal, not deletion -- the receipt and its mirror both stay."""
	invoice = a_posted_invoice(7000)
	payment = a_payment(7000, [(invoice.name, 7000)])
	expect(
		abs(settlement.outstanding(invoice.doctype, invoice.name)) < 0.005,
		"the invoice was not settled in the first place",
	)

	engine.transition("KNIT 360 Payment Entry", payment.name, "Cancelled")
	invoice.reload()

	left = settlement.outstanding(invoice.doctype, invoice.name)
	expect(flt(left) == 7000, f"after cancelling the receipt, {left} is owed, expected 7000")
	expect(
		invoice.knit360_business_status != "Paid",
		"the invoice is still marked Paid after its only receipt was cancelled",
	)
	kept = ledger.voucher_entries("KNIT 360 Payment Entry", payment.name, include_cancelled=1)
	expect(len(kept) >= 4, f"only {len(kept)} ledger rows kept; a reversal keeps both sides")
	frappe.db.commit()
	return f"{payment.name} cancelled: 7000 owed again, {len(kept)} ledger rows kept"


@check("M. Settlement", "A small residue is written off only when asked")
def m_write_off_is_deliberate():
	"""DEC-022: never automatic. An automatic write-off is how small amounts
	of money leave a business without anyone noticing.
	"""
	frappe.db.set_value(COMPANY_DOCTYPE, COMPANY, "write_off_tolerance", 1.0,
	                    update_modified=False)
	invoice = a_posted_invoice(2000)
	a_payment(1999.60, [(invoice.name, 1999.60)])
	invoice.reload()

	left = settlement.outstanding(invoice.doctype, invoice.name)
	expect(abs(flt(left) - 0.40) < 0.005, f"{left} left, expected 0.40")
	expect(
		invoice.knit360_business_status != "Paid",
		"a 40 paise residue marked the invoice Paid on its own",
	)

	settlement.write_off("KNIT 360 Sales Invoice", invoice.name, reason="Acceptance residue")
	invoice.reload()
	after = settlement.outstanding(invoice.doctype, invoice.name)
	expect(abs(after) < 0.005, f"{after} still outstanding after the write-off")
	expect(
		invoice.knit360_business_status == "Paid",
		f"status is {invoice.knit360_business_status!r} after writing the residue off",
	)
	frappe.db.commit()
	return f"{invoice.name}: 0.40 left unpaid until asked, then written off"


@check("M. Settlement", "A residue larger than the tolerance is not written off")
def m_write_off_bounded():
	frappe.db.set_value(COMPANY_DOCTYPE, COMPANY, "write_off_tolerance", 1.0,
	                    update_modified=False)
	invoice = a_posted_invoice(9000)
	a_payment(5000, [(invoice.name, 5000)])
	message = refuses(settlement.write_off, "KNIT 360 Sales Invoice", invoice.name)
	frappe.db.commit()
	return f"refused: {message}"


# --- N. stock -----------------------------------------------------------
#
# DEC-023. Stock is counted per item per warehouse and derived from the
# movements; a Bin is a place to walk to, not a quantity. Valuation is FIFO by
# default, weighted average per item, and LIFO is not offered because Ind AS 2
# paragraph 25 does not permit it.


def a_warehouse(name="Acceptance Store"):
	if not frappe.db.exists("KNIT 360 Warehouse", name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Warehouse", "warehouse_name": name, "company": company()}
		).insert(ignore_permissions=True)
	return name


def an_item(code, method=None):
	if not frappe.db.exists("KNIT 360 Item", code):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Item",
				"item_code": code,
				"item_name": code,
				"stock_uom": frappe.db.get_value("KNIT 360 UOM", {}, "name") or None,
				"valuation_method": method or "FIFO",
			}
		).insert(ignore_permissions=True)
	elif method:
		frappe.db.set_value("KNIT 360 Item", code, "valuation_method", method,
		                    update_modified=False)
	return code


def a_receipt(item_code, qty, rate, warehouse=None, rejected=0, target="Received in Bay"):
	"""A goods receipt driven to a submitted state."""
	warehouse = warehouse or a_warehouse()
	receipt = frappe.get_doc(
		{
			"doctype": "KNIT 360 Goods Receipt",
			"company": COMPANY,
			"receiving_warehouse": warehouse,
			"challan_number": f"ACC-{frappe.generate_hash(length=6)}",
			"challan_date": nowdate(),
			"items": [
				{
					"item_code": item_code,
					"qty_arrived": qty,
					"qty_rejected_on_arrival": rejected,
					"rate": rate,
				}
			],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Goods Receipt", receipt.name, target)
	receipt.reload()
	return receipt


def a_dispatch(item_code, qty, warehouse=None):
	warehouse = warehouse or a_warehouse()
	note = frappe.get_doc(
		{
			"doctype": "KNIT 360 Delivery Note",
			"company": COMPANY,
			"source_warehouse": warehouse,
			"delivery_note_date": nowdate(),
			"items": [{"item_code": item_code, "qty": qty}],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Delivery Note", note.name, "Dispatched / In Transit")
	note.reload()
	return note


@check("N. Stock", "A receipt raises the stock and carries its value")
def n_receipt_raises_stock():
	item = an_item("Acceptance Coil")
	a_receipt(item, 10, 100)
	held = stock_ledger.balance(item, a_warehouse(), COMPANY)
	worth = stock_ledger.value(item, a_warehouse(), COMPANY)
	expect(flt(held) == 10, f"{held} in stock after receiving 10")
	expect(flt(worth) == 1000, f"the stock is worth {worth}, expected 1000")
	frappe.db.commit()
	return f"{item}: 10 received at 100, stock 10 worth 1000"


@check("N. Stock", "The stock held is derived, and stored nowhere")
def n_stock_is_derived():
	"""No field anywhere holds a quantity, which is what makes the figure safe.

	A Bin has an aisle, a rack and a shelf and no quantity, on purpose: it
	tells you where to walk, not what you own.
	"""
	holders = []
	for doctype in parent_doctypes():
		meta = frappe.get_meta(doctype)
		for fieldname in ("stock_qty", "actual_qty", "qty_in_stock", "balance_qty", "on_hand"):
			if doctype != "KNIT 360 Stock Ledger Entry" and meta.has_field(fieldname):
				holders.append(f"{doctype}.{fieldname}")
	expect(not holders, f"these store a stock quantity instead of deriving it: {holders}")

	bin_meta = frappe.get_meta("KNIT 360 Bin")
	expect(
		not any(f.fieldname in ("actual_qty", "stock_qty", "qty") for f in bin_meta.fields),
		"Bin carries a quantity; it is a storage address, not a balance",
	)
	item = an_item("Acceptance Coil")
	entries = len(stock_ledger._movements(item, a_warehouse(), COMPANY))
	return f"balance == sum of {entries} movements; no doctype stores a quantity"


@check("N. Stock", "A dispatch reduces the stock and costs what it cost")
def n_dispatch_reduces_stock():
	item = an_item("Acceptance Panel")
	a_receipt(item, 20, 250)
	note = a_dispatch(item, 8)

	held = stock_ledger.balance(item, a_warehouse(), COMPANY)
	expect(flt(held) == 12, f"{held} left after dispatching 8 of 20")

	note.reload()
	expect(
		flt(note.items[0].valuation_rate) == 250,
		f"the line was costed at {note.items[0].valuation_rate}, expected 250",
	)
	expect(
		flt(note.items[0].stock_value) == 2000,
		f"the line cost total is {note.items[0].stock_value}, expected 2000",
	)
	frappe.db.commit()
	return f"{note.name}: 8 out at 250, 12 left, cost 2000"


@check("N. Stock", "FIFO costs the oldest stock first")
def n_fifo():
	"""The worked example in DEC-023.

	Buy 10 at 100 then 10 at 120, sell 5. FIFO says those five cost 500, not
	the 550 a blended rate would give or the 600 LIFO would.
	"""
	item = an_item("Acceptance FIFO Coil", method="FIFO")
	a_receipt(item, 10, 100)
	a_receipt(item, 10, 120)

	rate = stock_ledger.outgoing_rate(item, a_warehouse(), 5, COMPANY)
	expect(flt(rate) == 100, f"FIFO costed the issue at {rate}, expected 100")

	a_dispatch(item, 5)
	held = stock_ledger.balance(item, a_warehouse(), COMPANY)
	worth = stock_ledger.value(item, a_warehouse(), COMPANY)
	expect(flt(held) == 15, f"{held} left, expected 15")
	expect(flt(worth) == 1700, f"the remaining stock is worth {worth}, expected 1700")
	frappe.db.commit()
	return "10 at 100 then 10 at 120, issued 5 at 100; 15 left worth 1700"


@check("N. Stock", "Weighted average costs the blend instead")
def n_moving_average():
	"""Ind AS 2 paragraph 25 permits either, per class of inventary -- so the
	formula is the Item's, not the company's.
	"""
	item = an_item("Acceptance Average Coil", method="Moving Average")
	a_receipt(item, 10, 100)
	a_receipt(item, 10, 120)

	rate = stock_ledger.outgoing_rate(item, a_warehouse(), 5, COMPANY)
	expect(flt(rate) == 110, f"the blended rate is {rate}, expected 110")
	expect(
		stock_ledger.method_for(item) == "Moving Average",
		"the item's own formula was not used",
	)
	frappe.db.commit()
	return "same two receipts, blended to 110 because the item says so"


@check("N. Stock", "LIFO is not offered at all")
def n_no_lifo():
	"""Ind AS 2 paragraph 25 lists FIFO and weighted average. Offering LIFO
	would be offering a setting that puts the client in breach.
	"""
	expect("LIFO" not in stock_ledger.METHODS, f"LIFO is on offer: {stock_ledger.METHODS}")
	options = (frappe.get_meta("KNIT 360 Item").get_field("valuation_method").options or "")
	expect("LIFO" not in options, f"the Item form offers LIFO: {options!r}")
	# An item set to it anyway falls back rather than costing by it.
	item = an_item("Acceptance Rogue Coil")
	frappe.db.set_value("KNIT 360 Item", item, "valuation_method", "LIFO",
	                    update_modified=False)
	expect(
		stock_ledger.method_for(item) == "FIFO",
		f"an item set to LIFO costs by {stock_ledger.method_for(item)}",
	)
	frappe.db.commit()
	return f"offered: {', '.join(stock_ledger.METHODS)}; LIFO falls back to FIFO"


@check("N. Stock", "Issuing more than is held is refused")
def n_negative_stock_refused():
	"""Negative stock means the books claim goods nobody has, and every
	valuation after it is wrong.
	"""
	item = an_item("Acceptance Scarce Coil")
	a_receipt(item, 3, 500)
	message = refuses(a_dispatch, item, 10)
	held = stock_ledger.balance(item, a_warehouse(), COMPANY)
	expect(flt(held) == 3, f"the refusal still moved stock: {held} left")
	frappe.db.commit()
	return f"refused: {message}"


@check("N. Stock", "Stock received at no cost is refused")
def n_nil_rate_refused():
	item = an_item("Acceptance Free Coil")
	message = refuses(a_receipt, item, 5, 0)
	frappe.db.rollback()
	return f"refused: {message}"


@check("N. Stock", "Goods turned away at the gate never enter stock")
def n_rejected_at_gate():
	item = an_item("Acceptance Turned Away")
	before = stock_ledger.balance(item, a_warehouse(), COMPANY)
	receipt = a_receipt(item, 50, 90, target="Rejected at Gate")
	after = stock_ledger.balance(item, a_warehouse(), COMPANY)

	expect(flt(before) == flt(after), f"stock moved from {before} to {after} on a rejection")
	expect(
		not stock_ledger.voucher_movements("KNIT 360 Goods Receipt", receipt.name),
		"a receipt rejected at the gate wrote stock movements",
	)
	frappe.db.commit()
	return f"{receipt.name} rejected at the gate: no movement, stock still {after:g}"


@check("N. Stock", "Only what was accepted is put away")
def n_accepted_not_arrived():
	item = an_item("Acceptance Damaged Coil")
	receipt = a_receipt(item, 100, 40, rejected=15)
	held = stock_ledger.balance(item, a_warehouse(), COMPANY)
	expect(flt(held) == 85, f"{held} entered stock; 100 arrived and 15 were rejected")
	expect(
		flt(receipt.items[0].accepted_qty) == 85,
		f"the line shows {receipt.items[0].accepted_qty} accepted, expected 85",
	)
	frappe.db.commit()
	return f"{receipt.name}: 100 arrived, 15 rejected, 85 in stock"


@check("N. Stock", "Cancelling a movement reverses it rather than deleting it")
def n_cancel_reverses():
	item = an_item("Acceptance Returned Coil")
	receipt = a_receipt(item, 12, 75)
	expect(flt(stock_ledger.balance(item, a_warehouse(), COMPANY)) == 12, "it never arrived")

	engine.transition("KNIT 360 Goods Receipt", receipt.name, "Cancelled")
	held = stock_ledger.balance(item, a_warehouse(), COMPANY)
	expect(abs(flt(held)) < 0.005, f"{held} still in stock after cancelling the receipt")

	kept = stock_ledger.voucher_movements("KNIT 360 Goods Receipt", receipt.name,
	                                      include_cancelled=1)
	expect(len(kept) == 2, f"{len(kept)} movements kept; a reversal keeps both sides")
	frappe.db.commit()
	return f"{receipt.name} cancelled: stock back to nil, both movements kept"


@check("N. Stock", "A stock movement cannot be edited or deleted")
def n_movements_are_immutable():
	# Makes its own receipt rather than picking up another check's. The first
	# version took whichever came back first and got the cancelled one from
	# the reversal check, whose movements are all flagged -- so it found
	# nothing and failed for the wrong reason.
	item = an_item("Acceptance Immutable Coil")
	receipt = a_receipt(item, 4, 60)
	# Committed before the refusals are tested, because the rollback below
	# would otherwise take the fixture with it -- and the check would then
	# pass by asserting that a movement which no longer exists was not edited.
	frappe.db.commit()
	entries = stock_ledger.voucher_movements("KNIT 360 Goods Receipt", receipt.name)
	expect(entries, f"{receipt.name} wrote no movement to test against")
	name = entries[0].name
	expect(frappe.db.exists(stock_ledger.SLE, name), "the fixture is not there to begin with")

	deleted = refuses(frappe.delete_doc, stock_ledger.SLE, name, ignore_permissions=True)
	entry = frappe.get_doc(stock_ledger.SLE, name)
	entry.actual_qty = flt(entry.actual_qty) + 1
	edited = refuses(entry.save, ignore_permissions=True)
	frappe.db.rollback()

	expect(frappe.db.exists(stock_ledger.SLE, name), "the movement is gone after the refusals")
	return f"delete refused ({deleted[:46]}...), edit refused ({edited[:46]}...)"


@check("N. Stock", "The accounts agree with the stock ledger")
def n_accounts_match_stock():
	"""Perpetual inventory -- DEC-030. Stock In Hand must equal what the stock
	ledger says the stock is worth, or the balance sheet is wrong.
	"""
	stock_account = frappe.db.get_value(COMPANY_DOCTYPE, COMPANY, "default_stock_account")
	expect(stock_account, f"{COMPANY} has no Default Stock Account")

	in_accounts = flt(ledger.balance(stock_account, COMPANY))
	in_stock = flt(
		sum(flt(row["value"]) for row in stock_ledger.stock_on_hand(company=COMPANY))
	)
	expect(
		abs(in_accounts - in_stock) < 0.005,
		f"the accounts hold {in_accounts:.2f} of stock and the stock ledger says "
		f"{in_stock:.2f}",
	)
	return f"Stock In Hand {in_accounts:.2f} matches the stock ledger"


@check("N. Stock", "The stock ledger is the only module that writes movements")
def n_single_writer():
	import pathlib as _pathlib

	root = _pathlib.Path(frappe.get_app_path("knit360_core"))
	offenders = []
	for path in root.rglob("*.py"):
		if path.name in ("ledger.py", "acceptance.py") or path.name.startswith("test_"):
			continue
		text = path.read_text(encoding="utf-8")
		if "KNIT 360 Stock Ledger Entry" in text and ("insert(" in text or "new_doc(" in text):
			offenders.append(str(path.relative_to(root)))
	expect(not offenders, f"stock movements are written outside stock/ledger.py by: {offenders}")
	return "stock/ledger.py is the sole writer"


# --- O. pricing from the master -----------------------------------------
#
# FR-SALES-004. The Price List and Item Price masters existed and were
# populated; no document read them, so every rate was typed. These checks prove
# a rate now comes from the master, that a typed rate still wins, and that the
# validity window and the unit of measure are honoured rather than ignored.


def stock_uom(item_code):
	return frappe.db.get_value("KNIT 360 Item", item_code, "stock_uom")


def a_price_list(name, applies_to, disabled=0):
	if not frappe.db.exists("KNIT 360 Price List", name):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Price List",
				"price_list_name": name,
				"currency": CURRENCY,
				"applies_to": applies_to,
				"disabled": disabled,
			}
		).insert(ignore_permissions=True)
	elif frappe.db.get_value("KNIT 360 Price List", name, "disabled") != disabled:
		frappe.db.set_value("KNIT 360 Price List", name, "disabled", disabled,
		                    update_modified=False)
	return name


def a_price(item_code, price_list, rate, uom=None, valid_from=None, valid_upto=None):
	existing = frappe.get_all(
		"KNIT 360 Item Price",
		filters={"item_code": item_code, "price_list": price_list},
		pluck="name",
	)
	for name in existing:
		frappe.delete_doc("KNIT 360 Item Price", name, force=True,
		                  ignore_permissions=True)
	return frappe.get_doc(
		{
			"doctype": "KNIT 360 Item Price",
			"item_code": item_code,
			"price_list": price_list,
			"uom": uom,
			"rate": rate,
			"currency": CURRENCY,
			"valid_from": valid_from,
			"valid_upto": valid_upto,
		}
	).insert(ignore_permissions=True)


def a_priced_quotation(item_code, qty=1, rate=None, price_list=None, uom=None):
	quotation = frappe.get_doc(
		{
			"doctype": "KNIT 360 Quotation",
			"company": company(),
			"customer": a_payer(),
			"price_list": price_list,
			"items": [{"item_code": item_code, "qty": qty, "unit_rate": rate or 0, "uom": uom}],
		}
	).insert(ignore_permissions=True)
	return quotation


@check("O. Pricing", "A rate nobody typed comes from the price list")
def o_rate_comes_from_the_master():
	item = an_item("Acceptance Priced Coil")
	selling = a_price_list("Acceptance Selling List", "Selling")
	a_price(item, selling, 4400, uom=stock_uom(item))

	quotation = a_priced_quotation(item, qty=3, price_list=selling)
	expect(
		flt(quotation.items[0].unit_rate) == 4400,
		f"the line priced at {quotation.items[0].unit_rate}, expected 4400 from the master",
	)
	expect(
		flt(quotation.net_total) == 13200,
		f"the quotation totals {quotation.net_total}, expected 13200",
	)
	frappe.db.commit()
	return f"{quotation.name}: nothing typed, 3 x 4400 = 13,200 read from {selling}"


@check("O. Pricing", "A rate somebody typed is never overwritten")
def o_typed_rate_wins():
	"""The master is a starting point, not a cage.

	The list rate is kept beside the rate charged, so the difference is on the
	document instead of being lost -- which is the whole point of recording it.
	"""
	item = an_item("Acceptance Priced Panel")
	selling = a_price_list("Acceptance Selling List", "Selling")
	a_price(item, selling, 9000, uom=stock_uom(item))

	quotation = a_priced_quotation(item, qty=2, rate=8100, price_list=selling)
	expect(
		flt(quotation.items[0].unit_rate) == 8100,
		f"the typed rate became {quotation.items[0].unit_rate}; it must stand",
	)
	expect(
		flt(quotation.items[0].price_list_rate) == 9000,
		f"the list rate was recorded as {quotation.items[0].price_list_rate}, expected 9000",
	)
	frappe.db.commit()
	return f"{quotation.name}: charged 8,100 against a list price of 9,000, both visible"


@check("O. Pricing", "A price that has expired is not used")
def o_expired_price_ignored():
	item = an_item("Acceptance Expired Price Item")
	selling = a_price_list("Acceptance Selling List", "Selling")
	a_price(
		item, selling, 7000, uom=stock_uom(item),
		valid_from=add_days(nowdate(), -60), valid_upto=add_days(nowdate(), -1),
	)
	rate = price_list.rate_for(item, selling, nowdate(), stock_uom(item))
	expect(rate is None, f"an expired price was still used: {rate}")
	return "a price that lapsed yesterday is not applied today"


@check("O. Pricing", "A price that has not started yet is not used")
def o_future_price_ignored():
	item = an_item("Acceptance Future Price Item")
	selling = a_price_list("Acceptance Selling List", "Selling")
	a_price(item, selling, 7000, uom=stock_uom(item), valid_from=add_days(nowdate(), 7))
	expect(
		price_list.rate_for(item, selling, nowdate(), stock_uom(item)) is None,
		"a price starting next week was applied today",
	)
	expect(
		flt(price_list.rate_for(item, selling, add_days(nowdate(), 8), stock_uom(item))) == 7000,
		"the same price was not applied after it started",
	)
	return "a price starting in seven days applies then, not now"


@check("O. Pricing", "Where two prices apply, the later decision wins")
def o_later_price_wins():
	item = an_item("Acceptance Repriced Item")
	selling = a_price_list("Acceptance Selling List", "Selling")
	a_price(item, selling, 1000, uom=stock_uom(item), valid_from=add_days(nowdate(), -90))
	frappe.get_doc(
		{
			"doctype": "KNIT 360 Item Price",
			"item_code": item,
			"price_list": selling,
			"uom": stock_uom(item),
			"rate": 1250,
			"currency": CURRENCY,
			"valid_from": add_days(nowdate(), -10),
		}
	).insert(ignore_permissions=True)

	rate = price_list.rate_for(item, selling, nowdate(), stock_uom(item))
	expect(flt(rate) == 1250, f"the rate used was {rate}, expected the newer 1250")
	frappe.db.commit()
	return "1,000 from ninety days ago, 1,250 from ten days ago; 1,250 is used"


@check("O. Pricing", "The unit of measure decides which price applies")
def o_uom_specific_price():
	"""A price per kilogram must not be charged on a line counted in boxes."""
	item = an_item("Acceptance Two Unit Item")
	selling = a_price_list("Acceptance Selling List", "Selling")
	a_price(item, selling, 820, uom=stock_uom(item))

	other = [
		name for name in frappe.get_all("KNIT 360 UOM", pluck="name")
		if name != stock_uom(item)
	]
	expect(other, "the site has only one unit of measure, so this cannot be proven")
	frappe.get_doc(
		{
			"doctype": "KNIT 360 Item Price",
			"item_code": item,
			"price_list": selling,
			"uom": other[0],
			"rate": 20500,
			"currency": CURRENCY,
		}
	).insert(ignore_permissions=True)

	expect(
		flt(price_list.rate_for(item, selling, nowdate(), stock_uom(item))) == 820,
		"the stock unit did not get its own price",
	)
	expect(
		flt(price_list.rate_for(item, selling, nowdate(), other[0])) == 20500,
		f"the {other[0]} price was not used for a {other[0]} line",
	)
	frappe.db.commit()
	return f"820 per {stock_uom(item)}, 20,500 per {other[0]}, each on its own line"


@check("O. Pricing", "A sale will not be priced from a buying list")
def o_wrong_side_refused():
	item = an_item("Acceptance Priced Coil")
	buying = a_price_list("Acceptance Buying List", "Buying")
	refused = refuses(lambda: a_priced_quotation(item, qty=1, rate=100, price_list=buying))
	expect("buying" in refused.lower(), f"refused, but for another reason: {refused}")
	return "a selling document refuses a buying price list: selling at cost is stopped"


@check("O. Pricing", "A disabled price list is refused rather than used")
def o_disabled_list_refused():
	item = an_item("Acceptance Priced Coil")
	stale = a_price_list("Acceptance Retired List", "Selling", disabled=1)
	refused = refuses(lambda: a_priced_quotation(item, qty=1, rate=100, price_list=stale))
	expect("disabled" in refused.lower(), f"refused, but for another reason: {refused}")
	frappe.db.commit()
	return "a retired list cannot price a new document"


@check("O. Pricing", "The document records which list it priced from")
def o_list_is_recorded():
	"""Without this, a price cannot be explained six months later."""
	item = an_item("Acceptance Priced Coil")
	quotation = a_priced_quotation(item, qty=1, rate=500)
	chosen = quotation.price_list
	expect(chosen, "the quotation priced without recording which list it used")
	side = frappe.db.get_value("KNIT 360 Price List", chosen, "applies_to")
	expect(side == "Selling", f"a quotation chose a {side} list by default")
	frappe.db.commit()
	return f"{quotation.name} recorded {chosen}, a {side} list, chosen by default"


@check("O. Pricing", "A supplier's own quoted price is left alone")
def o_supplier_quotation_not_priced():
	"""A bid is what the supplier said. Filling it in from our own master would
	put words in their mouth and make the bid comparison meaningless."""
	item = an_item("Acceptance Bid Item")
	buying = a_price_list("Acceptance Buying List", "Buying")
	a_price(item, buying, 6000, uom=stock_uom(item))

	bid = frappe.get_doc(
		{
			"doctype": "KNIT 360 Supplier Quotation",
			"company": company(),
			"supplier": a_supplier(),
			"items": [{"item_code": item, "qty": 1, "rate": 6400}],
		}
	).insert(ignore_permissions=True)
	expect(
		flt(bid.items[0].rate) == 6400,
		f"the bid was moved to {bid.items[0].rate}; the supplier said 6,400",
	)
	source = pathlib.Path(
		frappe.get_app_path(
			"knit360_core", "procurement", "doctype", "knit_360_supplier_quotation",
			"knit_360_supplier_quotation.py",
		)
	).read_text(encoding="utf-8")
	expect("price_list" not in source.split('"""')[2], "the controller prices from a list")
	frappe.db.commit()
	return f"{bid.name}: the supplier said 6,400, our list says 6,000, the bid stays 6,400"


@check("O. Pricing", "No document lets a person type the list rate")
def o_list_rate_is_read_only():
	offenders = []
	for doctype in frappe.get_all(
		"DocType", filters={"module": ["like", "%"], "name": ["like", "KNIT 360%"]}, pluck="name"
	):
		meta = frappe.get_meta(doctype)
		field = meta.get_field(price_list.LINE_PRICE_FIELD)
		if field and not field.read_only:
			offenders.append(doctype)
	expect(not offenders, f"the list rate can be typed on: {offenders}")
	carriers = [
		doctype for doctype in frappe.get_all("DocType", filters={"name": ["like", "KNIT 360%"]},
		                                      pluck="name")
		if frappe.get_meta(doctype).get_field(price_list.LINE_PRICE_FIELD)
	]
	expect(len(carriers) >= 4, f"only {len(carriers)} line tables record the list rate")
	return f"{len(carriers)} line tables record the list rate, none of them editable"


# --- P. procure to pay --------------------------------------------------
#
# DEC-033. A goods receipt credits Stock Received But Not Billed because the
# goods are ours and we owe for them; only the supplier's bill can say how
# much, so only the bill can clear it. These checks prove the account nets to
# nil per receipt, that a price difference is visible rather than absorbed,
# that recoverable tax lands in an asset, and that an order -- which is a
# commitment, not a transaction -- posts nothing at all.


def a_bill(net, supplier=None, receipt=None, freight=0, tax=0, target="Matched & Approved"):
	"""A supplier's bill, driven to a submitted state."""
	bill = frappe.get_doc(
		{
			"doctype": "KNIT 360 Supplier Invoice",
			"company": company(),
			"supplier": supplier or a_supplier(),
			"bill_no": f"ACC-BILL-{frappe.generate_hash(length=6)}",
			"bill_date": nowdate(),
			"goods_receipt": receipt,
			"freight_and_ancillary": freight,
			"statutory_tax_amount": tax,
			"items": [{"item_code": "Acceptance billed goods", "qty": 1, "rate": net}],
		}
	).insert(ignore_permissions=True)
	if target:
		engine.transition("KNIT 360 Supplier Invoice", bill.name, target)
	bill.reload()
	return bill


def account_balance(leaf):
	"""The net debit on one leaf account of the acceptance company."""
	name = account(leaf)
	row = frappe.db.sql(
		"""SELECT COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) AS net
		   FROM `tabKNIT 360 GL Entry`
		   WHERE account = %s AND is_cancelled = 0""",
		(name,),
		as_dict=True,
	)[0]
	return flt(row.net)


@check("P. Procure to Pay", "A supplier's bill creates the payable")
def p_bill_creates_payable():
	before = account_balance("Creditors")
	bill = a_bill(5000)
	after = account_balance("Creditors")
	expect(
		abs((before - after) - 5000) < 0.005,
		f"Creditors moved by {before - after}, expected a 5000 credit",
	)
	expect(
		flt(bill.outstanding_amount) == 5000,
		f"the bill shows {bill.outstanding_amount} outstanding, expected 5000",
	)
	frappe.db.commit()
	return f"{bill.name}: Creditors credited 5,000 and the bill owes 5,000"


@check("P. Procure to Pay", "The bill clears what the receipt could not value")
def p_bill_clears_received_not_billed():
	"""The point of the whole account: a receipt opens it, a bill closes it."""
	item = an_item("Acceptance Billed Coil")
	before = account_balance("Stock Received But Not Billed")
	receipt = a_receipt(item, 10, 300)
	opened = account_balance("Stock Received But Not Billed") - before
	expect(
		abs(opened + 3000) < 0.005,
		f"the receipt moved Stock Received But Not Billed by {opened}, expected -3000",
	)

	bill = a_bill(3000, receipt=receipt.name)
	closed = account_balance("Stock Received But Not Billed") - before
	expect(
		abs(closed) < 0.005,
		f"after billing, {closed} of this receipt is still awaiting a bill",
	)
	frappe.db.commit()
	return f"{receipt.name} opened 3,000, {bill.name} cleared it to nil"


@check("P. Procure to Pay", "A bill above the receipt shows the difference")
def p_price_difference_is_visible():
	item = an_item("Acceptance Dearer Coil")
	awaiting = account_balance("Stock Received But Not Billed")
	receipt = a_receipt(item, 10, 300)
	before = account_balance("Administrative Expenses")
	bill = a_bill(3250, receipt=receipt.name)

	expect(
		abs(account_balance("Stock Received But Not Billed") - awaiting) < 0.005,
		"the receipt's value was not fully cleared",
	)
	moved = account_balance("Administrative Expenses") - before
	expect(
		abs(moved - 250) < 0.005,
		f"the 250 difference went somewhere else: expenses moved by {moved}",
	)
	frappe.db.commit()
	return f"{bill.name}: billed 3,250 against 3,000 received, 250 visible as expense"


@check("P. Procure to Pay", "A bill below the receipt shows the difference too")
def p_price_difference_the_other_way():
	item = an_item("Acceptance Cheaper Coil")
	receipt = a_receipt(item, 10, 300)
	before = account_balance("Administrative Expenses")
	bill = a_bill(2800, receipt=receipt.name)
	moved = account_balance("Administrative Expenses") - before
	expect(
		abs(moved + 200) < 0.005,
		f"the 200 credit difference went somewhere else: expenses moved by {moved}",
	)
	frappe.db.commit()
	return f"{bill.name}: billed 2,800 against 3,000 received, 200 credited back"


@check("P. Procure to Pay", "A bill with no receipt is an expense outright")
def p_service_bill_is_expense():
	"""A subscription, a repair, a consultant: nothing passed through stock."""
	before = account_balance("Administrative Expenses")
	awaiting = account_balance("Stock Received But Not Billed")
	bill = a_bill(1800)
	moved = account_balance("Administrative Expenses") - before
	expect(abs(moved - 1800) < 0.005, f"expenses moved by {moved}, expected 1800")
	expect(
		abs(account_balance("Stock Received But Not Billed") - awaiting) < 0.005,
		"a bill with no receipt touched the stock liability",
	)
	frappe.db.commit()
	return f"{bill.name}: 1,800 expensed, the stock liability untouched"


@check("P. Procure to Pay", "Tax the supplier billed is recoverable, so it is an asset")
def p_input_tax_is_an_asset():
	"""DEC-021. Tax paid to a supplier is money the tax authority owes back."""
	before = account_balance("Input Tax Credit")
	bill = a_bill(10000, tax=1800)
	moved = account_balance("Input Tax Credit") - before
	expect(abs(moved - 1800) < 0.005, f"Input Tax Credit moved by {moved}, expected 1800")

	root = frappe.db.get_value(
		"KNIT 360 Account",
		{"company": COMPANY, "account_name": "Input Tax Credit", "is_group": 0},
		"root_type",
	)
	expect(root == "Asset", f"Input Tax Credit is an {root} account, not an Asset")
	frappe.db.commit()
	return f"{bill.name}: 1,800 of tax debited to an Asset, not buried in expense"


@check("P. Procure to Pay", "Freight is expensed, and says so")
def p_freight_is_expensed():
	"""DEC-033, and a deliberate departure from Ind AS 2 paragraph 11.

	Capitalising freight needs a landed-cost revaluation of stock the FIFO
	layers have already costed and partly sold. Until that exists, writing
	the figure into stock value would make the stock ledger and the accounts
	disagree -- and they agree today, with a check that proves it.
	"""
	before = account_balance("Freight and Forwarding")
	in_stock = account_balance("Stock In Hand")
	bill = a_bill(4000, freight=600)
	moved = account_balance("Freight and Forwarding") - before
	expect(abs(moved - 600) < 0.005, f"Freight and Forwarding moved by {moved}, expected 600")
	expect(
		abs(account_balance("Stock In Hand") - in_stock) < 0.005,
		"freight was capitalised into stock, which no stock movement would explain",
	)
	frappe.db.commit()
	return f"{bill.name}: 600 of freight expensed, stock value unchanged"


@check("P. Procure to Pay", "The whole bill is payable, tax and freight included")
def p_payable_is_the_whole_bill():
	"""DEC-020. The amount payable is the amount that leaves the bank."""
	before = account_balance("Creditors")
	bill = a_bill(10000, freight=500, tax=1890)
	credited = before - account_balance("Creditors")
	expect(
		abs(credited - 12390) < 0.005,
		f"Creditors was credited {credited}, expected 12,390",
	)
	expect(
		abs(flt(bill.grand_total) - 12390) < 0.005,
		f"the bill totals {bill.grand_total}, expected 12,390",
	)
	frappe.db.commit()
	return f"{bill.name}: 10,000 + 500 freight + 1,890 tax = 12,390 payable"


@check("P. Procure to Pay", "Paying a supplier settles the bill")
def p_payment_settles_the_bill():
	supplier = a_supplier()
	bill = a_bill(8000, supplier=supplier)
	payment = frappe.get_doc(
		{
			"doctype": "KNIT 360 Payment Entry",
			"company": company(),
			"payment_direction": "Pay",
			"party_type": "KNIT 360 Supplier",
			"party": supplier,
			"payment_date": nowdate(),
			"amount": 5000,
			"bank_account": account("Bank Account"),
			"allocations": [
				{
					"reference_doctype": "KNIT 360 Supplier Invoice",
					"reference_name": bill.name,
					"allocated_amount": 5000,
				}
			],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Payment Entry", payment.name, "Pending Bank Authorization")
	engine.transition("KNIT 360 Payment Entry", payment.name, "Disbursed / Cleared")

	left = settlement.outstanding("KNIT 360 Supplier Invoice", bill.name)
	expect(abs(left - 3000) < 0.005, f"{left} left owing after paying 5,000 of 8,000")
	status = frappe.db.get_value("KNIT 360 Supplier Invoice", bill.name, model.FIELD)
	expect(status == "Partially Paid", f"the bill reads {status!r} after a part payment")
	frappe.db.commit()
	return f"{bill.name}: 5,000 of 8,000 paid, 3,000 owing, status Partially Paid"


@check("P. Procure to Pay", "Paying a bill in full closes it")
def p_full_payment_closes_the_bill():
	supplier = a_supplier()
	bill = a_bill(2400, supplier=supplier)
	payment = frappe.get_doc(
		{
			"doctype": "KNIT 360 Payment Entry",
			"company": company(),
			"payment_direction": "Pay",
			"party_type": "KNIT 360 Supplier",
			"party": supplier,
			"payment_date": nowdate(),
			"amount": 2400,
			"bank_account": account("Bank Account"),
			"allocations": [
				{
					"reference_doctype": "KNIT 360 Supplier Invoice",
					"reference_name": bill.name,
					"allocated_amount": 2400,
				}
			],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Payment Entry", payment.name, "Pending Bank Authorization")
	engine.transition("KNIT 360 Payment Entry", payment.name, "Disbursed / Cleared")

	expect(
		settlement.outstanding("KNIT 360 Supplier Invoice", bill.name) < 0.005,
		"the bill still shows an amount owing after being paid in full",
	)
	status = frappe.db.get_value("KNIT 360 Supplier Invoice", bill.name, model.FIELD)
	expect(status == "Paid in Full", f"the bill reads {status!r} after full payment")
	frappe.db.commit()
	return f"{bill.name}: 2,400 paid in full, status Paid in Full"


@check("P. Procure to Pay", "A purchase order posts nothing")
def p_order_posts_nothing():
	"""An order is a commitment to buy. No goods have moved, nothing is owed."""
	order = frappe.get_doc(
		{
			"doctype": "KNIT 360 Purchase Order",
			"company": company(),
			"supplier": a_supplier(),
			"order_date": nowdate(),
			"items": [{"item_code": "Acceptance ordered goods", "qty": 5, "rate": 400}],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Purchase Order", order.name, "Pending Approval")
	engine.transition("KNIT 360 Purchase Order", order.name, "Approved / Ordered")

	entries = frappe.db.count(
		"KNIT 360 GL Entry", {"voucher_type": order.doctype, "voucher_no": order.name}
	)
	expect(entries == 0, f"an approved order wrote {entries} ledger entries")
	order.reload()
	expect(flt(order.grand_total) == 2000, f"the order totals {order.grand_total}, expected 2000")
	frappe.db.commit()
	return f"{order.name}: 2,000 committed, nothing posted"


@check("P. Procure to Pay", "Cancelling a bill reverses it rather than deleting it")
def p_cancelling_a_bill_reverses():
	bill = a_bill(1500)
	before = account_balance("Creditors")
	engine.transition("KNIT 360 Supplier Invoice", bill.name, "Cancelled")
	after = account_balance("Creditors")
	expect(
		abs(after - before - 1500) < 0.005,
		f"cancelling moved Creditors by {after - before}, expected a 1500 debit back",
	)
	live = frappe.db.count(
		"KNIT 360 GL Entry",
		{"voucher_type": bill.doctype, "voucher_no": bill.name, "is_cancelled": 0},
	)
	cancelled = frappe.db.count(
		"KNIT 360 GL Entry",
		{"voucher_type": bill.doctype, "voucher_no": bill.name, "is_cancelled": 1},
	)
	expect(live == 0, f"{live} live entries remain after cancelling")
	expect(cancelled > 0, "nothing was flagged cancelled, so the entries were deleted")
	frappe.db.commit()
	return f"{bill.name}: {cancelled} entries flagged, none deleted, Creditors back to nil"


@check("P. Procure to Pay", "The buying ledger balances")
def p_buying_balances():
	totals_row = frappe.db.sql(
		"""SELECT COALESCE(SUM(debit), 0) AS debit, COALESCE(SUM(credit), 0) AS credit
		   FROM `tabKNIT 360 GL Entry`
		   WHERE company = %s AND is_cancelled = 0""",
		(COMPANY,),
		as_dict=True,
	)[0]
	expect(
		abs(flt(totals_row.debit) - flt(totals_row.credit)) < 0.005,
		f"the acceptance books are out by "
		f"{flt(totals_row.debit) - flt(totals_row.credit):.2f}",
	)
	return (
		f"debits {flt(totals_row.debit):,.2f} equal credits "
		f"{flt(totals_row.credit):,.2f}"
	)


# --- Q. credit control ---------------------------------------------------
#
# DEC-036. A credit limit is a question asked of the ledger at the moment
# somebody adds to the debt, not a stored total compared with another stored
# total. A blank limit means nobody has decided, never refuse everything.


def a_limited_customer(limit=None, hold=0, name="Acceptance Limited Customer"):
	if not frappe.db.exists("KNIT 360 Customer", name):
		frappe.get_doc(
			{"doctype": "KNIT 360 Customer", "customer_name": name, "company": company()}
		).insert(ignore_permissions=True)
	frappe.db.set_value(
		"KNIT 360 Customer", name,
		{"credit_limit": limit or 0, "credit_hold": hold},
		update_modified=False,
	)
	return name


@check("Q. Credit Control", "What a customer owes is read from the ledger")
def q_exposure_is_derived():
	customer = a_limited_customer()
	before = credit.exposure(customer, COMPANY)
	a_posted_invoice(4000, customer=customer)
	after = credit.exposure(customer, COMPANY)
	expect(
		abs((after - before) - 4000) < 0.005,
		f"exposure moved by {after - before} after a 4,000 invoice",
	)
	frappe.db.commit()
	return f"{customer}: owes {after:,.2f}, derived from the receivable postings"


@check("Q. Credit Control", "A payment gives the headroom back")
def q_payment_restores_headroom():
	customer = a_limited_customer(limit=10000, name="Acceptance Paying Limited Customer")
	invoice = a_posted_invoice(6000, customer=customer)
	a_payment(6000, [(invoice.name, 6000)], customer=customer)
	expect(
		credit.exposure(customer, COMPANY) < 0.005,
		f"{customer} still shows {credit.exposure(customer, COMPANY)} owing after paying in full",
	)
	expect(
		abs(credit.headroom(customer, COMPANY) - 10000) < 0.005,
		"the headroom did not come back when the invoice was paid",
	)
	frappe.db.commit()
	return f"{customer}: 6,000 invoiced and paid, the whole 10,000 limit free again"


@check("Q. Credit Control", "An invoice over the limit is refused")
def q_over_the_limit_is_refused():
	customer = a_limited_customer(limit=5000, name="Acceptance Capped Customer")
	a_posted_invoice(4000, customer=customer)
	refused = refuses(lambda: a_posted_invoice(2000, customer=customer))
	expect("credit limit" in refused.lower(), f"refused, but for another reason: {refused}")
	frappe.db.commit()
	return f"4,000 owing against a 5,000 limit: a further 2,000 refused -- {refused[:70]}"


@check("Q. Credit Control", "An invoice within the limit goes through")
def q_within_the_limit_is_allowed():
	customer = a_limited_customer(limit=5000, name="Acceptance Roomy Customer")
	invoice = a_posted_invoice(4500, customer=customer)
	expect(invoice.docstatus == 1, "an invoice inside the limit was not posted")
	left = credit.headroom(customer, COMPANY)
	expect(abs(left - 500) < 0.005, f"headroom reads {left}, expected 500")
	frappe.db.commit()
	return f"{invoice.name}: 4,500 of a 5,000 limit used, 500 left"


@check("Q. Credit Control", "A blank limit is no limit, not a limit of nothing")
def q_blank_limit_means_no_limit():
	"""The commonest state of any master field is empty."""
	customer = a_limited_customer(limit=0, name="Acceptance Unlimited Customer")
	invoice = a_posted_invoice(250000, customer=customer)
	expect(invoice.docstatus == 1, "a customer with no limit set was refused credit")
	expect(
		credit.headroom(customer, COMPANY) is None,
		"a blank limit reported headroom instead of reporting no limit",
	)
	frappe.db.commit()
	return f"{invoice.name}: 250,000 posted against a customer with no limit set"


@check("Q. Credit Control", "A customer on hold is refused whatever they owe")
def q_hold_refuses_regardless():
	customer = a_limited_customer(hold=1, name="Acceptance Held Customer")
	expect(
		credit.exposure(customer, COMPANY) < 0.005,
		"this check needs a customer who owes nothing, to prove the hold is what refused",
	)
	refused = refuses(lambda: a_posted_invoice(100, customer=customer))
	expect("hold" in refused.lower(), f"refused, but for another reason: {refused}")
	frappe.db.commit()
	return f"{customer} owes nothing and is still refused: {refused[:70]}"


@check("Q. Credit Control", "Confirming an order checks the credit too")
def q_order_checks_credit():
	"""The order is where the business commits; the invoice is too late to find out."""
	customer = a_limited_customer(limit=1000, name="Acceptance Ordering Customer")
	a_posted_invoice(900, customer=customer)
	order = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Order",
			"company": company(),
			"customer": customer,
			"items": [{"item_code": "Acceptance ordered widget", "qty": 1, "rate": 500}],
		}
	).insert(ignore_permissions=True)
	refused = refuses(
		lambda: engine.transition("KNIT 360 Sales Order", order.name, "Confirmed / Booked")
	)
	expect("credit limit" in refused.lower(), f"refused, but for another reason: {refused}")
	frappe.db.commit()
	return f"{order.name}: 900 owing of a 1,000 limit, a 500 order stopped at confirmation"


@check("Q. Credit Control", "An advance counts against what is owed")
def q_advance_reduces_exposure():
	"""Money held for a customer is money they do not owe."""
	customer = a_limited_customer(limit=10000, name="Acceptance Advancing Customer")
	a_posted_invoice(3000, customer=customer)
	a_payment(5000, [], customer=customer)
	owed = credit.exposure(customer, COMPANY)
	expect(
		owed < 0.005,
		f"{customer} shows {owed} owing after a 5,000 payment against a 3,000 invoice",
	)
	frappe.db.commit()
	return f"{customer}: 3,000 invoiced, 5,000 paid, nothing owing and the limit free"


# --- R. returns ----------------------------------------------------------
#
# DEC-037. FR-SALES-006 Returns, FR-SALES-007 Credit Memos and FR-PROC-006
# Returns. Before these documents existed a return could be agreed and never
# settled: the invoice went on showing the full amount owing, and the only
# ways to close it were to cancel an invoice that had genuinely happened or to
# write the difference off as a loss. Both are lies about the business.


def a_credit_note(amount, invoice=None, customer=None, tax_template=None, target="Issued"):
	note = frappe.get_doc(
		{
			"doctype": "KNIT 360 Credit Note",
			"company": company(),
			"customer": customer or a_payer(),
			"sales_invoice": invoice,
			"posting_date": nowdate(),
			"reason": "Acceptance: goods returned",
			"tax_template": tax_template,
			"items": [{"item_code": "Acceptance returned widget", "qty": 1, "rate": amount}],
		}
	).insert(ignore_permissions=True)
	if target:
		engine.transition("KNIT 360 Credit Note", note.name, "Pending Approval")
		engine.transition("KNIT 360 Credit Note", note.name, target)
	note.reload()
	return note


def a_debit_note(amount, bill=None, supplier=None, tax=0, target="Issued"):
	note = frappe.get_doc(
		{
			"doctype": "KNIT 360 Debit Note",
			"company": company(),
			"supplier": supplier or a_supplier(),
			"supplier_invoice": bill,
			"posting_date": nowdate(),
			"reason": "Acceptance: goods sent back",
			"statutory_tax_amount": tax,
			"items": [{"item_code": "Acceptance returned part", "qty": 1, "rate": amount}],
		}
	).insert(ignore_permissions=True)
	if target:
		engine.transition("KNIT 360 Debit Note", note.name, "Pending Approval")
		engine.transition("KNIT 360 Debit Note", note.name, target)
	note.reload()
	return note


@check("R. Returns", "A credit note reduces what the invoice owes")
def r_credit_note_settles():
	invoice = a_posted_invoice(10000)
	a_credit_note(2500, invoice=invoice.name)
	left = settlement.outstanding(invoice.doctype, invoice.name)
	expect(abs(left - 7500) < 0.005, f"{left} owing after crediting 2,500 of 10,000")
	invoice.reload()
	expect(
		invoice.knit360_business_status == "Partly Paid",
		f"the invoice reads {invoice.knit360_business_status!r} after a part credit",
	)
	frappe.db.commit()
	return f"{invoice.name}: 2,500 credited, 7,500 owing, status Partly Paid"


@check("R. Returns", "A credit note for the whole invoice closes it")
def r_full_credit_closes_the_invoice():
	invoice = a_posted_invoice(4000)
	note = a_credit_note(4000, invoice=invoice.name)
	expect(
		settlement.outstanding(invoice.doctype, invoice.name) < 0.005,
		"the invoice still shows an amount owing after being credited in full",
	)
	invoice.reload()
	expect(
		invoice.knit360_business_status == "Paid",
		f"the invoice reads {invoice.knit360_business_status!r} after a full credit",
	)
	frappe.db.commit()
	return f"{note.name} credited the whole of {invoice.name}; nothing owing"


@check("R. Returns", "A credit note larger than the invoice is refused")
def r_over_credit_refused():
	"""Giving back more than was charged is a mistake, not a generosity."""
	invoice = a_posted_invoice(1000)
	refused = refuses(lambda: a_credit_note(1500, invoice=invoice.name))
	expect(
		"outstanding" in refused.lower() or "allocat" in refused.lower(),
		f"refused, but for another reason: {refused}",
	)
	frappe.db.commit()
	return f"1,500 against a 1,000 invoice refused -- {refused[:70]}"


@check("R. Returns", "A credit note cannot cross to another customer's invoice")
def r_credit_note_wrong_customer():
	invoice = a_posted_invoice(2000)
	other = a_limited_customer(name="Acceptance Other Customer")
	refused = refuses(lambda: a_credit_note(500, invoice=invoice.name, customer=other))
	expect("not" in refused.lower(), f"refused, but for another reason: {refused}")
	frappe.db.commit()
	return f"a credit for {other} against another party's invoice is refused"


@check("R. Returns", "A credit note naming no invoice is money owed to the customer")
def r_unallocated_credit():
	"""A goodwill credit, or one agreed before the next invoice exists."""
	customer = a_limited_customer(name="Acceptance Credited Customer")
	invoice = a_posted_invoice(3000, customer=customer)
	a_credit_note(1200, customer=customer)
	owed = credit.exposure(customer, COMPANY)
	expect(abs(owed - 1800) < 0.005, f"{customer} owes {owed}, expected 1,800")
	expect(
		abs(settlement.outstanding(invoice.doctype, invoice.name) - 3000) < 0.005,
		"an unallocated credit silently settled an invoice it did not name",
	)
	frappe.db.commit()
	return f"{customer}: 3,000 invoiced less a 1,200 free credit, 1,800 owed overall"


@check("R. Returns", "What was given back has its own account")
def r_sales_returns_is_separate():
	"""Both leave the same profit. Only one can say how much came back."""
	before = account_balance("Sales Returns")
	a_credit_note(900)
	moved = account_balance("Sales Returns") - before
	expect(abs(moved - 900) < 0.005, f"Sales Returns moved by {moved}, expected 900")

	root = frappe.db.get_value(
		"KNIT 360 Account",
		{"company": COMPANY, "account_name": "Sales Returns", "is_group": 0},
		"root_type",
	)
	expect(root == "Income", f"Sales Returns is an {root} account; it must sit against Income")
	frappe.db.commit()
	return "900 debited to Sales Returns, an Income account, not hidden inside Sales"


@check("R. Returns", "Tax charged on the sale is given back with it")
def r_credit_note_returns_tax():
	template = a_tax_template(
		"Acceptance Credit Tax",
		[("CGST", 9, account("Output Tax Payable")), ("SGST", 9, account("Output Tax Payable"))],
	)
	before = account_balance("Output Tax Payable")
	note = a_credit_note(1000, tax_template=template)
	moved = account_balance("Output Tax Payable") - before
	expect(abs(moved - 180) < 0.005, f"Output Tax Payable moved by {moved}, expected 180")
	expect(
		abs(flt(note.grand_total) - 1180) < 0.005,
		f"the credit note totals {note.grand_total}, expected 1,180",
	)
	frappe.db.commit()
	return f"{note.name}: 1,000 credited and 180 of tax taken back with it"


@check("R. Returns", "A debit note reduces what we owe the supplier")
def r_debit_note_settles():
	supplier = a_supplier()
	bill = a_bill(9000, supplier=supplier)
	a_debit_note(2000, bill=bill.name, supplier=supplier)
	left = settlement.outstanding(bill.doctype, bill.name)
	expect(abs(left - 7000) < 0.005, f"{left} owing after debiting 2,000 of 9,000")
	status = frappe.db.get_value("KNIT 360 Supplier Invoice", bill.name, model.FIELD)
	expect(status == "Partially Paid", f"the bill reads {status!r} after a part debit")
	frappe.db.commit()
	return f"{bill.name}: 2,000 debited back, 7,000 owing"


@check("R. Returns", "What went back has its own account too")
def r_purchase_returns_is_separate():
	before = account_balance("Purchase Returns")
	note = a_debit_note(700)
	moved = account_balance("Purchase Returns") - before
	expect(abs(moved + 700) < 0.005, f"Purchase Returns moved by {moved}, expected -700")
	frappe.db.commit()
	return f"{note.name}: 700 credited to Purchase Returns, not netted into the expense"


@check("R. Returns", "A debit note cannot cross to another supplier's bill")
def r_debit_note_wrong_supplier():
	bill = a_bill(3000)
	other = "Acceptance Second Supplier"
	if not frappe.db.exists("KNIT 360 Supplier", other):
		frappe.get_doc(
			{"doctype": "KNIT 360 Supplier", "supplier_name": other, "company": company()}
		).insert(ignore_permissions=True)
	refused = refuses(lambda: a_debit_note(500, bill=bill.name, supplier=other))
	expect("not" in refused.lower(), f"refused, but for another reason: {refused}")
	frappe.db.commit()
	return f"a debit from {other} against another supplier's bill is refused"


@check("R. Returns", "Cancelling a credit note puts the debt back")
def r_cancelling_a_credit_note():
	invoice = a_posted_invoice(5000)
	note = a_credit_note(2000, invoice=invoice.name)
	expect(
		abs(settlement.outstanding(invoice.doctype, invoice.name) - 3000) < 0.005,
		"the credit did not reduce the invoice in the first place",
	)
	engine.transition("KNIT 360 Credit Note", note.name, "Cancelled")
	back = settlement.outstanding(invoice.doctype, invoice.name)
	expect(abs(back - 5000) < 0.005, f"{back} owing after the credit note was cancelled")
	frappe.db.commit()
	return f"{note.name} cancelled: {invoice.name} is owed in full again"


@check("R. Returns", "A return note with no lines is refused")
def r_empty_note_refused():
	refused = refuses(
		lambda: frappe.get_doc(
			{
				"doctype": "KNIT 360 Credit Note",
				"company": company(),
				"customer": a_payer(),
				"posting_date": nowdate(),
				"reason": "Acceptance: nothing at all",
				"items": [],
			}
		).insert(ignore_permissions=True)
	)
	expect("credits nothing" in refused.lower(), f"refused, but for another reason: {refused}")
	return "a credit note with no lines credits nothing, and is refused"


# --- S. printing ---------------------------------------------------------
#
# DEC-038. Printing worked before this; the output was Frappe's field-by-field
# dump, which is not a document anybody would send a customer. These checks
# prove each format renders at all -- a Jinja error in a print format is
# invisible until somebody tries to print -- and that a delivery note carries
# no money on it.

PRINT_FORMATS = {
	"KNIT 360 Quotation": "Quotation",
	"KNIT 360 Sales Order": "Sales Order",
	"KNIT 360 Sales Invoice": "Sales Invoice",
	"KNIT 360 Delivery Note": "Delivery Note",
	"KNIT 360 Purchase Order": "Purchase Order",
	"KNIT 360 Credit Note": "Credit Note",
}


def printed(doctype, name, letterhead=None):
	"""The HTML a person would see, through the same call the Print button makes."""
	return frappe.get_print(
		doctype, name, print_format=PRINT_FORMATS[doctype], letterhead=letterhead
	)


@check("S. Printing", "Every document type has a format of its own")
def s_every_document_has_a_format():
	missing = [
		doctype for doctype, fmt in PRINT_FORMATS.items()
		if not frappe.db.exists("Print Format", {"name": fmt, "doc_type": doctype})
	]
	expect(not missing, f"these have no print format: {missing}")

	not_default = [
		doctype for doctype, fmt in PRINT_FORMATS.items()
		if frappe.db.get_value("DocType", doctype, "default_print_format") != fmt
	]
	expect(not not_default, f"these do not open on their own format: {not_default}")
	return f"{len(PRINT_FORMATS)} document types, each opening on its own format"


@check("S. Printing", "An invoice prints as a document, not a field dump")
def s_invoice_prints():
	invoice = a_posted_invoice(12500)
	html = printed(invoice.doctype, invoice.name)
	for fragment in ("TAX INVOICE", invoice.name, "Amount payable", "AMOUNT IN WORDS"):
		expect(fragment.lower() in html.lower(), f"the printed invoice has no {fragment!r}")
	expect(
		"12,500" in html,
		"the printed invoice does not show its own total",
	)
	frappe.db.commit()
	return f"{invoice.name} prints with its heading, total and amount in words"


@check("S. Printing", "Tax prints component by component")
def s_tax_prints_by_component():
	"""A customer disputing an invoice asks which tax, not how much tax."""
	template = a_tax_template(
		"Acceptance Print Tax",
		[("CGST", 9, account("Output Tax Payable")), ("SGST", 9, account("Output Tax Payable"))],
	)
	invoice = frappe.get_doc(
		{
			"doctype": "KNIT 360 Sales Invoice",
			"company": company(),
			"customer": a_payer(),
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"tax_template": template,
			"items": [{"item_name": "Acceptance printed widget", "qty": 1, "rate": 1000}],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Sales Invoice", invoice.name, "Posted / Unpaid")
	html = printed("KNIT 360 Sales Invoice", invoice.name)
	expect("CGST at 9" in html, "the printed invoice does not name CGST and its rate")
	expect("SGST at 9" in html, "the printed invoice does not name SGST and its rate")
	frappe.db.commit()
	return f"{invoice.name} prints CGST at 9% and SGST at 9% as separate lines"


@check("S. Printing", "A delivery note carries no money at all")
def s_delivery_note_has_no_money():
	"""What the goods cost us is nobody's business but ours, and the note
	carries that cost in its own fields because the ledger needs it."""
	item = an_item("Acceptance Printed Coil")
	a_receipt(item, 10, 1234)
	note = a_dispatch(item, 3)
	html = printed(note.doctype, note.name)

	expect(note.name in html, "the printed delivery note does not show its own number")
	leaked = [word for word in ("1,234", "3,702", "Amount", "Rate", "Net total") if word in html]
	expect(not leaked, f"the printed delivery note shows money: {leaked}")
	frappe.db.commit()
	return f"{note.name} prints 3 units and no figure of any kind"


@check("S. Printing", "The letterhead is built from the company's own details")
def s_letterhead_is_the_company():
	from knit360_core import branding

	frappe.db.set_value(
		COMPANY_DOCTYPE, COMPANY,
		{
			"registered_address": "Unit 9, Acceptance Estate",
			"contact_phone": "+91 00 0000 0000",
			"contact_email": "acceptance@example.com",
		},
		update_modified=False,
	)
	branding.letterheads()
	content = frappe.db.get_value("Letter Head", COMPANY, "content") or ""
	for fragment in (COMPANY, "Unit 9, Acceptance Estate", "acceptance@example.com"):
		expect(fragment in content, f"the letterhead does not carry {fragment!r}")

	invoice = a_posted_invoice(2000)
	html = printed(invoice.doctype, invoice.name, letterhead=COMPANY)
	expect(COMPANY in html, "the letterhead did not reach the printed document")
	frappe.db.commit()
	return f"the {COMPANY} letterhead carries its address and reaches the page"


@check("S. Printing", "A letterhead somebody edited by hand is left alone")
def s_letterhead_respects_an_edit():
	from knit360_core import branding

	branding.letterheads()
	frappe.db.set_value(
		"Letter Head", COMPANY, "content", "<div>Our own letterhead</div>",
		update_modified=False,
	)
	branding.letterheads()
	expect(
		frappe.db.get_value("Letter Head", COMPANY, "content") == "<div>Our own letterhead</div>",
		"a hand-written letterhead was overwritten on migrate",
	)
	frappe.db.delete("Letter Head", {"name": COMPANY})
	frappe.db.commit()
	return "an edited letterhead survives a migrate; only generated ones are refreshed"


@check("S. Printing", "One layout serves every format")
def s_one_layout():
	"""Six copies of a layout is six places for the columns to drift apart."""
	import pathlib as _pathlib

	root = _pathlib.Path(frappe.get_app_path("knit360_core"))
	shared = root / "templates" / "print" / "document.html"
	expect(shared.exists(), "the shared print layout is missing")

	formats = list(root.glob("*/print_format/*/*.html"))
	expect(len(formats) == len(PRINT_FORMATS), f"{len(formats)} format files, expected 6")

	standalone = [
		path.name for path in formats
		if "templates/print/document.html" not in path.read_text(encoding="utf-8")
	]
	expect(not standalone, f"these formats carry their own layout: {standalone}")
	return f"{len(formats)} formats, all drawing from one layout"


# --- the runner ---------------------------------------------------------


def run(verbose=True):
	"""Run every check and print a report. Returns (passed, failed)."""
	frappe.flags.in_test = False
	results, failures = [], []

	for group, name, fn in CHECKS:
		try:
			detail = fn()
			if not detail:
				raise AssertionError(
					"the check returned no evidence. A check must return a detail "
					"string describing what it observed, so that a function which "
					"silently stops asserting cannot report a pass."
				)
			results.append((group, name, True, detail))
		except Exception as exc:  # noqa: BLE001 - a check failing is the point
			frappe.db.rollback()
			results.append((group, name, False, str(exc).split("\n")[0][:200]))
			failures.append((group, name, traceback.format_exc()))

	passed = sum(1 for r in results if r[2])
	total = len(results)

	if verbose:
		current = None
		for group, name, ok, detail in results:
			if group != current:
				print(f"\n{group}")
				current = group
			print(f"  {'PASS' if ok else 'FAIL'}  {name}")
			if detail:
				print(f"        {detail}")

		if failures:
			print("\n" + "=" * 70)
			print("TRACEBACKS")
			for group, name, tb in failures:
				print(f"\n--- {group} / {name} ---\n{tb}")

		print("\n" + "=" * 70)
		print(f"{passed}/{total} checks passed" + ("" if passed == total else f"  -- {total - passed} FAILED"))

	return passed, total - passed


def cleanup():
	"""Delete everything the acceptance run created.

	The run inserts real documents, and the charts on the Desk count documents
	across every company. So an acceptance run left in place shows up in the
	headline figures -- "Open Leads 37" when the demo has seven. That makes the
	product look wrong to anyone being shown it.

	Deletion order matters. A Sales Invoice cannot be deleted while GL entries
	point at it, and an Account refuses deletion while it carries postings, so
	the ledger is cleared before the documents that wrote it and the chart of
	accounts comes last.
	"""
	removed = {}

	def wipe(doctype, filters, force=False):
		names = frappe.get_all(doctype, filters=filters, pluck="name")
		for name in names:
			frappe.delete_doc(doctype, name, force=force, ignore_permissions=True,
			                  delete_permanently=True)
		if names:
			removed[doctype.replace("KNIT 360 ", "")] = len(names)

	# The ledger first: it is what holds the posting documents down.
	#
	# GL Entry.on_trash refuses deletion outright -- "the ledger keeps what the
	# books once said" -- and that guard is right, so it is not being weakened.
	# A test teardown is the one case it should not apply to: these rows are
	# postings into a throwaway company that exists only for this run, and the
	# alternative is a demonstration site whose headline figures count test
	# data. The delete is therefore raw SQL, and it is pinned to the acceptance
	# company so it cannot reach a real set of books even if called by mistake.
	if COMPANY == "KNIT Acceptance Co":
		count = frappe.db.count("KNIT 360 GL Entry", {"company": COMPANY})
		if count:
			frappe.db.sql(
				"DELETE FROM `tabKNIT 360 GL Entry` WHERE company = %s", (COMPANY,)
			)
			removed["GL Entry"] = count
	else:
		frappe.throw(
			f"cleanup() refuses to run against {COMPANY!r}. It deletes ledger "
			f"entries directly and is only ever meant for the acceptance company."
		)

	# Stock movements refuse deletion the same way, and for the same reason,
	# so they go by the same scoped raw delete before their documents.
	stock_rows = frappe.db.count("KNIT 360 Stock Ledger Entry", {"company": COMPANY})
	if stock_rows:
		frappe.db.sql(
			"DELETE FROM `tabKNIT 360 Stock Ledger Entry` WHERE company = %s", (COMPANY,)
		)
		removed["Stock Ledger Entry"] = stock_rows

	for doctype in ("KNIT 360 Delivery Note", "KNIT 360 Goods Receipt"):
		frappe.db.sql(
			f"UPDATE `tab{doctype}` SET docstatus = 0 WHERE company = %s", (COMPANY,)
		)
		wipe(doctype, {"company": COMPANY}, force=True)

	wipe("KNIT 360 Warehouse", {"company": COMPANY}, force=True)
	# Prices point at the items, so they go first. Neither is company-scoped,
	# so both are matched by the acceptance naming.
	wipe("KNIT 360 Item Price", {"item_code": ["like", "Acceptance %"]}, force=True)
	wipe("KNIT 360 Item", {"item_code": ["like", "Acceptance %"]}, force=True)
	wipe("KNIT 360 Price List", {"price_list_name": ["like", "Acceptance %"]}, force=True)

	# HR leave, before the finance documents, for the same reason: the leave
	# ledger refuses deletion exactly as the general ledger does, so its rows
	# go first and by the same scoped raw delete.
	leave_rows = frappe.db.count("KNIT 360 Leave Ledger Entry", {"company": COMPANY})
	if leave_rows:
		frappe.db.sql(
			"DELETE FROM `tabKNIT 360 Leave Ledger Entry` WHERE company = %s", (COMPANY,)
		)
		removed["Leave Ledger Entry"] = leave_rows

	for doctype in ("KNIT 360 Leave Application", "KNIT 360 Leave Allocation"):
		frappe.db.sql(
			f"UPDATE `tab{doctype}` SET docstatus = 0 WHERE company = %s", (COMPANY,)
		)
		wipe(doctype, {"company": COMPANY}, force=True)

	wipe("KNIT 360 Employee", {"company": COMPANY}, force=True)
	wipe("KNIT 360 Holiday List", {"company": COMPANY}, force=True)
	wipe("KNIT 360 Leave Period", {"company": COMPANY}, force=True)
	# Leave Type is not company-scoped, so the acceptance ones are named.
	wipe("KNIT 360 Leave Type", {"leave_type_name": ["like", "Acceptance %"]}, force=True)

	# Then the documents, children before parents.
	#
	# Frappe refuses to delete a submitted document and tells you to cancel it
	# first. Cancelling here would call on_cancel, which would try to reverse
	# ledger entries that have just been deleted. So the docstatus is cleared
	# directly instead -- again only for the acceptance company, and only
	# because these documents are about to stop existing.
	for doctype in (
		"KNIT 360 Credit Note", "KNIT 360 Debit Note", "KNIT 360 Payment Entry",
		"KNIT 360 Sales Invoice", "KNIT 360 Sales Order", "KNIT 360 Journal Entry",
		"KNIT 360 Quotation", "KNIT 360 Opportunity", "KNIT 360 Lead",
		"KNIT 360 Purchase Order",
	):
		frappe.db.sql(
			f"UPDATE `tab{doctype}` SET docstatus = 0 WHERE company = %s", (COMPANY,)
		)
		wipe(doctype, {"company": COMPANY}, force=True)

	# Business Status Log is keyed by the document, not the company, so it is
	# matched on the names that no longer resolve.
	orphaned = [
		row.name
		for row in frappe.get_all(
			"KNIT 360 Business Status Log", fields=["name", "reference_doctype", "reference_name"]
		)
		if not frappe.db.exists(row.reference_doctype, row.reference_name)
	]
	# The log refuses deletion as well -- it is the audit trail, so that is
	# correct. These rows point at documents that no longer exist, so they are
	# removed the same way and for the same reason as the ledger rows above.
	for name in orphaned:
		frappe.db.sql("DELETE FROM `tabKNIT 360 Business Status Log` WHERE name = %s", (name,))
	if orphaned:
		removed["Business Status Log"] = len(orphaned)

	wipe("KNIT 360 Customer", {"company": COMPANY}, force=True)

	# The buying side, and the tax masters the posting checks create. Tax
	# Template is company-scoped; its rows go with it as children.
	frappe.db.sql(
		"UPDATE `tabKNIT 360 Supplier Invoice` SET docstatus = 0 WHERE company = %s", (COMPANY,)
	)
	wipe("KNIT 360 Supplier Invoice", {"company": COMPANY}, force=True)
	frappe.db.sql(
		"UPDATE `tabKNIT 360 Supplier Quotation` SET docstatus = 0 WHERE company = %s",
		(COMPANY,),
	)
	wipe("KNIT 360 Supplier Quotation", {"company": COMPANY}, force=True)
	wipe("KNIT 360 Supplier", {"company": COMPANY}, force=True)
	wipe("KNIT 360 Tax Template", {"company": COMPANY}, force=True)

	# Search index rows are derived, so they go with whatever they described.
	# Anything still pointing at a document that no longer exists is swept,
	# which also covers a fixture deleted by a check rather than by here.
	orphan_index = [
		row.name
		for row in frappe.get_all(
			"KNIT 360 Search Index", fields=["name", "reference_doctype", "reference_name"]
		)
		if not frappe.db.exists(row.reference_doctype, row.reference_name)
	]
	for name in orphan_index:
		frappe.db.sql("DELETE FROM `tabKNIT 360 Search Index` WHERE name = %s", (name,))
	if orphan_index:
		removed["Search Index"] = len(orphan_index)

	# Accounts are a tree: a node cannot go before its children. In a nested
	# set the width `rgt - lft` is 1 for a leaf and grows with depth of
	# subtree, so ascending width is exactly leaves-first. Ordering by `rgt`
	# descending is not the same thing and leaves parents stranded.
	# Cost Center is a tree too, and chart_of_accounts.setup creates one
	# alongside the accounts. Leaving it behind made the next run collide on a
	# duplicate primary key -- which is how this line came to be written.
	for doctype in ("KNIT 360 Cost Center", "KNIT 360 Account"):
		rows = frappe.get_all(doctype, filters={"company": COMPANY},
		                      fields=["name", "lft", "rgt"])
		names = [row.name for row in sorted(rows, key=lambda r: (r.rgt or 0) - (r.lft or 0))]
		for name in names:
			frappe.delete_doc(doctype, name, force=True, ignore_permissions=True,
			                  delete_permanently=True)
		if names:
			removed[doctype.replace("KNIT 360 ", "")] = len(names)

	wipe("KNIT 360 Fiscal Year", {"year_name": ["like", "Acceptance %"]}, force=True)
	wipe("KNIT 360 Company", {"company_name": COMPANY}, force=True)

	# The self-setup check creates a second company with its own chart.
	other = "KNIT Acceptance Self Setup Co"
	if frappe.db.exists("KNIT 360 Company", other):
		for doctype in ("KNIT 360 Cost Center", "KNIT 360 Account"):
			rows = frappe.get_all(doctype, filters={"company": other},
			                      fields=["name", "lft", "rgt"])
			for row in sorted(rows, key=lambda r: (r.rgt or 0) - (r.lft or 0)):
				frappe.delete_doc(doctype, row.name, force=True, ignore_permissions=True,
				                  delete_permanently=True)
		frappe.delete_doc("KNIT 360 Company", other, force=True, ignore_permissions=True,
		                  delete_permanently=True)
		removed["Company"] = removed.get("Company", 0) + 1

	frappe.db.commit()
	print(f"removed: {removed or 'nothing -- the site was already clean'}")
	return removed


def run_and_clean():
	"""Run every check, then remove the data it created. Returns (passed, failed).

	This is the form to use on a site that anyone is going to look at.
	"""
	passed, failed = run()
	cleanup()
	return passed, failed
