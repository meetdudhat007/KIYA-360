"""KNIT 360 Supplier Quotation - FR-PROC-003.

DR-P2P-004 Supplier Quotation & Bid Evaluation.

A bid cannot be evaluated against another bid until both state a number, so the
shared pricing engine runs here too.

`taxes` on this doctype is free text describing what the supplier said about
tax, not a rate table, so no tax total is computed from it. The grand total is
therefore the net of the lines. Comparing bids on net is the right comparison
anyway, because tax is the same for every supplier.

Prices are **not** read from the buying price list here, although every other
pricing document reads its list -- FR-SALES-004. A supplier quotation records
what the supplier said their price is. Filling that in from our own master
would be putting words in their mouth, and the bid comparison this document
exists for would then be comparing our own figures with each other.
"""

import frappe
from frappe.model.document import Document

from knit360_core.pricing import totals

#: tax_template is deliberately absent: this doctype has no rate table to read.
SHAPE = totals.Shape(table="items", rate="rate", tax_total=None, tax_template=None)


class KNIT360SupplierQuotation(Document):
	def validate(self):
		grand_total = totals.apply(self, SHAPE)
		if self.items and not grand_total:
			frappe.throw(
				"This bid has lines but quotes no price. "
				"Enter a rate, or remove the lines."
			)
