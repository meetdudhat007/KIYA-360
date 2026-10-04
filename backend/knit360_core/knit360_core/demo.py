"""Sample master data and a worked pipeline, for a demonstration.

Why this exists.

The shared masters were installed empty, on purpose: how a business measures
things, how it groups its customers and what it calls its territories are
business decisions, and inventing them silently would have put guesses into the
system as though they were requirements. The consequence was that `stock_uom` on
an Item was a dropdown with nothing in it, which makes the product impossible to
show to anyone.

This module is the answer to that: one command that fills the masters with a
conventional starter set and walks a handful of deals through the whole
Customer-to-Cash flow, so the screens and the charts have something in them.

    bench --site knit360.localhost execute knit360_core.demo.seed

Everything here is SAMPLE DATA under a company called "KNIT 360 Demo Co".
It is not a requirement, it is not derived from the BRD, and it is not a
recommendation about how the business should be set up. It is a starting point
to edit or to delete.

Two things it deliberately does not do:

- No invoice is marked Paid. Payment Entry does not post to the ledger yet, so
  a Paid invoice would be a claim with no cash receipt behind it. The demo
  leaves receivables outstanding and overdue, which is the truth.
- No stock movement is recorded. Delivery Note has no ledger of its own yet.

Re-running is safe. Every master is created only if absent, and the pipeline is
only built the first time, so a second run does not multiply the deals.
"""

import frappe
from frappe.utils import add_days, nowdate

from knit360_core.business_status import engine
from knit360_core.finance import chart_of_accounts, ledger

COMPANY = "KNIT 360 Demo Co"
CURRENCY = "INR"

#: (name, symbol, category, whole numbers only)
UOMS = [
	("Nos", "Nos", "Quantity", 1),
	("Set", "Set", "Quantity", 1),
	("Kg", "kg", "Weight", 0),
	("Metre", "m", "Length", 0),
	("Litre", "L", "Volume", 0),
	("Hour", "hr", "Time", 0),
]

#: Trees are (parent, [children]). The root is a group; children are leaves.
ITEM_GROUPS = ("All Item Groups", ["Raw Materials", "Components", "Finished Goods", "Services"])
TERRITORIES = ("All Territories", ["North", "South", "East", "West", "Export"])
CUSTOMER_GROUPS = ("All Customer Groups", ["Commercial", "Government", "Dealer", "Export"])
SUPPLIER_GROUPS = ("All Supplier Groups", ["Local", "Imported", "Services"])

#: (code, name, group, uom, sales, purchase, selling rate, buying rate)
ITEMS = [
	("FG-COIL-01", "Induction Coil Assembly", "Finished Goods", "Nos", 1, 0, 24000, 0),
	("FG-PANEL-01", "Control Panel 50kW", "Finished Goods", "Nos", 1, 0, 86000, 0),
	("CM-IGBT-01", "IGBT Module", "Components", "Nos", 0, 1, 0, 7400),
	("CM-CAP-01", "Capacitor Bank", "Components", "Nos", 0, 1, 0, 3100),
	("RM-CU-01", "Copper Tube", "Raw Materials", "Kg", 0, 1, 0, 820),
	("SV-COMM-01", "Commissioning Service", "Services", "Hour", 1, 0, 1800, 0),
]

#: (name, group, territory, email)
CUSTOMERS = [
	("Northline Forgings Ltd", "Commercial", "North", "purchase@northline.example"),
	("Deccan Heat Treat Pvt Ltd", "Commercial", "South", "stores@deccanheat.example"),
	("State Metals Corporation", "Government", "West", "tenders@statemetals.example"),
	("Gulf Thermal Trading FZE", "Export", "Export", "orders@gulfthermal.example"),
]

#: (name, group, contact)
SUPPLIERS = [
	("Precision Semiconductors Pvt Ltd", "Local", "sales@precisionsemi.example"),
	("Hanover Komponenten GmbH", "Imported", "export@hanoverk.example"),
	("Shakti Calibration Services", "Services", "booking@shaktical.example"),
]

