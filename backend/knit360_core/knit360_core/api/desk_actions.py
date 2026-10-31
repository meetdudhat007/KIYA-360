"""Desk buttons that make the next document, from the quotation onwards.

c2c.actions_for answers this for leads and opportunities and passes every
other document here, so the order-to-cash and after-sales chains declare their
actions in one place.

Whether a button is enabled is the same rule the creating function enforces --
each module's *_refusal -- so the Desk can never offer a button that would
then refuse.
"""

import frappe

from knit360_core.business_status import engine
from knit360_core.maintenance import make, service_invoice
from knit360_core.sales import document_from


def _action(key, label, refusal):
	return {"key": key, "label": label, "enabled": not refusal, "reason": refusal}


def _quotation(doc):
	return [_action("make_sales_order", "Create Sales Order", document_from.order_refusal(doc))]


def _sales_order(doc):
	return [_action("make_delivery_note", "Create Delivery Note", document_from.dispatch_refusal(doc))]


def _delivery_note(doc):
	if engine.current_status(doc) == "Cancelled":
		return []
	return [_action("make_sales_invoice", "Create Sales Invoice", document_from.billing_refusal(doc))]


def _asset(doc):
	return [_action("log_service_request", "Log Service Request", make.request_refusal(doc))]


def _service_request(doc):
	refusal = make.work_refusal(doc)
	if refusal:
		return []
	return [
		_action("make_field_work_order", "Create Work Order", None),
		_action("make_service_dispatch", "Schedule Visit", None),
	]


def _maintenance_schedule(doc):
	return [_action("make_preventive_work_order", "Create Visit Work Order", None)]


def _field_work_order(doc):
	if doc.docstatus != 1:
		return []
	return [_action("make_service_invoice", "Raise Service Invoice", service_invoice.billing_refusal(doc))]


ACTIONS = {
	"KNIT 360 Quotation": _quotation,
	"KNIT 360 Sales Order": _sales_order,
	"KNIT 360 Delivery Note": _delivery_note,
	"KNIT 360 Asset": _asset,
	"KNIT 360 Service Request": _service_request,
	"KNIT 360 Maintenance Schedule": _maintenance_schedule,
	"KNIT 360 Field Work Order": _field_work_order,
}


def actions_for(doctype, name):
	"""[] for a doctype with nothing to offer; asked on every form that opens."""
	builder = ACTIONS.get(doctype)
	if not builder:
		return []
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("read")
	return builder(doc)
