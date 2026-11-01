"""Preventive maintenance due dates -- FR-MFS-003, DR-A2S-008.

"Completing a maintenance task records the execution history and calculates
the next scheduled maintenance date" (doc 33, DR-A2S-008 acceptance criteria).

The last visit is not stored as an entry somebody makes; it is read from the
completed preventive work orders on the schedule, and the next due date is the
last visit plus the interval. So cancelling a visit puts the dates back to what
the remaining visits say. Only a fixed number of days is built as the
interval; running hours and cycle counts would need meter readings, which
nothing records yet.
"""

import frappe
from frappe.utils import add_days, cint

SCHEDULE = "KNIT 360 Maintenance Schedule"
WORK_ORDER = "KNIT 360 Field Work Order"
PREVENTIVE = "Preventive Maintenance"


def last_visit(name):
	return frappe.db.sql(
		f"""SELECT MAX(posting_date) FROM `tab{WORK_ORDER}`
		    WHERE maintenance_schedule = %s AND docstatus = 1 AND work_type = %s""",
		(name, PREVENTIVE),
	)[0][0]


def refresh(name):
	"""Recompute the schedule's last and next visit from its completed visits."""
	interval = cint(frappe.db.get_value(SCHEDULE, name, "trigger_value"))
	last = last_visit(name)
	values = {"last_done_date": last}
	if last and interval > 0:
		values["next_due_date"] = add_days(last, interval)
	frappe.db.set_value(SCHEDULE, name, values)
	return values