#: (term, credit days)
PAYMENT_TERMS = [("Net 30", 30), ("Net 45", 45), ("Net 60", 60), ("Immediate", 0)]

#: (mode, type)
PAYMENT_MODES = [("Cash", "Cash"), ("Bank Transfer", "Bank"), ("Cheque", "Bank")]


def _insert(doctype, fields, key=None):
	"""Create a document unless one already matches `key`. Returns its name."""
	key = key or fields
	existing = frappe.db.exists(doctype, key)
	if existing:
		return existing if isinstance(existing, str) else existing[0]
	doc = frappe.get_doc(dict(doctype=doctype, **fields)).insert(ignore_permissions=True)
	return doc.name


def _tree(doctype, name_field, parent_field, root, children):
	"""A one-level tree: a root group with leaf children under it."""
	root_name = _insert(doctype, {name_field: root, "is_group": 1}, {name_field: root})
	made = [root_name]
	for child in children:
		made.append(
			_insert(
				doctype,
				{name_field: child, parent_field: root_name, "is_group": 0},
				{name_field: child},
			)
		)
	return made


# --- masters ------------------------------------------------------------


def company():
	"""The demo company, its chart of accounts, a fiscal year and a cost centre."""
	name = _insert(
		"KNIT 360 Company",
		{
			"company_name": COMPANY,
			"default_currency": CURRENCY,
			"business_type": "Manufacturing",
			"legal_entity": "Private Limited",
		},
		{"company_name": COMPANY},
	)

	if not frappe.db.exists("KNIT 360 Account", {"company": name}):
		chart_of_accounts.setup(name)

	# Only create a year if none already covers today. The Fiscal Year
	# controller refuses overlapping years -- correctly, because a posting date
	# must fall in exactly one of them -- and a site set up for an Indian
	# financial year (April to March) already has the right one.
	if not fiscal_year():
		year = nowdate()[:4]
		_insert(
			"KNIT 360 Fiscal Year",
			{
				"year_name": f"FY {year}",
				"year_start_date": f"{year}-01-01",
				"year_end_date": f"{year}-12-31",
			},
			{"year_name": f"FY {year}"},
		)

	# Sales Invoice reads default_cost_center from the company. Without one,
	# every invoice line posts with no cost centre, so nothing can be reported
	# by department later. chart_of_accounts does not create one, so it is
	# created here and wired up.
	cost_center = _insert(
		"KNIT 360 Cost Center",
		{"cost_center_name": "Main", "company": name, "is_group": 0},
		{"cost_center_name": "Main", "company": name},
	)
	if not frappe.db.get_value("KNIT 360 Company", name, "default_cost_center"):
		frappe.db.set_value("KNIT 360 Company", name, "default_cost_center", cost_center)

	frappe.db.commit()
	return name


def fiscal_year():
	"""The open fiscal year covering today, or None."""
	return frappe.db.get_value(
		"KNIT 360 Fiscal Year",
		{"year_start_date": ["<=", nowdate()], "year_end_date": [">=", nowdate()],
		 "is_closed": 0},
		["name", "year_start_date"],
		as_dict=True,
	)


