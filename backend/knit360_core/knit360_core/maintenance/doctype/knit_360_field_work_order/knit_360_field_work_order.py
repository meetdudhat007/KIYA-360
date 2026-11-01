"""KNIT 360 Field Work Order - FR-MFS-002 / FR-MFS-005 / FR-MFS-007.

DR-A2S-006 and DR-A2S-007: the job an engineer does on an installed unit --
installation, a planned visit, or a breakdown repair. Deliberately a separate
doctype from KNIT 360 Work Order (manufacturing); doc 33 forbids sharing that
schema.

**Cover.** Each line is tagged Warranty Covered, Contract Covered or Billable
to Customer from the unit's agreements, judged on the day the customer
reported the fault -- or on the work date when nobody reported one, as for a
planned visit. It is worked out on every save while the job is open, and
never typed (DR-A2S-007).

**What it posts, on Work Complete.** Spare-part lines leave the parts store,
costed by the stock ledger, and that cost is charged:

    warranty-covered parts   debit Warranty Expense
    every other part         debit Cost of Goods Sold
                             credit Stock In Hand

A part covered by a paid contract is a cost of serving that contract, so it
goes to Cost of Goods Sold with parts sold; only the maker's warranty has an
account of its own -- DEC-041. Labour and travel move nothing: they are
charges, and reach the books on the service invoice raised from this job
(DR-A2S-009).
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate

from knit360_core.finance import ledger
from knit360_core.maintenance import entitlement, schedule
from knit360_core.stock import ledger as stock_ledger

ASSET = "KNIT 360 Asset"
COMPANY = "KNIT 360 Company"
SERVICE_REQUEST = "KNIT 360 Service Request"
SCHEDULE = "KNIT 360 Maintenance Schedule"
SALES_INVOICE = "KNIT 360 Sales Invoice"

WORK_COMPLETE = "Work Complete"
SIGNED_OFF = "Customer Signed Off"
CANCELLED = "Cancelled"


class KNIT360FieldWorkOrder(Document):
	def validate(self):
		self._check_unit()
		self._check_lines()
		self._check_times()
		if self.assigned_technician and not frappe.db.get_value("User", self.assigned_technician, "enabled"):
			frappe.throw(f"{self.assigned_technician} is a disabled user and cannot be assigned work.")
		if self.docstatus == 0:
			self._apply_cover()

	def _check_unit(self):
		unit = frappe.db.get_value(ASSET, self.asset, ["customer", "knit360_business_status"], as_dict=True)
		if not unit:
			return
		self.customer = unit.customer
		if self.service_request:
			reported_on = frappe.db.get_value(SERVICE_REQUEST, self.service_request, "asset")
			if reported_on and reported_on != self.asset:
				frappe.throw(f"{self.service_request} was raised for {reported_on}, not {self.asset}.")
		if self.maintenance_schedule:
			scheduled_for = frappe.db.get_value(SCHEDULE, self.maintenance_schedule, "asset")
			if scheduled_for and scheduled_for != self.asset:
				frappe.throw(f"{self.maintenance_schedule} is the schedule for {scheduled_for}, not {self.asset}.")

	def _check_lines(self):
		for row in self.items:
			if flt(row.qty) <= stock_ledger.TOLERANCE:
				frappe.throw(f"Parts and Charges line {row.idx}: a quantity of {flt(row.qty):g} is not a quantity.")

	def _check_times(self):
		if self.planned_start and self.planned_end and self.planned_end <= self.planned_start:
			frappe.throw("The planned end is not after the planned start.")

	def _cover_date(self):
		if self.service_request:
			reported = frappe.db.get_value(SERVICE_REQUEST, self.service_request, "request_timestamp")
			if reported:
				return getdate(reported)
		return getdate(self.posting_date or nowdate())

	def _apply_cover(self):
		contracts = entitlement.contracts_on(self.asset, self._cover_date())
		self.covering_contract = contracts[0].name if contracts else None
		self.warranty_entitlement = 1 if contracts else 0
		for row in self.items:
			row.coverage = entitlement.cover_for(row.line_type, contracts)

	# --- lifecycle --------------------------------------------------------

	def before_business_status(self, from_status, to_status):
		if to_status == WORK_COMPLETE:
			if flt(self.actual_labor_hours) <= 0:
				frappe.throw("Record the hours spent on the job before marking the work complete.")
			if self._parts() and not self.parts_warehouse:
				frappe.throw("Say which store or van the spare parts came from (Spare Parts From).")
			needed = {}
			for row in self._parts():
				needed[row.item_code] = needed.get(row.item_code, 0.0) + flt(row.qty)
			for item, qty in needed.items():
				stock_ledger.check_can_issue(item, self.parts_warehouse, qty, self.company)
		if to_status == SIGNED_OFF and not (self.customer_signature or "").strip():
			frappe.throw("Record who signed for the work on the customer's side first.")
		if to_status == CANCELLED and self.sales_invoice:
			billed = frappe.db.get_value(SALES_INVOICE, self.sales_invoice, "knit360_business_status")
			if billed and billed != CANCELLED:
				frappe.throw(f"This job is billed on {self.sales_invoice}. Cancel that invoice first.")

	def after_business_status(self, from_status, to_status):
		if self.maintenance_schedule and to_status in (WORK_COMPLETE, CANCELLED):
			schedule.refresh(self.maintenance_schedule)

	# --- stock and ledger -------------------------------------------------

	def _parts(self):
		return [row for row in self.items if row.line_type == entitlement.PART]

	def on_submit(self):
		parts = self._parts()
		if not parts:
			return
		posted = stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.posting_date or nowdate(),
			[
				{
					"item_code": row.item_code,
					"warehouse": self.parts_warehouse,
					"qty": -flt(row.qty),
					"remarks": f"Used on {self.name} for {self.asset}",
				}
				for row in parts
			],
		)
		self._record_cost(parts, posted)
		self._post_cost(parts)

	def on_cancel(self):
		stock_ledger.reverse(self.doctype, self.name)
		ledger.reverse(self.doctype, self.name)

	def _record_cost(self, parts, posted):
		"""Copy what the stock ledger worked out back onto the lines, to be read."""
		total = 0.0
		for row, entry in zip(parts, posted):
			move = frappe.db.get_value(stock_ledger.SLE, entry, ["rate", "value_change"], as_dict=True)
			row.stock_value = abs(flt(move.value_change))
			row.valuation_rate = flt(move.rate)
			row.db_set("valuation_rate", row.valuation_rate, update_modified=False)
			row.db_set("stock_value", row.stock_value, update_modified=False)
			total += row.stock_value
		self.db_set("parts_cost", total, update_modified=False)

	def _post_cost(self, parts):
		warranty = flt(sum(flt(r.stock_value) for r in parts if r.coverage == entitlement.WARRANTY))
		other = flt(sum(flt(r.stock_value) for r in parts if r.coverage != entitlement.WARRANTY))
		if warranty + other <= stock_ledger.TOLERANCE:
			return

		accounts = frappe.db.get_value(
			COMPANY,
			self.company,
			["default_stock_account", "default_cogs_account", "default_warranty_expense_account"],
			as_dict=True,
		)
		if not accounts.default_stock_account:
			frappe.throw(f"{self.company} has no Default Stock Account, so these parts cannot leave the books.")
		if other > stock_ledger.TOLERANCE and not accounts.default_cogs_account:
			frappe.throw(f"{self.company} has no Default Cost of Goods Sold Account for the parts used.")
		if warranty > stock_ledger.TOLERANCE and not accounts.default_warranty_expense_account:
			frappe.throw(
				f"{self.company} has no Default Warranty Expense Account, so the parts given "
				f"free under warranty have nowhere to be charged."
			)

		lines = []
		if warranty > stock_ledger.TOLERANCE:
			lines.append(ledger.Line(account=accounts.default_warranty_expense_account, debit=warranty,
			                         remarks="Spare parts given under warranty"))
		if other > stock_ledger.TOLERANCE:
			lines.append(ledger.Line(account=accounts.default_cogs_account, debit=other,
			                         remarks="Spare parts used"))
		lines.append(ledger.Line(account=accounts.default_stock_account, credit=warranty + other))
		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.posting_date or nowdate(),
			lines,
			remarks=f"Spare parts used on {self.name} for {self.asset}",
		)
