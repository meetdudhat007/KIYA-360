"""KNIT 360 Account - FR-FIN-001.

The chart of accounts, as a tree. Frappe's NestedSet maintains lft/rgt, which
is what makes "the balance of Current Assets" answerable as one range query
rather than a recursive walk.

Account names are qualified with the company abbreviation because two companies
on one site both need an account called Debtors, and Frappe document names are
unique per doctype, not per company.
"""

import frappe
from frappe.utils.nestedset import NestedSet

#: Which side of a leaf account is its natural balance. Used to warn on a
#: balance that has gone the wrong way, not to forbid it -- a bank account can
#: legitimately be overdrawn.
NATURAL_SIDE = {
	"Asset": "Debit",
	"Expense": "Debit",
	"Liability": "Credit",
	"Income": "Credit",
	"Equity": "Credit",
}


class KNIT360Account(NestedSet):
	nsm_parent_field = "parent_account"

	def autoname(self):
		abbr = frappe.db.get_value("KNIT 360 Company", self.company, "abbreviation") or self.company
		parts = [p for p in (self.account_number, self.account_name) if p]
		self.name = f"{' - '.join(parts)} - {abbr}"

	def validate(self):
		self.inherit_from_parent()
		self.forbid_postings_to_a_parent()

	def inherit_from_parent(self):
		"""root_type is a property of where the account sits, not a free choice."""
		if not self.parent_account:
			if not self.root_type:
				frappe.throw("A root account must declare its root type.")
			return

		parent = frappe.db.get_value(
			"KNIT 360 Account", self.parent_account, ["root_type", "is_group", "company"], as_dict=True
		)
		if not parent.is_group:
			frappe.throw(
				f"{self.parent_account} is not a group account, so it cannot hold children."
			)
		if parent.company != self.company:
			frappe.throw(
				f"{self.parent_account} belongs to {parent.company}. "
				f"An account cannot sit under another company's chart."
			)
		if self.root_type and self.root_type != parent.root_type:
			frappe.throw(
				f"{self.account_name} is {self.root_type} but sits under a "
				f"{parent.root_type} parent. Move it, or correct the root type."
			)
		self.root_type = parent.root_type

	def forbid_postings_to_a_parent(self):
		"""A group's balance is the sum of its children, so it must have none of
		its own."""
		if not self.is_group or self.is_new():
			return
		posted = frappe.db.exists("KNIT 360 GL Entry", {"account": self.name, "is_cancelled": 0})
		if posted:
			frappe.throw(
				f"{self.name} already carries postings, so it cannot become a group account."
			)

	def on_trash(self):
		if frappe.db.exists("KNIT 360 GL Entry", {"account": self.name}):
			frappe.throw(
				f"{self.name} carries ledger entries and cannot be deleted. "
				f"Disable it instead -- FR-FIN-001 keeps the history of what the books said."
			)
		super().on_trash()
