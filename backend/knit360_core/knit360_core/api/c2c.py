"""The two Desk buttons that move a sale into its next stage.

A Qualified lead offers "Convert to Customer + Opportunity" and an opportunity
offers "Raise Quotation" (public/js/business_status.bundle.js). This module says
when each is open, says why when it is not, and does the work, so the rule is
stated in one place.

It began as the HTTP seam for /knit360, a simplified Customer-to-Cash page for
salespeople (ADR-004, UX/Mobile seam). The owner removed that page on
31 October 2026 -- leads are entered on the Desk's Lead form and nowhere else
(DEC-044) -- and the endpoints only the page called went with it.

Lifecycle changes go through business_status.engine.transition, never around it.
"""

import frappe

from knit360_core.business_status import engine
from knit360_core.crm import conversion
from knit360_core.sales import quotation_from

LEAD = "KNIT 360 Lead"
OPPORTUNITY = "KNIT 360 Opportunity"


@frappe.whitelist()
def convert_lead(name, customer=None):
	"""{"customer", "opportunity", ...} -- see crm.conversion.convert_lead."""
	return conversion.convert_lead(name, customer=customer)


@frappe.whitelist()
def create_quotation(opportunity):
	return {"name": quotation_from.from_opportunity(opportunity)}


@frappe.whitelist()
def actions_for(doctype, name):
	"""The actions open to a document that make its next document.

	Status moves within a document's own lifecycle are engine.next_steps's job.
	Leads and opportunities are answered here; every other document by
	desk_actions, which this passes through unchanged.
	"""
	from knit360_core.api import desk_actions

	desk_only = desk_actions.actions_for(doctype, name)
	if doctype not in (LEAD, OPPORTUNITY):
		return desk_only
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("read")
	return _actions(doc, engine.current_status(doc)) + desk_only


def _actions(doc, status):
	if doc.doctype == LEAD:
		return [
			{
				"key": "convert_lead",
				"label": "Convert to Customer + Opportunity",
				"enabled": status == conversion.REQUIRED_STATUS and not doc.converted_opportunity,
				"reason": _convert_reason(doc, status),
				# The status this action reaches by itself. The Desk also draws
				# plain status buttons and hides the matching one, so nobody
				# marks a lead Converted without converting it.
				"produces_status": conversion.CONVERTED,
			}
		]
	return [
		{
			"key": "create_quotation",
			"label": "Raise Quotation",
			"enabled": bool(doc.customer),
			"reason": None if doc.customer else "The opportunity has no customer.",
		}
	]


def _convert_reason(doc, status):
	if doc.converted_opportunity:
		return f"Already converted to {doc.converted_opportunity}."
	if status != conversion.REQUIRED_STATUS:
		return f"A lead converts from '{conversion.REQUIRED_STATUS}', not '{status}'."
	return None
