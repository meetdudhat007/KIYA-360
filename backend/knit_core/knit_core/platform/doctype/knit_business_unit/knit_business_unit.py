"""KNIT Business Unit — FR-PADM-1.1.3.

BRD descriptor: "Business Unit -- unit master, product line, profit center, cost center"

Fields trace to that descriptor. The BRD specifies no further detail
(see docs/00-requirements/05-requirement-traceability.md), so anything
beyond it is marked TBD in the field description rather than invented.
"""

from frappe.model.document import Document


class KNITBusinessUnit(Document):
	pass
