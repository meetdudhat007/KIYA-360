"""KNIT 360 Supplier Invoice - FR-PROC-006 / FR-FIN-002.

DR-P2P-009 Supplier Invoice & 3-Way Matching. Approval creates the payable.

**What the total is, and why -- DEC-020.** A supplier's bill shows the goods,
then freight and ancillary charges, then statutory tax. The amount payable is
all of it, because that is the amount that leaves the bank. So:

    net total     = sum of the billed lines
    grand total   = net total + freight and ancillary + statutory tax

The statutory tax figure stays **entered, not computed**. On a sales invoice the
tax is ours to calculate; on a supplier's invoice it is printed on their
document, and the figure that belongs in our books is the one they billed. The
tax template on this document records the treatment; it does not overwrite the
supplier's number.

**What it posts -- DEC-033.** On reaching Matched & Approved:

    credit  Creditors                       the whole amount payable
    debit   Stock Received But Not Billed   what the named receipt put there
    debit   the difference, if any          to the expense account
    debit   Input Tax Credit                the supplier's tax figure
    debit   Freight and Forwarding          the freight and ancillary charges

The **Stock Received But Not Billed** line is the one that matters. A goods
receipt credits that account because the goods are ours and we owe for them,
but nothing has yet said how much. This bill says how much, so it clears
exactly what that receipt put there -- read back from the ledger, not
recomputed -- and whatever the bill came to beyond that is a price difference
and goes to the expense account where somebody will see it. The account
therefore nets to nil per receipt, which is what makes a non-nil balance on it
mean something: goods received and not yet billed.

A bill that names no receipt is a bill for something that never passed through
stock -- a service, a subscription, a repair -- so its lines are an expense
directly.

**Where freight lands is DEC-033, and it is a deliberate departure.** Ind AS 2
paragraph 11 includes transport in the cost of purchase. Capitalising it would
mean apportioning it across the lines and revaluing stock that the FIFO layers
have already costed and in part already sold -- a landed-cost revaluation,
which is not built. Writing the figure into stock value without it would make
the stock ledger and the accounts disagree, and they agree today with a check
that proves it. So freight is expensed, the understatement is bounded by the
freight on goods still unsold, and landed cost is recorded as `W13`.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.finance import ledger, settlement
from knit360_core.pricing import totals

COMPANY = "KNIT 360 Company"

#: No tax template and no computed tax total: see the note above.
SHAPE = totals.Shape(
	table="items",
	rate="rate",
	tax_total=None,
	tax_template=None,
	additions=("freight_and_ancillary", "statutory_tax_amount"),
)

#: The account a goods receipt credits, and that this bill clears.
RECEIVED_NOT_BILLED = "stock_received_but_not_billed"


class KNIT360SupplierInvoice(Document):
	def validate(self):
		totals.apply(self, SHAPE)
		self._resolve_payable()
		if self.docstatus == 0:
			self.outstanding_amount = flt(self.grand_total)

	def _resolve_payable(self):
		"""Fix the payable account on the bill while it is still a draft.

		Stored rather than looked up at payment time, so that changing the
		company default later cannot move a debt that is already on the books.
		"""
		if self.credit_to:
			return
		self.credit_to = frappe.db.get_value(
			COMPANY, self.company, "default_payable_account"
		)
		if not self.credit_to:
			frappe.throw(
				f"{self.company} has no Default Payable Account, so this bill has "
				f"nowhere to create the debt. Set one before approving bills."
			)

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		if not flt(self.grand_total):
			frappe.throw("A bill for nothing creates no payable.")
		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.bill_date or nowdate(),
			self._lines(),
			remarks=f"Bill {self.bill_no or self.name} from {self.supplier}",
		)
		settlement.refresh(self.doctype, self.name, move_status=False)

	def on_cancel(self):
		ledger.reverse(self.doctype, self.name)
		settlement.refresh(self.doctype, self.name, move_status=False)

	def _lines(self):
		lines = [
			ledger.Line(
				account=self.credit_to,
				credit=flt(self.grand_total),
				party_type="Supplier",
				party=self.supplier,
				against_voucher_type=self.doctype,
				against_voucher=self.name,
			)
		]
		lines += self._goods_lines()
		lines += self._tax_line()
		lines += self._freight_line()
		return lines

	def _goods_lines(self):
		"""The billed lines: clearing a receipt, or an expense outright."""
		net = flt(self.net_total)
		if not net:
			return []

		expense = frappe.db.get_value(COMPANY, self.company, "default_expense_account")
		if not self.goods_receipt:
			if not expense:
				frappe.throw(
					f"{self.company} has no Default Expense Account, so the "
					f"{net:.2f} on this bill has nowhere to go."
				)
			return [
				ledger.Line(
					account=expense,
					debit=net,
					remarks="Billed without a goods receipt, so expensed directly",
				)
			]

		held = self._awaiting_bill()
		lines = []
		if held > settlement.TOLERANCE:
			lines.append(
				ledger.Line(
					account=frappe.db.get_value(COMPANY, self.company, RECEIVED_NOT_BILLED),
					debit=held,
					remarks=f"Clears what {self.goods_receipt} received and did not bill",
				)
			)

		difference = flt(net - held)
		if abs(difference) > settlement.TOLERANCE:
			if not expense:
				frappe.throw(
					f"This bill differs from {self.goods_receipt} by "
					f"{difference:.2f} and {self.company} has no Default Expense "
					f"Account for the difference."
				)
			lines.append(
				ledger.Line(
					account=expense,
					debit=difference if difference > 0 else 0,
					credit=0 if difference > 0 else abs(difference),
					remarks=f"Billed {net:.2f} against {held:.2f} received on "
					        f"{self.goods_receipt}",
				)
			)
		return lines

	def _awaiting_bill(self):
		"""What the named receipt put into Stock Received But Not Billed.

		Read back from the ledger rather than recomputed from the receipt's
		own lines, so this clears what was actually posted. A receipt whose
		value was already cleared by another bill leaves nothing here, and
		this bill becomes an expense difference instead of double-clearing.
		"""
		account = frappe.db.get_value(COMPANY, self.company, RECEIVED_NOT_BILLED)
		if not account:
			frappe.throw(
				f"{self.company} has no Stock Received But Not Billed account, so "
				f"what {self.goods_receipt} received cannot be cleared."
			)
		row = frappe.db.sql(
			f"""SELECT COALESCE(SUM(credit), 0) AS credit, COALESCE(SUM(debit), 0) AS debit
			    FROM `tab{ledger.GL}`
			    WHERE account = %s AND company = %s AND is_cancelled = 0
			      AND ((voucher_type = %s AND voucher_no = %s)
			           OR (against_voucher_type = %s AND against_voucher = %s))""",
			(account, self.company, "KNIT 360 Goods Receipt", self.goods_receipt,
			 "KNIT 360 Goods Receipt", self.goods_receipt),
			as_dict=True,
		)[0]
		return flt(flt(row.credit) - flt(row.debit))

	def _tax_line(self):
		"""The supplier's own tax figure, to an asset -- DEC-021.

		Tax paid to a supplier is recoverable, so it is an asset and not an
		expense. The figure is theirs; it is posted, not recalculated.
		"""
		tax = flt(self.statutory_tax_amount)
		if not tax:
			return []
		account = frappe.db.get_value(COMPANY, self.company, "default_input_tax_account")
		if not account:
			frappe.throw(
				f"{self.company} has no Default Input Tax Account, so the "
				f"{tax:.2f} of tax on this bill has nowhere to go. Recoverable tax "
				f"is an asset; it must not be buried in an expense."
			)
		return [
			ledger.Line(
				account=account,
				debit=tax,
				remarks=f"Tax billed by {self.supplier} on {self.bill_no or self.name}",
			)
		]

	def _freight_line(self):
		"""Freight and ancillary charges, expensed -- DEC-033."""
		freight = flt(self.freight_and_ancillary)
		if not freight:
			return []
		account = frappe.db.get_value(COMPANY, self.company, "default_freight_account")
		if not account:
			frappe.throw(
				f"{self.company} has no Default Freight Account, so the "
				f"{freight:.2f} of freight on this bill has nowhere to go."
			)
		return [
			ledger.Line(
				account=account,
				debit=freight,
				remarks=f"Freight and ancillary on {self.bill_no or self.name}",
			)
		]
