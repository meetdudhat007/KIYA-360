"""Bootstrap a company's chart of accounts -- FR-FIN-001.

The structure below is ordinary double-entry bookkeeping: five roots, current
and non-current under assets and liabilities, and the control accounts every
subledger needs. It is a starting point a bookkeeper will rearrange, not a
prescription -- which is why setup() will not touch a company that already has
accounts.

Also sets the company's default accounts, because a Sales Invoice that cannot
resolve the account it debits refuses to post, and nothing else would supply it.
"""

import frappe

ACCOUNT = "KNIT 360 Account"
COST_CENTER = "KNIT 360 Cost Center"
COMPANY = "KNIT 360 Company"

#: (name, account_type, [children]). A node with children is a group.
TREE = {
	"Assets": ("Asset", [
		("Current Assets", None, [
			("Accounts Receivable", None, [
				("Debtors", "Receivable", []),
			]),
			("Bank Accounts", None, [
				("Bank Account", "Bank", []),
			]),
			("Cash In Hand", None, [
				("Cash", "Cash", []),
			]),
			("Stock Assets", None, [
				("Stock In Hand", "Stock", []),
			]),
			("Tax Assets", None, [
				("Input Tax Credit", "Tax", []),
			]),
		]),
		("Fixed Assets", None, [
			("Plant and Machinery", "Fixed Asset", []),
			("Accumulated Depreciation", "Accumulated Depreciation", []),
		]),
	]),
	"Liabilities": ("Liability", [
		("Current Liabilities", None, [
			("Accounts Payable", None, [
				("Creditors", "Payable", []),
			]),
			("Duties and Taxes", None, [
				("Output Tax Payable", "Tax", []),
			]),
			("Stock Liabilities", None, [
				("Stock Received But Not Billed", "Stock Received But Not Billed", []),
			]),
		]),
	]),
	"Equity": ("Equity", [
		("Share Capital", "Equity", []),
		("Retained Earnings", "Equity", []),
	]),
	"Income": ("Income", [
		("Direct Income", None, [
			("Sales", "Income Account", []),
			("Service Revenue", "Income Account", []),
		]),
		("Indirect Income", None, [
			("Other Income", "Income Account", []),
		]),
	]),
	"Expenses": ("Expense", [
		("Cost of Goods Sold", "Cost of Goods Sold", []),
		("Direct Expenses", None, [
			("Freight and Forwarding", "Expense Account", []),
		]),
		("Indirect Expenses", None, [
			("Administrative Expenses", "Expense Account", []),
			("Depreciation", "Depreciation", []),
			("Round Off", "Round Off", []),
		]),
	]),
}

#: Company field -> the leaf account that fills it.
DEFAULTS = {
	"default_receivable_account": "Debtors",
	"default_payable_account": "Creditors",
	"default_income_account": "Sales",
	"default_expense_account": "Administrative Expenses",
	"default_cash_account": "Cash",
	"default_bank_account": "Bank Account",
	"round_off_account": "Round Off",
	# DEC-021. Tax charged to a customer is money held for the tax authority,
	# so it belongs in a liability; tax paid to a supplier is recoverable, so
	# it belongs in an asset. Neither is income or expense.
	"default_output_tax_account": "Output Tax Payable",
	"default_input_tax_account": "Input Tax Credit",
	# Perpetual inventory -- DEC-030. Stock on hand is an asset; the cost of
	# what has been sold is an expense; goods received but not yet billed are
	# a liability, because they are ours and we owe for them.
	"default_stock_account": "Stock In Hand",
	"default_cogs_account": "Cost of Goods Sold",
	"stock_received_but_not_billed": "Stock Received But Not Billed",
	# DEC-033. Freight on a supplier's bill is a direct expense rather than
	# part of the cost of the goods. It sits beside Cost of Goods Sold so that
	# gross margin still carries it.
	"default_freight_account": "Freight and Forwarding",
}


def _abbreviation(company):
	"""Initials, so 'Kelvinotherm Induction LLP' becomes 'KIL'."""
	abbr = frappe.db.get_value(COMPANY, company, "abbreviation")
	if abbr:
		return abbr
	abbr = "".join(word[0] for word in company.split() if word)[:5].upper() or "CO"
	frappe.db.set_value(COMPANY, company, "abbreviation", abbr, update_modified=False)
	return abbr


def _create(company, account_name, root_type, account_type, parent, is_group):
	doc = frappe.get_doc(
		{
			"doctype": ACCOUNT,
			"account_name": account_name,
			"company": company,
			"root_type": root_type,
			"account_type": account_type,
			"parent_account": parent,
			"is_group": 1 if is_group else 0,
		}
	).insert(ignore_permissions=True)
	return doc.name


def _walk(company, nodes, root_type, parent):
	created = {}
	for account_name, account_type, children in nodes:
		name = _create(company, account_name, root_type, account_type, parent, bool(children))
		created[account_name] = name
		created.update(_walk(company, children, root_type, name))
	return created


@frappe.whitelist()
def backfill_defaults(company=None):
	"""Fill a default account field that is empty, from the existing chart.

	setup() refuses to touch a company that already has accounts, which is the
	right rule -- but it means a company created before a default was added
	never gets it. This fills only what is empty, by looking the leaf up in the
	chart the company already has, and never overwrites a chosen account.
	"""
	companies = [company] if company else frappe.get_all(COMPANY, pluck="name")
	filled = {}
	for name in companies:
		current = frappe.db.get_value(COMPANY, name, list(DEFAULTS), as_dict=True)
		if not current:
			continue
		values = {}
		for field, leaf in DEFAULTS.items():
			if current.get(field):
				continue
			account = frappe.db.get_value(
				ACCOUNT, {"company": name, "account_name": leaf, "is_group": 0}, "name"
			)
			if account:
				values[field] = account
		if values:
			frappe.db.set_value(COMPANY, name, values, update_modified=False)
			filled[name] = values
	if filled:
		frappe.db.commit()
	return filled


@frappe.whitelist()
def setup(company):
	"""Create the chart, a root cost centre, and the company's defaults.

	Idempotent by refusal: a company that already has accounts is left alone
	rather than merged into, because merging two charts silently is worse than
	doing nothing.
	"""
	if frappe.db.exists(ACCOUNT, {"company": company}):
		return {"company": company, "created": 0, "note": "already has a chart of accounts"}

	_abbreviation(company)
	created = {}
	for root_name, (root_type, children) in TREE.items():
		root = _create(company, root_name, root_type, None, None, True)
		created[root_name] = root
		created.update(_walk(company, children, root_type, root))

	cost_center = frappe.get_doc(
		{
			"doctype": COST_CENTER,
			"cost_center_name": "Main",
			"company": company,
			"is_group": 0,
		}
	).insert(ignore_permissions=True)

	values = {field: created[leaf] for field, leaf in DEFAULTS.items() if leaf in created}
	values["default_cost_center"] = cost_center.name
	frappe.db.set_value(COMPANY, company, values, update_modified=False)

	frappe.db.commit()
	return {
		"company": company,
		"created": len(created),
		"cost_center": cost_center.name,
		"defaults": values,
	}
