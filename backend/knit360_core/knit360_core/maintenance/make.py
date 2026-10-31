"""The next service document from the last -- DR-A2S-004 and DR-A2S-008.

Doc 33 (DR-A2S-004, BRD-DERIVED): a service request converts into technician
assignment and a field work order. These make each as a draft carrying the
unit, customer and company across. As elsewhere, the source's own status is
not moved here; the user moves each document with its own buttons.
"""

import frappe
from frappe.utils import now_datetime, nowdate

from knit360_core.business_status import engine

ASSET = "KNIT 360 Asset"
REQUEST = "KNIT 360 Service Request"
DISPATCH = "KNIT 360 Service Dispatch"
WORK_ORDER = "KNIT 360 Field Work Order"
SCHEDULE = "KNIT 360 Maintenance Schedule"

RETIRED = ("Decommissioned", "Scrapped")
REQUEST_FINISHED = ("Resolved", "Closed", "Cancelled")


def request_refusal(unit):
	status = engine.current_status(unit)
	if status in RETIRED:
		return f"It is {status} and no longer in service."
	return None


@frappe.whitelist()
def service_request_for_asset(asset, problem_description):
	unit = frappe.get_doc(ASSET, asset)
	unit.check_permission("read")
	refusal = request_refusal(unit)
	if refusal:
		frappe.throw(f"{asset}: {refusal}")
	request = frappe.get_doc(
		{
			"doctype": REQUEST,
			"asset": unit.name,
			"customer": unit.customer,
			"company": unit.company,
			"request_timestamp": now_datetime(),
			"contact_details": unit.site_contact_person,
			"problem_description": problem_description,
		}
	).insert()
	return request.name


def work_refusal(request):
	status = engine.current_status(request)
	if status in REQUEST_FINISHED:
		return f"The request is {status}."
	return None


@frappe.whitelist()
def work_order_from_request(service_request):
	request = frappe.get_doc(REQUEST, service_request)
	request.check_permission("read")
	refusal = work_refusal(request)
	if refusal:
		frappe.throw(f"{service_request}: {refusal}")
	job = frappe.get_doc(
		{
			"doctype": WORK_ORDER,
			"work_type": "Breakdown Repair",
			"service_request": request.name,
			"asset": request.asset,
			"company": request.company,
			"posting_date": nowdate(),
		}
	).insert()
	return job.name


@frappe.whitelist()
def dispatch_from_request(service_request):
	request = frappe.get_doc(REQUEST, service_request)
	request.check_permission("read")
	refusal = work_refusal(request)
	if refusal:
		frappe.throw(f"{service_request}: {refusal}")
	visit = frappe.get_doc(
		{"doctype": DISPATCH, "service_request": request.name, "company": request.company}
	).insert()
	return visit.name


@frappe.whitelist()
def work_order_from_schedule(maintenance_schedule):
	plan = frappe.get_doc(SCHEDULE, maintenance_schedule)
	plan.check_permission("read")
	job = frappe.get_doc(
		{
			"doctype": WORK_ORDER,
			"work_type": "Preventive Maintenance",
			"maintenance_schedule": plan.name,
			"asset": plan.asset,
			"company": plan.company,
			"posting_date": nowdate(),
			"sop": plan.tasks,
		}
	).insert()
	return job.name
