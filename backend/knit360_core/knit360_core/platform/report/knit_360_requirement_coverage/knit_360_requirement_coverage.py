"""Requirement coverage, as a report you can open in front of a client.

Every row is one of the 238 BRD requirements. The status column is derived from
the system itself -- see knit360_core.traceability for how, and for why this
reports what is modelled and proven rather than what is "met".

Filters default to showing everything, including the 171 requirements nothing
has been built for. That is deliberate. A coverage report that hides its own
gaps is worth less than no report, because the first gap a client finds on
their own costs more trust than all of them disclosed at once.
"""

import frappe
from frappe import _

from knit360_core import brd_requirements, traceability

STATUS_COLOUR = {
	traceability.PROVEN: "green",
	traceability.MODELLED: "blue",
	traceability.NOT_STARTED: "gray",
}


def execute(filters=None):
	filters = frappe._dict(filters or {})
	rows = traceability.coverage()

	if filters.get("module"):
		rows = [r for r in rows if r["module"] == filters.module]
	if filters.get("status"):
		rows = [r for r in rows if r["status"] == filters.status]
	if filters.get("only_gaps"):
		rows = [r for r in rows if r["status"] == traceability.NOT_STARTED]

	data = [
		{
			"requirement": r["requirement"],
			"title": r["title"],
			"module": f"{r['module_no']:02d} {r['module']}",
			"status": r["status"],
			"doctypes": r["doctypes"],
			"field_count": r["field_count"],
			"referenced_by": r["referenced_by"],
			"records": r["records"],
			"proven_by": r["proven_by"],
		}
		for r in rows
	]
	# Frappe's order is (columns, data, message, chart, report_summary).
	# Getting chart and report_summary the wrong way round throws
	# "e.forEach is not a function" out of render_summary and the table never
	# draws -- which is exactly what happened the first time.
	return columns(), data, message(rows), chart(rows), cards()


def columns():
	return [
		{"label": _("Requirement"), "fieldname": "requirement", "fieldtype": "Data", "width": 130},
		{"label": _("What the BRD calls it"), "fieldname": "title", "fieldtype": "Data", "width": 220},
		{"label": _("BRD Module"), "fieldname": "module", "fieldtype": "Data", "width": 200},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": _("Built as"), "fieldname": "doctypes", "fieldtype": "Data", "width": 240},
		{"label": _("Fields"), "fieldname": "field_count", "fieldtype": "Int", "width": 70},
		{"label": _("Also linked from"), "fieldname": "referenced_by", "fieldtype": "Int", "width": 120},
		{"label": _("Live records"), "fieldname": "records", "fieldtype": "Int", "width": 100},
		{"label": _("Proven by this check"), "fieldname": "proven_by", "fieldtype": "Data", "width": 300},
	]


def message(rows):
	"""The headline, stated above the table so nobody has to total it up."""
	summary = traceability.summary()
	return _(
		"<b>{covered} of {total} BRD requirements are covered ({percent}%)</b> &mdash; "
		"{proven} proven by an automated check that drives a live site, "
		"{modelled} modelled but not yet proven, "
		"{gaps} not started. "
		"{touched} of {modules} BRD modules have anything built.<br><br>"
		"<i>Every requirement in the BRD carries the detail "
		"&ldquo;TBD &mdash; The BRD does not specify this detail.&rdquo; "
		"With no stated acceptance condition there is nothing to test &ldquo;met&rdquo; "
		"against, so this reports what the system models and what it proves.</i>"
	).format(
		covered=summary["covered"],
		total=summary["total_requirements"],
		percent=summary["covered_percent"],
		proven=summary["proven"],
		modelled=summary["modelled"],
		gaps=summary["not_started"],
		touched=summary["modules_touched"],
		modules=summary["modules_total"],
	)


def cards():
	"""The three figures to read out first, as cards above the table."""
	s = traceability.summary()
	return [
		{"label": _("Proven by a live check"), "value": s["proven"],
		 "indicator": "Green", "datatype": "Int"},
		{"label": _("Modelled, not yet proven"), "value": s["modelled"],
		 "indicator": "Blue", "datatype": "Int"},
		{"label": _("Not started"), "value": s["not_started"],
		 "indicator": "Grey", "datatype": "Int"},
		{"label": _("BRD modules with anything built"),
		 "value": f"{s['modules_touched']} / {s['modules_total']}", "datatype": "Data"},
	]


def chart(rows):
	counts = {traceability.PROVEN: 0, traceability.MODELLED: 0, traceability.NOT_STARTED: 0}
	for row in rows:
		counts[row["status"]] += 1
	return {
		"data": {
			"labels": [traceability.PROVEN, traceability.MODELLED, traceability.NOT_STARTED],
			"datasets": [
				{
					"name": _("Requirements"),
					"values": [
						counts[traceability.PROVEN],
						counts[traceability.MODELLED],
						counts[traceability.NOT_STARTED],
					],
				}
			],
		},
		"type": "donut",
		"height": 260,
		"colors": ["#16a34a", "#2d4a6b", "#9ca3af"],
	}
