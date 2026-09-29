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

Taxes are read from the KNIT 360 Tax Template as a percentage of net. The
template carries no account of its own yet, so the tax total is credited to the
company's round-off account and flagged in the remarks. That is a placeholder,
and FR-TAX-001 will replace it once the tax masters exist; it is recorded rather
than hidden because a placeholder you can see is safer than one you cannot.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt

from knit360_core.finance import ledger

COMPANY = "KNIT 360 Company"


class KNIT360SalesInvoice(Document):
	def validate(self):
		self._compute_totals()
		self._resolve_defaults()

	def _compute_totals(self):
		for row in self.items:
			row.amount = flt(row.qty) * flt(row.rate)
		self.net_total = flt(sum(flt(row.amount) for row in self.items))
		self.total_taxes = self._tax_total()
		self.grand_total = flt(self.net_total + self.total_taxes)

		if not self.grand_total:
			frappe.throw("An invoice for nothing cannot be posted.")

		# Only reset the outstanding while the invoice is still a draft. Once
		# posted it is driven by what has been settled against it.
		if self.docstatus == 0:
			self.outstanding_amount = self.grand_total

	def _tax_total(self):
		if not self.tax_template:
			return 0.0
		rows = frappe.get_all(
			"KNIT 360 Tax Template Row",
			filters={"parent": self.tax_template},
			fields=["rate"],
		)
		return flt(sum(flt(self.net_total) * flt(row.rate) / 100.0 for row in rows))

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
		if flt(self.total_taxes):
			tax_account = frappe.db.get_value(COMPANY, self.company, "round_off_account")
			if not tax_account:
				frappe.throw(
					f"This invoice carries {self.total_taxes:.2f} in tax, but {self.company} "
					f"has no account to post it to. FR-TAX-001 tax masters are not built yet; "
					f"set a Round Off Account, or clear the tax template."
				)
			lines.append(
				ledger.Line(
					account=tax_account,
					credit=self.total_taxes,
					remarks="Tax placeholder pending FR-TAX-001 tax accounts",
				)
			)
		return lines
