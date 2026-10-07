"""One-time renumbering of every counter-named document -- FR-PADM-1.6.1.

**Why this exists.** `format:SINV-{YYYY}-{####}` hands Frappe's counter an empty
prefix, because `_format_autoname` parses each `{...}` on its own. Every document
type in KNIT 360 therefore drew from a single shared pool. These four documents
were created in the same second:

    OPP-2026-0163   QTN-2026-0164   SO-2026-0165   SINV-2026-0166

Consecutive numbers, four different document types. There was no SINV-2026-0001,
the gaps could not be explained, and the year was decoration because the counter
never reset.

The doctypes now use `SINV-.YYYY.-.####`, which gives a counter key of
`SINV-2026-`: one counter per document type per year. This module brings the
documents that already exist into line with that, numbering each type from 0001
in creation order and leaving each counter where the last one ends.

**This is a one-time data migration, not a feature.** It renames posted
documents. That is acceptable here and only here: this site holds demonstration
data with no external references to its numbers. Run it against a client's books
and the invoice numbers their customers already hold stop matching. The guard in
`run()` makes that refusal explicit rather than relying on anyone remembering.

**What a rename does and does not carry.** Frappe updates Link and Dynamic Link
fields across the whole database by itself, and rewrites child rows' `parent`.
It does not touch a plain `Data` field, and KNIT 360 holds document references in
several of those -- `GL Entry.voucher_no` among them. So after the renames this
module sweeps every Data column of every KNIT 360 doctype for exact matches and
rewrites them, rather than trusting a hand-written list to stay complete.
"""

import inspect
import re

import frappe

#: Set this true in a session to allow the run on a site that is not the
#: demonstration site. Nothing in the app sets it.
OVERRIDE_SITE_GUARD = False

#: Companies this site is allowed to hold for the run to be considered
#: demonstration data.
DEMO_COMPANIES = {"KNIT 360 Demo Co", "Kelvinotherm Induction LLP", "KNIT Acceptance Co"}


def counter_named():
	"""Every KNIT 360 doctype whose name comes from a series, and its series."""
	out = {}
	for doctype in frappe.get_all(
		"DocType",
		filters={"module": ["in", frappe.get_module_list("knit360_core")], "istable": 0},
		pluck="name",
	):
		autoname = frappe.db.get_value("DocType", doctype, "autoname") or ""
		if "#" in autoname and autoname.split(":")[0] not in ("field", "naming_series"):
			out[doctype] = autoname
	return out


def _render(series, year, number):
	"""Build one name from a dot series, e.g. SINV-.YYYY.-.#### -> SINV-2026-0001."""
	name = ""
	for part in series.split("."):
		if not part:
			continue
		if part.startswith("#"):
			name += str(number).zfill(len(part))
		elif part == "YYYY":
			name += str(year)
		elif part == "YY":
			name += str(year)[-2:]
		else:
			name += part
	return name


def plan():
	"""old name -> new name, per doctype, in creation order.

	Numbered within a year when the series carries one, so a document created in
	2026 keeps 2026 in its name. A document whose name is already what the plan
	would give it is left out, which is what makes a second run a no-op.
	"""
	mapping = {}
	for doctype, series in sorted(counter_named().items()):
		rows = frappe.get_all(doctype, fields=["name", "creation"], order_by="creation asc, name asc")
		if not rows:
			continue
		per_year = {}
		pairs = {}
		for row in rows:
			year = row.creation.year
			key = year if "YYYY" in series or "YY" in series else "all"
			per_year[key] = per_year.get(key, 0) + 1
			new = _render(series, year, per_year[key])
			if new != row.name:
				pairs[row.name] = new
		if pairs:
			mapping[doctype] = pairs
	return mapping


def _data_columns():
	"""Every Data column on a KNIT 360 doctype, parent and child alike.

	A document reference hiding in one of these is the whole reason the sweep
	exists, and listing them by hand is how one gets missed.
	"""
	columns = []
	for doctype in frappe.get_all(
		"DocType", filters={"module": ["in", frappe.get_module_list("knit360_core")]}, pluck="name"
	):
		for field in frappe.get_meta(doctype).fields:
			if field.fieldtype == "Data":
				columns.append((doctype, field.fieldname))
	return columns


def _long_text_mentions(old_names):
	"""Small Text / Text Editor values that contain an old name.

	These are NOT rewritten. A remark reading "settled against SINV-2026-0166"
	is prose, and a blind substitution inside prose is how a migration quietly
	corrupts an audit trail. They are reported so the decision is visible.
	"""
	found = []
	for doctype in frappe.get_all(
		"DocType", filters={"module": ["in", frappe.get_module_list("knit360_core")]}, pluck="name"
	):
		# The search index is derived from the documents, so of course it
		# mentions their old numbers. It is rebuilt after the renames, and
		# reporting it here would bury the mentions that need a human decision.
		if doctype == "KNIT 360 Search Index":
			continue
		for field in frappe.get_meta(doctype).fields:
			if field.fieldtype not in ("Small Text", "Text", "Text Editor", "Long Text"):
				continue
			for old in old_names:
				hits = frappe.db.sql(
					f"SELECT name FROM `tab{doctype}` WHERE `{field.fieldname}` LIKE %s LIMIT 3",
					(f"%{old}%",),
				)
				for (row,) in hits:
					found.append((doctype, field.fieldname, row, old))
	return found


