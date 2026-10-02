"""KNIT 360 Customer Group - FR-PADM-1.4.1.

A tree, so a parent's rollup is the sum of its children. Frappe's
NestedSet maintains lft/rgt.
"""

from frappe.utils.nestedset import NestedSet


class KNIT360CustomerGroup(NestedSet):
	nsm_parent_field = "parent_customer_group"
