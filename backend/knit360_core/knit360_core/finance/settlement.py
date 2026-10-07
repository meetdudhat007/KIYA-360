"""What a document still owes, and what settles it -- DEC-022, FR-FIN-003/004.

**The one idea here.** An invoice's outstanding amount is never stored as the
truth. It is the difference between what was posted against that invoice as a
receivable and what has since been posted the other way:

    outstanding = sum(debit) - sum(credit)
                  on live ledger rows whose against_voucher is this invoice

The invoice itself posts the debit when it is raised. A receipt posts the
credit. A reversal posts its mirror. So the figure follows the books by
construction and cannot disagree with them -- which a stored running total
eventually does, after which nothing can tell you which of the two is right.

`outstanding_amount` on the document is a **cache of that figure**, refreshed
whenever something settles against it, because a list view and a chart need a
column to sort and sum. `check_cache` asserts the two agree, and an acceptance
check calls it. The ledger is the source; the field is a convenience.

**Signs.** A receivable is a debit balance and a payable is a credit one, so
`outstanding()` returns the amount still owed as a positive number in both
directions, and the caller does not have to know which way round the account
sits.

**What this module does not decide.** Whether a residue is worth writing off is
a person's judgement, so `write_off` exists but nothing calls it automatically.
DEC-022: "a residue within tolerance may be closed by explicit action only,
never automatically. Automatic write-offs are how small amounts of money leave
a business without anyone noticing."
"""

import frappe
from frappe.utils import flt

from knit360_core.business_status import engine, model
from knit360_core.finance import ledger

GL = "KNIT 360 GL Entry"
COMPANY = "KNIT 360 Company"

#: Outstanding is reported against these, and their status follows settlement.
#: doctype -> (the status when nothing is settled, partly, fully)
SETTLES = {
	"KNIT 360 Sales Invoice": ("Posted / Unpaid", "Partly Paid", "Paid"),
}

#: Below this, a difference is arithmetic rather than money. Matches the
#: ledger's own tolerance so the two never disagree about whether a thing is
#: settled.
TOLERANCE = ledger.TOLERANCE


def outstanding(doctype, name):
	"""What is still owed on one document, as a positive amount.

	Reads the ledger, not the document. A document with no postings at all is
	not outstanding -- it is a draft, and returns nil.
	"""
	row = frappe.db.sql(
		f"""SELECT COALESCE(SUM(debit), 0) AS debit, COALESCE(SUM(credit), 0) AS credit
		    FROM `tab{GL}`
		    WHERE against_voucher_type = %s AND against_voucher = %s AND is_cancelled = 0""",
		(doctype, name),
		as_dict=True,
	)[0]
	return abs(flt(row.debit) - flt(row.credit))


def settled(doctype, name):
	"""How much of this document has been settled so far."""
	total = flt(frappe.db.get_value(doctype, name, "grand_total"))
	return flt(total - outstanding(doctype, name))


def status_for(doctype, name):
	"""The business status settlement implies, or None if it implies nothing."""
	if doctype not in SETTLES:
		return None
	unpaid, partly, paid = SETTLES[doctype]
	left = outstanding(doctype, name)
	if left <= TOLERANCE:
		return paid
	if left < flt(frappe.db.get_value(doctype, name, "grand_total")) - TOLERANCE:
		return partly
	return unpaid


def refresh(doctype, name, move_status=True):
	"""Re-cache the outstanding figure and move the status to match.

	Called after anything settles against the document, and after that is
	reversed. The status move goes through the engine like every other, so an
	illegal one is refused here exactly as it would be from the Desk -- a
	payment cannot drag an invoice into a state its lifecycle forbids.
	"""
	left = outstanding(doctype, name)
	if frappe.get_meta(doctype).has_field("outstanding_amount"):
		frappe.db.set_value(doctype, name, "outstanding_amount", left, update_modified=False)

	if not move_status:
		return left

	wanted = status_for(doctype, name)
	if not wanted:
		return left

	current = frappe.db.get_value(doctype, name, model.FIELD)
	if current == wanted:
		return left

	lifecycle = model.for_doctype(doctype)
	if wanted not in lifecycle.transitions.get(current, set()):
		# Not an error. An invoice that was cancelled, or is sitting in an
		# approval state, is not dragged somewhere else because money arrived;
		# the figure is still correct and the person decides the status.
		return left

	engine.transition(doctype, name, wanted, reason="Settlement")
	return left


