"""KNIT 360 Asset - FR-AST-001 / FR-AST-002 / FR-AST-003.

DR-A2S-001 Asset / Installed Equipment Registry. This is the CUSTOMER INSTALLED
BASE -- a unit the business has sold and goes on servicing. Doc 33 requires it
be kept architecturally distinct from corporate fixed assets, which are the
business's own property and are depreciated; these are not.

A unit is usually registered by its delivery note (DR-A2S-001: serialised
equipment dispatched feeds the registry), and can be registered by hand for a
unit sold before the system existed.

**Commissioning** (DR-A2S-002). Reaching Commissioned / Operational needs the
commissioning date, which may not fall before the unit was dispatched. The
first time a unit is commissioned, the maker's warranty is drafted for it from
the item's Standard Warranty (Months), starting that day. It is drafted, not put
in force: what the warranty covers -- parts, labour, travel -- is the
business's own terms (`OQ-011`), so somebody ticks them and activates it.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, add_months, cint, getdate

ASSET = "KNIT 360 Asset"
CONTRACT = "KNIT 360 Service Contract"
DELIVERY_NOTE = "KNIT 360 Delivery Note"
ITEM = "KNIT 360 Item"

REGISTERED = "Registered"
COMMISSIONED = "Commissioned / Operational"
#: A unit in either of these is out of service for good.
RETIRED = ("Decommissioned", "Scrapped")


class KNIT360Asset(Document):
	def validate(self):
		self._one_record_per_unit()

	def _one_record_per_unit(self):
		if not (self.serial_number and self.item_code):
			return
		clash = frappe.db.get_value(
			ASSET,
			{"item_code": self.item_code, "serial_number": self.serial_number,
			 "name": ["!=", self.name or ""]},
			"name",
		)
		if clash:
			frappe.throw(
				f"{self.item_code} serial number {self.serial_number} is already registered "
				f"as {clash}. One unit needs one record, or its warranty and service "
				f"history would split in two."
			)

	def before_business_status(self, from_status, to_status):
		if to_status != COMMISSIONED:
			return
		if not self.commissioning_date:
			frappe.throw(
				"Enter the commissioning date first -- the day the unit was installed "
				"and handed over. The warranty runs from it."
			)
		if self.delivery_note:
			dispatched = frappe.db.get_value(DELIVERY_NOTE, self.delivery_note, "delivery_note_date")
			if dispatched and getdate(self.commissioning_date) < getdate(dispatched):
				frappe.throw(
					f"The commissioning date {self.commissioning_date} is before the unit "
					f"was dispatched on {dispatched}."
				)

	def after_business_status(self, from_status, to_status):
		if to_status == COMMISSIONED and from_status == REGISTERED:
			self._draft_warranty()

	def _draft_warranty(self):
		months = cint(frappe.db.get_value(ITEM, self.item_code, "warranty_period_months")) if self.item_code else 0
		if months <= 0:
			return None
		if frappe.db.exists(CONTRACT, {"asset": self.name, "contract_type": "Standard Warranty"}):
			return None

		start = getdate(self.commissioning_date)
		contract = frappe.get_doc(
			{
				"doctype": CONTRACT,
				"asset": self.name,
				"company": self.company,
				"contract_type": "Standard Warranty",
				"start_date": start,
				"end_date": add_days(add_months(start, months), -1),
			}
		).insert(ignore_permissions=True)
		frappe.msgprint(
			f"Drafted the {months}-month warranty {contract.name}, from {start}. Tick what "
			f"it covers -- parts, labour, travel -- and put it in force.",
			alert=True,
		)
		return contract.name
