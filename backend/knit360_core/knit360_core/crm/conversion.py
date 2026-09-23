"""Lead conversion -- FR-CRM-001 (DR-C2C-001).

The Lead doctype already declares what conversion means, in the descriptions of
two fields nothing yet writes:

    converted_customer     "conversion creates or links a unified Customer
                            Master (DR-C2C-001)"
    converted_opportunity  "conversion generates an Opportunity (DR-C2C-001)"

This module is the only writer of those fields. It creates the records the
Lead's own lifecycle presupposes, then moves the Lead to Converted through
business_status.engine.transition like any other status change, so the
transition matrix and the audit log stay the single authority on lifecycle.
"""

import frappe

from knit360_core.business_status import engine

LEAD = "KNIT 360 Lead"
CUSTOMER = "KNIT 360 Customer"
OPPORTUNITY = "KNIT 360 Opportunity"

#: DR-C2C-001 puts Converted only after Qualified. Enforced here as well as in
#: the transition matrix, so the reason given is about conversion, not states.
REQUIRED_STATUS = "Qualified"
CONVERTED = "Converted"


def customer_name_for(lead):
	"""KNIT 360 Customer is autonamed field:customer_name, so this is also its id."""
	return lead.organization_name or lead.lead_name


def _find_or_create_customer(lead):
	"""'Creates OR LINKS a unified Customer Master' -- an existing customer of
	the same name is reused rather than duplicated, which is the point of a
	unified master (SF-003)."""
	name = customer_name_for(lead)
	if frappe.db.exists(CUSTOMER, name):
		return name, False

	customer = frappe.get_doc(
		{
			"doctype": CUSTOMER,
			"customer_name": name,
			"company": lead.company,
			"territory": lead.territory,
			"email": lead.email,
			"phone": lead.phone,
			"address": lead.address,
		}
	).insert()
	return customer.name, True


@frappe.whitelist()
def convert_lead(lead, customer=None):
	"""Convert a Qualified lead into a Customer and an Opportunity.

	customer -- an existing KNIT 360 Customer to link instead of deriving one from
	the lead's organisation name. Supplied by the caller when the prospect is
	already on file under a different name.
	"""
	doc = frappe.get_doc(LEAD, lead)
	doc.check_permission("write")

	if doc.converted_opportunity:
		frappe.throw(
			f"{LEAD} {doc.name} is already converted "
			f"(opportunity {doc.converted_opportunity})."
		)

	status = engine.current_status(doc)
	if status != REQUIRED_STATUS:
		frappe.throw(
			f"{LEAD} {doc.name} must be '{REQUIRED_STATUS}' before conversion; "
			f"it is '{status}'."
		)

	if customer:
		if not frappe.db.exists(CUSTOMER, customer):
			frappe.throw(f"{CUSTOMER} {customer} does not exist.")
		customer_id, created = customer, False
	else:
		customer_id, created = _find_or_create_customer(doc)

	opportunity = frappe.get_doc(
		{
			"doctype": OPPORTUNITY,
			"title": customer_name_for(doc),
			"customer": customer_id,
			"company": doc.company,
			"source_lead": doc.name,
			"currency": frappe.db.get_value(CUSTOMER, customer_id, "default_currency"),
		}
	).insert()

	doc.db_set("converted_customer", customer_id, update_modified=False)
	doc.db_set("converted_opportunity", opportunity.name, update_modified=False)
	engine.transition(LEAD, doc.name, CONVERTED, reason=f"Converted to {opportunity.name}")

	return {
		"customer": customer_id,
		"customer_created": created,
		"opportunity": opportunity.name,
	}