def check_cache(doctype=None):
	"""Every cached outstanding figure against the ledger behind it.

	A cache nobody checks is a cache that silently stops being true.
	"""
	wrong = {}
	for name in (SETTLES if doctype is None else [doctype]):
		if not frappe.get_meta(name).has_field("outstanding_amount"):
			continue
		for row in frappe.get_all(name, fields=["name", "outstanding_amount", "docstatus"]):
			if row.docstatus != 1:
				continue
			derived = outstanding(name, row.name)
			if abs(flt(row.outstanding_amount) - derived) > TOLERANCE:
				wrong[row.name] = f"cached {flt(row.outstanding_amount)}, ledger says {derived}"
	return wrong


# --- allocation ---------------------------------------------------------


def check_can_allocate(doctype, name, amount, ignore_payment=None):
	"""Refuse an allocation larger than the document still owes.

	Over-allocation is refused rather than capped, because capping silently
	changes a figure somebody typed. The surplus belongs on the payment as
	unallocated -- money held for that party -- not inflated onto an invoice.
	"""
	if not frappe.db.exists(doctype, name):
		frappe.throw(f"There is no {doctype.replace('KNIT 360 ', '')} called {name}.")

	if frappe.db.get_value(doctype, name, "docstatus") != 1:
		frappe.throw(
			f"{name} is not posted, so there is nothing to settle against it yet."
		)

	left = outstanding(doctype, name)
	# An allocation being re-saved should not be counted against itself.
	if ignore_payment:
		left += _allocated_by(ignore_payment, doctype, name)

	if flt(amount) <= 0:
		frappe.throw(f"An allocation of {flt(amount)} against {name} settles nothing.")

	if flt(amount) - left > TOLERANCE:
		frappe.throw(
			f"{name} has {left:.2f} outstanding and this allocates {flt(amount):.2f}. "
			f"Reduce it, or leave the surplus unallocated -- an overpayment is "
			f"money held for the party, not extra income on the invoice."
		)
	return left


def _allocated_by(payment, doctype, name):
	"""How much a given payment currently allocates to a given document."""
	return flt(
		frappe.db.sql(
			"""SELECT COALESCE(SUM(allocated_amount), 0)
			   FROM `tabKNIT 360 Payment Allocation`
			   WHERE parent = %s AND reference_doctype = %s AND reference_name = %s""",
			(payment, doctype, name),
		)[0][0]
	)


def payments_against(doctype, name):
	"""Every payment that has settled part of this document, for showing on it."""
	return frappe.db.sql(
		"""SELECT p.name, p.payment_date, p.payment_mode, a.allocated_amount
		   FROM `tabKNIT 360 Payment Allocation` a
		   JOIN `tabKNIT 360 Payment Entry` p ON p.name = a.parent
		   WHERE a.reference_doctype = %s AND a.reference_name = %s AND p.docstatus = 1
		   ORDER BY p.payment_date, p.name""",
		(doctype, name),
		as_dict=True,
	)


# --- writing off a residue ----------------------------------------------


@frappe.whitelist()
def write_off(doctype, name, reason=None):
	"""Close a residue too small to chase, to the round-off account.

	This is the one legitimate use of that account -- it exists for exactly
	this. Nothing calls it on its own: a person presses a button and the entry
	carries their name, because an automatic write-off is how small amounts of
	money leave a business unnoticed.
	"""
	left = outstanding(doctype, name)
	if left <= TOLERANCE:
		frappe.throw(f"{name} has nothing outstanding to write off.")

	company = frappe.db.get_value(doctype, name, "company")
	tolerance = flt(frappe.db.get_value(COMPANY, company, "write_off_tolerance"))
	if not tolerance:
		frappe.throw(
			f"{company} has no Write Off Tolerance set, so no residue can be "
			f"written off. Set one, or settle {name} in full."
		)
	if left > tolerance + TOLERANCE:
		frappe.throw(
			f"{name} has {left:.2f} outstanding, which is more than {company}'s "
			f"write-off tolerance of {tolerance:.2f}. A balance this size is "
			f"collected or credited, not written off."
		)

	accounts = frappe.db.get_value(
		COMPANY, company, ["round_off_account", "default_receivable_account"], as_dict=True
	)
	if not accounts.round_off_account:
		frappe.throw(f"{company} has no Round Off Account, so there is nowhere to post this.")

	invoice = frappe.get_doc(doctype, name)
	ledger.post(
		"KNIT 360 Write Off",
		name,
		company,
		frappe.utils.nowdate(),
		[
			ledger.Line(account=accounts.round_off_account, debit=left,
			            remarks=reason or f"Write off of {name}"),
			ledger.Line(
				account=invoice.get("debit_to") or accounts.default_receivable_account,
				credit=left,
				party_type="Customer",
				party=invoice.get("customer"),
				against_voucher_type=doctype,
				against_voucher=name,
			),
		],
		remarks=f"Write off: {reason or 'residue below tolerance'}",
	)
	refresh(doctype, name)
	return {"written_off": left, "outstanding": outstanding(doctype, name)}