def masters():
	"""Every shared master the transaction screens need before they are usable."""
	made = {}

	for uom, symbol, category, whole in UOMS:
		_insert(
			"KNIT 360 UOM",
			{"uom_name": uom, "symbol": symbol, "category": category,
			 "must_be_whole_number": whole},
			{"uom_name": uom},
		)
	made["UOM"] = len(UOMS)

	made["Item Group"] = len(_tree("KNIT 360 Item Group", "item_group_name", "parent_item_group", *ITEM_GROUPS))
	made["Territory"] = len(_tree("KNIT 360 Territory", "territory_name", "parent_territory", *TERRITORIES))
	made["Customer Group"] = len(_tree("KNIT 360 Customer Group", "customer_group_name", "parent_customer_group", *CUSTOMER_GROUPS))
	made["Supplier Group"] = len(_tree("KNIT 360 Supplier Group", "supplier_group_name", "parent_supplier_group", *SUPPLIER_GROUPS))

	_insert("KNIT 360 Brand", {"brand_name": "KNIT"}, {"brand_name": "KNIT"})

	selling = _insert(
		"KNIT 360 Price List",
		{"price_list_name": "Standard Selling", "currency": CURRENCY,
		 "applies_to": "Selling", "is_default": 1},
		{"price_list_name": "Standard Selling"},
	)
	buying = _insert(
		"KNIT 360 Price List",
		{"price_list_name": "Standard Buying", "currency": CURRENCY,
		 "applies_to": "Buying", "is_default": 1},
		{"price_list_name": "Standard Buying"},
	)
	made["Price List"] = 2

	for term, days in PAYMENT_TERMS:
		_insert(
			"KNIT 360 Payment Term",
			{"term_name": term, "credit_days": days, "invoice_portion": 100},
			{"term_name": term},
		)
	made["Payment Term"] = len(PAYMENT_TERMS)

	for mode, kind in PAYMENT_MODES:
		_insert("KNIT 360 Mode of Payment", {"mode_name": mode, "payment_type": kind},
		        {"mode_name": mode})
	made["Mode of Payment"] = len(PAYMENT_MODES)

	# GST at 18%, split the way an intra-state invoice splits it. The rates are
	# a plausible default, not advice: FR-TAX-001 is not built, so this template
	# computes a figure and the posting still lands on the round-off account.
	if not frappe.db.exists("KNIT 360 Tax Template", "GST 18% (Intra-State)"):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Tax Template",
				"template_name": "GST 18% (Intra-State)",
				"company": COMPANY,
				"taxes": [
					{"tax_component": "CGST", "rate": 9},
					{"tax_component": "SGST", "rate": 9},
				],
			}
		).insert(ignore_permissions=True)
	made["Tax Template"] = 1

	for warehouse in ("Main Store", "Finished Goods Store", "Quarantine"):
		_insert(
			"KNIT 360 Warehouse",
			{"warehouse_name": warehouse, "company": COMPANY},
			{"warehouse_name": warehouse},
		)
	made["Warehouse"] = 3

	for code, name, group, uom, sales, purchase, sell_rate, buy_rate in ITEMS:
		_insert(
			"KNIT 360 Item",
			{"item_code": code, "item_name": name, "item_group": group, "stock_uom": uom,
			 "brand": "KNIT", "is_sales_item": sales, "is_purchase_item": purchase,
			 "valuation_method": "FIFO"},
			{"item_code": code},
		)
		for rate, price_list in ((sell_rate, selling), (buy_rate, buying)):
			if not rate:
				continue
			if frappe.db.exists("KNIT 360 Item Price", {"item_code": code, "price_list": price_list}):
				continue
			frappe.get_doc(
				{
					"doctype": "KNIT 360 Item Price",
					"item_code": code,
					"price_list": price_list,
					"uom": uom,
					"rate": rate,
					"currency": CURRENCY,
					"valid_from": nowdate(),
				}
			).insert(ignore_permissions=True)
	made["Item"] = len(ITEMS)

	for name, group, territory, email in CUSTOMERS:
		_insert(
			"KNIT 360 Customer",
			{"customer_name": name, "company": COMPANY, "customer_group": group,
			 "territory": territory, "email": email, "default_currency": CURRENCY,
			 "default_price_list": selling, "customer_type": "Company"},
			{"customer_name": name},
		)
	made["Customer"] = len(CUSTOMERS)

	for name, group, email in SUPPLIERS:
		_insert(
			"KNIT 360 Supplier",
			{"supplier_name": name, "company": COMPANY, "supplier_group": group,
			 "contact_email": email, "default_currency": CURRENCY},
			{"supplier_name": name},
		)
	made["Supplier"] = len(SUPPLIERS)

	frappe.db.commit()
	return made


# --- a worked pipeline --------------------------------------------------


def _walk_to(doctype, name, target):
	"""Move a document along its happy path until it reaches `target`."""
	from knit360_core.business_status import model

	lifecycle = model.for_doctype(doctype)
	status = frappe.db.get_value(doctype, name, model.FIELD)
	for _ in range(len(lifecycle.states) + 1):
		if status == target:
			return status
		nxt = lifecycle.forward_from(status)
		if not nxt:
			return status
		engine.transition(doctype, name, nxt)
		status = nxt
	return status


