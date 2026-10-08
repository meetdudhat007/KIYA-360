"""KNIT 360 Purchase Order - FR-PROC-004.

DR-P2P-005 Purchase Order Commitment & Scheduling.

Totals come from knit360_core.pricing.totals, the same engine the sales side
uses, so a purchase order and a sales order are costed by one piece of code.

**It posts nothing to the ledger, on purpose.** An order is a commitment to
buy, not a transaction: no goods have moved and no money is owed. The books
first hear about it when the goods arrive (the receipt debits stock) and then
when the bill arrives (the bill creates the payable). Posting an order would
put a liability on the balance sheet for something that can still be
cancelled. An acceptance check asserts that an approved order writes no ledger
entry, so this stays true rather than merely being intended.
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
