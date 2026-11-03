"""Give existing leads the client's stage names (DEC-050).

On 1 November 2026 the Lead's statuses became the first rows of the owner's
client's sales sheet. Three of the old names have a stage that means the same
thing under a new name; Qualified, Converted and Lost keep theirs. A lead at a
renamed status is moved to its new name and re-indexed, because search shows
the status under each result.

The Business Status Log is left as it was written: its rows record the names
the statuses had when each move was made.
"""

import frappe

from knit360_core.business_status.model import FIELD
from knit360_core.search.index import index_document

LEAD = "KNIT 360 Lead"
RENAMED = {"New": "New Lead", "Contacted": "Initial Contact", "Disqualified": "Not Qualified"}


def execute():
	frappe.reload_doc("crm", "doctype", "knit_360_lead")
	for old, new in RENAMED.items():
		for name in frappe.get_all(LEAD, filters={FIELD: old}, pluck="name"):
			frappe.db.set_value(LEAD, name, FIELD, new, update_modified=False)
			index_document(frappe.get_doc(LEAD, name))
