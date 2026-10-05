"""KNIT 360 Sales Invoice - FR-FIN-003.

The document that turns a delivery into a receivable. Its posting is the
canonical one:

    debit   the receivable account        grand total
    credit  each line's income account    line amount
    credit  tax accounts                  tax amount

Accounts are resolved in one place, _resolve_defaults, and always from the
company. An invoice that cannot name the account it debits is not posted with a
guess -- it is refused, because a wrong account is harder to find later than a
blocked invoice is now.

Taxes are read from the KNIT 360 Tax Template as a percentage of net, and
credited **one line per component** -- DEC-021. Tax charged to a customer is not
income: it is money held on behalf of the tax authority until it is paid over,
so it is credited to a liability. Each component posts to the account its
template row names, or to the company's Default Output Tax Account. An invoice
that carries tax and can resolve neither is refused rather than posted
somewhere plausible, for the same reason the receivable is.

Until DEC-021 this credited the round-off account as a visible placeholder. It
no longer does, and an acceptance check asserts that the round-off account takes
no tax.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt

from knit360_core.finance import ledger
from knit360_core.pricing import totals

COMPANY = "KNIT 360 Company"

SHAPE = totals.Shape(table="items", rate="rate")


class KNIT360SalesInvoice(Document):
	def validate(self):
		self._compute_totals()
		self._resolve_defaults()

	def _compute_totals(self):
		# Shared with Quotation and Sales Order, so an invoice raised from an
		# order cannot total differently from the order it bills.
		if not totals.apply(self, SHAPE):
			frappe.throw("An invoice for nothing cannot be posted.")

		# Only reset the outstanding while the invoice is still a draft. Once
		# posted it is driven by what has been settled against it.
		if self.docstatus == 0:
			self.outstanding_amount = self.grand_total

	def _resolve_defaults(self):
		defaults = frappe.db.get_value(
			COMPANY,
			self.company,
			["default_receivable_account", "default_income_account", "default_cost_center"],
			as_dict=True,
		) or frappe._dict()

		if not self.debit_to:
			self.debit_to = defaults.default_receivable_account
		if not self.debit_to:
			frappe.throw(
				f"{self.company} has no Default Receivable Account, and this invoice "
				f"names none. Set one before posting."
			)

		for row in self.items:
			if not row.income_account:
				row.income_account = defaults.default_income_account
			if not row.income_account:
				frappe.throw(
					f"Line {row.idx} ({row.item_code or 'unnamed'}) has no income account, "
					f"and {self.company} has no Default Income Account."
				)
			if not row.cost_center:
				row.cost_center = defaults.default_cost_center

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.posting_date,
			self._lines(),
			remarks=f"Sales Invoice to {self.customer}",
		)

	def on_cancel(self):
		ledger.reverse(self.doctype, self.name)

	def _lines(self):
		lines = [
			ledger.Line(
				account=self.debit_to,
				debit=self.grand_total,
				party_type="Customer",
				party=self.customer,
				against_voucher_type=self.doctype,
				against_voucher=self.name,
			)
		]
		lines += [
			ledger.Line(account=row.income_account, credit=row.amount, cost_center=row.cost_center)
			for row in self.items
			if flt(row.amount)
		]
		lines += self._tax_lines()
		return lines

	def _tax_lines(self):
		"""One credit per tax component, to the account that component names.

		The components are recomputed from the same template and net total that
		produced the stored tax figure, so the sum of these lines is that
		figure and the entry balances by construction.
		"""
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
					f"{tax.component} of {tax.amount:.2f} has no account to post to. "
					f"Name one on the tax template row, or set a Default Output Tax "
					f"Account on {self.company}."
				)
			lines.append(
				ledger.Line(
					account=account,
					credit=tax.amount,
					remarks=f"{tax.component} at {tax.rate}%",
				)
			)
		return lines
