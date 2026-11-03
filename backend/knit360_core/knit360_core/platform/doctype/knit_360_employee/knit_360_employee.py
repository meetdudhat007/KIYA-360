"""KNIT 360 Employee - FR-PADM-1.4.4.

Reports To draws the line a lead's access follows upward (DEC-048): whoever an
employee reports to, directly or further up, can read the leads assigned to
them. So a change to an employee's manager, login or active flag reworks who
can open those leads.
"""

import frappe
from frappe.model.document import Document

from knit360_core.crm import lead_access, lead_search


class KNIT360Employee(Document):
	def validate(self):
		if self.reports_to and self.reports_to == self.name:
			frappe.throw("An employee cannot report to themselves.")
		if self.reports_to and self.name in lead_access.managers(self.reports_to):
			frappe.throw(
				f"{self.employee_name} cannot report to "
				f"{frappe.db.get_value(lead_access.EMPLOYEE, self.reports_to, 'employee_name')}, "
				f"who already reports to {self.employee_name}, directly or further up."
			)

	def on_update(self):
		if any(self.has_value_changed(f) for f in ("user", "reports_to", "is_active")):
			lead_access.resync_for(self.name)
		# The lead list's search box finds a lead by the names of its people.
		if self.has_value_changed("employee_name"):
			lead_search.refresh_for(self.name)
