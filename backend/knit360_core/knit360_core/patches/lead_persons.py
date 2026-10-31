"""Move each lead's one person into Contact Persons (DEC-045).

Until 1 November 2026 a lead held a single person in three fields of its own --
Prospect Name, Email and Phone. A lead now holds any number of people as rows
of Contact Persons, and those three fields are gone from the form.

Frappe drops a removed field from the form but leaves its database column, so
the values are still there after the model sync; this copies them into a first
row. A lead that already has a row is left alone, so running it twice changes
nothing. Every lead then has its list columns filled from its people (DEC-046)
and is re-indexed for search, because its title is now its organization rather
than its person.
"""

import frappe

from knit360_core.crm.doctype.knit_360_lead.knit_360_lead import columns
from knit360_core.search.index import index_document

LEAD = "KNIT 360 Lead"
PERSON = "KNIT 360 Lead Person"


def execute():
	frappe.reload_doc("crm", "doctype", "knit_360_lead_person")
	frappe.reload_doc("crm", "doctype", "knit_360_lead")

	if frappe.db.has_column(LEAD, "lead_name"):
		for row in frappe.db.sql(
			"SELECT name, lead_name, email, phone FROM `tabKNIT 360 Lead`", as_dict=True
		):
			if not row.lead_name:
				continue
			if frappe.db.exists(PERSON, {"parent": row.name, "parenttype": LEAD}):
				continue
			now = frappe.utils.now()
			frappe.get_doc(
				{
					"doctype": PERSON,
					"parent": row.name,
					"parenttype": LEAD,
					"parentfield": "contact_persons",
					"idx": 1,
					"person_name": row.lead_name,
					"email": row.email,
					"phone": row.phone,
					"owner": "Administrator",
					"creation": now,
					"modified": now,
				}
			).db_insert()

	for name in frappe.get_all(LEAD, pluck="name"):
		lead = frappe.get_doc(LEAD, name)
		cells = columns(lead.contact_persons)
		frappe.db.set_value(LEAD, name, cells, update_modified=False)
		lead.update(cells)
		index_document(lead)
