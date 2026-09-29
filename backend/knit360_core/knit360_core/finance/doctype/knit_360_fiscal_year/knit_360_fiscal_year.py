"""KNIT 360 Fiscal Year - FR-FIN-007.

Every posting is dated into exactly one year, so the years must not overlap and
must not leave gaps that a posting date could fall into.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class KNIT360FiscalYear(Document):
	def validate(self):
		if getdate(self.year_end_date) <= getdate(self.year_start_date):
			frappe.throw("A fiscal year ends after it starts.")
		self.forbid_overlap()

	def forbid_overlap(self):
		clash = frappe.db.sql(
			"""
			select name from `tabKNIT 360 Fiscal Year`
			where name != %(name)s
			  and year_start_date <= %(end)s
			  and year_end_date   >= %(start)s
			""",
			{"name": self.name or "", "start": self.year_start_date, "end": self.year_end_date},
		)
		if clash:
			frappe.throw(
				f"{self.year_name} overlaps fiscal year {clash[0][0]}. "
				f"A posting date must fall in exactly one year."
			)
