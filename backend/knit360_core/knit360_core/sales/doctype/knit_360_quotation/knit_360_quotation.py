"""KNIT 360 Quotation - FR-SALES-002 / FR-SALES-004.

DR-C2C-004 Sales Quotation, including Pricing and Discounts (FR-SALES-004).

BRD 7.3 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via each field description.

Pricing lives in knit360_core.pricing.totals, shared with Sales Order, so the
two documents cannot disagree about what a line is worth. The line rate column
here is `unit_rate` rather than `rate`, which is why the shape is declared
rather than assumed.
"""

import frappe
from frappe.model.document import Document

from knit360_core.pricing import totals

SHAPE = totals.Shape(
	table="items",
	rate="unit_rate",
	discount="discount_percentage",
)


class KNIT360Quotation(Document):
	def validate(self):
		grand_total = totals.apply(self, SHAPE)
		if self.items and not grand_total:
			frappe.throw(
				"This quotation has lines but totals nothing. "
				"Enter a unit rate, or remove the lines."
			)
