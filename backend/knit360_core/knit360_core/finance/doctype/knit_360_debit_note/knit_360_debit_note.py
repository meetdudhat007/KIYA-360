"""KNIT 360 Debit Note - FR-PROC-006 Returns / FR-FIN-002 Accounts Payable.

A purchase reduced, or sent back. The mirror of the credit note, and it exists
for the same reason: without it a supplier's bill that was wrong, or goods
that went back, left the payable standing at the full amount with no honest
way to reduce it.

**What it posts.**

    debit   the payable                the whole amount, against the bill
    credit  Purchase Returns           the net
    credit  Input Tax Credit           the tax reversed with it

The tax figure is **entered, not computed**, exactly as it is on the bill
itself: the supplier's own credit note states what tax they are reversing, and
that is the figure that belongs in our books.

**Naming the bill is what settles it.** The debit is posted against the bill,
so what we still owe falls and the bill's status follows. Left blank it is a
balance in our favour, to set against a later bill from the same supplier.

**Goods going back are a separate document**, for the same reason a credit
note does not move stock: a debit note for an overcharge involves no goods at
all. Stock leaving on a return is a Delivery Note, which since `DEC-031` no
longer needs a sales order.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.finance import ledger, settlement
from knit360_core.pricing import totals

COMPANY = "KNIT 360 Company"
SUPPLIER_INVOICE = "KNIT 360 Supplier Invoice"

SHAPE = totals.Shape(
	table="items",
	rate="rate",
	tax_total=None,
	tax_template=None,
	additions=("statutory_tax_amount",),
)


class KNIT360DebitNote(Document):
	def validate(self):
		if not self.items:
			frappe.throw("A debit note with no lines debits nothing.")
		for row in self.items:
			if flt(row.qty) <= 0 or flt(row.rate) < 0:
				frappe.throw(
					f"Line {row.idx}: a debit note states what is going back as a "
					f"positive quantity. The document's direction is what makes it "
					f"a debit."
				)
		if not totals.apply(self, SHAPE):
			frappe.throw("A debit note for nothing cannot be posted.")
		self._check_against_bill()
		self._resolve_payable()

	def _check_against_bill(self):
		if not self.supplier_invoice:
			return
		bill = frappe.db.get_value(
			SUPPLIER_INVOICE, self.supplier_invoice,
			["supplier", "docstatus"], as_dict=True,
		)
		if bill.supplier != self.supplier:
			frappe.throw(
				f"{self.supplier_invoice} came from {bill.supplier}, not "
				f"{self.supplier}. A debit note settles one supplier's bill."
			)
		if bill.docstatus != 1:
			frappe.throw(
				f"{self.supplier_invoice} is not posted, so there is nothing to "
				f"debit against it yet."
			)
		if self.docstatus == 0:
			settlement.check_can_allocate(
				SUPPLIER_INVOICE, self.supplier_invoice, self.grand_total
			)

	def _resolve_payable(self):
		if self.debit_to:
			return
		self.debit_to = (
			frappe.db.get_value(SUPPLIER_INVOICE, self.supplier_invoice, "credit_to")
			if self.supplier_invoice
			else None
		) or frappe.db.get_value(COMPANY, self.company, "default_payable_account")
		if not self.debit_to:
			frappe.throw(
				f"{self.company} has no Default Payable Account, so this debit has "
				f"nowhere to go."
			)

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		self._check_against_bill()
		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.posting_date or nowdate(),
			self._lines(),
			remarks=f"Debit to {self.supplier}: {self.reason}",
		)
		if self.supplier_invoice:
			settlement.refresh(SUPPLIER_INVOICE, self.supplier_invoice)

	def on_cancel(self):
		ledger.reverse(self.doctype, self.name)
		if self.supplier_invoice:
			settlement.refresh(SUPPLIER_INVOICE, self.supplier_invoice)

	def _lines(self):
		returns = frappe.db.get_value(COMPANY, self.company, "default_purchase_returns_account")
		if not returns:
			frappe.throw(
				f"{self.company} has no Default Purchase Returns Account, so what "
				f"went back has nowhere to go."
			)

		lines = [
			ledger.Line(
				account=self.debit_to,
				debit=flt(self.grand_total),
				party_type="Supplier",
				party=self.supplier,
				against_voucher_type=SUPPLIER_INVOICE if self.supplier_invoice else None,
				against_voucher=self.supplier_invoice or None,
			),
			ledger.Line(account=returns, credit=flt(self.net_total)),
		]

		tax = flt(self.statutory_tax_amount)
		if tax:
			account = frappe.db.get_value(COMPANY, self.company, "default_input_tax_account")
			if not account:
				frappe.throw(
					f"{self.company} has no Default Input Tax Account, so the "
					f"{tax:.2f} of tax being reversed has nowhere to go."
				)
			lines.append(
				ledger.Line(
					account=account,
					credit=tax,
					remarks=f"Tax reversed by {self.supplier}",
				)
			)
		return lines
