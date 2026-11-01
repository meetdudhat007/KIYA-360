"""KNIT 360 Lead - FR-CRM-001.

DR-C2C-001 Lead Acquisition and Qualification. Inputs: prospect name, organization name, contact details, lead source, estimated requirement, assigned territory.

BRD 7.2 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via traceability_map.json.

A lead is an organization with one or more people to speak to (DEC-045). The
people are rows of Contact Persons. A list or report shows one value per
column and a child table has many, so each detail of a person also has a
column of its own on the lead, listing every person's value (DEC-046).
"""

from frappe.model.document import Document

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
	def validate(self):
		self.update(columns(self.contact_persons))