#: (contact, organisation, territory, source, how far to take it)
PIPELINE = [
	("Rakesh Menon", "Northline Forgings Ltd", "North", "Website", "New"),
	("Sunita Rao", "Deccan Heat Treat Pvt Ltd", "South", "Referral", "Contacted"),
	("Imran Qureshi", "State Metals Corporation", "West", "Tender Portal", "Contacted"),
	("Daniel Okafor", "Gulf Thermal Trading FZE", "Export", "Trade Show", "Qualified"),
	("Priya Nair", "Vertex Castings Pvt Ltd", "South", "Cold Call", "Qualified"),
	("Harish Gupta", "Ambar Alloys Ltd", "North", "Website", "Converted"),
	("Meera Joshi", "Konkan Steel Works", "West", "Referral", "Converted"),
]

#: Quotation lines for the deals that get that far.
QUOTE_LINES = [
	[("FG-COIL-01", 4, 24000, 0), ("SV-COMM-01", 16, 1800, 0)],
	[("FG-PANEL-01", 1, 86000, 5), ("FG-COIL-01", 2, 24000, 0)],
]


def pipeline():
	"""Leads at every stage, two converted into priced quotations and orders."""
	if frappe.db.count("KNIT 360 Lead", {"company": COMPANY}):
		return {"skipped": "the pipeline is already built; delete the leads to rebuild"}

	from knit360_core.api import c2c

	made = {"leads": 0, "opportunities": 0, "quotations": 0, "orders": 0, "invoices": 0}
	converted = []

	for contact, organisation, territory, source, target in PIPELINE:
		lead = frappe.get_doc(
			{
				"doctype": "KNIT 360 Lead",
				"lead_name": contact,
				"organization_name": organisation,
				"company": COMPANY,
				"territory": territory,
				"lead_source": source,
				"email": f"{contact.split()[0].lower()}@{organisation.split()[0].lower()}.example",
				"estimated_requirement": "Induction heating line, capacity to be confirmed.",
			}
		).insert(ignore_permissions=True)
		made["leads"] += 1

		if target == "Converted":
			_walk_to("KNIT 360 Lead", lead.name, "Qualified")
			result = c2c.convert_lead(lead.name)
			converted.append(result["opportunity"])
			made["opportunities"] += 1
		else:
			_walk_to("KNIT 360 Lead", lead.name, target)
		frappe.db.commit()

	# Two of the opportunities become priced quotations, then orders, then
	# invoices. The statuses are spread out so the charts show a shape rather
	# than one bar.
	for index, opportunity in enumerate(converted[:2]):
		frappe.db.set_value(
			"KNIT 360 Opportunity", opportunity,
			{"estimated_deal_value": 500000 + index * 250000,
			 "expected_closing_date": add_days(nowdate(), 30 + index * 15),
			 "probability": 60 + index * 20},
		)
		_walk_to("KNIT 360 Opportunity", opportunity, "Proposal Sent")

		quotation = c2c.create_quotation(opportunity)["name"]
		c2c.set_items(
			"quotation", quotation,
			[{"item_code": code, "qty": qty, "unit_rate": rate, "discount_percentage": discount}
			 for code, qty, rate, discount in QUOTE_LINES[index]],
		)
		made["quotations"] += 1

		customer = frappe.db.get_value("KNIT 360 Quotation", quotation, "customer")

		if index == 0:
			# The first deal goes all the way to an outstanding invoice.
			_walk_to("KNIT 360 Quotation", quotation, "Accepted")
			order = frappe.get_doc(
				{
					"doctype": "KNIT 360 Sales Order",
					"customer": customer,
					"company": COMPANY,
					"quotation": quotation,
					"currency": CURRENCY,
					"order_date": nowdate(),
					"items": [
						{"item_code": code, "qty": qty, "rate": rate}
						for code, qty, rate, _ in QUOTE_LINES[index]
					],
				}
			).insert(ignore_permissions=True)
			_walk_to("KNIT 360 Sales Order", order.name, "Confirmed / Booked")
			made["orders"] += 1

			for days, status in ((-45, "Posted / Unpaid"), (-10, "Posted / Unpaid")):
				invoice = frappe.get_doc(
					{
						"doctype": "KNIT 360 Sales Invoice",
						"customer": customer,
						"company": COMPANY,
						"sales_order": order.name,
						"currency": CURRENCY,
						"posting_date": add_days(nowdate(), days),
						"due_date": add_days(nowdate(), days + 30),
						"items": [{"item_code": "FG-COIL-01", "qty": 2, "rate": 24000}],
					}
				).insert(ignore_permissions=True)
				_walk_to("KNIT 360 Sales Invoice", invoice.name, status)
				made["invoices"] += 1

			# One of them is past its due date, which is what Overdue means.
			overdue = frappe.get_all(
				"KNIT 360 Sales Invoice",
				filters={"customer": customer, "due_date": ["<", nowdate()]},
				pluck="name",
			)
			for name in overdue:
				engine.transition("KNIT 360 Sales Invoice", name, "Overdue",
				                  reason="Past its due date")
		else:
			# The second is still with the customer, awaiting a reply.
			_walk_to("KNIT 360 Quotation", quotation, "Issued / Sent")

		frappe.db.commit()

	return made


