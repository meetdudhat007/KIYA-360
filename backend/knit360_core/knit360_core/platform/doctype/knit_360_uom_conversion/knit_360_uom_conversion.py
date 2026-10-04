"""KNIT 360 UOM Conversion - FR-PADM-1.4.7.

A factor between two units, named after the pair it converts.

The name is set here rather than with a `field:` autoname because the identity
of this record is the *pair*, not any one field. Without this the record took a
random hash for a name, which is unreadable in a report and impossible to refer
to from outside the system.

Naming it after the pair also makes the duplicate case a database error rather
than a silent second factor for the same conversion, which is the kind of
duplicate that produces two different answers to the same question.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class KNIT360UOMConversion(Document):
	def autoname(self):
		self.name = f"{self.from_uom} to {self.to_uom}"

	def validate(self):
		if self.from_uom == self.to_uom:
			frappe.throw("A unit does not need converting to itself.")
		if flt(self.factor) <= 0:
			frappe.throw(
				"A conversion factor must be greater than zero. "
				"A factor of zero would make every converted quantity nil."
			)
