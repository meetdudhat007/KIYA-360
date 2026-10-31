"""A unit's whole life on one page -- FR-AST-006, DR-A2S-011.

Read from the documents themselves every time it is asked for, never kept as a
copy: delivery, status changes, warranty and contracts, service requests,
visits scheduled, work done with the parts used, and service invoices. A copy
would drift from its sources; this cannot, because it has none of its own
(doc 33: the timeline is derived from approved transactions and is never
edited by hand).

Totals are counts and sums of what is recorded. Reliability measures -- mean
time between failures, mean time to repair -- and total cost of ownership are
PROPOSED in doc 33 and are not built.
"""

import frappe
from frappe.utils import flt, get_datetime

ASSET = "KNIT 360 Asset"
LOG = "KNIT 360 Business Status Log"
CONTRACT = "KNIT 360 Service Contract"
REQUEST = "KNIT 360 Service Request"
DISPATCH = "KNIT 360 Service Dispatch"
WORK_ORDER = "KNIT 360 Field Work Order"
WORK_LINE = "KNIT 360 Field Work Order Item"
INVOICE = "KNIT 360 Sales Invoice"
DELIVERY_NOTE = "KNIT 360 Delivery Note"

PART = "Spare Part"
WARRANTY = "Warranty Covered"


def _event(when, what, detail, doctype, name, status=None):
	return {
		"when": get_datetime(when) if when else None,
		"what": what,
		"detail": detail or "",
		"doctype": doctype,
		"name": name,
		"status": status or "",
	}


@frappe.whitelist()
def asset_history(asset):
	unit = frappe.get_doc(ASSET, asset)
	unit.check_permission("read")
	events = []

	if unit.delivery_note:
		dn = frappe.db.get_value(DELIVERY_NOTE, unit.delivery_note,
		                         ["delivery_note_date", "knit360_business_status"], as_dict=True)
		if dn:
			events.append(_event(dn.delivery_note_date, "Delivered", f"Dispatched on {unit.delivery_note}",
			                     DELIVERY_NOTE, unit.delivery_note, dn.knit360_business_status))

	for row in frappe.get_all(LOG, filters={"reference_doctype": ASSET, "reference_name": asset},
	                          fields=["to_status", "reason", "transitioned_at", "transitioned_by"]):
		events.append(_event(row.transitioned_at, f"Became {row.to_status}",
		                     row.reason or f"by {row.transitioned_by}", ASSET, asset))

	for row in frappe.get_all(CONTRACT, filters={"asset": asset},
	                          fields=["name", "contract_type", "start_date", "end_date",
	                                  "knit360_business_status", "creation"]):
		events.append(_event(row.start_date or row.creation, row.contract_type,
		                     f"{row.start_date or '?'} to {row.end_date or '?'}",
		                     CONTRACT, row.name, row.knit360_business_status))

	requests = frappe.get_all(REQUEST, filters={"asset": asset},
	                          fields=["name", "request_timestamp", "problem_description",
	                                  "knit360_business_status", "warranty_status"])
	for row in requests:
		events.append(_event(row.request_timestamp, "Service request",
		                     f"{(row.problem_description or '')[:120]} ({row.warranty_status or 'cover not judged'})",
		                     REQUEST, row.name, row.knit360_business_status))

	if requests:
		for row in frappe.get_all(DISPATCH, filters={"service_request": ["in", [r.name for r in requests]]},
		                          fields=["name", "scheduled_datetime", "assigned_technician",
		                                  "knit360_business_status", "creation"]):
			events.append(_event(row.scheduled_datetime or row.creation, "Visit scheduled",
			                     f"Engineer: {row.assigned_technician or 'not assigned'}",
			                     DISPATCH, row.name, row.knit360_business_status))

	totals = {
		"service_requests": len(requests),
		"breakdown_repairs": 0,
		"preventive_visits": 0,
		"installations": 0,
		"labour_hours": 0.0,
		"parts_cost": 0.0,
		"warranty_parts_cost": 0.0,
		"billed": 0.0,
	}
	kinds = {"Breakdown Repair": "breakdown_repairs", "Preventive Maintenance": "preventive_visits",
	         "Installation": "installations"}

	jobs = frappe.get_all(WORK_ORDER, filters={"asset": asset},
	                      fields=["name", "work_type", "posting_date", "findings", "docstatus",
	                              "actual_labor_hours", "knit360_business_status", "sales_invoice"])
	for job in jobs:
		parts = frappe.get_all(WORK_LINE, filters={"parent": job.name, "line_type": PART},
		                       fields=["item_code", "qty", "coverage", "stock_value"])
		used = ", ".join(f"{flt(p.qty):g} x {p.item_code}" for p in parts)
		detail = "; ".join(x for x in ((job.findings or "")[:120], f"parts: {used}" if used else "") if x)
		events.append(_event(job.posting_date, job.work_type, detail, WORK_ORDER, job.name,
		                     job.knit360_business_status))
		if job.docstatus != 1:
			continue
		totals[kinds.get(job.work_type, "breakdown_repairs")] += 1
		totals["labour_hours"] += flt(job.actual_labor_hours)
		for p in parts:
			totals["parts_cost"] += flt(p.stock_value)
			if p.coverage == WARRANTY:
				totals["warranty_parts_cost"] += flt(p.stock_value)
		if job.sales_invoice:
			bill = frappe.db.get_value(INVOICE, job.sales_invoice,
			                           ["posting_date", "grand_total", "knit360_business_status", "docstatus"],
			                           as_dict=True)
			if bill:
				events.append(_event(bill.posting_date, "Service invoice", f"{flt(bill.grand_total):,.2f}",
				                     INVOICE, job.sales_invoice, bill.knit360_business_status))
				# A draft has not been billed yet, and a cancelled one no longer is.
				if bill.docstatus == 1:
					totals["billed"] += flt(bill.grand_total)

	events.sort(key=lambda e: e["when"] or get_datetime("1900-01-01"), reverse=True)
	for event in events:
		event["when"] = event["when"].strftime("%d-%m-%Y") if event["when"] else ""
	return {"events": events, "totals": totals}
