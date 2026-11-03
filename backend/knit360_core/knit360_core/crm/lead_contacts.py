"""A lead's people kept in the Contacts list -- DEC-049, FR-CRM-004.

Every person on a lead is also a KNIT 360 Contact from the moment the lead is
saved, carrying the lead and its organization, as ERPNext does with its
"auto-create contact" setting. Each person row remembers its contact, so
changing a person changes that contact rather than making a second one.

Until the lead is converted the two are kept the same, and a person removed
from the lead takes their contact with them. Conversion hands the contacts to
the customer (crm.conversion). After that the contacts are the customer's and
are changed on the contact itself: a person added to a converted lead still
gets a contact, under the customer, but existing contacts are no longer
rewritten from the lead.
"""

import frappe

CONTACT = "KNIT 360 Contact"
#: The person's fields a contact carries, besides the name.
FIELDS = ("designation", "department", "email", "phone")


def _values(person):
	return {"contact_name": person.person_name, **{f: person.get(f) for f in FIELDS}}


def sync(lead):
	customer = lead.converted_customer
	kept = set()
	for person in lead.contact_persons:
		if person.contact and frappe.db.exists(CONTACT, person.contact):
			kept.add(person.contact)
			if customer:
				continue
			contact = frappe.get_doc(CONTACT, person.contact)
			values = dict(_values(person), organization_name=lead.organization_name)
			if any((contact.get(k) or None) != (v or None) for k, v in values.items()):
				contact.update(values)
				contact.save(ignore_permissions=True)
			continue

		contact = frappe.get_doc(
			{
				"doctype": CONTACT,
				**_values(person),
				"lead": lead.name,
				"organization_name": customer or lead.organization_name,
				"customer": customer,
				"is_primary": int(
					bool(customer) and not frappe.db.exists(CONTACT, {"customer": customer, "is_primary": 1})
				),
			}
		).insert(ignore_permissions=True)
		person.db_set("contact", contact.name, update_modified=False)
		kept.add(contact.name)

	if not customer:
		for name in frappe.get_all(
			CONTACT,
			filters={"lead": lead.name, "customer": ["is", "not set"], "name": ["not in", list(kept) or [""]]},
			pluck="name",
		):
			frappe.delete_doc(CONTACT, name, ignore_permissions=True)


def release(lead):
	"""A lead being deleted: contacts that were only the lead's go with it;
	a customer's contacts stay, no longer pointing at the lead."""
	for contact in frappe.get_all(CONTACT, filters={"lead": lead.name}, fields=["name", "customer"]):
		if contact.customer:
			frappe.db.set_value(CONTACT, contact.name, "lead", None, update_modified=False)
		else:
			# force: the lead's own person rows still point at it until the
			# lead itself is gone, a moment from now.
			frappe.delete_doc(CONTACT, contact.name, ignore_permissions=True, force=True)
