"""The general ledger -- FR-FIN-001.

Every posting in KNIT 360 goes through post(). Nothing else writes a GL Entry.

The rules enforced here are double-entry bookkeeping, not KNIT policy:

  * an entry balances, or it is not written at all
  * a line is a debit or a credit, never both and never neither
  * a posted entry is never edited or deleted; it is reversed

That last rule is CD-002's, and it is why cancellation writes a mirrored entry
flagged is_cancelled rather than removing rows. The audit trail of what the
books once said is part of the books.

Posting is wired to Frappe's on_submit / on_cancel, which is what the business
status adapter already drives: a document reaching a submitted state calls
doc.submit(), Frappe calls on_submit, and the controller calls post() from
there. So the ledger is a consequence of the lifecycle, never a parallel path
around it.
"""

import frappe
from frappe.utils import flt, getdate

GL = "KNIT 360 GL Entry"
ACCOUNT = "KNIT 360 Account"
FISCAL_YEAR = "KNIT 360 Fiscal Year"

#: Rounding tolerance. Currency arithmetic in Python is not exact, and a
#: half-paisa difference is not an unbalanced entry.
TOLERANCE = 0.005


class Line:
	"""One side of one posting."""

	def __init__(self, account, debit=0.0, credit=0.0, party_type=None, party=None,
	             cost_center=None, against_voucher_type=None, against_voucher=None,
	             remarks=None):
		self.account = account
		self.debit = flt(debit)
		self.credit = flt(credit)
		self.party_type = party_type
		self.party = party
		self.cost_center = cost_center
		self.against_voucher_type = against_voucher_type
		self.against_voucher = against_voucher
		self.remarks = remarks

	def validate(self):
		if self.debit and self.credit:
			frappe.throw(f"{self.account}: a line is a debit or a credit, not both.")
		if not self.debit and not self.credit:
			frappe.throw(f"{self.account}: a line with neither a debit nor a credit posts nothing.")
		if self.debit < 0 or self.credit < 0:
			frappe.throw(
				f"{self.account}: negative amounts are not postings. "
				f"Post the opposite side instead."
			)


def fiscal_year_for(posting_date):
	"""The open fiscal year containing the date."""
	date = getdate(posting_date)
	year = frappe.db.get_value(
		FISCAL_YEAR,
		{"year_start_date": ["<=", date], "year_end_date": [">=", date]},
		["name", "is_closed"],
		as_dict=True,
	)
	if not year:
		frappe.throw(
			f"No {FISCAL_YEAR} covers {date}. "
			f"Create one before posting into that period."
		)
	if year.is_closed:
		frappe.throw(f"Fiscal year {year.name} is closed. It takes no further postings.")
	return year.name


def _check_accounts(lines, company):
	for line in lines:
		account = frappe.db.get_value(
			ACCOUNT, line.account, ["company", "is_group", "disabled"], as_dict=True
		)
		if not account:
			frappe.throw(f"{ACCOUNT} {line.account} does not exist.")
		if account.is_group:
			frappe.throw(
				f"{line.account} is a group account. Postings go to leaf accounts, "
				f"so that a group's balance stays the sum of its children."
			)
		if account.disabled:
			frappe.throw(f"{line.account} is disabled and takes no new postings.")
		if account.company != company:
			frappe.throw(
				f"{line.account} belongs to {account.company}, "
				f"but this posting is for {company}."
			)


def _against(lines):
	"""The contra side of each line, for readability on the entry itself."""
	debits = sorted({line.account for line in lines if line.debit})
	credits = sorted({line.account for line in lines if line.credit})
	return {
		"debit": ", ".join(credits),
		"credit": ", ".join(debits),
	}


def post(voucher_type, voucher_no, company, posting_date, lines, remarks=None):
	"""Write a balanced set of GL entries for one document.

	Returns the names of the entries written.
	"""
	if not lines:
		frappe.throw(f"{voucher_type} {voucher_no}: nothing to post.")

	for line in lines:
		line.validate()

	total_debit = sum(line.debit for line in lines)
	total_credit = sum(line.credit for line in lines)
	if abs(total_debit - total_credit) > TOLERANCE:
		frappe.throw(
			f"{voucher_type} {voucher_no} does not balance: "
			f"debits {total_debit:.2f} against credits {total_credit:.2f}. "
			f"An unbalanced entry is never written."
		)

	_check_accounts(lines, company)
	fiscal_year = fiscal_year_for(posting_date)
	against = _against(lines)

	written = []
	for line in lines:
		entry = frappe.get_doc(
			{
				"doctype": GL,
				"posting_date": posting_date,
				"account": line.account,
				"debit": line.debit,
				"credit": line.credit,
				"company": company,
				"cost_center": line.cost_center,
				"fiscal_year": fiscal_year,
				"party_type": line.party_type,
				"party": line.party,
				"voucher_type": voucher_type,
				"voucher_no": voucher_no,
				"against_voucher_type": line.against_voucher_type,
				"against_voucher": line.against_voucher,
				"against_account": against["debit"] if line.debit else against["credit"],
				"remarks": line.remarks or remarks,
				"is_cancelled": 0,
			}
		).insert(ignore_permissions=True)
		written.append(entry.name)
	return written


