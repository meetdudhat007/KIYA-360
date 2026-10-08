"""The KNIT 360 search index -- the only writer of KNIT 360 Search Index.

**Why this exists rather than the framework's own index.** The framework keeps a
global search table that only ever holds fields a doctype explicitly marks for
it. No field in any of the 93 KNIT 360 record types marked itself, so that table
held zero rows and typing a document number into the search bar returned
nothing. This index holds **one row per document**, written on every insert,
update and rename, so a document is findable the moment it exists.

**What goes into a row.** Everything a person could reasonably type: the
document's own number, and the values of its Data, Select, Link, Date and short
text fields. Not currency, not quantities -- nobody searches for 1180.00 and
matching it would bury the result that was wanted. Child tables are included,
because the item code on a quotation line is exactly what someone searches for.

**How matching works, and its limit.** A typed query is matched with LIKE
against the joined content, after splitting on whitespace: every word must
appear. That gives partial matches -- `SINV-2026` finds `SINV-2026-0001` -- which
a word-based full-text index does not. It is a scan of one narrow table. At this
system's size that is the right trade; past roughly a hundred thousand documents
it becomes the wrong one, and the note in `search_sql` says what to do then.

This module is infrastructure. It implements no BRD requirement, because search
appears in none of the 238 -- see the module exemption in the structural tests.
"""

import frappe
from frappe.utils import now

INDEX = "KNIT 360 Search Index"

#: Fieldtypes worth matching a typed query against.
INDEXED_TYPES = {"Data", "Select", "Link", "Dynamic Link", "Small Text", "Text", "Date", "Datetime"}

#: Never indexed: secrets, and the index itself.
SKIP_TYPES = {"Password"}
SKIP_FIELDS = {"amended_from"}

def is_derived(doctype):
	"""True for a record the system writes, rather than one a person authors.

	Read from the doctype's own `in_create` flag -- the framework labels it
	"User Cannot Create" -- so ledgers and logs are recognised by what they
	are, not by a list of names kept in step by hand.

	Such a row stays indexed, because a ledger entry has a number somebody may
	look up. It just ranks below real documents: its content holds the number
	of the document it came from, so without this, searching for an invoice
	returns that invoice's own ledger rows and audit log above the invoice.
	"""
	return bool(frappe.get_meta(doctype).in_create)


def is_indexable(doctype):
	"""A KNIT 360 parent document, and not this index."""
	if not doctype or not doctype.startswith("KNIT 360 ") or doctype == INDEX:
		return False
	meta = frappe.get_meta(doctype)
	return not meta.istable and not meta.issingle


def _values(doc, meta):
	"""Every searchable value on a document, including its child rows."""
	out = [doc.name]
	for field in meta.fields:
		if field.fieldtype in SKIP_TYPES or field.fieldname in SKIP_FIELDS:
			continue
		if field.fieldtype == "Table":
			for row in doc.get(field.fieldname) or []:
				out.extend(_values(row, frappe.get_meta(field.options)))
			continue
		if field.fieldtype not in INDEXED_TYPES:
			continue
		value = doc.get(field.fieldname)
		if value not in (None, ""):
			out.append(str(value))
	return out


def _title(doc, meta):
	"""What to show as the result's headline.

	The document's title field if it declares one and it is filled, otherwise
	its number -- never an empty string, because a result you cannot read is
	not a result.
	"""
	if meta.title_field:
		title = doc.get(meta.title_field)
		if title:
			return str(title)[:140]
	return doc.name


def _subtitle(doc, meta):
	"""Enough to tell two similar results apart: the status, and the number.

	A search for a customer's name can return four quotations. Without this the
	person has to open each one.
	"""
	parts = []
	status = doc.get("knit360_business_status")
	if status:
		parts.append(str(status))
	if _title(doc, meta) != doc.name:
		parts.append(doc.name)
	return " · ".join(parts)[:140]


def route_for(doctype, name):
	"""The address that opens this document."""
	return f"/app/{frappe.scrub(doctype).replace('_', '-')}/{name}"


def index_document(doc, method=None):
	"""Write, or rewrite, this document's row. The only entry point for writes.

	Delete-then-insert rather than update, because a document's fields change
	shape over its life and a stale fragment of old content is worse than a
	rebuild of one row.
	"""
	if not is_indexable(doc.doctype):
		return
	# A delete can still move a field on its way out -- Frappe cancels before
	# it trashes -- and an index row written after the document has gone is a
	# result that opens nothing.
	if doc.flags.get("in_delete"):
		return
	meta = frappe.get_meta(doc.doctype)

	# A business status moves by db_set, which fires on_change and not
	# on_update, so both are hooked -- otherwise the bar went on describing an
	# invoice as Overdue after it had been paid. Hooking both means an
	# ordinary save indexes twice, so a row that would be written identically
	# is left where it is.
	fresh = {
		"title": _title(doc, meta),
		"subtitle": _subtitle(doc, meta),
		"content": " ".join(_values(doc, meta)),
	}
	existing = frappe.db.get_value(
		INDEX,
		{"reference_doctype": doc.doctype, "reference_name": doc.name},
		["title", "subtitle", "content"],
		as_dict=True,
	)
	if existing and all(existing.get(key) == value for key, value in fresh.items()):
		return

	remove_document(doc)
	row = frappe.get_doc(
		{
			"doctype": INDEX,
			"reference_doctype": doc.doctype,
			"reference_name": doc.name,
			"record_type": doc.doctype.replace("KNIT 360 ", ""),
			"route": route_for(doc.doctype, doc.name),
			"indexed_at": now(),
			"title": fresh["title"],
			"subtitle": fresh["subtitle"],
			"company": doc.get("company") or "",
			"weight": 1 if is_derived(doc.doctype) else 0,
			"content": fresh["content"],
		}
	)
	# Says "this write came from here". The row refuses any other author.
	row.flags.written_by_indexer = True
	row.insert(ignore_permissions=True)


