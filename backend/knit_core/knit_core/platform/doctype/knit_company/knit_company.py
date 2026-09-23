"""KNIT Company — FR-PADM-1.1.1.

BRD descriptor: "Company Master -- company details, business type, legal entity, fiscal year, currency, tax registration"

Fields trace to that descriptor. The BRD specifies no further detail
(see docs/00-requirements/05-requirement-traceability.md), so anything
beyond it is marked TBD in the field description rather than invented.
"""

from frappe.model.document import Document


class KNITCompany(Document):
	pass
