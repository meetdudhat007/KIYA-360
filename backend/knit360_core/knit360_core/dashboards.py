"""Charts and number cards for the KNIT 360 workspaces -- FR-FIN-007, FR-CRM-006.

Worth being precise about what this is, because the licence question hangs on it.

Dashboard Chart, Number Card, Dashboard Chart Source and the frappe-charts
rendering library are all **Frappe framework, MIT**. None of them is ERPNext.
So the whole charting apparatus is ours to use outright, with no obligation.

What ERPNext adds on top is chart *definitions* -- which doctype, which field,
grouped how. A definition like "count of invoices by month" is a fact about your
own data, not someone's creative expression. The definitions below are written
against KNIT 360's own doctypes and fields, which ERPNext does not have.

Charts are created with is_public so they appear for every user, and are
rebuilt from here on every migrate so they cannot drift from the doctypes.
"""

import json

import frappe

CHART = "Dashboard Chart"
CARD = "Number Card"
PREFIX = "KNIT 360 "
STATUS = "knit360_business_status"


def _json(value):
	return json.dumps(value)


#: Charts. Named without a prefix, because Frappe's workspace chart block finds
#: its widget by matching the block's chart_name against the Workspace Chart
#: row's *label* (blocks/block.js make()). Name, label and reference therefore
#: have to be one and the same string -- a mismatch renders nothing, silently.
#: Each is (name, doctype, spec).
#: "group" charts count or sum by a field; "time" charts plot a value over time.
CHARTS = [
	{
		"name": "Leads by Status",
		"doctype": PREFIX + "Lead",
		"kind": "group", "field": STATUS, "agg": "Count",
		"type": "Donut", "color": "#1d4ed8",
	},
	{
		"name": "Opportunities by Status",
		"doctype": PREFIX + "Opportunity",
		"kind": "group", "field": STATUS, "agg": "Count",
		"type": "Bar", "color": "#0891b2",
	},
	{
		"name": "Opportunity Value by Status",
		"doctype": PREFIX + "Opportunity",
		"kind": "group", "field": STATUS, "agg": "Sum", "agg_field": "estimated_deal_value",
		"type": "Bar", "color": "#7c3aed", "currency": "INR",
	},
	{
		"name": "Quotations by Status",
		"doctype": PREFIX + "Quotation",
		"kind": "group", "field": STATUS, "agg": "Count",
		"type": "Donut", "color": "#ea580c",
	},
	{
		"name": "Sales Orders by Status",
		"doctype": PREFIX + "Sales Order",
		"kind": "group", "field": STATUS, "agg": "Count",
		"type": "Bar", "color": "#16a34a",
	},
	{
		"name": "Invoiced Value by Month",
		"doctype": PREFIX + "Sales Invoice",
		"kind": "time", "date_field": "posting_date", "value_field": "grand_total",
		"type": "Bar", "color": "#1d4ed8", "currency": "INR",
	},
	{
		"name": "Invoices by Status",
		"doctype": PREFIX + "Sales Invoice",
		"kind": "group", "field": STATUS, "agg": "Count",
		"type": "Pie", "color": "#b45309",
	},
	{
		"name": "Purchase Orders by Status",
		"doctype": PREFIX + "Purchase Order",
		"kind": "group", "field": STATUS, "agg": "Count",
		"type": "Bar", "color": "#0f766e",
	},
]

#: Number cards. The headline figures a workspace opens with.
#: Named by label -- Number Card has no autoname and Frappe falls back to the
#: label, so the label IS the document name and PLACEMENT must match it.
CARDS = [
	{"name": "Open Leads", "doctype": PREFIX + "Lead", "function": "Count",
	 "filters": [[PREFIX + "Lead", STATUS, "not in", ["Converted", "Disqualified", "Lost"]]],
	 "color": "#1d4ed8"},
	{"name": "Open Opportunities", "doctype": PREFIX + "Opportunity", "function": "Count",
	 "filters": [[PREFIX + "Opportunity", STATUS, "not in", ["Won", "Lost"]]],
	 "color": "#0891b2"},
	{"name": "Pipeline Value", "doctype": PREFIX + "Opportunity", "function": "Sum",
	 "based_on": "estimated_deal_value",
	 "filters": [[PREFIX + "Opportunity", STATUS, "not in", ["Won", "Lost"]]],
	 "color": "#7c3aed"},
	{"name": "Quotations Awaiting Reply", "doctype": PREFIX + "Quotation", "function": "Count",
	 "filters": [[PREFIX + "Quotation", STATUS, "=", "Issued / Sent"]],
	 "color": "#ea580c"},
	{"name": "Unpaid Invoices", "doctype": PREFIX + "Sales Invoice", "function": "Count",
	 "filters": [[PREFIX + "Sales Invoice", STATUS, "in", ["Posted / Unpaid", "Partly Paid", "Overdue"]]],
	 "color": "#b91c1c"},
	{"name": "Amount Outstanding", "doctype": PREFIX + "Sales Invoice", "function": "Sum",
	 "based_on": "outstanding_amount",
	 "filters": [[PREFIX + "Sales Invoice", STATUS, "in", ["Posted / Unpaid", "Partly Paid", "Overdue"]]],
	 "color": "#b91c1c"},
]

