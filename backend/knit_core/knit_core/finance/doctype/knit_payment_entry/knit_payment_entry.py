"""KNIT Payment Entry - FR-FIN-002 / FR-FIN-004.

DR-P2P-011 payment disbursement and DR-A2S-010 customer collection. One entry type with a direction, since both carry the same inputs.
"""

from frappe.model.document import Document


class KNITPaymentEntry(Document):
	pass
