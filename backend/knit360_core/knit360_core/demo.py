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
from frappe.utils import add_days, flt, getdate, nowdate

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


def settlements():
	"""Receive money against the demo invoices -- DEC-022.

	Two of the three invoices are left owing something on purpose. A
	demonstration where everything is paid shows nothing: the interesting
	screen is the one with a part payment on it, where the invoice says what
	arrived and what is still owed.

	It also re-derives every invoice's status from the ledger before it starts.
	A status moved by hand during a demonstration -- an invoice clicked to Paid
	with no receipt behind it -- is put back to what the books actually say.
	"""
	from knit360_core.finance import settlement

	made = {"realigned": [], "payments": 0}

	# A residue smaller than one rupee may be written off, by asking. Nothing
	# is ever written off on its own.
	frappe.db.set_value("KNIT 360 Company", COMPANY, "write_off_tolerance", 1.0,
	                    update_modified=False)

	for name in frappe.get_all(
		"KNIT 360 Sales Invoice", filters={"company": COMPANY, "docstatus": 1}, pluck="name"
	):
		before = frappe.db.get_value("KNIT 360 Sales Invoice", name, "knit360_business_status")
		settlement.refresh("KNIT 360 Sales Invoice", name)
		after = frappe.db.get_value("KNIT 360 Sales Invoice", name, "knit360_business_status")
		if before != after:
			made["realigned"].append(f"{name}: {before} -> {after}")

	if frappe.db.count("KNIT 360 Payment Entry", {"company": COMPANY}):
		made["payments"] = "already settled"
		frappe.db.commit()
		return made

	bank = frappe.db.get_value("KNIT 360 Company", COMPANY, "default_bank_account")
	mode = frappe.db.get_value("KNIT 360 Mode of Payment", {}, "name")

	owing = [
		row for row in frappe.get_all(
			"KNIT 360 Sales Invoice",
			filters={"company": COMPANY, "docstatus": 1},
			fields=["name", "customer", "grand_total"],
			order_by="posting_date asc",
		)
		if settlement.outstanding("KNIT 360 Sales Invoice", row.name) > 0
	]

	# The oldest gets a part payment; it is the screen worth showing.
	for index, invoice in enumerate(owing[:2]):
		left = settlement.outstanding("KNIT 360 Sales Invoice", invoice.name)
		amount = flt(left * 0.4) if index == 0 else left
		payment = frappe.get_doc(
			{
				"doctype": "KNIT 360 Payment Entry",
				"company": COMPANY,
				"payment_direction": "Receive",
				"party_type": "KNIT 360 Customer",
				"party": invoice.customer,
				"payment_date": nowdate(),
				"amount": amount,
				"payment_mode": mode,
				"bank_account": bank,
				"allocations": [
					{
						"doctype": "KNIT 360 Payment Allocation",
						"reference_doctype": "KNIT 360 Sales Invoice",
						"reference_name": invoice.name,
						"allocated_amount": amount,
					}
				],
			}
		).insert(ignore_permissions=True)
		reached = _walk_to("KNIT 360 Payment Entry", payment.name, "Disbursed / Cleared")
		if reached != "Disbursed / Cleared":
			# A payment left in Draft has settled nothing. Saying otherwise is
			# how seeded data comes to disagree with the books.
			frappe.throw(
				f"{payment.name} stopped at {reached!r} instead of reaching "
				f"'Disbursed / Cleared', so nothing was settled."
			)
		made["payments"] += 1
		made.setdefault("against", []).append(
			f"{payment.name} {amount:.2f} -> {invoice.name}"
		)

	frappe.db.commit()
	return made


#: (name, company-scoped). The organisation a demonstration needs before it
#: can have an employee: somebody has to be in a department with a job title.
DEPARTMENTS = ("Production", "Quality", "Sales", "Accounts")
DESIGNATIONS = ("Plant Manager", "Quality Engineer", "Sales Executive", "Accountant")

#: (name, designation, department, joined how many days ago)
PEOPLE = [
	("Anil Deshpande", "Plant Manager", "Production", 1400),
	("Fatima Shaikh", "Quality Engineer", "Quality", 900),
	("Vikram Thakkar", "Sales Executive", "Sales", 500),
	("Leena Pillai", "Accountant", "Accounts", 260),
]

