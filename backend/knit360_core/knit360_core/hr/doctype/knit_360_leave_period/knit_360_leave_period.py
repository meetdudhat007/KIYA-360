"""KNIT 360 Leave Period - FR-HR-003.

The window an allocation and its balance belong to.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class KNIT360LeavePeriod(Document):
	def validate(self):
		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw("A leave period cannot end before it starts.")

		clash = frappe.db.exists(
			self.doctype,
			{
				"company": self.company,
				"name": ["!=", self.name],
				"from_date": ["<=", self.to_date],
				"to_date": [">=", self.from_date],
			},
		)
		if clash:
			frappe.throw(
				f"This period overlaps {clash}. A date must fall in exactly one "
				f"leave period, or a balance belongs to two of them at once."
			)
