"""What the search bar calls -- knit360_core.search.api.

One endpoint. It returns results the bar can render directly: a label, a line of
context, and the address to go to. The bar decides nothing about what matches.

Permissions are checked per result rather than per query. A row in the index is
not a grant: the index is written by the system with permissions ignored, so a
person who cannot read Sales Invoices must not learn their numbers by typing
into a search box.
"""

import frappe

from knit360_core.search import index


@frappe.whitelist()
def search(text, limit=20, company=None):
	"""Documents matching `text`, as the search bar shows them."""
	rows = index.search_sql(text, limit=int(limit or 20) * 2, company=company)

	out = []
	for row in rows:
		if not frappe.has_permission(row.reference_doctype, "read", doc=row.reference_name):
			continue
		out.append(
			{
				"label": row.title or row.reference_name,
				"description": " · ".join(p for p in (row.record_type, row.subtitle) if p),
				"route": row.route,
				"doctype": row.reference_doctype,
				"name": row.reference_name,
				"record_type": row.record_type,
			}
		)
		if len(out) >= int(limit or 20):
			break
	return out


@frappe.whitelist()
def awesomebar(txt):
	"""The search bar's extra results -- the `awesomebar_search` hook.

	The framework calls every hooked method with what was typed and merges what
	comes back, so this adds KNIT 360's documents to the bar without replacing
	anything the bar already does. Record types and reports keep coming from the
	framework's own sources; only the documents are ours.

	`index` ranks a result. The framework's own "Search for ..." entry scores
	100, so a document that actually matches is put above it -- somebody who
	typed a document number wants the document, not an invitation to search.
	"""
	rows = search(txt, limit=10)
	return [
		{
			"label": row["label"],
			"value": f"{row['label']} ({row['name']})",
			"description": row["description"],
			# The desk route form. A document's address is three parts, and
			# building the URL by hand would break the moment a route changes.
			"route": ["Form", row["doctype"], row["name"]],
			"index": 110,
		}
		for row in rows
	]
