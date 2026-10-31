"""KNIT 360 Service Request - FR-MFS-004 / FR-MFS-007.

DR-A2S-004 Service Request (Customer Incident & Triage). The customer's call:
which unit, what is wrong, and -- worked out, not typed -- whether a warranty
or contract covered the unit on the day they reported it.

The customer is taken from the unit, and a request naming a different customer
from the unit's owner is refused (doc 33 section 7): a fault logged against
somebody else's furnace would put the repair, and its bill, on the wrong
account.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime

from knit360_core.maintenance import entitlement

ASSET = "KNIT 360 Asset"
RETIRED = ("Decommissioned", "Scrapped")


class KNIT360ServiceRequest(Document):
	def validate(self):
		if not self.request_timestamp:
			self.request_timestamp = now_datetime()
		self._check_unit()
		self._show_cover()

	def _check_unit(self):
		unit = frappe.db.get_value(ASSET, self.asset, ["customer", "knit360_business_status"], as_dict=True)
		if not unit:
			return
		if unit.knit360_business_status in RETIRED:
			frappe.throw(
				f"{self.asset} is {unit.knit360_business_status} and no longer in service."
			)
		if not self.customer:
			self.customer = unit.customer
		elif unit.customer and unit.customer != self.customer:
			frappe.throw(
				f"{self.asset} belongs to {unit.customer}, not {self.customer}. "
				f"Log the request against the customer who owns the unit."
			)

	def _show_cover(self):
		label, contract = entitlement.summary(self.asset, getdate(self.request_timestamp))
		self.warranty_status = label
		self.covering_contract = contract
