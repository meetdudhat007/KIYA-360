"""KNIT 360 Cost Center - FR-FIN-006.

The attribution dimension, as a tree, for the same reason accounts are one: a
division's cost is the sum of the departments beneath it.
"""

import frappe
from frappe.utils.nestedset import NestedSet


class KNIT360CostCenter(NestedSet):
	nsm_parent_field = "parent_cost_center"

	def autoname(self):
		abbr = frappe.db.get_value("KNIT 360 Company", self.company, "abbreviation") or self.company
		parts = [p for p in (self.cost_center_number, self.cost_center_name) if p]
		self.name = f"{' - '.join(parts)} - {abbr}"

	def validate(self):
		if not self.parent_cost_center:
			return
		parent = frappe.db.get_value(
			"KNIT 360 Cost Center", self.parent_cost_center, ["is_group", "company"], as_dict=True
		)
		if not parent.is_group:
			frappe.throw(f"{self.parent_cost_center} is not a group and cannot hold children.")
		if parent.company != self.company:
			frappe.throw(f"{self.parent_cost_center} belongs to {parent.company}.")

	def on_trash(self):
		if frappe.db.exists("KNIT 360 GL Entry", {"cost_center": self.name}):
			frappe.throw(f"{self.name} carries ledger entries and cannot be deleted. Disable it instead.")
		super().on_trash()
