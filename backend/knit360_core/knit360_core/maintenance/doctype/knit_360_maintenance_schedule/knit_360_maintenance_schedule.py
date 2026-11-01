"""KNIT 360 Maintenance Schedule - FR-MFS-003 / FR-MFS-004.

DR-A2S-008 Maintenance Execution (Preventive & Corrective). A recurring
programme of visits to one unit. Its dates move in
knit360_core.maintenance.schedule when a visit is completed or cancelled.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt

ASSET = "KNIT 360 Asset"
RETIRED = ("Decommissioned", "Scrapped")


class KNIT360MaintenanceSchedule(Document):
	def validate(self):
		if flt(self.trigger_value) <= 0:
			frappe.throw("Say how many days apart the visits are (Interval (Days)).")
		status = frappe.db.get_value(ASSET, self.asset, "knit360_business_status")
		if status in RETIRED:
			frappe.throw(f"{self.asset} is {status} and no longer in service, so it needs no visits.")
