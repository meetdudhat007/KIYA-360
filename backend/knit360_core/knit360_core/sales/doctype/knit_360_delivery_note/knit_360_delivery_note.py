"""KNIT 360 Delivery Note - FR-SALES-005 / FR-INV-002.

DR-C2C-012 Dispatch and Delivery Note. Goods leave, so stock falls and the
cost of what left is charged to profit.

**What it posts.** Two things, in this order, because the second needs the
first's answer:

    stock   each line out of the shipping warehouse, at what it cost
    ledger  debit Cost of Goods Sold, credit Stock In Hand -- that same cost

The cost is **not** on this document and is never typed. It is what the stock
ledger says those units cost, worked out by FIFO over the receipts that
actually brought them in -- DEC-023. A dispatch is a quantity decision; what
it cost was settled when the goods were bought.

**Why it refuses to over-issue.** Stock is not allowed to go negative. The
alternative is books that claim goods nobody has, every later valuation wrong,
and nobody finding out until a count months later. Better a blocked delivery
note today.

This posts no revenue. The invoice does that, and the two are deliberately
separate: goods can leave before they are billed.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.finance import ledger
from knit360_core.stock import ledger as stock_ledger

COMPANY = "KNIT 360 Company"


class KNIT360DeliveryNote(Document):
	def validate(self):
		if not self.items:
			frappe.throw("A delivery note with no lines dispatches nothing.")
		for row in self.items:
			if flt(row.qty) <= 0:
				frappe.throw(f"Line {row.idx}: a dispatch of {flt(row.qty)} is not a dispatch.")
			if self.docstatus == 0:
				# Shown while it is still a draft, so somebody sees the refusal
				# in time to do something about it.
				stock_ledger.check_can_issue(
					row.item_code, self.source_warehouse, row.qty, self.company
				)

	def on_submit(self):
		movements = stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.delivery_note_date or nowdate(),
			[
				{
					"item_code": row.item_code,
					"warehouse": self.source_warehouse,
					"qty": -flt(row.qty),
					"remarks": f"Dispatched on {self.name}",
				}
				for row in self.items
			],
		)
		self._record_cost(movements)
		self._post_cost_of_sales()

	def on_cancel(self):
		stock_ledger.reverse(self.doctype, self.name)
		ledger.reverse(self.doctype, self.name)

	def _record_cost(self, movements):
		"""Copy what the ledger worked out back onto the lines, to be read.

		A figure shown on the document and a figure in the ledger must come
		from one place, so these are written from the movement rather than
		recomputed here.
		"""
		by_item = {}
		for name in movements:
			row = frappe.db.get_value(
				stock_ledger.SLE, name, ["item_code", "rate", "value_change"], as_dict=True
			)
			by_item[row.item_code] = row

		for line in self.items:
			move = by_item.get(line.item_code)
			if not move:
				continue
			line.db_set("valuation_rate", flt(move.rate), update_modified=False)
			line.db_set("stock_value", abs(flt(move.value_change)), update_modified=False)

	def _post_cost_of_sales(self):
		"""Charge what left to Cost of Goods Sold and take it off Stock In Hand."""
		cost = abs(
			flt(sum(flt(m.value_change) for m in
			        stock_ledger.voucher_movements(self.doctype, self.name)))
		)
		if cost <= stock_ledger.TOLERANCE:
			return

		accounts = frappe.db.get_value(
			COMPANY, self.company, ["default_cogs_account", "default_stock_account"], as_dict=True
		)
		if not accounts.default_cogs_account or not accounts.default_stock_account:
			frappe.throw(
				f"{self.company} has no Default Cost of Goods Sold Account or no "
				f"Default Stock Account, so the cost of this dispatch has nowhere "
				f"to go. Set them before dispatching."
			)

		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.delivery_note_date or nowdate(),
			[
				ledger.Line(account=accounts.default_cogs_account, debit=cost),
				ledger.Line(account=accounts.default_stock_account, credit=cost),
			],
			remarks=f"Cost of goods dispatched on {self.name}",
		)
