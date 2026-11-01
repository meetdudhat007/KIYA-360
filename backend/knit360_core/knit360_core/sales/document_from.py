"""The next document from the last -- BRD section 11 "Document-to-document linking".

Quotation -> Sales Order -> Delivery Note -> Sales Invoice, each carrying the
lines and terms across so nothing is typed twice and nothing can disagree.
Each refuses to make a second live document from the same source, which is
what stops a quotation being ordered twice or a dispatch billed twice.

As in quotation_from, the source document's own status is not advanced here:
making an order is not the same as the customer's quotation being Ordered
until the order is confirmed, and no DR- record couples the two. The user
moves each document with its own buttons.
"""

import frappe
from frappe.utils import flt, nowdate

from knit360_core.business_status import engine
from knit360_core.sales.doctype.knit_360_delivery_note.knit_360_delivery_note import ordered_and_dispatched

QUOTATION = "KNIT 360 Quotation"
SALES_ORDER = "KNIT 360 Sales Order"
DELIVERY_NOTE = "KNIT 360 Delivery Note"
SALES_INVOICE = "KNIT 360 Sales Invoice"
STATUS = engine.FIELD

ORDERABLE = ("Accepted",)
DISPATCHABLE = ("Confirmed / Booked", "In Fulfillment")


def _live(doctype, filters):
	"""A document made from this source that has not been cancelled."""
	filters = dict(filters)
	filters[STATUS] = ["!=", "Cancelled"]
	return frappe.db.get_value(doctype, filters, "name")


def order_refusal(quotation):
	status = engine.current_status(quotation)
	if status not in ORDERABLE:
		return f"An order is made from an accepted quotation; this one is {status}."
	existing = _live(SALES_ORDER, {"quotation": quotation.name})
	if existing:
		return f"Already on order as {existing}."
	return None


@frappe.whitelist()
def sales_order_from_quotation(quotation):
	source = frappe.get_doc(QUOTATION, quotation)
	source.check_permission("read")
	refusal = order_refusal(source)
	if refusal:
		frappe.throw(f"{quotation}: {refusal}")

	order = frappe.get_doc(
		{
			"doctype": SALES_ORDER,
			"customer": source.customer,
			"company": source.company,
			"quotation": source.name,
			"currency": source.currency,
			"price_list": source.price_list,
			"tax_template": source.tax_template,
			"payment_terms": source.payment_terms,
			"items": [
				{
					"item_code": row.item_code,
					"description": row.description,
					"qty": row.qty,
					"uom": row.uom,
					# The price agreed is the quotation's, discount included. An
					# order has no discount column, so it carries the net rate.
					"rate": flt(row.amount) / flt(row.qty) if flt(row.qty) else row.unit_rate,
				}
				for row in source.items
			],
		}
	).insert()
	return order.name


def remaining(order_name):
	"""item -> quantity still to dispatch, counting dispatches already drafted."""
	balance, _sent = ordered_and_dispatched(order_name, include_drafts=True)
	return {item: ordered - sent for item, (ordered, sent) in balance.items() if ordered - sent > 0.0001}


def dispatch_refusal(order):
	status = engine.current_status(order)
	if status not in DISPATCHABLE:
		return f"Goods are dispatched against a confirmed order; this one is {status}."
	if not remaining(order.name):
		return "Everything on it has been dispatched or is on a draft delivery note."
	return None


@frappe.whitelist()
def delivery_note_from_sales_order(sales_order, source_warehouse):
	order = frappe.get_doc(SALES_ORDER, sales_order)
	order.check_permission("read")
	refusal = dispatch_refusal(order)
	if refusal:
		frappe.throw(f"{sales_order}: {refusal}")

	left = remaining(sales_order)
	lines, seen = [], set()
	for row in order.items:
		if row.item_code in seen or row.item_code not in left:
			continue
		seen.add(row.item_code)
		lines.append({"item_code": row.item_code, "description": row.description, "qty": left[row.item_code]})

	note = frappe.get_doc(
		{
			"doctype": DELIVERY_NOTE,
			"sales_order": order.name,
			"company": order.company,
			"source_warehouse": source_warehouse,
			"delivery_note_date": nowdate(),
			"ship_to_address": order.shipping_address,
			"items": lines,
		}
	).insert()
	return note.name


def billing_refusal(note):
	if note.docstatus != 1:
		return "Bill goods once they have been dispatched; this delivery note is not."
	if not note.sales_order:
		return "It was not sold on a sales order, so there is no agreed price to bill. Raise the invoice by hand."
	existing = _live(SALES_INVOICE, {"delivery_note": note.name})
	if existing:
		return f"Already billed on {existing}."
	return None


@frappe.whitelist()
def sales_invoice_from_delivery_note(delivery_note):
	note = frappe.get_doc(DELIVERY_NOTE, delivery_note)
	note.check_permission("read")
	refusal = billing_refusal(note)
	if refusal:
		frappe.throw(f"{delivery_note}: {refusal}")

	order = frappe.get_doc(SALES_ORDER, note.sales_order)
	agreed = {}
	for row in order.items:
		agreed.setdefault(row.item_code, row)

	invoice = frappe.get_doc(
		{
			"doctype": SALES_INVOICE,
			"customer": order.customer,
			"company": order.company,
			"posting_date": nowdate(),
			"sales_order": order.name,
			"delivery_note": note.name,
			"currency": order.currency,
			"price_list": order.price_list,
			"tax_template": order.tax_template,
			"payment_terms": order.payment_terms,
			"items": [
				{
					"item_code": row.item_code,
					"description": row.description,
					"qty": row.qty,
					"uom": agreed[row.item_code].uom if row.item_code in agreed else None,
					"rate": agreed[row.item_code].rate if row.item_code in agreed else None,
				}
				for row in note.items
			],
		}
	).insert()
	return invoice.name
