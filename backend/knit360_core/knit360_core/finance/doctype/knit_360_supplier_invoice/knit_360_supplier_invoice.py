"""KNIT 360 Supplier Invoice - FR-PROC-006 / FR-FIN-002.

DR-P2P-009 Supplier Invoice & 3-Way Matching. Approval creates the payable.

**What the total is, and why -- DEC-020.** A supplier's bill shows the goods,
then freight and ancillary charges, then statutory tax. The amount payable is
all of it, because that is the amount that leaves the bank. So:

    net total     = sum of the billed lines
    grand total   = net total + freight and ancillary + statutory tax

The statutory tax figure stays **entered, not computed**. On a sales invoice the
tax is ours to calculate; on a supplier's invoice it is printed on their
document, and the figure that belongs in our books is the one they billed. The
tax template on this document records the treatment; it does not overwrite the
supplier's number.

Where freight posts in the ledger -- expensed, or added to the cost of the
stock received -- is a separate question and is recorded as `OQ-025`. It does
not affect the total, which is why this is built and that is still open.
"""

from frappe.model.document import Document

from knit360_core.pricing import totals

#: No tax template and no computed tax total: see the note above.
SHAPE = totals.Shape(
	table="items",
	rate="rate",
	tax_total=None,
	tax_template=None,
	additions=("freight_and_ancillary", "statutory_tax_amount"),
)


class KNIT360SupplierInvoice(Document):
	def validate(self):
		totals.apply(self, SHAPE)
