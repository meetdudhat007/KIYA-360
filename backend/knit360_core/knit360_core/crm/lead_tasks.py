"""Tasks on leads: the lead page's Tasks panel, the CRM page's My Tasks, and
the bell reminder (DEC-058).

A task is its creator's alone. Permissions already keep other users out, but
an Administrator is past every permission, so each read here asks for the
session user's own tasks by name rather than for whatever the user may read.
"""

import frappe
from frappe.utils import escape_html, format_time, get_datetime, now_datetime

from knit360_core.crm.lead_access import LEAD

TASK = "KNIT 360 Task"
FIELDS = ["name", "lead", "organization_name", "task_type", "due_date", "due_time", "description", "done"]


def due_at(task):
	"""The moment a task is due."""
	return get_datetime(f"{task.due_date} {task.due_time}")


def types():
	"""Call, Meeting, Email, Other -- as the task record type lists them."""
	return frappe.get_meta(TASK).get_field("task_type").options.split("\n")


def _mine(**filters):
	return frappe.get_all(
		TASK,
		filters={"owner": frappe.session.user, **filters},
		fields=FIELDS,
		order_by="due_date asc, due_time asc",
	)


@frappe.whitelist()
def for_lead(lead):
	"""The session user's tasks on one lead, for its Tasks panel."""
	frappe.has_permission(LEAD, "read", doc=lead, throw=True)
	return _mine(lead=lead)


@frappe.whitelist()
def on_day(date):
	"""The session user's tasks on one day, for the CRM page."""
	return _mine(due_date=date)


def send_reminders():
	"""Every minute: a bell notification to the creator of each open task
	whose time has come, once."""
	now = now_datetime()
	due = frappe.get_all(
		TASK,
		filters={"done": 0, "reminder_sent": 0, "due_date": ["<=", now.date()]},
		fields=[*FIELDS, "owner"],
	)
	for task in due:
		if due_at(task) > now:
			continue
		frappe.get_doc(
			{
				"doctype": "Notification Log",
				"for_user": task.owner,
				"type": "Alert",
				"document_type": LEAD,
				"document_name": task.lead,
				"subject": escape_html(
					f"{task.task_type} at {format_time(task.due_time, 'HH:mm')}: "
					f"{task.organization_name or task.lead} ({task.lead}) - {task.description}"
				),
			}
		).insert(ignore_permissions=True)
		frappe.db.set_value(TASK, task.name, "reminder_sent", 1, update_modified=False)
	if due:
		frappe.db.commit()
