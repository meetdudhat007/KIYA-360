"""KNIT 360 Contact - FR-CRM-004.

Contact persons against a Customer, and -- before there is one -- against the
lead they were entered on (crm.lead_contacts, DEC-049).

BRD 7.2 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via each field description.
"""

import frappe
from frappe.model.document import Document


class KNIT360Contact(Document):
	def validate(self):
		# Organization is what the Contacts list is read by. A contact entered
		# by hand under a customer takes the customer's name.
		if not self.organization_name:
			if self.customer:
				self.organization_name = self.customer
			elif self.lead:
				self.organization_name = frappe.db.get_value("KNIT 360 Lead", self.lead, "organization_name")
