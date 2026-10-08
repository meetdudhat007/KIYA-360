"""KNIT 360 Credit Note - FR-SALES-006 Returns / FR-SALES-007 Credit Memos.

A sale reduced, or given back. Until this existed a return could be agreed and
never settled: the invoice went on showing the full amount owing, and the only
ways to close it were to cancel an invoice that had genuinely happened or to
write the difference off as a loss. Both are lies about the business.

**What it posts.**

    debit   Sales Returns              the net credited
    debit   the tax accounts           the tax given back with it
    credit  the receivable             the whole amount, against the invoice

Sales Returns is a separate account rather than a debit straight back to
Sales. Both leave the same profit, but one of them can answer "how much did we
take back this quarter?" and the other cannot.

**Naming the invoice is what settles it.** The credit is posted with
`against_voucher` pointing at the invoice, which is the same mechanism a
receipt uses, so the invoice's outstanding falls and its status follows
without this document knowing anything about settlement. Left blank, the
credit sits as a balance in the customer's favour -- a debt we owe them --
exactly as an unallocated receipt does.

**Goods coming back are a separate document.** This one moves money. If the
goods physically return they are received on a Goods Receipt, which is why
`DEC-031` stopped requiring a purchase order on one. Keeping them apart means
a credit for a price dispute, where nothing comes back, is not forced to
pretend stock moved.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.finance import ledger, settlement
from knit360_core.pricing import totals

COMPANY = "KNIT 360 Company"
SALES_INVOICE = "KNIT 360 Sales Invoice"

SHAPE = totals.Shape(table="items", rate="rate")


class KNIT360CreditNote(Document):
	def validate(self):
		if not self.items:
			frappe.throw("A credit note with no lines credits nothing.")
		for row in self.items:
			if flt(row.qty) <= 0 or flt(row.rate) < 0:
				frappe.throw(
					f"Line {row.idx}: a credit note states what is coming back as a "
					f"positive quantity. The document's direction is what makes it "
					f"a credit."
				)
		if not totals.apply(self, SHAPE):
			frappe.throw("A credit note for nothing cannot be posted.")
		self._check_against_invoice()
		self._resolve_receivable()

	def _check_against_invoice(self):
		"""A credit cannot exceed what the invoice still owes."""
		if not self.sales_invoice:
			return

		invoice = frappe.db.get_value(
			SALES_INVOICE, self.sales_invoice, ["customer", "company", "docstatus"], as_dict=True
		)
		if invoice.customer != self.customer:
			frappe.throw(
				f"{self.sales_invoice} was issued to {invoice.customer}, not "
				f"{self.customer}. A credit note settles one customer's invoice."
			)
		if invoice.docstatus != 1:
			frappe.throw(
				f"{self.sales_invoice} is not posted, so there is nothing to credit "
				f"against it yet."
			)
		if self.docstatus == 0:
			settlement.check_can_allocate(
				SALES_INVOICE, self.sales_invoice, self.grand_total
			)

	def _resolve_receivable(self):
		"""Credit the account the invoice debited, not today's default."""
		if self.credit_to:
			return
		self.credit_to = (
			frappe.db.get_value(SALES_INVOICE, self.sales_invoice, "debit_to")
			if self.sales_invoice
			else None
		) or frappe.db.get_value(COMPANY, self.company, "default_receivable_account")
		if not self.credit_to:
			frappe.throw(
				f"{self.company} has no Default Receivable Account, so this credit "
				f"has nowhere to go."
			)

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		# Re-checked at posting: another credit note may have been raised
		# against the same invoice since this one was saved.
		self._check_against_invoice()
		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.posting_date or nowdate(),
			self._lines(),
			remarks=f"Credit to {self.customer}: {self.reason}",
		)
		if self.sales_invoice:
			settlement.refresh(SALES_INVOICE, self.sales_invoice)

	def on_cancel(self):
		ledger.reverse(self.doctype, self.name)
		if self.sales_invoice:
			settlement.refresh(SALES_INVOICE, self.sales_invoice)

	def _lines(self):
		returns = frappe.db.get_value(COMPANY, self.company, "default_sales_returns_account")
		if not returns:
			frappe.throw(
				f"{self.company} has no Default Sales Returns Account, so what was "
				f"given back has nowhere to go. Crediting it straight to Sales "
				f"would leave no way to say how much was returned."
			)

		lines = [
			ledger.Line(
				account=self.credit_to,
				credit=flt(self.grand_total),
				party_type="Customer",
				party=self.customer,
				# This is what makes the invoice's outstanding fall.
				against_voucher_type=SALES_INVOICE if self.sales_invoice else None,
				against_voucher=self.sales_invoice or None,
			),
			ledger.Line(account=returns, debit=flt(self.net_total)),
		]
		lines += self._tax_lines()
		return lines

	def _tax_lines(self):
		"""Tax charged on the sale is given back with it -- DEC-021."""
		if not flt(self.total_taxes):
			return []
		fallback = frappe.db.get_value(COMPANY, self.company, "default_output_tax_account")
		lines = []
		for tax in totals.tax_lines(self.net_total, self.tax_template):
			if not flt(tax.amount):
				continue
			account = tax.account or fallback
			if not account:
				frappe.throw(
					f"{tax.component} of {tax.amount:.2f} has no account to take "
					f"back from. Name one on the tax template row, or set a Default "
					f"Output Tax Account on {self.company}."
				)
			lines.append(
				ledger.Line(
					account=account,
					debit=tax.amount,
					remarks=f"{tax.component} at {tax.rate}% given back",
				)
			)
		return lines
