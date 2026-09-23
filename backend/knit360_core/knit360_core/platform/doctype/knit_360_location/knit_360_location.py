"""KNIT 360 Location — FR-PADM-1.1.6.

BRD descriptor: "Location -- location master, geo location, plant/warehouse, GPS"

Fields trace to that descriptor. The BRD specifies no further detail
(see docs/00-requirements/05-requirement-traceability.md), so anything
beyond it is marked TBD in the field description rather than invented.
"""

from frappe.model.document import Document


class KNIT360Location(Document):
	pass
