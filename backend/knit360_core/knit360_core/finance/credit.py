"""What a customer is allowed to owe -- FR-FIN-003 / FR-SALES-003.

**The one idea.** A credit limit is not a number stored against a customer and
compared with another stored number. It is a question asked of the ledger at
the moment somebody tries to add to the debt:

    exposure = what the books say this customer owes, right now
    headroom = limit - exposure

`exposure` is derived the same way an invoice's outstanding is derived, and
for the same reason: a running total maintained by hand eventually disagrees
with the books, and then nothing can say which of the two is right. It counts
every posting against the party on a receivable account, so an unallocated
advance reduces the exposure exactly as a payment does -- money held for the
customer is money they do not owe.

**What a nil limit means.** No limit. Not a limit of zero. A field left blank
on a master is the commonest state in any real system and it must mean "nobody
has decided", never "refuse everything".

**Credit hold is separate from the limit**, because the reasons differ. A
limit is about size; a hold is about trust -- a dispute, a bounced payment, a
legal notice. A customer on hold is refused whatever their balance, and a
customer within their limit is served even if they were on hold last month.

**Where it is enforced.** At the two points where the business commits to a
debt: confirming a Sales Order and posting a Sales Invoice. Not on a quotation,
which commits to nothing, and not on a draft, which is a person thinking.
"""

import frappe
from frappe.utils import flt

CUSTOMER = "KNIT 360 Customer"
GL = "KNIT 360 GL Entry"
ACCOUNT = "KNIT 360 Account"

#: Below this a difference is arithmetic, not money.
TOLERANCE = 0.005


def exposure(customer, company):
	"""What the books say this customer owes, as a positive number.

	Nil when they owe nothing, and nil rather than negative when they are in
	credit: an advance is not headroom to be spent twice, it is already
	counted by reducing what is owed.
	"""
	row = frappe.db.sql(
		f"""SELECT COALESCE(SUM(gl.debit), 0) - COALESCE(SUM(gl.credit), 0) AS owed
		    FROM `tab{GL}` gl
		    JOIN `tab{ACCOUNT}` acc ON acc.name = gl.account
		    WHERE gl.party_type = 'Customer' AND gl.party = %s
		      AND gl.company = %s AND gl.is_cancelled = 0
		      AND acc.account_type = 'Receivable'""",
		(customer, company),
		as_dict=True,
	)[0]
	return max(flt(row.owed), 0.0)


def terms_for(customer):
	"""The limit and the hold, as the master records them."""
	row = frappe.db.get_value(
		CUSTOMER, customer, ["credit_limit", "credit_hold"], as_dict=True
	)
	if not row:
		return 0.0, False
	return flt(row.credit_limit), bool(row.credit_hold)


def headroom(customer, company):
	"""What this customer may still be allowed to owe, or None for no limit."""
	limit, _ = terms_for(customer)
	if not limit:
		return None
	return flt(limit - exposure(customer, company))


def check_can_owe(customer, company, amount, document=None):
	"""Refuse a commitment this customer is not allowed to take on.

	Refused rather than flagged for later. A credit control that writes a
	warning into a log is a credit control nobody reads: by the time anyone
	looks, the goods have gone.
	"""
	if not customer:
		return

	limit, on_hold = terms_for(customer)
	label = document or "this document"

	if on_hold:
		frappe.throw(
			f"{customer} is on credit hold, so {label} cannot be committed. "
			f"Clear the hold on the customer record, or take the order on "
			f"advance payment."
		)

	if not limit:
		return

	owed = exposure(customer, company)
	after = flt(owed + flt(amount))
	if after - limit > TOLERANCE:
		frappe.throw(
			f"{customer} owes {owed:,.2f} and {label} would take that to "
			f"{after:,.2f}, against a credit limit of {limit:,.2f}. Raise the "
			f"limit, take a payment against what is outstanding, or reduce "
			f"this document."
		)


@frappe.whitelist()
def standing(customer, company):
	"""The customer's credit position, for a screen to show. Reads only."""
	limit, on_hold = terms_for(customer)
	owed = exposure(customer, company)
	return {
		"customer": customer,
		"owed": owed,
		"limit": limit,
		"on_hold": on_hold,
		"headroom": None if not limit else flt(limit - owed),
	}
