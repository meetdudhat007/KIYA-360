"""The service invoice for a repair job -- DR-A2S-009.

Doc 33's invoicing consistency rule: a service invoice is an ordinary Sales
Invoice, through the same posting, tax and settlement as any other, never a
separate billing model. So this only builds the draft.

Only lines tagged Billable to Customer are billed. Labour and travel are
credited to the company's service income account; spare parts to the ordinary
income account, like any goods sold -- DEC-041. Rates are left for the price
list to fill, as on every other selling document. The invoice is left a
draft: the office checks it, chooses the tax template, and posts it.
"""

import frappe
from frappe.utils import nowdate

from knit360_core.maintenance import entitlement
from knit360_core.pricing import price_list

WORK_ORDER = "KNIT 360 Field Work Order"
SALES_INVOICE = "KNIT 360 Sales Invoice"
COMPANY = "KNIT 360 Company"


def billing_refusal(job):
	if job.docstatus != 1:
		return "Bill a job once the work is complete."
	if job.sales_invoice:
		status = frappe.db.get_value(SALES_INVOICE, job.sales_invoice, "knit360_business_status")
		if status and status != "Cancelled":
			return f"Already billed on {job.sales_invoice}."
	if not job.customer:
		return "The unit has no customer to bill."
	if not any(row.coverage == entitlement.BILLABLE for row in job.items):
		return "Nothing on it is billable: every line is covered by warranty or contract."
	return None


@frappe.whitelist()
def from_field_work_order(field_work_order):
	job = frappe.get_doc(WORK_ORDER, field_work_order)
	job.check_permission("read")
	refusal = billing_refusal(job)
	if refusal:
		frappe.throw(f"{field_work_order}: {refusal}")

	service_income = frappe.db.get_value(COMPANY, job.company, "default_service_income_account")
	invoice = frappe.get_doc(
		{
			"doctype": SALES_INVOICE,
			"customer": job.customer,
			"company": job.company,
			"posting_date": nowdate(),
			"field_work_order": job.name,
			"items": [
				{
					"item_code": row.item_code,
					"description": row.description,
					"qty": row.qty,
					"income_account": service_income if row.line_type != entitlement.PART else None,
				}
				for row in job.items
				if row.coverage == entitlement.BILLABLE
			],
		}
	)
	# A billable line with no price would post as nil and the charge would be
	# lost without anyone noticing, so the draft is refused until every line
	# can be priced.
	price_list_name = price_list.for_document(invoice, price_list.SELLING)
	unpriced = sorted({
		row.item_code for row in invoice.items
		if price_list.rate_for(row.item_code, price_list_name) is None
	})
	if unpriced:
		frappe.throw(
			f"{field_work_order}: give {', '.join(unpriced)} a selling price in "
			f"{price_list_name or 'a selling price list'} first, so every billable line has a rate."
		)
	invoice.insert()
	job.db_set("sales_invoice", invoice.name, update_modified=False)
	return invoice.name
