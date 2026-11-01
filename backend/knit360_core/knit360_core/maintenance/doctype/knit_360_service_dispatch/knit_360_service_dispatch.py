"""KNIT 360 Service Dispatch - FR-MFS-007 / FR-MFS-001.

DR-A2S-005 Technician Assignment & Dispatch. Doc 33 section 7: the assigned
technician must be active, so a disabled user cannot be sent to a site.
"""

import frappe
from frappe.model.document import Document


class KNIT360ServiceDispatch(Document):
	def validate(self):
		if self.assigned_technician and not frappe.db.get_value("User", self.assigned_technician, "enabled"):
			frappe.throw(f"{self.assigned_technician} is a disabled user and cannot be sent to a site.")
