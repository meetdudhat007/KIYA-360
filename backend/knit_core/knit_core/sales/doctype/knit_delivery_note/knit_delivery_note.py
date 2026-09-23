"""KNIT Delivery Note - FR-SALES-005.

DR-C2C-012 Dispatch and Delivery Note. Moves stock (FR-INV-002), so it submits.

BRD 7.3 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via each field description.
"""

from frappe.model.document import Document


class KNITDeliveryNote(Document):
	pass