#: (name, paid, carry forward, allow a negative balance, days a year)
LEAVE_TYPES = [
	("Casual Leave", 1, 0, 0, 12),
	("Sick Leave", 1, 0, 1, 8),
	("Earned Leave", 1, 1, 0, 15),
	("Leave Without Pay", 0, 0, 1, 0),
]

#: (month, day, what it is). Fixed-date national holidays only -- the ones that
#: move with the lunar calendar are not invented here.
HOLIDAYS = [
	(1, 26, "Republic Day"),
	(5, 1, "Labour Day"),
	(8, 15, "Independence Day"),
	(10, 2, "Gandhi Jayanti"),
	(12, 25, "Christmas Day"),
]


def hr():
	"""People, a holiday list, leave types, allocations and three requests.

	The three requests are deliberately in three different states. A
	demonstration of leave where everything is approved shows nothing: the
	screens worth seeing are the one waiting for a decision and the one that
	was refused and touched no balance.
	"""
	made = {}
	year = getdate(nowdate()).year

	for name in DESIGNATIONS:
		_insert("KNIT 360 Designation", {"designation_name": name}, key="designation_name")
	made["Designation"] = len(DESIGNATIONS)

	for name in DEPARTMENTS:
		_insert("KNIT 360 Department", {"department_name": name, "company": COMPANY},
		        key="department_name")
	made["Department"] = len(DEPARTMENTS)

	holiday_list = f"India {year}"
	if not frappe.db.exists("KNIT 360 Holiday List", holiday_list):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Holiday List",
				"holiday_list_name": holiday_list,
				"company": COMPANY,
				"from_date": f"{year}-01-01",
				"to_date": f"{year}-12-31",
				"holidays": [
					{"holiday_date": f"{year}-{month:02d}-{day:02d}", "description": what}
					for month, day, what in HOLIDAYS
				],
			}
		).insert(ignore_permissions=True)
	made["Holiday List"] = 1

	period = f"{year} Leave Year"
	if not frappe.db.exists("KNIT 360 Leave Period", period):
		frappe.get_doc(
			{
				"doctype": "KNIT 360 Leave Period",
				"period_name": period,
				"company": COMPANY,
				"from_date": f"{year}-01-01",
				"to_date": f"{year}-12-31",
				"is_active": 1,
				"holiday_list": holiday_list,
			}
		).insert(ignore_permissions=True)
	made["Leave Period"] = 1

	for name, paid, carry, negative, days in LEAVE_TYPES:
		_insert(
			"KNIT 360 Leave Type",
			{
				"leave_type_name": name,
				"is_paid_leave": paid,
				"is_carry_forward": carry,
				"allow_negative_balance": negative,
				"max_leaves_allowed": days,
			},
			key="leave_type_name",
		)
	made["Leave Type"] = len(LEAVE_TYPES)

	employees = []
	for name, designation, department, joined in PEOPLE:
		existing = frappe.db.get_value("KNIT 360 Employee", {"employee_name": name}, "name")
		if existing:
			employees.append(existing)
			continue
		doc = frappe.get_doc(
			{
				"doctype": "KNIT 360 Employee",
				"employee_name": name,
				"company": COMPANY,
				"designation": designation,
				"department": department,
				"date_of_joining": add_days(nowdate(), -joined),
				"is_active": 1,
			}
		).insert(ignore_permissions=True)
		employees.append(doc.name)
	made["Employee"] = len(employees)

	# Everybody gets Casual and Sick leave for the year.
	allocated = 0
	for employee in employees:
		for leave_type, days in (("Casual Leave", 12), ("Sick Leave", 8)):
			if frappe.db.exists(
				"KNIT 360 Leave Allocation",
				{"employee": employee, "leave_type": leave_type, "leave_period": period,
				 "docstatus": ["!=", 2]},
			):
				continue
			allocation = frappe.get_doc(
				{
					"doctype": "KNIT 360 Leave Allocation",
					"employee": employee,
					"leave_type": leave_type,
					"company": COMPANY,
					"leave_period": period,
					"from_date": f"{year}-01-01",
					"to_date": f"{year}-12-31",
					"new_leaves_allocated": days,
					"description": f"{leave_type} entitlement for {year}",
				}
			).insert(ignore_permissions=True)
			_walk_to("KNIT 360 Leave Allocation", allocation.name, "Allocated")
			allocated += 1
	made["Leave Allocation"] = allocated

	# Three requests, three states, so each screen has something on it.
	if not frappe.db.count("KNIT 360 Leave Application", {"company": COMPANY}):
		requests = [
			(employees[0], "Casual Leave", -20, -19, "Approved", "Family function"),
			(employees[1], "Sick Leave", 5, 6, "Pending Approval", "Medical appointment"),
			(employees[2], "Casual Leave", 12, 16, "Rejected", "Holiday - clashes with the audit"),
		]
		for employee, leave_type, start, end, target, reason in requests:
			application = frappe.get_doc(
				{
					"doctype": "KNIT 360 Leave Application",
					"employee": employee,
					"leave_type": leave_type,
					"company": COMPANY,
					"from_date": add_days(nowdate(), start),
					"to_date": add_days(nowdate(), end),
					"holiday_list": holiday_list,
					"reason": reason,
				}
			).insert(ignore_permissions=True)
			if target == "Rejected":
				engine.transition("KNIT 360 Leave Application", application.name,
				                  "Pending Approval")
				engine.transition("KNIT 360 Leave Application", application.name, "Rejected",
				                  reason="Clashes with the statutory audit")
			else:
				reached = _walk_to("KNIT 360 Leave Application", application.name, target)
				if reached != target:
					frappe.throw(
						f"{application.name} stopped at {reached!r}, not {target!r}."
					)
		made["Leave Application"] = len(requests)

	frappe.db.commit()
	return made


