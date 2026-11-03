"""Put every existing lead's people into the Contacts list (DEC-049).

Until 1 November 2026 a lead's people became contacts only when the lead was
converted, and only for leads converted after DEC-045. Now every person on a
lead is a contact from the moment the lead is saved, so the leads already on
file are brought up to that: each person gets a contact, under the customer if
the lead was converted. A converted lead's person whom the customer already has
a same-named contact for is pointed at that contact rather than given a second.

Contacts already under a customer that have no organization take the
customer's name. Running it twice changes nothing: a person who already has a
contact is left as they are. Leads have no assignment yet, so no access is granted here (DEC-048).
"""

import frappe

from knit360_core.crm import lead_contacts

LEAD = "KNIT 360 Lead"
CONTACT = "KNIT 360 Contact"


def execute():
	for doctype in ("knit_360_contact", "knit_360_lead_person", "knit_360_lead_access", "knit_360_lead"):
		frappe.reload_doc("crm", "doctype", doctype)

	for name in frappe.get_all(LEAD, pluck="name"):
		lead = frappe.get_doc(LEAD, name)
		if lead.converted_customer:
			for person in lead.contact_persons:
				if person.contact:
					continue
				existing = frappe.db.get_value(
					CONTACT, {"customer": lead.converted_customer, "contact_name": person.person_name}, "name"
				)
				if existing:
					person.db_set("contact", existing, update_modified=False)
		lead_contacts.sync(lead)

	# Contacts made by hand or by conversion before DEC-049 have no
	# organization yet; a customer's contact takes the customer's name.
	for contact in frappe.get_all(CONTACT, filters={"organization_name": ["is", "not set"], "customer": ["is", "set"]},
	                              fields=["name", "customer"]):
		frappe.db.set_value(CONTACT, contact.name, "organization_name", contact.customer, update_modified=False)
