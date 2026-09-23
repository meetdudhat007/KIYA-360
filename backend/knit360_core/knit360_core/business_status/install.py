"""Adds the business status field to the doctypes the adapter governs.

    bench --site <site> execute knit360_core.business_status.install.install
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from knit360_core.business_status import model
from knit360_core.business_status.engine import FIELD, conflicting_workflow

# Sales Order only, for the spike. Widen once the matrix is ratified.
GOVERNED_DOCTYPES = ["Sales Order"]


def install(doctypes=None):
	doctypes = doctypes or GOVERNED_DOCTYPES

	clashes = {d: conflicting_workflow(d) for d in doctypes if conflicting_workflow(d)}
	if clashes:
		detail = ", ".join(f"{d} ({w})" for d, w in clashes.items())
		frappe.throw(
			f"Active Frappe Workflow(s) already govern: {detail}. "
			f"Deactivate them first; the Workflow engine and this adapter both own docstatus."
		)
	fields = {
		doctype: [
			{
				"fieldname": FIELD,
				"label": "Business Status",
				"fieldtype": "Select",
				"options": "\n".join(model.STATES),
				"default": model.DRAFT,
				"read_only": 1,
				"allow_on_submit": 1,
				"in_list_view": 1,
				"insert_after": "status",
				"description": "CD-002 operational status. Set only via knit360_core.business_status.engine.transition.",
			}
		]
		for doctype in doctypes
	}
	create_custom_fields(fields, ignore_validate=True)
	for doctype in doctypes:
		frappe.clear_cache(doctype=doctype)
	frappe.db.commit()
	return doctypes
