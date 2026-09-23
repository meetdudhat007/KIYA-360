"""Shared seeding helpers.

No field name is assumed anywhere in this package: assert_fields checks each
one against the installed doctype metadata and raises naming the missing
fields, rather than silently writing bad data.
"""

import frappe


def assert_fields(doctype, fieldnames):
	"""Raise if the installed doctype lacks any of these fields."""
	meta = frappe.get_meta(doctype)
	missing = [f for f in fieldnames if meta.get_field(f) is None]
	if missing:
		frappe.throw(
			f"{doctype} has no field(s): {', '.join(missing)}. "
			f"Check the installed app version before seeding."
		)


def insert_if_absent(doctype, filters, values):
	"""Insert a document unless one matching filters exists. Returns its name."""
	existing = frappe.db.exists(doctype, filters)
	if existing:
		return existing

	doc = frappe.get_doc(dict(doctype=doctype, **values))
	doc.insert(ignore_permissions=True)
	return doc.name


def submit_new(doc):
	"""Insert and submit a mapped document. Returns its name."""
	doc.insert(ignore_permissions=True)
	doc.submit()
	return doc.name


def require(doctype, name, hint):
	"""Raise if a prerequisite record is missing."""
	if not frappe.db.exists(doctype, name):
		frappe.throw(f"{doctype} '{name}' does not exist. {hint}")
	return name