#: (supplier, bill number, [(item, qty, rate)], freight, statutory tax)
#: (supplier, bill number, lines, freight, tax, the item whose receipt this
#: bill settles -- or None for a bill that never passed through stock).
SUPPLIER_BILLS = [
	("Precision Semiconductors Pvt Ltd", "PSPL/2026/4471",
	 [("CM-IGBT-01", 40, 7200)], 2400, 51840, "CM-IGBT-01"),
	("Hanover Komponenten GmbH", "HK-INV-90233",
	 [("RM-CU-01", 150, 820)], 18500, 0, None),
]


def _receipt_for(item_code):
	"""The earliest demonstration receipt that brought this item in.

	A bill that names its receipt is the one worth showing: the receipt put a
	figure into Stock Received But Not Billed and this bill is what clears it.
	"""
	if not item_code:
		return None
	rows = frappe.db.sql(
		"""SELECT parent FROM `tabKNIT 360 Goods Receipt Item` item
		   JOIN `tabKNIT 360 Goods Receipt` receipt ON receipt.name = item.parent
		   WHERE item.item_code = %s AND receipt.company = %s AND receipt.docstatus = 1
		   ORDER BY receipt.creation ASC LIMIT 1""",
		(item_code, COMPANY),
	)
	return rows[0][0] if rows else None


def buying():
	"""Supplier bills that reach the books -- DEC-020 and DEC-033.

	The first bill names the goods receipt it settles, so the demonstration can
	show Stock Received But Not Billed opened by the receipt and closed by the
	bill. The second names none: freight on an import that was expensed, which
	is what DEC-033 decided and what a client's accountant will ask about.
	"""
	made = {"Supplier Invoice": 0}
	for supplier, bill_no, lines, freight, tax, settles in SUPPLIER_BILLS:
		if frappe.db.exists("KNIT 360 Supplier Invoice", {"bill_no": bill_no}):
			continue
		invoice = frappe.get_doc(
			{
				"doctype": "KNIT 360 Supplier Invoice",
				"supplier": supplier,
				"company": COMPANY,
				"bill_no": bill_no,
				"bill_date": add_days(nowdate(), -12),
				"currency": CURRENCY,
				"goods_receipt": _receipt_for(settles),
				"freight_and_ancillary": freight,
				"statutory_tax_amount": tax,
				"payment_terms": "30 days from the date of the bill",
				"items": [
					{"item_code": code, "qty": qty, "rate": rate} for code, qty, rate in lines
				],
			}
		).insert(ignore_permissions=True)
		reached = _walk_to("KNIT 360 Supplier Invoice", invoice.name, "Matched & Approved")
		if reached != "Matched & Approved":
			frappe.throw(f"{invoice.name} stopped at {reached!r}; no payable was created.")
		invoice.reload()
		made["Supplier Invoice"] += 1
		made.setdefault("payable", []).append(
			f"{invoice.name} {invoice.grand_total:,.2f} owing {invoice.outstanding_amount:,.2f}"
		)
	frappe.db.commit()
	return made


