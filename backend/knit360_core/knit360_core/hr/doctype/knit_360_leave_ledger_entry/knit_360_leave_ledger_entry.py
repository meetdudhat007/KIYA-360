"""KNIT 360 Leave Ledger Entry - FR-HR-003.

One movement of one leave balance. The same contract as KNIT 360 GL Entry and
for the same reason: a balance derived from a ledger is only trustworthy if the
ledger cannot be quietly rewritten.

Written only by knit360_core.hr.leave_ledger. A structural test enforces that.
"""

import frappe
from frappe.model.document import Document

#: The fields that make an entry what it is. is_cancelled is deliberately
#: absent: flagging a reversal is the one permitted change.
IMMUTABLE = ("employee", "leave_type", "company", "posting_date", "leaves",
             "from_date", "to_date", "voucher_type", "voucher_no")


class KNIT360LeaveLedgerEntry(Document):
	def on_update(self):
		if self.is_new():
			return
		before = self.get_doc_before_save()
		if not before:
			return
		for field in IMMUTABLE:
			if self.get(field) != before.get(field):
				frappe.throw(
					f"{self.doctype} {self.name} is already posted. "
					f"Reverse the document that created it instead of editing it "
					f"-- FR-HR-003."
				)

	def on_trash(self):
		frappe.throw(
			f"{self.doctype} {self.name} cannot be deleted. "
			f"The ledger keeps what the balance was once made of; reverse the "
			f"document instead."
		)
