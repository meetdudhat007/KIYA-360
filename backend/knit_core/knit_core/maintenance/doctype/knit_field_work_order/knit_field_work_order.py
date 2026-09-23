"""KNIT Field Work Order - FR-MFS-002 / FR-MFS-007.

DR-A2S-007 Field Service Work Order Execution. Deliberately a separate doctype from KNIT Work Order (manufacturing) — doc 33 forbids sharing that schema.
"""

from frappe.model.document import Document


class KNITFieldWorkOrder(Document):
	pass
