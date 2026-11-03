"""KNIT 360 Item Raw Material -- one line of a main product's group (DEC-054).

A child of KNIT 360 Item. The checks on the group as a whole -- no line for
the product itself, no item twice, no loops -- live in inventory/grouping.py,
because they need to see every line at once.
"""

from frappe.model.document import Document


class KNIT360ItemRawMaterial(Document):
	pass
