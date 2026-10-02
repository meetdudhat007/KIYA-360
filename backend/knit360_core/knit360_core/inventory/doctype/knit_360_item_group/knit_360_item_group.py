"""KNIT 360 Item Group - FR-INV-001.

A tree, so a parent's rollup is the sum of its children. Frappe's
NestedSet maintains lft/rgt.
"""

from frappe.utils.nestedset import NestedSet


class KNIT360ItemGroup(NestedSet):
	nsm_parent_field = "parent_item_group"
