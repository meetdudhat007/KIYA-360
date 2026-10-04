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
import traceback

import frappe
from frappe.utils import add_days, flt, getdate, nowdate

from knit360_core.business_status import engine, guard, model
from knit360_core.finance import chart_of_accounts, ledger

#: Acceptance data lives under its own company so a run is isolated from
#: anything a person has entered. GL entries are immutable by design, so an
#: acceptance run that posted into the real company could not be undone.
COMPANY = "KNIT Acceptance Co"
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
		"KNIT 360 Supplier Invoice": "OPEN QUESTION: whether `freight_and_ancillary` and "
		                             "`statutory_tax_amount` belong inside the grand total "
		                             "is a business decision, not a coding one",
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

	# Then the documents, children before parents.
	#
	# Frappe refuses to delete a submitted document and tells you to cancel it
	# first. Cancelling here would call on_cancel, which would try to reverse
	# ledger entries that have just been deleted. So the docstatus is cleared
	# directly instead -- again only for the acceptance company, and only
	# because these documents are about to stop existing.
	for doctype in (
		"KNIT 360 Sales Invoice", "KNIT 360 Sales Order", "KNIT 360 Journal Entry",
		"KNIT 360 Quotation", "KNIT 360 Opportunity", "KNIT 360 Lead",
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