def opening_balances():
	"""A cash and bank opening balance, so the ledger reports are not empty."""
	if frappe.db.exists("KNIT 360 Journal Entry", {"company": COMPANY, "entry_type": "Opening Entry"}):
		return "already posted"

	def leaf(name):
		"""A leaf account by its bare name, or a readable refusal.

		Without the check this returned None and Frappe reported the failure as
		the single word "account", which says nothing about which account was
		missing or why.
		"""
		found = frappe.db.get_value(
			"KNIT 360 Account", {"company": COMPANY, "account_name": name, "is_group": 0}, "name"
		)
		if not found:
			frappe.throw(
				f"{COMPANY} has no leaf account called {name!r}. "
				f"knit360_core.finance.chart_of_accounts.TREE is what creates them."
			)
		return found

	year = fiscal_year()
	if not year:
		return "no open fiscal year covers today; nothing posted"

	entry = frappe.get_doc(
		{
			"doctype": "KNIT 360 Journal Entry",
			"company": COMPANY,
			# The first day of the fiscal year, not of the calendar year. The
			# site here runs an April-to-March year, and a posting outside the
			# open year is refused by the ledger.
			"posting_date": year.year_start_date,
			"entry_type": "Opening Entry",
			"user_remark": "Sample opening balances (demo data).",
			"accounts": [
				{"account": leaf("Bank Account"), "debit": 2500000, "credit": 0},
				{"account": leaf("Cash"), "debit": 150000, "credit": 0},
				{"account": leaf("Share Capital"), "debit": 0, "credit": 2650000},
			],
		}
	).insert(ignore_permissions=True)
	engine.transition("KNIT 360 Journal Entry", entry.name, "Posted")
	frappe.db.commit()
	return entry.name


def seed():
	"""Fill the masters and build the pipeline. Safe to run more than once."""
	report = {"company": company(), "masters": masters()}
	try:
		report["opening_balances"] = opening_balances()
	except Exception as exc:  # noqa: BLE001 - reported, not hidden
		report["opening_balances"] = f"FAILED: {exc}"
	report["pipeline"] = pipeline()

	trial = ledger.trial_balance(COMPANY)
	report["trial_balance"] = {
		"accounts_with_movement": len(trial["rows"]),
		"debits": trial["total_debit"],
		"credits": trial["total_credit"],
		"balanced": trial["balanced"],
	}

	print("\nKNIT 360 demo data")
	print("=" * 60)
	print(f"company            {report['company']}")
	for doctype, count in sorted(report["masters"].items()):
		print(f"  {doctype:<18} {count}")
	print(f"opening balances   {report['opening_balances']}")
	print(f"pipeline           {report['pipeline']}")
	print(f"trial balance      {report['trial_balance']}")
	print("\nThis is sample data. Edit it or delete it; none of it is a requirement.")
	return report
