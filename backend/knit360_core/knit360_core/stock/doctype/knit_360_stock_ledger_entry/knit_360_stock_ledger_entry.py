"""KNIT 360 Stock Ledger Entry - FR-INV-002 / FR-INV-006.

A movement, not a document. It is written once and never changes, for the same
reason a GL entry is: the record of what the stock once was is part of the
stock record. A document that moved stock wrongly is reversed, which writes the
mirror movement and flags both.

knit360_core.stock.ledger is the only thing that should create these. The
guards below are what makes "should" into "does".
"""

import frappe
from frappe.model.document import Document

#: The fields that make a movement what it was. is_cancelled is deliberately
#: absent: flagging a reversal is the one permitted change.
IMMUTABLE = ("item_code", "warehouse", "company", "posting_date",
             "actual_qty", "rate", "value_change", "voucher_type", "voucher_no")


class KNIT360StockLedgerEntry(Document):
	def validate(self):
		before = self.get_doc_before_save()
		if before and any(before.get(f) != self.get(f) for f in IMMUTABLE):
			frappe.throw(
				f"{self.doctype} {self.name} has already been posted. Reverse the "
				f"document that made it instead of editing it -- FR-INV-002."
			)

	def on_trash(self):
		frappe.throw(
			f"{self.doctype} {self.name} cannot be deleted. The stock ledger keeps "
			f"what the stock once was; reverse the voucher instead."
		)