def remove_document(doc, method=None):
	"""Drop this document's row. Called on delete, and before a rewrite."""
	if not is_indexable(doc.doctype):
		return
	frappe.db.delete(INDEX, {"reference_doctype": doc.doctype, "reference_name": doc.name})


def rename_document(doc, method=None, old=None, new=None, merge=False):
	"""A renamed document keeps its row, but the row no longer describes it.

	The number is part of the content and the whole of the route, so the row is
	rebuilt rather than patched.
	"""
	if not is_indexable(doc.doctype):
		return
	if old:
		frappe.db.delete(INDEX, {"reference_doctype": doc.doctype, "reference_name": old})
	index_document(doc)


# --- reading ------------------------------------------------------------


def search_sql(text, limit=20, company=None):
	"""Rows matching every word in `text`.

	Ordered so an exact number match comes first -- somebody who typed a
	document number wants that document, not a document mentioning it.

	Should this table ever outgrow a scan, the replacement is a FULLTEXT index
	on `content` with a BOOLEAN MODE query, plus a prefix branch for the
	`PREFIX-YYYY-` case that full text cannot match. Nothing above this
	function would change.
	"""
	words = [w for w in (text or "").split() if w]
	if not words:
		return []

	conditions, values = [], {}
	for i, word in enumerate(words):
		conditions.append(f"content LIKE %(w{i})s")
		values[f"w{i}"] = f"%{word}%"
	where = " AND ".join(conditions)

	if company:
		where += " AND (company = %(company)s OR company = '')"
		values["company"] = company

	values["exact"] = text.strip()
	values["starts"] = f"{text.strip()}%"
	values["limit"] = int(limit)

	return frappe.db.sql(
		f"""
		SELECT reference_doctype, reference_name, record_type, route,
		       title, subtitle, company, weight
		FROM `tab{INDEX}`
		WHERE {where}
		ORDER BY
		    CASE WHEN reference_name = %(exact)s THEN 0
		         WHEN reference_name LIKE %(starts)s THEN 1
		         WHEN title LIKE %(starts)s THEN 2
		         ELSE 3 END,
		    weight,
		    reference_name DESC
		LIMIT %(limit)s
		""",
		values,
		as_dict=True,
	)


# --- maintenance --------------------------------------------------------


def rebuild(doctype=None):
	"""Index every document, or every document of one type.

	Run after the index is first installed, and after any bulk change made
	outside the document API -- a renumbering, an import, a restore.
	"""
	doctypes = [doctype] if doctype else sorted(
		d for d in frappe.get_all(
			"DocType",
			filters={"module": ["in", frappe.get_module_list("knit360_core")], "istable": 0},
			pluck="name",
		) if is_indexable(d)
	)

	if not doctype:
		frappe.db.delete(INDEX)

	counts = {}
	for name in doctypes:
		if doctype:
			frappe.db.delete(INDEX, {"reference_doctype": name})
		rows = frappe.get_all(name, pluck="name")
		for row in rows:
			index_document(frappe.get_doc(name, row))
		if rows:
			counts[name.replace("KNIT 360 ", "")] = len(rows)
		frappe.db.commit()

	total = sum(counts.values())
	print(f"indexed {total} documents across {len(counts)} record types")
	return counts


def top_up():
	"""Index only the documents that have no row yet.

	Run on every migrate. When nothing is missing it costs one count per record
	type and writes nothing, so it is safe to leave in the hook; when a restore
	or an import has put documents in behind the document API, it quietly
	repairs the index instead of leaving a silent gap.
	"""
	added = {}
	for name in frappe.get_all(
		"DocType",
		filters={"module": ["in", frappe.get_module_list("knit360_core")], "istable": 0},
		pluck="name",
	):
		if not is_indexable(name):
			continue
		indexed = set(
			frappe.get_all(INDEX, filters={"reference_doctype": name}, pluck="reference_name")
		)
		missing = [n for n in frappe.get_all(name, pluck="name") if n not in indexed]
		for row in missing:
			index_document(frappe.get_doc(name, row))
		if missing:
			added[name.replace("KNIT 360 ", "")] = len(missing)
	if added:
		frappe.db.commit()
		print(f"search index topped up: {added}")
	return added


def coverage():
	"""How many documents exist, and how many of them are findable.

	A search index nobody checks is a search index that silently stops being
	true. This is what the acceptance check asserts on.
	"""
	# Counted per doctype, so a gap names the record type it is in rather than
	# only saying the totals disagree.
	missing, indexed, total = {}, 0, 0
	for name in frappe.get_all(
		"DocType",
		filters={"module": ["in", frappe.get_module_list("knit360_core")], "istable": 0},
		pluck="name",
	):
		if not is_indexable(name):
			continue
		count = frappe.db.count(name)
		if not count:
			continue
		rows = frappe.db.count(INDEX, {"reference_doctype": name})
		total += count
		indexed += rows
		if rows != count:
			missing[name.replace("KNIT 360 ", "")] = f"{rows} of {count}"
	return {"documents": total, "indexed": indexed, "incomplete": missing}