#: Which workspace shows what.
PLACEMENT = {
	"KNIT 360": {
		"cards": ["Open Leads", "Open Opportunities",
		          "Quotations Awaiting Reply", "Amount Outstanding"],
		"charts": ["Leads by Status", "Opportunities by Status",
		           "Quotations by Status", "Invoiced Value by Month"],
	},
	"CRM": {
		"cards": ["Open Leads", "Open Opportunities", "Pipeline Value"],
		"charts": ["Leads by Status", "Opportunity Value by Status"],
	},
	"Sales": {
		"cards": ["Quotations Awaiting Reply"],
		"charts": ["Quotations by Status", "Sales Orders by Status"],
	},
	"Finance": {
		"cards": ["Unpaid Invoices", "Amount Outstanding"],
		"charts": ["Invoiced Value by Month", "Invoices by Status"],
	},
	"Procurement": {
		"cards": [],
		"charts": ["Purchase Orders by Status"],
	},
}


def _exists(doctype):
	return frappe.db.exists("DocType", doctype)


def _has_field(doctype, fieldname):
	return bool(frappe.get_meta(doctype).get_field(fieldname))


def build_charts():
	built = []
	for spec in CHARTS:
		if not _exists(spec["doctype"]):
			continue
		doc = (frappe.get_doc(CHART, spec["name"])
		       if frappe.db.exists(CHART, spec["name"]) else frappe.new_doc(CHART))
		doc.chart_name = spec["name"]
		doc.document_type = spec["doctype"]
		doc.is_public = 1
		doc.type = spec["type"]
		doc.color = spec["color"]
		doc.filters_json = _json([])
		doc.dynamic_filters_json = _json([])
		# Frappe defaults this Link to the global currency, and chart_widget.js
		# formats every value as money the moment it is set. Correct for a chart
		# of amounts, nonsense for a chart that counts documents -- "3 leads"
		# renders as "₹ 3.00". Set it only where the aggregate really is money.
		doc.currency = None

		if spec["kind"] == "group":
			if not _has_field(spec["doctype"], spec["field"]):
				continue
			doc.chart_type = "Group By"
			doc.group_by_type = spec["agg"]
			doc.group_by_based_on = spec["field"]
			doc.number_of_groups = 0
			doc.timeseries = 0
			if spec["agg"] == "Sum":
				if not _has_field(spec["doctype"], spec["agg_field"]):
					continue
				doc.aggregate_function_based_on = spec["agg_field"]
				doc.currency = spec.get("currency")
			else:
				doc.aggregate_function_based_on = None
		else:
			if not (_has_field(spec["doctype"], spec["date_field"])
			        and _has_field(spec["doctype"], spec["value_field"])):
				continue
			doc.chart_type = "Sum"
			doc.based_on = spec["date_field"]
			doc.value_based_on = spec["value_field"]
			doc.timeseries = 1
			doc.timespan = "Last Year"
			doc.time_interval = "Monthly"
			doc.currency = spec.get("currency")

		doc.save(ignore_permissions=True)
		built.append(doc.name)
	return built


def build_cards():
	built = []
	for spec in CARDS:
		if not _exists(spec["doctype"]) or not _has_field(spec["doctype"], STATUS):
			continue
		if spec.get("based_on") and not _has_field(spec["doctype"], spec["based_on"]):
			continue
		doc = (frappe.get_doc(CARD, spec["name"])
		       if frappe.db.exists(CARD, spec["name"]) else frappe.new_doc(CARD))
		doc.label = spec["name"]
		doc.document_type = spec["doctype"]
		doc.type = "Document Type"
		doc.function = spec["function"]
		doc.aggregate_function_based_on = spec.get("based_on")
		doc.filters_json = _json(spec["filters"])
		doc.dynamic_filters_json = _json([])
		doc.is_public = 1
		doc.show_percentage_stats = 1
		doc.stats_time_interval = "Monthly"
		doc.color = spec["color"]
		doc.save(ignore_permissions=True)
		built.append(doc.name)
	return built


def place_on_workspaces():
	"""Attach the charts and cards to their workspaces, above the links.

	knit360_core.desk owns the link blocks; this prepends the visual ones, so
	the two can be rebuilt independently without fighting over content.
	"""
	placed = []
	for workspace, spec in PLACEMENT.items():
		if not frappe.db.exists("Workspace", workspace):
			continue
		doc = frappe.get_doc("Workspace", workspace)
		cards = [c for c in spec["cards"] if frappe.db.exists(CARD, c)]
		charts = [c for c in spec["charts"] if frappe.db.exists(CHART, c)]

		doc.number_cards = []
		for card in cards:
			doc.append("number_cards", {"number_card_name": card, "label": card})
		doc.charts = []
		for chart in charts:
			doc.append("charts", {"chart_name": chart, "label": chart})

		# Rebuild content: visuals first, then whatever desk.py laid out.
		existing = [b for b in json.loads(doc.content or "[]")
		            if b.get("type") not in ("chart", "number_card")
		            and not (b.get("type") == "header"
		                     and b.get("data", {}).get("text", "").find("At a glance") >= 0)]
		blocks = []
		if cards:
			blocks.append(_header("At a glance"))
			blocks += [{"id": _bid("c", c), "type": "number_card",
			            "data": {"number_card_name": c, "col": 3}} for c in cards]
		if charts:
			blocks += [{"id": _bid("g", c), "type": "chart",
			            "data": {"chart_name": c, "col": 6}} for c in charts]
		doc.content = json.dumps(blocks + existing)
		doc.save(ignore_permissions=True)
		placed.append(workspace)
	return placed


def _header(text):
	return {"id": _bid("h", text), "type": "header",
	        "data": {"text": f"<span class='h4'><b>{text}</b></span>", "col": 12}}


def _bid(kind, seed):
	return f"knit{kind}{abs(hash(seed)) % 10**8}"


def build():
	charts = build_charts()
	cards = build_cards()
	placed = place_on_workspaces()
	frappe.db.commit()
	frappe.clear_cache()
	return {"charts": charts, "cards": cards, "workspaces": placed}


def after_migrate():
	build()
