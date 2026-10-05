"""KNIT 360 Holiday List - FR-HR-003.

The non-working days a leave calculation skips.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class KNIT360HolidayList(Document):
	def validate(self):
		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw("A holiday list cannot end before it starts.")

		seen = set()
		for row in self.holidays or []:
			date = getdate(row.holiday_date)
			if not (getdate(self.from_date) <= date <= getdate(self.to_date)):
				frappe.throw(
					f"{date} is outside the period this list covers "
					f"({self.from_date} to {self.to_date})."
				)
			if date in seen:
				frappe.throw(f"{date} appears twice. A day is a holiday once.")
			seen.add(date)

		self.total_holidays = len(self.holidays or [])

	def dates(self):
		"""The holiday dates as a set, for a leave day count."""
		return {getdate(row.holiday_date) for row in self.holidays or []}
