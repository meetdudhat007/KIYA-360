"""HTTP seam for the Customer-to-Cash front end (ADR-004, UX/Mobile seam).

ADR-004 names UX/Mobile as one of eight KNIT 360-owned strategic seams. A front end
that called Frappe's generic /api/resource/<DocType> endpoints would defeat
that: every field rename in a doctype would become a front-end change, and the
front end would be coupled to the framework rather than to KNIT 360.

So the front end calls only these methods. They speak stages and statuses, not
doctypes and docstatus. Everything behind them -- the doctype names, the child
table shapes, the fact that a status change may submit a Frappe document -- is
free to change without the front end knowing.

Lifecycle changes go through business_status.engine.transition, never around it.
This module adds no rules of its own; it only narrows what the web can reach.
"""

import frappe

from knit360_core.business_status import engine, model
from knit360_core.crm import conversion
from knit360_core.sales import quotation_from

#: The stages this seam exposes, in flow order (Customer-to-Cash, BRD 6.1).
#: Anything not listed here is unreachable from the front end.
STAGES = (
	{
		"key": "lead",
		"doctype": "KNIT 360 Lead",
		"label": "Leads",
		"title_field": "lead_name",
		"fields": ["name", "lead_name", "organization_name", "lead_source", "email", "phone"],
	},
	{
		"key": "opportunity",
		"doctype": "KNIT 360 Opportunity",
		"label": "Opportunities",
		"title_field": "title",
		"fields": ["name", "title", "customer", "estimated_deal_value", "currency", "expected_closing_date"],
	},
	{
		"key": "quotation",
		"doctype": "KNIT 360 Quotation",
		"label": "Quotations",
		"title_field": "customer",
		"fields": ["name", "customer", "opportunity", "currency", "valid_till"],
	},
)

BY_KEY = {stage["key"]: stage for stage in STAGES}
STATUS = model.FIELD


def _stage(key):
	stage = BY_KEY.get(key)
	if not stage:
		frappe.throw(f"Unknown stage '{key}'. This seam exposes: {', '.join(BY_KEY)}.")
	return stage


def _lifecycle(stage):
	return model.for_doctype(stage["doctype"])


@frappe.whitelist()
def stages():
	"""The board: every stage, its states, and how many documents sit in each.

	The front end draws itself from this, so adding a state to a lifecycle needs
	no front-end change.
	"""
	out = []
	for stage in STAGES:
		lifecycle = _lifecycle(stage)
		counts = dict(
			frappe.get_all(
				stage["doctype"],
				fields=[STATUS, "count(name) as n"],
				group_by=STATUS,
				as_list=True,
			)
		)
		out.append(
			{
				"key": stage["key"],
				"label": stage["label"],
				"doctype": stage["doctype"],
				"states": lifecycle.states,
				"initial": lifecycle.initial,
				"terminal": sorted(lifecycle.terminal_states),
				"counts": {state: counts.get(state, 0) for state in lifecycle.states},
				"total": sum(counts.values()),
			}
		)
	return out


@frappe.whitelist()
def documents(stage, status=None, limit=100):
	"""Rows for one stage, newest first."""
	spec = _stage(stage)
	filters = {STATUS: status} if status else None
	rows = frappe.get_all(
		spec["doctype"],
		fields=spec["fields"] + [STATUS, "docstatus", "modified"],
		filters=filters,
		order_by="modified desc",
		limit_page_length=int(limit),
	)
	for row in rows:
		row["title"] = row.get(spec["title_field"]) or row["name"]
		row["status"] = row.pop(STATUS)
	return rows


@frappe.whitelist()
def document(stage, name):
	"""One document, with the transitions and actions currently open to it."""
	spec = _stage(stage)
	doc = frappe.get_doc(spec["doctype"], name)
	doc.check_permission("read")
	lifecycle = _lifecycle(spec)
	status = engine.current_status(doc)

	return {
		"stage": spec["key"],
		"doctype": spec["doctype"],
		"name": doc.name,
		"title": doc.get(spec["title_field"]) or doc.name,
		"status": status,
		"docstatus": doc.docstatus,
		"states": lifecycle.states,
		"allowed_next": lifecycle.allowed_next(status),
		"fields": _display_fields(doc),
		"items": _items(doc),
		"actions": _actions(spec, doc, status),
		"history": _history(spec["doctype"], doc.name),
	}


def _display_fields(doc):
	"""Every stored value the doctype declares, labelled as the doctype labels
	it. Reading labels from the meta rather than repeating them here is what
	keeps the front end from needing to know the schema."""
	skip = {"Section Break", "Column Break", "Table", "Tab Break", "HTML"}
	out = []
	for field in doc.meta.fields:
		if field.fieldtype in skip or field.fieldname == STATUS:
			continue
		value = doc.get(field.fieldname)
		if value in (None, ""):
			continue
		out.append({"label": field.label, "value": str(value), "fieldtype": field.fieldtype})
	return out


