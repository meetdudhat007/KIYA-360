"""KNIT 360 Journal Entry - FR-FIN-001.

A manual double-entry posting: the escape hatch for anything the automated
documents do not cover -- opening balances, depreciation, write-offs, corrections.

The ledger effect is hung on Frappe's on_submit / on_cancel rather than on the
business status directly. The business status adapter reaches docstatus 1 by
calling doc.submit(), so on_submit fires exactly once, at the moment CD-002 says
the effect becomes real. Hanging it here rather than on the status means there
is one posting path, not two.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt

from knit360_core.finance import ledger


class KNIT360JournalEntry(Document):
	def validate(self):
		self.total_debit = flt(sum(flt(row.debit) for row in self.accounts))
		self.total_credit = flt(sum(flt(row.credit) for row in self.accounts))

		if abs(self.total_debit - self.total_credit) > ledger.TOLERANCE:
			frappe.throw(
				f"This entry does not balance: debits {self.total_debit:.2f} "
				f"against credits {self.total_credit:.2f}."
			)
		if not self.total_debit:
			frappe.throw("An entry with no amounts posts nothing.")

	def on_submit(self):
		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.posting_date,
			[
				ledger.Line(
					account=row.account,
					debit=row.debit,
					credit=row.credit,
					party_type=row.party_type,
					party=row.party,
					cost_center=row.cost_center,
					against_voucher_type=row.reference_type,
					against_voucher=row.reference_name,
				)
				for row in self.accounts
			],
			remarks=self.user_remark or self.entry_type,
		)

	def on_cancel(self):
		ledger.reverse(self.doctype, self.name)
