"""KNIT 360 Leave Application - FR-HR-003.

An employee's request to consume a leave balance.

Two things are worth knowing about how this is built.

**The day count skips holidays.** Leave taken across a public holiday should
not spend the balance on a day nobody was working anyway. The holiday list
comes from the application, or from the leave period covering the dates. If
neither names one, every calendar day counts and the document says so rather
than guessing a weekend.

**The balance is checked twice, for different reasons.** On save, so a person
sees the refusal while the document is still a draft and can do something about
it. On submit, because the balance may have moved between the two -- somebody
else's application for the same employee may have been approved in between.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, flt, getdate

from knit360_core.hr import leave_ledger

HOLIDAY_LIST = "KNIT 360 Holiday List"
LEAVE_TYPE = "KNIT 360 Leave Type"
LEAVE_PERIOD = "KNIT 360 Leave Period"


class KNIT360LeaveApplication(Document):
	def validate(self):
		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw("Leave cannot end before it starts.")

		if self.half_day and getdate(self.from_date) != getdate(self.to_date):
			frappe.throw(
				"A half day applies to one date. Set the same from and to date, "
				"or clear the half day."
			)

		if not self.posting_date:
			self.posting_date = frappe.utils.nowdate()

		self.total_leave_days = self.count_days()
		if self.total_leave_days <= 0:
			frappe.throw(
				"Every day of this application is a holiday, so there is no leave "
				"to take."
			)

		self._not_overlapping()

		self.leave_balance = leave_ledger.balance(
			self.employee, self.leave_type, on_date=self.from_date, company=self.company
		)
		leave_ledger.check_can_consume(
			self.employee, self.leave_type, self.total_leave_days,
			on_date=self.from_date, company=self.company,
		)

	# --- the day count --------------------------------------------------

	def holiday_dates(self):
		"""Dates to skip: the named list, or the leave period's default.

		Returns an empty set when no list is reachable, and the count then
		treats every day as a working day.
		"""
		name = self.holiday_list or self._period_holiday_list()
		if not name or not frappe.db.exists(HOLIDAY_LIST, name):
			return set()
		return frappe.get_doc(HOLIDAY_LIST, name).dates()

	def _period_holiday_list(self):
		return frappe.db.get_value(
			LEAVE_PERIOD,
			{
				"company": self.company,
				"from_date": ["<=", self.from_date],
				"to_date": [">=", self.from_date],
			},
			"holiday_list",
		)

	def count_days(self):
		"""Days of leave, after skipping holidays unless the type counts them."""
		if frappe.db.get_value(LEAVE_TYPE, self.leave_type, "include_holidays_in_leave"):
			holidays = set()
		else:
			holidays = self.holiday_dates()

		start, end = getdate(self.from_date), getdate(self.to_date)
		days = 0.0
		day = start
		while day <= end:
			if day not in holidays:
				days += 1
			day = add_days(day, 1)

		if self.half_day and days:
			days -= 0.5
		return flt(days)

	def _not_overlapping(self):
		"""An employee cannot be on two leaves at once."""
		clash = frappe.db.sql(
			"""SELECT name FROM `tabKNIT 360 Leave Application`
			   WHERE employee = %(employee)s AND name != %(name)s
			     AND docstatus = 1
			     AND from_date <= %(to_date)s AND to_date >= %(from_date)s
			   LIMIT 1""",
			{
				"employee": self.employee,
				"name": self.name or "",
				"from_date": self.from_date,
				"to_date": self.to_date,
			},
		)
		if clash:
			frappe.throw(
				f"{self.employee} already has approved leave in {clash[0][0]} over "
				f"these dates. Cancel it before applying again."
			)

	# --- ledger ---------------------------------------------------------

	def on_submit(self):
		# Checked again here: the balance may have moved since this was saved.
		leave_ledger.check_can_consume(
			self.employee, self.leave_type, self.total_leave_days,
			on_date=self.from_date, company=self.company,
		)
		leave_ledger.post(
			self.doctype,
			self.name,
			employee=self.employee,
			leave_type=self.leave_type,
			company=self.company,
			posting_date=self.from_date,
			leaves=-flt(self.total_leave_days),
			from_date=self.from_date,
			to_date=self.to_date,
			remarks=self.reason or "Leave taken",
		)

	def on_cancel(self):
		leave_ledger.reverse(self.doctype, self.name)
