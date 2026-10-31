"""KNIT 360 BOM - FR-MFG-001.

FR-MFG-001 BOM Management. Version control is FR-MFG-001 plus the revision-locking rule recorded in doc 39 (OQ-017, not yet approved scope).
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class KNIT360BOM(Document):
	def validate(self):
		if flt(self.quantity) <= 0:
			self.quantity = 1
		if not self.items:
			frappe.throw("A BOM with no materials makes something out of nothing.")
		for row in self.items:
			if row.item_code == self.item_code:
				frappe.throw(f"Line {row.idx}: {self.item_code} cannot be made out of itself.")
			if flt(row.qty) <= 0:
				frappe.throw(f"Line {row.idx}: a quantity of {flt(row.qty):g} is not a quantity.")
