"""Give existing leads their words for the lead list's search box (DEC-053).

Search Keywords is filled in on every save. Leads saved before it existed have
none, and the search box would not find them.
"""

import frappe

from knit360_core.crm import lead_search


def execute():
	frappe.reload_doc("crm", "doctype", "knit_360_lead")
	for name in frappe.get_all(lead_search.LEAD, pluck="name"):
		lead_search.refresh(frappe.get_doc(lead_search.LEAD, name))