#: (item, warehouse, qty, rate, how many days ago). Two receipts of the same
#: item at different prices, so a dispatch has something to choose between and
#: FIFO can be shown rather than asserted.
RECEIPTS = [
	("CM-IGBT-01", "Main Store", 40, 7200, 60),
	("CM-IGBT-01", "Main Store", 40, 7650, 20),
	("CM-CAP-01", "Main Store", 25, 3100, 45),
	("RM-CU-01", "Main Store", 400, 790, 50),
	("FG-COIL-01", "Finished Goods Store", 12, 18400, 30),
	("FG-PANEL-01", "Finished Goods Store", 5, 64000, 30),
]

#: (item, warehouse, qty, how many days ago). Deliberately crosses the two
#: IGBT receipts: 50 out of 80 takes all forty at 7,200 and ten at 7,650.
DISPATCHES = [
	("FG-COIL-01", "Finished Goods Store", 4, 12),
	("CM-IGBT-01", "Main Store", 50, 5),
]


def stock():
	"""Receive and dispatch, so the stock ledger has something to show.

	The receipts are priced differently on purpose. A demonstration of FIFO
	where every receipt cost the same proves nothing -- the screen worth
	showing is the dispatch that crossed two price layers.
	"""
	from knit360_core.stock import ledger as stock_ledger

	made = {"receipts": 0, "dispatches": 0}

	if frappe.db.count("KNIT 360 Goods Receipt", {"company": COMPANY}):
		made["receipts"] = "already received"
	else:
		for item, warehouse, qty, rate, days in RECEIPTS:
			receipt = frappe.get_doc(
				{
					"doctype": "KNIT 360 Goods Receipt",
					"company": COMPANY,
					"receiving_warehouse": warehouse,
					"challan_number": f"CH-{nowdate().replace('-', '')}-{made['receipts'] + 1:03d}",
					"challan_date": add_days(nowdate(), -days),
					"items": [
						{
							"item_code": item,
							"qty_arrived": qty,
							"qty_rejected_on_arrival": 0,
							"rate": rate,
						}
					],
				}
			).insert(ignore_permissions=True)
			reached = _walk_to("KNIT 360 Goods Receipt", receipt.name, "Received in Bay")
			if reached != "Received in Bay":
				frappe.throw(f"{receipt.name} stopped at {reached!r}; nothing was put away.")
			made["receipts"] += 1

	if frappe.db.count("KNIT 360 Delivery Note", {"company": COMPANY}):
		made["dispatches"] = "already dispatched"
	else:
		for item, warehouse, qty, days in DISPATCHES:
			note = frappe.get_doc(
				{
					"doctype": "KNIT 360 Delivery Note",
					"company": COMPANY,
					"source_warehouse": warehouse,
					"delivery_note_date": add_days(nowdate(), -days),
					"items": [{"item_code": item, "qty": qty}],
				}
			).insert(ignore_permissions=True)
			reached = _walk_to("KNIT 360 Delivery Note", note.name, "Dispatched / In Transit")
			if reached != "Dispatched / In Transit":
				frappe.throw(f"{note.name} stopped at {reached!r}; no stock left the warehouse.")
			made["dispatches"] += 1

	made["on_hand"] = [
		f"{row['item_code']} @ {row['warehouse']}: {row['qty']:g} worth {row['value']:,.2f}"
		for row in stock_ledger.stock_on_hand(company=COMPANY)
	]
	frappe.db.commit()
	return made