def _line_table(doc):
	"""The doctype's first child table, and the columns it declares.

	Read from the meta rather than listed here, so a column added to KNIT 360
	Quotation Item appears in the front end without a front-end change.
	"""
	table = doc.meta.get_table_fields()
	if not table:
		return None, [], []
	field = table[0]
	cells = [
		f
		for f in frappe.get_meta(field.options).fields
		if f.fieldtype not in {"Section Break", "Column Break"}
	]
	return field, [f.fieldname for f in cells], [f.label or f.fieldname for f in cells]


def _items(doc):
	field, columns, labels = _line_table(doc)
	if not field:
		return None
	rows = doc.get(field.fieldname) or []
	return {
		"label": field.label,
		"columns": columns,
		"column_labels": labels,
		"rows": [{c: row.get(c) for c in columns} for row in rows],
		# Frappe refuses field changes after submission (UpdateAfterSubmitError),
		# so the front end is told rather than left to discover it by failing.
		"editable": doc.docstatus == 0,
	}


def _actions(spec, doc, status):
	"""Stage-crossing actions, as opposed to status transitions within a stage."""
	out = []
	if spec["key"] == "lead":
		out.append(
			{
				"key": "convert_lead",
				"label": "Convert to Customer + Opportunity",
				"enabled": status == conversion.REQUIRED_STATUS and not doc.converted_opportunity,
				"reason": _convert_reason(doc, status),
				"goes_to": "opportunity",
			}
		)
	if spec["key"] == "opportunity":
		out.append(
			{
				"key": "create_quotation",
				"label": "Raise Quotation",
				"enabled": bool(doc.customer),
				"reason": None if doc.customer else "The opportunity has no customer.",
				"goes_to": "quotation",
			}
		)
	return out


def _convert_reason(doc, status):
	if doc.converted_opportunity:
		return f"Already converted to {doc.converted_opportunity}."
	if status != conversion.REQUIRED_STATUS:
		return f"A lead converts from '{conversion.REQUIRED_STATUS}', not '{status}'."
	return None


def _history(doctype, name):
	return frappe.get_all(
		engine.LOG_DOCTYPE,
		fields=[
			"from_status",
			"to_status",
			"from_docstatus",
			"to_docstatus",
			"reason",
			"transitioned_by",
			"transitioned_at",
		],
		filters={"reference_doctype": doctype, "reference_name": name},
		order_by="transitioned_at desc, creation desc",
	)


@frappe.whitelist()
def advance(stage, name, to_status, reason=None):
	"""Move a document to the next business status.

	A thin pass-through. The matrix, the docstatus derivation and the audit row
	are all engine.transition's job -- this only stops the web reaching a stage
	the seam does not expose.
	"""
	spec = _stage(stage)
	engine.transition(spec["doctype"], name, to_status, reason=reason)
	return document(spec["key"], name)


@frappe.whitelist()
def set_items(stage, name, items):
	"""Replace a draft document's line items.

	Whole-table replacement rather than per-row editing: the child rows carry no
	identity of their own in the seam, and a quotation's lines are meaningful
	only as a set.
	"""
	spec = _stage(stage)
	doc = frappe.get_doc(spec["doctype"], name)
	doc.check_permission("write")

	field, columns, _labels = _line_table(doc)
	if not field:
		frappe.throw(f"{spec['doctype']} has no line items.")
	if doc.docstatus != 0:
		frappe.throw(
			f"{doc.doctype} {doc.name} is submitted (docstatus {doc.docstatus}). "
			f"Its lines can no longer be changed."
		)

	doc.set(field.fieldname, [])
	for row in frappe.parse_json(items):
		doc.append(field.fieldname, {c: row.get(c) for c in columns if c in row})
	doc.save()
	return document(spec["key"], name)


@frappe.whitelist()
def create_lead(
	lead_name,
	company,
	organization_name=None,
	email=None,
	phone=None,
	lead_source=None,
	territory=None,
	estimated_requirement=None,
):
	"""FR-CRM-001. Named arguments rather than a dict, so the web cannot set
	knit360_business_status or any other field the seam does not offer."""
	doc = frappe.get_doc(
		{
			"doctype": "KNIT 360 Lead",
			"lead_name": lead_name,
			"organization_name": organization_name,
			"company": company,
			"email": email,
			"phone": phone,
			"lead_source": lead_source,
			"territory": territory,
			"estimated_requirement": estimated_requirement,
		}
	).insert()
	return document("lead", doc.name)


@frappe.whitelist()
def convert_lead(name, customer=None):
	result = conversion.convert_lead(name, customer=customer)
	result["opportunity_detail"] = document("opportunity", result["opportunity"])
	return result


@frappe.whitelist()
def create_quotation(opportunity):
	quotation = quotation_from.from_opportunity(opportunity)
	return document("quotation", quotation)


@frappe.whitelist()
def companies():
	"""Every doctype in the flow needs a company (FR-PADM-1.1.1)."""
	return frappe.get_all("KNIT 360 Company", fields=["name", "default_currency"], order_by="name")
