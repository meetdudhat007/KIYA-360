"""Requirement coverage, derived from the running system.

What this answers, and what it refuses to answer.

A client asking "have you met our requirements?" wants evidence, not a claim.
This module produces the evidence by reading the system itself: every field on
every KNIT 360 doctype carries the BRD requirement it came from in its
description -- a rule the structural test suite enforces -- so the link from a
requirement to the thing that implements it is already in the data. Nothing
here is hand-maintained except one small list, described below.

What it will not do is report that a requirement is "met". It cannot, for a
reason that belongs to the BRD rather than to the build: all 238 requirements
are recorded with the detail "TBD -- The BRD does not specify this detail."
A requirement with no stated acceptance condition has nothing to be met
against. So coverage is reported in three honest levels instead:

    Not started   nothing in the system cites this requirement
    Modelled      fields exist that cite it -- the data is designed for it,
                  but no automated check proves any behaviour
    Proven        an acceptance check drives it on a live site and asserts
                  on the result

"Modelled" is deliberately not called "done". A Delivery Note exists and cites
FR-SALES-005, and it moves no stock; saying "done" there would be the exact
overstatement this module is written to avoid.
"""

import json
import pathlib
import re

import frappe

from knit360_core import brd_requirements

#: A requirement id as it appears in a field description. Trailing dots are
#: stripped by the caller, because "FR-FIN-001." ends a sentence.
CODE = re.compile(r"FR-[A-Z]+-[0-9]+(?:\.[0-9]+)*")

#: Ranges such as "FR-QLTY-002..004" appear in a few descriptions, meaning
#: every requirement between the two. Expanded rather than ignored.
RANGE = re.compile(r"(FR-[A-Z]+-)([0-9]+)\.\.([0-9]+)")

NOT_STARTED = "Not started"
MODELLED = "Modelled"
PROVEN = "Proven"

#: Requirements an acceptance check actually exercises against a live site,
#: with the check that does it. This is the one hand-maintained list here, and
#: it is deliberately short: a requirement earns a place only when a named
#: check inserts a document, drives it and asserts on the outcome.
#:
#: Keep it honest. Adding a line that no check backs turns this report into
#: the marketing it exists to replace.
PROVEN_BY = {
	"FR-PADM-1.1.1": "A company created the ordinary way gets its own books",
	"FR-CRM-001": "A lead can be created through the web seam",
	"FR-CRM-002": "A lead converts to a customer and an opportunity",
	"FR-SALES-002": "An opportunity becomes a quotation carrying its value",
	"FR-SALES-003": "A sales order totals with the same engine as the quotation",
	"FR-SALES-004": "Quotation lines compute an amount and a total",
	"FR-FIN-001": "A balanced journal entry posts and the ledger agrees",
	"FR-FIN-003": "A sales invoice posts a receivable and reports it outstanding",
	"FR-FIN-007": "The trial balance balances",
	"FR-HR-003": "An approved application consumes the balance",
	"FR-FIN-002": "A supplier's bill totals goods, freight and tax",
	"FR-TAX-001": "Tax posts to a tax account, never to round-off",
}


def _ids():
	return {row[0] for row in brd_requirements.REQUIREMENTS}


def citations():
	"""requirement id -> {doctype: field count}, read from the doctype JSON.

	Read from the files rather than from frappe.get_meta so the answer is about
	what this app ships, not about anything a site has customised on top.
	"""
	known = _ids()
	found = {}
	app = pathlib.Path(frappe.get_app_path("knit360_core"))

	for path in app.glob("*/doctype/*/*.json"):
		doc = json.loads(path.read_text(encoding="utf-8"))
		if doc.get("doctype") != "DocType":
			continue
		for field in doc.get("fields", []):
			text = field.get("description") or ""
			for prefix, start, end in RANGE.findall(text):
				width = len(start)
				for n in range(int(start), int(end) + 1):
					text += f" {prefix}{str(n).zfill(width)}"
			for code in CODE.findall(text):
				code = code.rstrip(".")
				if code not in known:
					# A description may cite a parent such as FR-PADM-1.4,
					# which covers every requirement beneath it.
					children = [r for r in known if r.startswith(code + ".")]
					if not children:
						continue
					for child in children:
						found.setdefault(child, {}).setdefault(doc["name"], 0)
						found[child][doc["name"]] += 1
					continue
				found.setdefault(code, {}).setdefault(doc["name"], 0)
				found[code][doc["name"]] += 1
	return found


