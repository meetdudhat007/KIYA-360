"""KNIT 360 Leave Allocation - FR-HR-003.

Grants an employee a balance of one leave type for one leave period.

The ledger effect hangs on Frappe's on_submit / on_cancel rather than on the
business status directly, exactly as KNIT 360 Journal Entry does. The business
status adapter reaches docstatus 1 by calling doc.submit(), so on_submit fires
once, at the moment CD-002 says the effect becomes real. One posting path, not
two.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate

from knit360_core.hr import leave_ledger

LEAVE_TYPE = "KNIT 360 Leave Type"


class KNIT360LeaveAllocation(Document):
	def validate(self):
		self.total_leaves_allocated = flt(self.new_leaves_allocated) + flt(self.carried_forward)

		if self.total_leaves_allocated <= 0:
			frappe.throw("An allocation of nothing grants nothing. Enter the days to allocate.")

		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw("An allocation cannot end before it starts.")

		self._within_the_period()
		self._within_the_type_limit()
		self._not_already_allocated()

	def _within_the_period(self):
		period = frappe.db.get_value(
			"KNIT 360 Leave Period", self.leave_period, ["from_date", "to_date", "is_active"],
			as_dict=True,
		)
		if not period:
			return
		if not period.is_active:
			frappe.throw(f"{self.leave_period} is not active and takes no new allocations.")
		if getdate(self.from_date) < getdate(period.from_date) or getdate(self.to_date) > getdate(period.to_date):
			frappe.throw(
				f"This allocation runs {self.from_date} to {self.to_date}, outside "
				f"{self.leave_period} ({period.from_date} to {period.to_date}). "
				f"An allocation belongs to one period."
			)

	def _within_the_type_limit(self):
		limit = flt(frappe.db.get_value(LEAVE_TYPE, self.leave_type, "max_leaves_allowed"))
		if limit and self.total_leaves_allocated > limit:
			frappe.throw(
				f"{self.leave_type} allows at most {limit:g} day(s) per period, and "
				f"this allocates {self.total_leaves_allocated:g}."
			)

	def _not_already_allocated(self):
		"""One live allocation per employee, leave type and period.

		Two allocations for the same period are almost always a double entry
		rather than an intention, and the ledger would happily add them up.
		"""
		clash = frappe.db.exists(
			self.doctype,
			{
				"employee": self.employee,
				"leave_type": self.leave_type,
				"leave_period": self.leave_period,
				"name": ["!=", self.name],
				"docstatus": 1,
			},
		)
		if clash:
			frappe.throw(
				f"{self.employee} already has {clash} allocating {self.leave_type} "
				f"for {self.leave_period}. Cancel it, or amend the days there."
			)

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		leave_ledger.post(
			self.doctype,
			self.name,
			employee=self.employee,
			leave_type=self.leave_type,
			company=self.company,
			posting_date=self.from_date,
			leaves=self.total_leaves_allocated,
			from_date=self.from_date,
			to_date=self.to_date,
			leave_period=self.leave_period,
			remarks=self.description or "Leave allocated",
		)

	def on_cancel(self):
		leave_ledger.reverse(self.doctype, self.name)
