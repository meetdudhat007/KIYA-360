"""KNIT 360 Task - FR-CRM-005 Activities.

A call, meeting, email or other to-do a user sets for themselves on a lead, for
a date and a time (DEC-058). A task is its creator's alone: every role reads
only the tasks it created, a manager's included. The bell reminds the creator
when it falls due (crm.lead_tasks).
"""

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from knit360_core.crm import lead_tasks


class KNIT360Task(Document):
	def validate(self):
		# Only on a lead the user can open.
		if not frappe.has_permission(lead_tasks.LEAD, "read", doc=self.lead):
			frappe.throw(f"You cannot open {self.lead}, so you cannot set a task on it.")
		# A time moved into the future earns a fresh reminder; a time already
		# past -- a task logged after the fact -- gets none.
		if self.is_new() or self.has_value_changed("due_date") or self.has_value_changed("due_time"):
			self.reminder_sent = int(lead_tasks.due_at(self) <= now_datetime())
