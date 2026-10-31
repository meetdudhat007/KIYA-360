"""KNIT 360 Service Contract - FR-AST-003 / FR-MFS-006.

DR-A2S-003 Warranty & Service Contract Management. What a contract covers is
read by knit360_core.maintenance.entitlement; this controller keeps the dates
it reads sound.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

from knit360_core.maintenance import entitlement


class KNIT360ServiceContract(Document):
	def validate(self):
		self._check_dates()

	def _check_dates(self):
		if self.start_date and self.end_date and getdate(self.end_date) <= getdate(self.start_date):
			frappe.throw(
				f"The cover ends on {self.end_date}, which is not after it starts on "
				f"{self.start_date}. A contract must end after it begins."
			)

	def before_business_status(self, from_status, to_status):
		if to_status == entitlement.ACTIVE:
			if not (self.start_date and self.end_date):
				frappe.throw(
					"Enter the start and end dates before putting this cover in force. "
					"Without them nothing can be judged covered or not."
				)
			self._check_dates()
