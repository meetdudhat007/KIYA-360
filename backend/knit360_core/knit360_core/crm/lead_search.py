"""The lead list's search box and its Assigned To dropdown (DEC-053).

The owner wanted one box that finds a lead by any word in it. Each lead keeps
its words in Search Keywords, a hidden field the box matches with LIKE, one
condition per typed word, so "konkan ravi" finds the lead that has both, in
any field and in any order. Because the words live on the lead itself, the
match is an ordinary list filter: paging, the count and who may see which lead
work as they do for any other filter.

The words are the ones the search bar indexes for the lead (search.index), so
the two find the same things, plus the names of the employees the lead is
assigned or given to -- the lead holds only their numbers.
"""

import frappe

from knit360_core.crm.lead_access import ACCESS, EMPLOYEE, LEAD
from knit360_core.search import index

FIELD = "search_keywords"


def keywords(lead):
	"""Every word the search box finds this lead by."""
	words = index.searchable_values(lead, lead.meta)
	employees = [e for e in (lead.assigned_to, *(row.employee for row in lead.lead_access)) if e]
	if employees:
		words += frappe.get_all(EMPLOYEE, filters={"name": ["in", employees]}, pluck="employee_name")
	return " ".join(words)


def refresh(lead):
	"""Rewrite a lead's words after a change made without a save -- a status
	move, or the rename of an employee it names."""
	lead.db_set(FIELD, keywords(lead), update_modified=False)


def refresh_for(employee):
	"""Rewrite the words of every lead that names this employee."""
	leads = set(frappe.get_all(LEAD, filters={"assigned_to": employee}, pluck="name"))
	leads.update(frappe.get_all(ACCESS, filters={"employee": employee, "parenttype": LEAD}, pluck="parent"))
	for name in leads:
		refresh(frappe.get_doc(LEAD, name))


@frappe.whitelist()
def assignees():
	"""The Assigned To dropdown's choices: every employee, those still with the
	company first, so a lead waiting with someone who has left can be found."""
	frappe.has_permission(LEAD, "read", throw=True)
	return frappe.get_all(
		EMPLOYEE,
		fields=["name", "employee_name", "is_active"],
		order_by="is_active desc, employee_name asc",
	)