def _implementers(by_doctype):
	"""Separate the doctype that *is* a requirement from ones that reference it.

	Every doctype with a `company` link carries "FR-PADM-1.1.1" on that one
	field, because that is where the Company master is defined. Listing all
	forty of them as implementing "Company Master" is accurate and useless: it
	makes a one-doctype requirement look like forty doctypes of work.

	A doctype that cites a requirement on two or more fields is building it; a
	doctype citing it once is almost always just pointing at it. Where nothing
	clears that bar, every citing doctype is shown, because a single-field
	requirement is real and should not vanish.

	Returns (implementers, other_count).
	"""
	primary = sorted(d for d, n in by_doctype.items() if n >= 2)
	if primary:
		return primary, len(by_doctype) - len(primary)
	return sorted(by_doctype), 0


def _records(doctypes):
	"""How many live documents exist across the doctypes implementing this."""
	total = 0
	for doctype in doctypes:
		if frappe.db.exists("DocType", doctype):
			total += frappe.db.count(doctype)
	return total


def coverage(with_records=True):
	"""One row per requirement, in BRD order."""
	cited = citations()
	rows = []
	for req_id, name, module_no, classification in brd_requirements.REQUIREMENTS:
		by_doctype = cited.get(req_id, {})
		doctypes, referenced_by = _implementers(by_doctype) if by_doctype else ([], 0)
		if req_id in PROVEN_BY and doctypes:
			status = PROVEN
		elif doctypes:
			status = MODELLED
		else:
			status = NOT_STARTED
		rows.append(
			{
				"requirement": req_id,
				"title": name,
				"module_no": module_no,
				"module": brd_requirements.MODULES.get(module_no, ""),
				"classification": classification,
				"status": status,
				"doctypes": ", ".join(d.replace("KNIT 360 ", "") for d in doctypes),
				"referenced_by": referenced_by,
				"field_count": sum(by_doctype.get(d, 0) for d in doctypes),
				"records": _records(doctypes) if with_records else 0,
				"proven_by": PROVEN_BY.get(req_id, "") if status == PROVEN else "",
			}
		)
	return rows


@frappe.whitelist()
def summary():
	"""The headline figures, and the per-module breakdown behind them."""
	rows = coverage(with_records=False)
	counts = {NOT_STARTED: 0, MODELLED: 0, PROVEN: 0}
	per_module = {}

	for row in rows:
		counts[row["status"]] += 1
		module = per_module.setdefault(
			row["module_no"],
			{"module_no": row["module_no"], "module": row["module"], "total": 0,
			 NOT_STARTED: 0, MODELLED: 0, PROVEN: 0},
		)
		module["total"] += 1
		module[row["status"]] += 1

	total = len(rows)
	covered = counts[MODELLED] + counts[PROVEN]
	return {
		"total_requirements": total,
		"not_started": counts[NOT_STARTED],
		"modelled": counts[MODELLED],
		"proven": counts[PROVEN],
		"covered": covered,
		"covered_percent": round(100.0 * covered / total, 1) if total else 0.0,
		"modules_total": len(brd_requirements.MODULES),
		"modules_touched": sum(1 for m in per_module.values() if m["total"] > m[NOT_STARTED]),
		"per_module": [per_module[k] for k in sorted(per_module)],
	}


@frappe.whitelist()
def report():
	"""Everything a client meeting needs, in one call."""
	return {"summary": summary(), "rows": coverage()}


def print_summary():
	"""Readable from the command line, for a screen share.

	bench --site <site> execute knit360_core.traceability.print_summary
	"""
	s = summary()
	print("\nKNIT 360 — requirement coverage against the approved BRD inventory")
	print("=" * 72)
	print(f"  requirements in the BRD      {s['total_requirements']}")
	print(f"  proven by an automated check {s['proven']}")
	print(f"  modelled, not yet proven     {s['modelled']}")
	print(f"  not started                  {s['not_started']}")
	print(f"  covered                      {s['covered']} ({s['covered_percent']}%)")
	print(f"  modules with anything built  {s['modules_touched']} of {s['modules_total']}")
	print("\n  per module")
	print("  " + "-" * 68)
	for m in s["per_module"]:
		built = m["total"] - m[NOT_STARTED]
		print(f"  {m['module'][:34]:<34} {built:>3}/{m['total']:<4} "
		      f"proven {m[PROVEN]:<3} modelled {m[MODELLED]:<3}")
	print()
	return s
