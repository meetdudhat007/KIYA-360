"""KNIT 360 Goods Receipt - FR-PROC-005 / FR-WH-001 / FR-INV-002.

DR-P2P-006 Goods Receipt and Inward Gate Entry. Goods arrive, so stock rises
and the value of them is held until the supplier's bill turns up.

**What it posts.**

    stock   accepted quantity into the receiving warehouse, at the line rate
    ledger  debit Stock In Hand, credit Stock Received But Not Billed

That second account is the one worth explaining: the goods are ours the moment
we accept them, and we owe for them, but no bill has arrived to say exactly
how much. So the value sits in a liability of its own rather than being
guessed at in Creditors. The supplier's invoice clears it later, which is `W7`
and is not built -- so for now the balance simply accumulates, visibly.

**Accepted, not arrived.** What enters stock is the quantity that arrived less
the quantity rejected at arrival. Goods turned away at the gate never became
ours and never enter the ledger. A receipt driven straight to "Rejected at
Gate" posts nothing at all, which is why this controller reads where the
status is going rather than only that it submitted.

**The rate is required.** Stock received at nil cannot be valued, and every
later issue of it would be costed wrongly -- so it is refused rather than
accepted and quietly worth nothing.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.finance import ledger
from knit360_core.stock import ledger as stock_ledger

COMPANY = "KNIT 360 Company"

#: Reaching this status means nothing was taken in.
REJECTED = "Rejected at Gate"


class KNIT360GoodsReceipt(Document):
	def validate(self):
		if not self.items:
			frappe.throw("A goods receipt with no lines receives nothing.")
		for row in self.items:
			arrived = flt(row.qty_arrived)
			rejected = flt(row.qty_rejected_on_arrival)
			if arrived <= 0:
				frappe.throw(f"Line {row.idx}: nothing arrived, so there is nothing to receive.")
			if rejected < 0 or rejected - arrived > stock_ledger.TOLERANCE:
				frappe.throw(
					f"Line {row.idx}: {rejected:g} rejected out of {arrived:g} that "
					f"arrived. More cannot be turned away than turned up."
				)
			row.accepted_qty = flt(arrived - rejected)

	def on_submit(self):
		# Both "Received in Bay" and "Rejected at Gate" submit from the same
		# draft state, so the flag is how this tells them apart. See
		# business_status/engine.py.
		if self.flags.get("knit360_to_status") == REJECTED:
			return

		accepted = [row for row in self.items if flt(row.accepted_qty) > 0]
		if not accepted:
			frappe.throw(
				f"{self.name}: every line was rejected on arrival, so nothing can "
				f"be put away. Move it to '{REJECTED}' instead."
			)

		stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.challan_date or nowdate(),
			[
				{
					"item_code": row.item_code,
					"warehouse": self.receiving_warehouse,
					"qty": flt(row.accepted_qty),
					"rate": flt(row.rate),
					"remarks": f"Received on {self.name}",
				}
				for row in accepted
			],
		)
		self._post_stock_value()

	def on_cancel(self):
		stock_ledger.reverse(self.doctype, self.name)
		ledger.reverse(self.doctype, self.name)

	def _post_stock_value(self):
		value = flt(
			sum(flt(m.value_change) for m in
			    stock_ledger.voucher_movements(self.doctype, self.name))
		)
		if value <= stock_ledger.TOLERANCE:
			return

		accounts = frappe.db.get_value(
			COMPANY, self.company,
			["default_stock_account", "stock_received_but_not_billed"], as_dict=True,
		)
		if not accounts.default_stock_account or not accounts.stock_received_but_not_billed:
			frappe.throw(
				f"{self.company} has no Default Stock Account or no Stock Received "
				f"But Not Billed account, so the value of these goods has nowhere "
				f"to go. Set them before receiving."
			)

		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.challan_date or nowdate(),
			[
				ledger.Line(account=accounts.default_stock_account, debit=value),
				ledger.Line(account=accounts.stock_received_but_not_billed, credit=value),
			],
			remarks=f"Goods received on {self.name}, supplier bill not yet arrived",
		)
