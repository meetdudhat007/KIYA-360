"""KNIT 360 Sales Order - FR-SALES-003.

DR-C2C-005 Sales Order Commitment.

BRD 7.3 gives requirement names only; fields are traced to the approved
Phase 0B-2 expansion in document 31 via each field description.

Pricing is the shared knit360_core.pricing.totals, the same engine the Quotation
uses, so an order carries the same arithmetic as the quotation it came from.
"""

import frappe
from frappe.model.document import Document

from knit360_core.pricing import price_list, totals

SHAPE = totals.Shape(table="items", rate="rate")


class KNIT360SalesOrder(Document):
	def validate(self):
		price_list.apply(self, SHAPE, price_list.SELLING)
		grand_total = totals.apply(self, SHAPE)
		if self.items and not grand_total:
			frappe.throw(
				"This order has lines but totals nothing. "
				"Enter a rate, or remove the lines."
			)
