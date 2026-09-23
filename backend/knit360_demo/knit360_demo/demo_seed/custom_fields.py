"""knit360_core custom fields.

Both fields exist because the BRD requires data core ERPNext has no field for:

- Role.knit360_approval_authority -- BRD FR-PADM-1.2.4 (Approval Authority).
  Frappe's Role doctype has no monetary approval ceiling.

- Item.knit360_hsn_sac_code -- BRD Section 1.4 Item Master ("item code, category,
  HSN/SAC"). India GST localization was removed from the core ERPNext tree
  (see docs/00-requirements/24-erpnext-kiya-gap-analysis.md, module 18), so
  gst_hsn_code is not present unless the separate india_compliance app is
  installed. Tax & Statutory Compliance is a KNIT 360-owned seam, so the field is
  owned here.

Fields are defined in knit360_core only; no ERPNext or Frappe file is modified.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

CUSTOM_FIELDS = {
	"Role": [
		{
			"fieldname": "knit360_approval_authority",
			"label": "Approval Authority",
			"fieldtype": "Currency",
			"insert_after": "desk_access",
			"description": "BRD FR-PADM-1.2.4. Maximum transaction value this role may approve.",
		}
	],
	"Item": [
		{
			"fieldname": "knit360_hsn_sac_code",
			"label": "HSN/SAC Code",
			"fieldtype": "Data",
			"insert_after": "item_group",
			"description": "BRD Section 1.4 Item Master.",
		}
	],
}


def install():
	"""Create or update the knit360_core custom fields. Idempotent."""
	create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
	for doctype in CUSTOM_FIELDS:
		frappe.clear_cache(doctype=doctype)
