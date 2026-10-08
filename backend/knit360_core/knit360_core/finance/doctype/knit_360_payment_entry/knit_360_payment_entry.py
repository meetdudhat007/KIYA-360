"""KNIT 360 Payment Entry - FR-FIN-002 / FR-FIN-004.

DR-P2P-011 payment disbursement and DR-A2S-010 customer collection. One record
with a direction, because both carry the same inputs.

**The posting.** A receipt from a customer:

    debit   the bank or cash account        the whole amount
    credit  the receivable, per allocation  against each invoice settled
    credit  the receivable, unallocated     whatever is left over

A payment to a supplier is the same entry the other way round. The unallocated
line is the part worth explaining: money that arrived without an invoice to
match, or more than the invoices came to, is **an advance held for that party**.
It sits as a credit on the receivable -- a debt to them -- and is applied to a
later invoice. It is not income, and it never inflates an invoice.

**What is refused, and why refusal rather than adjustment.** Allocating more
than a document still owes is refused outright. Capping it silently would
change a figure somebody typed, and the surplus has a correct home already.
Allocating more in total than the payment is worth is refused for the same
reason.

**Settlement rules are DEC-022**, taken by the owner on 6 October 2026 after the
BRD named Payment Entry without defining settlement. Outstanding is derived
from the ledger, never stored as the truth -- see finance/settlement.py.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt

from knit360_core.finance import ledger, settlement

COMPANY = "KNIT 360 Company"
ACCOUNT = "KNIT 360 Account"

#: Which company account each direction settles against, and the party side.
#: ("Receive") a customer owes us, so the balance sits on the receivable.
DIRECTIONS = {
	"Receive": {"account": "default_receivable_account", "party_type": "Customer"},
	"Pay": {"account": "default_payable_account", "party_type": "Supplier"},
}


class KNIT360PaymentEntry(Document):
	def validate(self):
		self._check_direction()
		self._check_bank_account()
		self._check_allocations()
		self._total()

	# --- validation -----------------------------------------------------

	def _check_direction(self):
		if self.payment_direction not in DIRECTIONS:
			frappe.throw(
				f"'{self.payment_direction}' is not a direction. A payment is "
				f"either Received or Paid."
			)
		expected = f"KNIT 360 {DIRECTIONS[self.payment_direction]['party_type']}"
		if self.party_type != expected:
			frappe.throw(
				f"A payment you {self.payment_direction.lower()} settles with a "
				f"{DIRECTIONS[self.payment_direction]['party_type']}, but the party "
				f"type is {self.party_type.replace('KNIT 360 ', '')}."
			)
		if flt(self.amount) <= 0:
			frappe.throw("A payment of nothing settles nothing.")

		if flt(self.early_payment_discount):
			# The field exists and the arithmetic is easy; where the discount
			# posts is not decided. Refused rather than posted somewhere
			# plausible, for the same reason tax is. Raised as OQ-027.
			frappe.throw(
				"An early payment discount cannot be posted yet: no account is "
				"configured for it, and putting it somewhere plausible is how a "
				"profit figure goes quietly wrong. Clear the field, or raise the "
				"discount as a credit note."
			)

	def _check_bank_account(self):
		account_type, company = frappe.db.get_value(
			ACCOUNT, self.bank_account, ["account_type", "company"]
		) or (None, None)
		if company != self.company:
			frappe.throw(
				f"{self.bank_account} does not belong to {self.company}. A payment "
				f"cannot move money through another company's books."
			)
		if account_type not in ("Bank", "Cash"):
			frappe.throw(
				f"{self.bank_account} is a {account_type or 'general'} account. "
				f"Money moves through a Bank or Cash account."
			)

	def _check_allocations(self):
		seen = set()
		for row in self.allocations or []:
			key = (row.reference_doctype, row.reference_name)
			if key in seen:
				frappe.throw(
					f"Line {row.idx}: {row.reference_name} is allocated twice on "
					f"this payment. Put the whole amount on one line."
				)
			seen.add(key)

			party = frappe.db.get_value(
				row.reference_doctype, row.reference_name,
				"customer" if self.payment_direction == "Receive" else "supplier",
			)
			if party and party != self.party:
				frappe.throw(
					f"Line {row.idx}: {row.reference_name} belongs to {party}, not "
					f"{self.party}. A payment settles one party's documents."
				)

			row.outstanding_amount = settlement.check_can_allocate(
				row.reference_doctype,
				row.reference_name,
				row.allocated_amount,
				ignore_payment=self.name if not self.is_new() else None,
			)

	def _total(self):
		allocated = flt(sum(flt(row.allocated_amount) for row in self.allocations or []))
		if allocated - flt(self.amount) > settlement.TOLERANCE:
			frappe.throw(
				f"This payment is {flt(self.amount):.2f} but {allocated:.2f} has been "
				f"allocated. A payment cannot settle more than it is worth."
			)
		self.allocated_total = allocated
		self.unallocated_amount = flt(flt(self.amount) - allocated)

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		# Re-checked here: another payment may have settled these documents
		# between this one being saved and being posted.
		self._check_allocations()
		self._total()

		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.payment_date,
			self._lines(),
			remarks=f"{self.payment_direction} {self.party}",
		)
		self._refresh_settled()

	def on_cancel(self):
		ledger.reverse(self.doctype, self.name)
		self._refresh_settled()

	def _refresh_settled(self):
		"""Re-derive each settled document's outstanding, and move its status."""
		for row in self.allocations or []:
			settlement.refresh(row.reference_doctype, row.reference_name)

	def _lines(self):
		rule = DIRECTIONS[self.payment_direction]
		receiving = self.payment_direction == "Receive"

		default_account = frappe.db.get_value(COMPANY, self.company, rule["account"])
		party_name = self.party

		bank = ledger.Line(
			account=self.bank_account,
			debit=flt(self.amount) if receiving else 0,
			credit=0 if receiving else flt(self.amount),
			remarks=f"{self.payment_mode or 'Payment'} {self.name}",
		)
		lines = [bank]

		for row in self.allocations or []:
			# Post against the account the document itself used, so a payment
			# lands exactly where the invoice put the debt.
			# A sales invoice names the account it debited; a supplier's bill
			# names the one it credited. Either way the payment lands where
			# the document actually put the debt, not where the company
			# default happens to point today.
			held_on = "debit_to" if receiving else "credit_to"
			account = (
				frappe.db.get_value(row.reference_doctype, row.reference_name, held_on)
				if frappe.get_meta(row.reference_doctype).has_field(held_on)
				else None
			) or default_account
			if not account:
				frappe.throw(
					f"Line {row.idx}: {self.company} has no "
					f"{rule['account'].replace('_', ' ')}, and {row.reference_name} "
					f"names none."
				)
			lines.append(
				ledger.Line(
					account=account,
					debit=0 if receiving else flt(row.allocated_amount),
					credit=flt(row.allocated_amount) if receiving else 0,
					party_type=rule["party_type"],
					party=party_name,
					against_voucher_type=row.reference_doctype,
					against_voucher=row.reference_name,
				)
			)

		if flt(self.unallocated_amount) > settlement.TOLERANCE:
			if not default_account:
				frappe.throw(
					f"{flt(self.unallocated_amount):.2f} of this payment is "
					f"unallocated, but {self.company} has no "
					f"{rule['account'].replace('_', ' ')} to hold it against."
				)
			lines.append(
				ledger.Line(
					account=default_account,
					debit=0 if receiving else flt(self.unallocated_amount),
					credit=flt(self.unallocated_amount) if receiving else 0,
					party_type=rule["party_type"],
					party=party_name,
					# No against_voucher on purpose: this is held for the party,
					# not settled against anything yet.
					remarks="Advance held for the party, not allocated to a document",
				)
			)
		return lines
