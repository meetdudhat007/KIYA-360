"""KNIT 360 Territory - FR-CRM-003.

A tree, so a parent's rollup is the sum of its children. Frappe's
NestedSet maintains lft/rgt.
"""

from frappe.utils.nestedset import NestedSet


class KNIT360Territory(NestedSet):
	nsm_parent_field = "parent_territory"
