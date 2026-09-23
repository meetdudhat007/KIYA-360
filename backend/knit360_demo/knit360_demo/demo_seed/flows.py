"""Day 3-4: the Customer-to-Cash and Procure-to-Pay demo chains.

Every hop uses ERPNext's own mapper function rather than hand-building the
next document, so field mapping, taxes and item defaults follow upstream
logic instead of anything guessed here.

Run after seed.execute():
    bench --site <site> execute knit360_demo.demo_seed.flows.run_c2c
    bench --site <site> execute knit360_demo.demo_seed.flows.run_p2p

Run both BEFORE installing the Sales Order workflow (platform.install_workflow),
otherwise the Sales Order submit in run_c2c is governed by the workflow and
will stop at Pending Approval.
"""

import frappe
from frappe.utils import add_days, nowdate

from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from erpnext.buying.doctype.purchase_order.purchase_order import (
	make_purchase_invoice,
	make_purchase_receipt,
)
from erpnext.buying.doctype.request_for_quotation.request_for_quotation import (
	make_supplier_quotation_from_rfq,
)
from erpnext.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order
from erpnext.crm.doctype.lead.lead import make_opportunity
from erpnext.crm.doctype.opportunity.opportunity import make_quotation
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
from erpnext.stock.doctype.material_request.material_request import make_request_for_quotation

from knit360_core import brd_data
from knit360_demo.demo_seed._util import assert_fields, insert_if_absent, require, submit_new

COMPANY = brd_data.BRD_ORG_CONTEXT["company"]
ITEM = brd_data.BRD_ITEM["item_code"]
QTY = brd_data.PLACEHOLDER_DEMO_QTY
RATE = brd_data.PLACEHOLDER_DEMO_RATE


def _warehouse():
	"""First non-group warehouse for the company. Avoids assuming a name."""
	warehouse = frappe.db.get_value("Warehouse", {"company": COMPANY, "is_group": 0}, "name")
	if not warehouse:
		frappe.throw(f"No non-group Warehouse exists for company '{COMPANY}'.")
	return warehouse


def receive_stock(item_code=None, qty=None):
	"""Material Receipt so Delivery Note has stock to draw on.

	ERPNext blocks the Delivery Note submit without it; the plan's chain
	does not account for this.
	"""
	item_code = item_code or ITEM
	qty = qty or QTY

	entry = frappe.get_doc(
		{
			"doctype": "Stock Entry",
			"stock_entry_type": "Material Receipt",
			"company": COMPANY,
			"items": [
				{
					"item_code": item_code,
					"qty": qty,
					"t_warehouse": _warehouse(),
					"basic_rate": RATE,
				}
			],
		}
	)
	return submit_new(entry)


def _pay(reference_doctype, reference_name):
	payment = get_payment_entry(reference_doctype, reference_name)
	payment.reference_no = reference_name
	payment.reference_date = nowdate()
	return submit_new(payment)


def run_c2c():
	"""Lead -> Opportunity -> Quotation -> Sales Order -> Delivery Note
	-> Sales Invoice -> Payment Entry."""
	lead_data = brd_data.PLACEHOLDER_LEAD
	assert_fields("Lead", ["first_name", "last_name", "company_name", "email_id", "status"])
	lead = insert_if_absent(
		"Lead",
		{"company_name": lead_data["company_name"]},
		dict(status="Lead", **lead_data),
	)

	opportunity = make_opportunity(lead)
	opportunity.append("items", {"item_code": ITEM, "qty": QTY})
	opportunity.insert(ignore_permissions=True)

	quotation = make_quotation(opportunity.name)
	for row in quotation.items:
		row.rate = RATE
	quotation_name = submit_new(quotation)

	# make_sales_order converts the Lead into a Customer on the way through.
	sales_order = make_sales_order(quotation_name)
	sales_order.delivery_date = add_days(nowdate(), 7)
	sales_order_name = submit_new(sales_order)

	receive_stock()

	delivery_note = submit_new(make_delivery_note(sales_order_name))
	sales_invoice = submit_new(make_sales_invoice(sales_order_name))
	payment = _pay("Sales Invoice", sales_invoice)

	frappe.db.commit()
	return {
		"Lead": lead,
		"Opportunity": opportunity.name,
		"Quotation": quotation_name,
		"Sales Order": sales_order_name,
		"Delivery Note": delivery_note,
		"Sales Invoice": sales_invoice,
		"Payment Entry": payment,
	}


