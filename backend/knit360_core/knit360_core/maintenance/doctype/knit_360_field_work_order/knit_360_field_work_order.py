"""KNIT 360 Field Work Order - FR-MFS-002 / FR-MFS-007.

DR-A2S-007 Field Service Work Order Execution. Deliberately a separate doctype from KNIT 360 Work Order (manufacturing) — doc 33 forbids sharing that schema.
"""

from frappe.model.document import Document


class KNIT360FieldWorkOrder(Document):
	pass
