"""KNIT Department — FR-PADM-1.1.4.

BRD descriptor: "Department -- department master, head, cost center, reporting line"

Fields trace to that descriptor. The BRD specifies no further detail
(see docs/00-requirements/05-requirement-traceability.md), so anything
beyond it is marked TBD in the field description rather than invented.
"""

from frappe.model.document import Document


class KNITDepartment(Document):
	pass