def _allow_rename(doctypes, allowed):
	"""Flip allow_rename on the DocType rows for the duration of the run.

	26 of the 36 doctypes are declared `allow_rename: 0`, which is correct -- a
	user must not be able to rename a posted invoice. This migration is not a
	user, so the flag is lifted for the renames and put back afterwards. It is
	changed in the database only; the JSON on disk keeps saying 0.
	"""
	for doctype in doctypes:
		frappe.db.set_value("DocType", doctype, "allow_rename", 1 if allowed else 0,
		                    update_modified=False)
	frappe.clear_cache()


def _rename_kwargs():
	"""Only the keyword arguments this Frappe's rename_doc actually declares."""
	available = inspect.signature(frappe.rename_doc).parameters
	wanted = {"force": True, "merge": False, "ignore_permissions": True,
	          "show_alert": False, "validate": False}
	return {k: v for k, v in wanted.items() if k in available}


def _reset_counters():
	"""Point each series at the last number used, and drop the shared one.

	The empty-key row is the defect itself: one counter for the whole system.
	It is removed rather than left at 1118, so a doctype that somehow still
	resolves to an empty prefix starts from 1 and the mistake is visible
	immediately instead of hiding behind a plausible number.
	"""
	counters = {}
	for doctype, series in sorted(counter_named().items()):
		for row in frappe.get_all(doctype, pluck="name"):
			prefix = re.match(r"^(.*?)(\d+)$", row)
			if not prefix:
				continue
			key, number = prefix.group(1), int(prefix.group(2))
			counters[key] = max(counters.get(key, 0), number)

	for key, current in sorted(counters.items()):
		frappe.db.sql(
			"INSERT INTO tabSeries (name, current) VALUES (%s, %s) "
			"ON DUPLICATE KEY UPDATE current = %s",
			(key, current, current),
		)
	frappe.db.sql("DELETE FROM tabSeries WHERE name = ''")
	return counters


def run(apply=False):
	"""Show the plan, or carry it out.

	Called with no argument it changes nothing and prints what it would do.
	"""
	companies = set(frappe.get_all("KNIT 360 Company", pluck="name"))
	if not OVERRIDE_SITE_GUARD and not companies <= DEMO_COMPANIES:
		frappe.throw(
			f"This site holds companies outside the demonstration set: "
			f"{sorted(companies - DEMO_COMPANIES)}. Renumbering rewrites document "
			f"numbers that people outside this system may already hold. Refusing."
		)

	mapping = plan()
	total = sum(len(pairs) for pairs in mapping.values())
	if not total:
		# Nothing to rename, but the counters may still have run ahead: an
		# acceptance run creates documents, numbers them, and deletes them
		# again, and a counter never goes backwards on its own. So this is
		# also how the numbering is tidied after a test run.
		if not apply:
			print("Nothing to renumber. Call run(apply=True) to reset the counters.")
			return {}
		counters = _reset_counters()
		frappe.db.commit()
		print(f"Nothing to rename. {len(counters)} counters reset to the last number in use.")
		return {"renamed": 0, "counters": counters}

	print(f"{total} documents across {len(mapping)} document types\n")
	for doctype, pairs in mapping.items():
		sample = list(pairs.items())[:3]
		shown = ", ".join(f"{old} -> {new}" for old, new in sample)
		more = f" (+{len(pairs) - len(sample)} more)" if len(pairs) > len(sample) else ""
		print(f"  {doctype.replace('KNIT 360 ', ''):28} {len(pairs):4}   {shown}{more}")

	# A collision would mean renaming onto a name already in use.
	for doctype, pairs in mapping.items():
		taken = set(frappe.get_all(doctype, pluck="name")) - set(pairs)
		clash = set(pairs.values()) & taken
		if clash:
			frappe.throw(f"{doctype}: {sorted(clash)[:5]} already exist. Refusing.")

	old_names = [old for pairs in mapping.values() for old in pairs]
	prose = _long_text_mentions(old_names)
	if prose:
		print(f"\n  {len(prose)} mention(s) of an old number inside free text, NOT rewritten:")
		for doctype, fieldname, row, old in prose[:10]:
			print(f"     {doctype}.{fieldname} on {row} mentions {old}")

	if not apply:
		print("\nDry run. Nothing changed. Call run(apply=True) to carry it out.")
		return mapping

	renamed = 0
	kwargs = _rename_kwargs()
	_allow_rename(mapping, True)
	try:
		for doctype, pairs in mapping.items():
			for old, new in pairs.items():
				frappe.rename_doc(doctype, old, new, **kwargs)
				renamed += 1
	finally:
		_allow_rename(mapping, False)

	# Data columns Frappe did not follow, swept by value rather than by a list.
	swept = {}
	for doctype, fieldname in _data_columns():
		for pairs in mapping.values():
			for old, new in pairs.items():
				count = frappe.db.sql(
					f"UPDATE `tab{doctype}` SET `{fieldname}` = %s WHERE `{fieldname}` = %s",
					(new, old),
				)
				affected = frappe.db._cursor.rowcount
				if affected:
					swept[f"{doctype}.{fieldname}"] = swept.get(f"{doctype}.{fieldname}", 0) + affected

	counters = _reset_counters()
	frappe.db.commit()

	print(f"\nrenamed   {renamed}")
	print(f"swept     {swept or 'no plain-text references needed rewriting'}")
	print(f"counters  {len(counters)} set; the shared empty-key counter is gone")
	return {"renamed": renamed, "swept": swept, "counters": counters}
