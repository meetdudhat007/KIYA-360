"""KNIT 360 Purchase Order - FR-PROC-004.

DR-P2P-005 Purchase Order Commitment & Scheduling.

Totals come from knit360_core.pricing.totals, the same engine the sales side
uses, so a purchase order and a sales order are costed by one piece of code.
"""

import frappe
from frappe.model.document import Document

from knit360_core.pricing import price_list, totals

SHAPE = totals.Shape(table="items", rate="rate", discount="discount_percentage")


class KNIT360PurchaseOrder(Document):
	def validate(self):
		price_list.apply(self, SHAPE, price_list.BUYING, date_field="order_date")
		grand_total = totals.apply(self, SHAPE)
		if self.items and not grand_total:
			frappe.throw(
				"This order has lines but commits to nothing. "
				"Enter a rate, or remove the lines."
			)
