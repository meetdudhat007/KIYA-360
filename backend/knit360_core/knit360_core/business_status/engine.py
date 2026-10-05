"""Drives Frappe's docstatus from the business status, rather than bypassing it.

This is the RSK-02 adapter. The integrity rule it rests on: KNIT 360 never writes
docstatus directly. It decides the business status, derives the docstatus that
status implies, and reaches it through Frappe's own submit() and cancel(), so
GL entries, stock ledger entries and reversals stay upstream's responsibility.

Business status advances across states that share a docstatus (Approved ->
In Progress -> Completed -> Closed) via db_set, which is how ERPNext itself
updates status on a submitted document.
"""

import frappe
from frappe.utils import now

from knit360_core.business_status import guard, model

FIELD = model.FIELD
LOG_DOCTYPE = "KNIT 360 Business Status Log"


def current_status(doc):
	return doc.get(FIELD) or model.for_doctype(doc.doctype).initial


def conflicting_workflow(doctype):
	"""An active Frappe Workflow on the same doctype, if one exists.

	Frappe's Workflow engine owns docstatus for any doctype it governs, and so
	does this adapter. Both on one doctype means two things racing to submit
	the same document. They are mutually exclusive by design, not by accident:
	the Workflow doctype IS the docstatus model CD-002 rejects.
	"""
	return frappe.db.get_value("Workflow", {"document_type": doctype, "is_active": 1}, "name")


def _apply_docstatus(doc, target):
	if doc.docstatus == target:
		return

	# guard.py refuses a submit or cancel that does not carry this flag, so
	# this is the only place in the app that can move docstatus.
	doc.flags[guard.FLAG] = True
	if doc.docstatus == 0 and target == 1:
		doc.submit()
	elif doc.docstatus == 1 and target == 2:
		doc.cancel()
	else:
		# Frappe allows 0->1 and 1->2 only. Anything else would mean rewriting
		# a posted document, which DEC-009 forbids.
		frappe.throw(
			f"{doc.doctype} {doc.name}: cannot move docstatus {doc.docstatus} -> {target}. "
			f"Reverse the posted document instead of rewriting it."
		)


def _log(doc, from_status, to_status, reason, from_docstatus, to_docstatus):
	frappe.get_doc(
		{
			"doctype": LOG_DOCTYPE,
			"reference_doctype": doc.doctype,
			"reference_name": doc.name,
			"from_status": from_status,
			"to_status": to_status,
			"from_docstatus": from_docstatus,
			"to_docstatus": to_docstatus,
			"reason": reason,
			"transitioned_by": frappe.session.user,
			"transitioned_at": now(),
		}
	).insert(ignore_permissions=True)


@frappe.whitelist()
def transition(reference_doctype, reference_name, to_status, reason=None):
	"""Move a document to a new business status.

	Raises if the transition is not in the approved matrix, or if it would
	require an impossible docstatus change.
	"""
	lifecycle = model.for_doctype(reference_doctype)
	if to_status not in lifecycle.states:
		frappe.throw(
			f"{reference_doctype} has no business status '{to_status}'. "
			f"Its '{lifecycle.name}' lifecycle allows: {', '.join(lifecycle.states)}."
		)

	workflow = conflicting_workflow(reference_doctype)
	if workflow:
		frappe.throw(
			f"Active Frappe Workflow '{workflow}' also governs {reference_doctype}. "
			f"Deactivate it before using the business status adapter; both control docstatus."
		)

	doc = frappe.get_doc(reference_doctype, reference_name)
	from_status = current_status(doc)

	if from_status == to_status:
		return to_status

	if not lifecycle.is_allowed(from_status, to_status):
		allowed = lifecycle.allowed_next(from_status) or ["(terminal)"]
		frappe.throw(
			f"{reference_doctype} {reference_name}: "
			f"'{from_status}' -> '{to_status}' is not an allowed transition. "
			f"Allowed: {', '.join(allowed)}."
		)

	from_docstatus = doc.docstatus
	_apply_docstatus(doc, lifecycle.required_docstatus(to_status, from_docstatus))
	doc.db_set(FIELD, to_status, update_modified=True)
	_log(doc, from_status, to_status, reason, from_docstatus, doc.docstatus)
	return to_status


@frappe.whitelist()
def allowed_next(reference_doctype, reference_name):
	doc = frappe.get_doc(reference_doctype, reference_name)
	return model.for_doctype(reference_doctype).allowed_next(current_status(doc))


@frappe.whitelist()
def next_steps(reference_doctype, reference_name):
	"""The moves open to a document, with enough context to warn before one.

	allowed_next returns bare status names, which is all the tests need. The
	Desk needs more than that: whether a move locks the document, whether it is
	the end of the road, and which one is the ordinary next step -- so a button
	can be made primary and a one-way move can ask before it happens.

	Returns [] for a doctype with no registered lifecycle, rather than raising,
	because this is called on every form that opens.
	"""
	if reference_doctype not in model.REGISTRY:
		return []

	doc = frappe.get_doc(reference_doctype, reference_name)
	lifecycle = model.for_doctype(reference_doctype)
	status = current_status(doc)
	forward = lifecycle.forward_from(status)

	return [
		{
			"status": target,
			"locks": lifecycle.locks_on(target, doc.docstatus),
			"terminal": not lifecycle.allowed_next(target),
			"is_forward": target == forward,
		}
		for target in lifecycle.allowed_next(status)
	]
