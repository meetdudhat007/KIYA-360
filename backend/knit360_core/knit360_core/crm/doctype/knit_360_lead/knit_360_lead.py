"""KNIT 360 Lead - FR-CRM-001.

DR-C2C-001 Lead Acquisition and Qualification. Inputs: prospect name, organization name, contact details, lead source, estimated requirement, assigned territory.

BRD 7.2 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via traceability_map.json.

A lead is an organization with one or more people to speak to (DEC-045). The
people are rows of Contact Persons. A list or report shows one value per
column and a child table has many, so each detail of a person also has a
column of its own on the lead, listing every person's value (DEC-046).

Each person is also kept in the Contacts list (crm.lead_contacts, DEC-049), and
who may open the lead follows its assignment (crm.lead_access, DEC-048). Its
stages are the owner's client's (DEC-050), with the step reached within a
stage as Stage Detail (crm.lead_stages). Every word in it is kept for the list's
search box (crm.lead_search, DEC-053).
"""

import frappe
from frappe.model.document import Document

from knit360_core.crm import lead_access, lead_contacts, lead_search, lead_stages

#: Each list column on the lead, and the person's field it lists, in the
#: order the list shows them.
COLUMNS = {
	"person_names": "person_name",
	"designations": "designation",
	"phones": "phone",
	"emails": "email",
	"departments": "department",
}


def columns(persons):
	"""Each column's cell: every person's value, in row order.

	A person with no value takes a dash, so the second entry in every cell is
	always the second person; a cell where nobody has a value stays empty.
	"""
	cells = {}
	for column, field in COLUMNS.items():
		values = [person.get(field) or "" for person in persons]
		cells[column] = ", ".join(v or "-" for v in values) if any(values) else ""
	return cells


class KNIT360Lead(Document):
	def before_insert(self):
		# A new lead is its creator's unless they hand it to someone, as a
		# record's owner defaults to its creator in Salesforce and ERPNext. So
		# a lead a salesperson enters is read by their manager from the start.
		if not self.assigned_to:
			self.assigned_to = frappe.db.get_value(
				lead_access.EMPLOYEE, {"user": frappe.session.user, "is_active": 1}, "name"
			)

	def onload(self):
		# The form offers only the current stage's steps.
		self.set_onload("stage_details", lead_stages.STAGE_DETAILS)

	def validate(self):
		self.update(columns(self.contact_persons))
		self.refuse_inactive()
		self.refuse_stray_detail()
		self.search_keywords = lead_search.keywords(self)

	def refuse_stray_detail(self):
		stage = self.knit360_business_status
		if self.stage_detail and self.stage_detail not in lead_stages.details_for(stage):
			frappe.throw(f"{self.stage_detail} is not a step of the {stage} stage.")

	def after_business_status(self, from_status, to_status):
		# A step belongs to the stage it was reached in.
		if self.stage_detail:
			self.db_set("stage_detail", None, update_modified=False)
		# A status moves without a save, so the search box would go on
		# finding the lead by its old one.
		lead_search.refresh(self)

	def refuse_inactive(self):
		"""A lead is not handed to someone who has left.

		Only someone newly picked is checked: a lead whose handler has since
		left still saves, and simply waits to be reassigned.
		"""
		before = self.get_doc_before_save()
		had = {before.assigned_to, *(row.employee for row in before.lead_access)} if before else set()
		for employee in [self.assigned_to, *(row.employee for row in self.lead_access)]:
			if employee in had:
				continue
			if employee and not frappe.db.get_value(lead_access.EMPLOYEE, employee, "is_active"):
				name = frappe.db.get_value(lead_access.EMPLOYEE, employee, "employee_name") or employee
				frappe.throw(f"{name} is not an active employee, so cannot be given this lead.")

	def on_update(self):
		lead_contacts.sync(self)
		lead_access.sync(self)

	def on_trash(self):
		lead_contacts.release(self)
