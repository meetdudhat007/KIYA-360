"""KNIT 360 Supplier Group - FR-SUPM-002.

A tree, so a parent's rollup is the sum of its children. Frappe's
NestedSet maintains lft/rgt.
"""

from frappe.utils.nestedset import NestedSet


class KNIT360SupplierGroup(NestedSet):
	nsm_parent_field = "parent_supplier_group"