def reverse(voucher_type, voucher_no, posting_date=None):
	"""Reverse a document's postings by writing their mirror image.

	The original entries are flagged rather than deleted, and the reversing
	entries are flagged too, so a query that excludes is_cancelled sees neither
	and the books net to zero either way.
	"""
	existing = frappe.get_all(
		GL,
		filters={"voucher_type": voucher_type, "voucher_no": voucher_no, "is_cancelled": 0},
		fields=["name", "posting_date", "account", "debit", "credit", "company",
		        "cost_center", "fiscal_year", "party_type", "party",
		        "against_voucher_type", "against_voucher", "against_account", "remarks"],
	)
	if not existing:
		return []

	written = []
	for row in existing:
		mirror = dict(row)
		name = mirror.pop("name")
		mirror["debit"], mirror["credit"] = row["credit"], row["debit"]
		mirror["posting_date"] = posting_date or row["posting_date"]
		mirror["remarks"] = f"Reversal of {voucher_type} {voucher_no}"
		mirror.update({"doctype": GL, "voucher_type": voucher_type,
		               "voucher_no": voucher_no, "is_cancelled": 1})
		written.append(frappe.get_doc(mirror).insert(ignore_permissions=True).name)
		frappe.db.set_value(GL, name, "is_cancelled", 1, update_modified=False)
	return written


# --- Reading the ledger ---------------------------------------------------

def balance(account, company=None, upto=None):
	"""Net debit balance of one account. Negative means it is in credit."""
	filters = {"account": account, "is_cancelled": 0}
	if company:
		filters["company"] = company
	if upto:
		filters["posting_date"] = ["<=", getdate(upto)]
	rows = frappe.get_all(filters=filters, doctype=GL, fields=["sum(debit) as d", "sum(credit) as c"])
	row = rows[0] if rows else {}
	return flt(row.get("d")) - flt(row.get("c"))


def party_balance(party_type, party, company=None):
	"""What a customer owes, or what is owed to a supplier."""
	filters = {"party_type": party_type, "party": party, "is_cancelled": 0}
	if company:
		filters["company"] = company
	rows = frappe.get_all(doctype=GL, filters=filters, fields=["sum(debit) as d", "sum(credit) as c"])
	row = rows[0] if rows else {}
	return flt(row.get("d")) - flt(row.get("c"))


@frappe.whitelist()
def trial_balance(company, upto=None):
	"""FR-FIN-007. Every account with a movement, and the proof that it balances."""
	filters = {"company": company, "is_cancelled": 0}
	if upto:
		filters["posting_date"] = ["<=", getdate(upto)]

	rows = frappe.get_all(
		GL,
		filters=filters,
		fields=["account", "sum(debit) as debit", "sum(credit) as credit"],
		group_by="account",
		order_by="account",
	)
	meta = {
		a.name: a
		for a in frappe.get_all(
			ACCOUNT, filters={"company": company}, fields=["name", "account_number", "root_type"]
		)
	}
	out = []
	for row in rows:
		info = meta.get(row.account, {})
		net = flt(row.debit) - flt(row.credit)
		out.append(
			{
				"account": row.account,
				"account_number": info.get("account_number"),
				"root_type": info.get("root_type"),
				"debit": flt(row.debit),
				"credit": flt(row.credit),
				"balance": net,
			}
		)
	total_debit = sum(r["debit"] for r in out)
	total_credit = sum(r["credit"] for r in out)
	return {
		"company": company,
		"upto": upto,
		"rows": out,
		"total_debit": total_debit,
		"total_credit": total_credit,
		"balanced": abs(total_debit - total_credit) <= TOLERANCE,
	}


@frappe.whitelist()
def voucher_entries(voucher_type, voucher_no, include_cancelled=0):
	"""The ledger effect of one document, for showing on that document."""
	filters = {"voucher_type": voucher_type, "voucher_no": voucher_no}
	if not int(include_cancelled or 0):
		filters["is_cancelled"] = 0
	return frappe.get_all(
		GL,
		filters=filters,
		fields=["name", "posting_date", "account", "debit", "credit",
		        "party_type", "party", "against_account", "remarks", "is_cancelled",
		        # Which document this line settles. Without these a caller
		        # cannot tell an allocated line from an advance, and reads
		        # every line as unallocated.
		        "against_voucher_type", "against_voucher"],
		order_by="creation",
	)
