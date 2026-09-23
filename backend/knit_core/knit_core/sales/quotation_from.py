"""Quotation origination -- FR-SALES-002 (DR-C2C-004).

The Quotation doctype carries Link fields to both an Opportunity and an
Enquiry, described as "Opportunity reference" and "Enquiry reference". This
module creates a Quotation from either, carrying the line items across.

Deliberately not done here: advancing the source document's own status. The
Opportunity lifecycle has 'Proposal Sent' and the Enquiry lifecycle has
'Quoted', and both look like the natural consequence of raising a quotation --
but neither DR-C2C-002 nor DR-C2C-003 says the source advances when the
quotation is *created* rather than issued. Coupling them would be an assumption,
so the caller advances the source explicitly. Recorded as part of OQ-018.
"""

import frappe

QUOTATION = "KNIT Quotation"
OPPORTUNITY = "KNIT Opportunity"
ENQUIRY = "KNIT Enquiry"


def _quotation_items(rows):
	"""Opportunity and Enquiry items carry no price, so unit_rate is left unset
	rather than guessed. Pricing is FR-SALES-004 and needs a price list, which
	is BRD-DERIVED and TBD."""
	return [
		{
			"item_code": row.item_code,
			"description": row.description,
			"qty": row.qty,
			# Enquiry Item carries a uom, Opportunity Item does not.
			"uom": row.get("uom"),
		}
		for row in rows
	]


@frappe.whitelist()
def from_opportunity(opportunity):
	source = frappe.get_doc(OPPORTUNITY, opportunity)
	source.check_permission("read")

	quotation = frappe.get_doc(
		{
			"doctype": QUOTATION,
			"customer": source.customer,
			"company": source.company,
			"opportunity": source.name,
			"currency": source.currency,
			"items": _quotation_items(source.items),
		}
	).insert()
	return quotation.name


@frappe.whitelist()
def from_enquiry(enquiry):
	source = frappe.get_doc(ENQUIRY, enquiry)
	source.check_permission("read")

	quotation = frappe.get_doc(
		{
			"doctype": QUOTATION,
			"customer": source.customer,
			"company": source.company,
			"enquiry": source.name,
			"items": _quotation_items(source.items),
		}
	).insert()
	return quotation.name