def returns():
	"""One credit note and one debit note -- DEC-037.

	A return is the screen a client asks about within the first ten minutes,
	because every business has them and most systems handle them by cancelling
	the invoice and pretending it never happened. The credit note here is
	raised against a part-paid invoice on purpose: it shows the outstanding
	falling for a reason other than money arriving.
	"""
	from knit360_core.finance import settlement

	made = {"Credit Note": 0, "Debit Note": 0}

	if frappe.db.count("KNIT 360 Credit Note", {"company": COMPANY}):
		made["Credit Note"] = "already raised"
	else:
		owing = [
			row for row in frappe.get_all(
				"KNIT 360 Sales Invoice",
				filters={"company": COMPANY, "docstatus": 1},
				fields=["name", "customer"],
				order_by="posting_date asc",
			)
			if settlement.outstanding("KNIT 360 Sales Invoice", row.name) > 1000
		]
		if owing:
			invoice = owing[0]
			note = frappe.get_doc(
				{
					"doctype": "KNIT 360 Credit Note",
					"company": COMPANY,
					"customer": invoice.customer,
					"sales_invoice": invoice.name,
					"posting_date": nowdate(),
					"reason": "One coil returned: winding damaged in transit.",
					"items": [{"item_code": "FG-COIL-01", "qty": 1, "rate": 24000}],
				}
			).insert(ignore_permissions=True)
			reached = _walk_to("KNIT 360 Credit Note", note.name, "Issued")
			if reached != "Issued":
				frappe.throw(f"{note.name} stopped at {reached!r}; nothing was credited.")
			made["Credit Note"] = 1
			made["credited"] = (
				f"{note.name} against {invoice.name}, now owing "
				f"{settlement.outstanding('KNIT 360 Sales Invoice', invoice.name):,.2f}"
			)

	if frappe.db.count("KNIT 360 Debit Note", {"company": COMPANY}):
		made["Debit Note"] = "already raised"
	else:
		bills = [
			row for row in frappe.get_all(
				"KNIT 360 Supplier Invoice",
				filters={"company": COMPANY, "docstatus": 1},
				fields=["name", "supplier"],
				order_by="bill_date asc",
			)
			if settlement.outstanding("KNIT 360 Supplier Invoice", row.name) > 10000
		]
		if bills:
			bill = bills[0]
			note = frappe.get_doc(
				{
					"doctype": "KNIT 360 Debit Note",
					"company": COMPANY,
					"supplier": bill.supplier,
					"supplier_invoice": bill.name,
					"posting_date": nowdate(),
					"reason": "Two modules failed incoming inspection and went back.",
					"items": [{"item_code": "CM-IGBT-01", "qty": 2, "rate": 7200}],
				}
			).insert(ignore_permissions=True)
			reached = _walk_to("KNIT 360 Debit Note", note.name, "Issued")
			if reached != "Issued":
				frappe.throw(f"{note.name} stopped at {reached!r}; nothing was debited.")
			made["Debit Note"] = 1
			made["debited"] = (
				f"{note.name} against {bill.name}, now owing "
				f"{settlement.outstanding('KNIT 360 Supplier Invoice', bill.name):,.2f}"
			)

	frappe.db.commit()
	return made


def seed():
	"""Fill the masters and build the pipeline. Safe to run more than once."""
	report = {"company": company(), "masters": masters()}
	try:
		report["opening_balances"] = opening_balances()
	except Exception as exc:  # noqa: BLE001 - reported, not hidden
		report["opening_balances"] = f"FAILED: {exc}"
	report["pipeline"] = pipeline()
	report["settlements"] = settlements()
	report["hr"] = hr()
	report["stock"] = stock()
	report["buying"] = buying()
	report["returns"] = returns()

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
	print(f"settlements        {report['settlements']}")
	print(f"hr                 {report['hr']}")
	print(f"stock              {report['stock']}")
	print(f"buying             {report['buying']}")
	print(f"returns            {report['returns']}")
	print(f"trial balance      {report['trial_balance']}")
	print("\nThis is sample data. Edit it or delete it; none of it is a requirement.")
	return report
