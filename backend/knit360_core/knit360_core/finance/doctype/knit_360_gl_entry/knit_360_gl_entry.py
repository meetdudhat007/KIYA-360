"""KNIT 360 GL Entry - FR-FIN-001.

A ledger row, not a business document. It carries no business status, because
it has no lifecycle: it is written once and never changes. CD-002's rule that a
posted effect is reversed rather than rewritten is enforced here at its
narrowest point.

knit360_core.finance.ledger is the only thing that should create these. The
guards below are what makes "should" into "does".
"""

import frappe
from frappe.model.document import Document


class KNIT360GLEntry(Document):
	def validate(self):
		if self.debit and self.credit:
			frappe.throw("A ledger entry is a debit or a credit, not both.")
		if not self.debit and not self.credit:
			frappe.throw("A ledger entry with no amount records nothing.")

		before = self.get_doc_before_save()
		if before and _financials_changed(before, self):
			frappe.throw(
				f"{self.doctype} {self.name} is already posted. "
				f"Reverse it instead of editing it -- FR-FIN-001."
			)

	def on_trash(self):
		frappe.throw(
			f"{self.doctype} {self.name} cannot be deleted. "
			f"The ledger keeps what the books once said; reverse the voucher instead."
		)


#: The fields that make an entry what it is. is_cancelled is deliberately absent:
#: flagging a reversal is the one permitted change.
IMMUTABLE = ("posting_date", "account", "debit", "credit", "company",
             "party_type", "party", "voucher_type", "voucher_no")


def _financials_changed(before, after):
	return any(before.get(field) != after.get(field) for field in IMMUTABLE)