def _quality_inspection(purchase_receipt, item_code):
	"""Incoming inspection against a draft Purchase Receipt."""
	assert_fields(
		"Quality Inspection",
		["inspection_type", "reference_type", "reference_name", "item_code", "status"],
	)
	inspection = frappe.get_doc(
		{
			"doctype": "Quality Inspection",
			"inspection_type": "Incoming",
			"reference_type": "Purchase Receipt",
			"reference_name": purchase_receipt,
			"item_code": item_code,
			"sample_size": QTY,
			"inspected_by": frappe.session.user,
			"report_date": nowdate(),
			"status": "Accepted",
		}
	)
	return submit_new(inspection)


def run_p2p():
	"""Material Request -> RFQ -> Supplier Quotation -> Purchase Order
	-> Purchase Receipt (with Quality Inspection) -> Purchase Invoice
	-> Payment Entry."""
	item_code = brd_data.PLACEHOLDER_RAW_ITEM["item_code"]
	require(
		"Item", item_code, "Run knit360_demo.demo_seed.operations.seed_production first."
	)

	supplier = insert_if_absent(
		"Supplier",
		{"supplier_name": brd_data.PLACEHOLDER_SUPPLIER["supplier_name"]},
		{
			"supplier_name": brd_data.PLACEHOLDER_SUPPLIER["supplier_name"],
			"supplier_group": "All Supplier Groups",
		},
	)

	material_request = frappe.get_doc(
		{
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"company": COMPANY,
			"schedule_date": add_days(nowdate(), 7),
			"items": [
				{
					"item_code": item_code,
					"qty": QTY,
					"schedule_date": add_days(nowdate(), 7),
					"warehouse": _warehouse(),
				}
			],
		}
	)
	material_request_name = submit_new(material_request)

	rfq = make_request_for_quotation(material_request_name)
	rfq.append("suppliers", {"supplier": supplier})
	rfq_name = submit_new(rfq)

	supplier_quotation = make_supplier_quotation_from_rfq(rfq_name, for_supplier=supplier)
	for row in supplier_quotation.items:
		row.rate = RATE
	supplier_quotation_name = submit_new(supplier_quotation)

	purchase_order = make_purchase_order(supplier_quotation_name)
	purchase_order.schedule_date = add_days(nowdate(), 7)
	purchase_order_name = submit_new(purchase_order)

	# Draft receipt, inspect, then submit.
	purchase_receipt = make_purchase_receipt(purchase_order_name)
	purchase_receipt.insert(ignore_permissions=True)
	inspection = _quality_inspection(purchase_receipt.name, item_code)
	purchase_receipt.reload()
	purchase_receipt.submit()

	purchase_invoice = make_purchase_invoice(purchase_order_name)
	purchase_invoice.bill_no = purchase_invoice.name or purchase_order_name
	purchase_invoice.bill_date = nowdate()
	purchase_invoice_name = submit_new(purchase_invoice)

	payment = _pay("Purchase Invoice", purchase_invoice_name)

	frappe.db.commit()
	return {
		"Material Request": material_request_name,
		"Request for Quotation": rfq_name,
		"Supplier Quotation": supplier_quotation_name,
		"Purchase Order": purchase_order_name,
		"Purchase Receipt": purchase_receipt.name,
		"Quality Inspection": inspection,
		"Purchase Invoice": purchase_invoice_name,
		"Payment Entry": payment,
	}
