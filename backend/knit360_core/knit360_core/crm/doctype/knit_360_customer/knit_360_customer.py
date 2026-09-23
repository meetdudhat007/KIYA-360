"""KNIT 360 Customer - FR-CRM-003 / FR-CRM-004 / FR-PADM-1.4.1.

Unified single customer record across CRM, Sales and Receivables (SF-004, DEC-007). The BRD's CRM 'Accounts' requirement and the Customer Master are the same entity.

BRD 7.2 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via each field description.
"""

from frappe.model.document import Document


class KNIT360Customer(Document):
	pass
