"""Line amounts and document totals -- FR-SALES-004 Pricing and Discounts.

Why this exists as one module rather than a method on each document.

The acceptance run found that of the fifteen KNIT 360 documents that carry a
table of line items, only two computed a total: Sales Invoice and Journal Entry.
The other thirteen -- Quotation, Sales Order, Purchase Order, Supplier Quotation
and the rest -- stored a quantity and a rate per line and then never multiplied
them. A quotation that cannot state its own price is a form, not a document.

The arithmetic is the same in all of them:

    line amount   = qty * rate, less any line discount
    net total     = sum of line amounts
    tax           = net total * the template's rates
    grand total   = net total + tax

Copying that into thirteen controllers would mean thirteen places to get
rounding wrong. So it lives here once, and each controller declares the field
names it happens to use. The field names genuinely differ between documents
(Quotation Item calls its rate `unit_rate`, Sales Order Item calls it `rate`),
and a declaration is cheaper and safer than renaming columns that already exist.

Tax is read from KNIT 360 Tax Template the same way Sales Invoice reads it. The
template still carries no account of its own; that is FR-TAX-001 and is not
solved here. This module computes the tax *figure* only. Where that figure is
posted stays the posting document's business, which is why nothing here touches
the ledger.
"""

import frappe
from frappe.utils import flt

TAX_TEMPLATE_ROW = "KNIT 360 Tax Template Row"


class Shape:
	"""Which fields on a document and its lines hold the money.

	Only `table` and `rate` are required. Everything else is optional, so a
	document that has no discount column or no tax template still totals.
	"""

	def __init__(self, table="items", rate="rate", qty="qty", amount="amount",
	             discount=None, net_total="net_total", tax_total="total_taxes",
	             grand_total="grand_total", tax_template="tax_template"):
		self.table = table
		self.rate = rate
		self.qty = qty
		self.amount = amount
		self.discount = discount
		self.net_total = net_total
		self.tax_total = tax_total
		self.grand_total = grand_total
		self.tax_template = tax_template


def line_amount(row, shape):
	"""qty * rate, less the line discount if the document has one.

	The discount is a percentage, because that is what the column stores. A
	discount outside 0-100 is refused rather than clamped: a negative discount
	is a surcharge entered in the wrong place, and over 100 is a document that
	pays the customer.
	"""
	gross = flt(row.get(shape.qty)) * flt(row.get(shape.rate))
	if not shape.discount:
		return flt(gross)

	percent = flt(row.get(shape.discount))
	if percent < 0 or percent > 100:
		frappe.throw(
			f"Line {row.idx}: a discount of {percent}% is not a discount. "
			f"Enter a percentage between 0 and 100."
		)
	return flt(gross * (1 - percent / 100.0))


def tax_amount(net, template):
	"""The template's rates applied to the net total. No template means no tax."""
	if not template or not net:
		return 0.0
	rates = frappe.get_all(TAX_TEMPLATE_ROW, filters={"parent": template}, pluck="rate")
	return flt(sum(flt(net) * flt(rate) / 100.0 for rate in rates))


def apply(doc, shape):
	"""Write the line amounts and the document totals onto `doc`.

	Called from the document's own validate, so the stored figures are always
	what the lines add up to and a person cannot type a total that disagrees
	with its own lines. Every total field is read-only in the doctype for the
	same reason.

	Returns the grand total, so a caller can refuse an empty document.
	"""
	rows = doc.get(shape.table) or []
	net = 0.0
	for row in rows:
		amount = line_amount(row, shape)
		if shape.amount and row.meta.has_field(shape.amount):
			row.set(shape.amount, amount)
		net += amount

	net = flt(net)
	tax = tax_amount(net, doc.get(shape.tax_template)) if shape.tax_template else 0.0

	_set(doc, shape.net_total, net)
	_set(doc, shape.tax_total, tax)
	_set(doc, shape.grand_total, flt(net + tax))
	return flt(net + tax)


def _set(doc, fieldname, value):
	"""Set a total only if the doctype actually declares the field.

	This lets one Shape describe documents at different stages of build-out --
	a document with no tax column simply does not get a tax total, rather than
	raising on a field that is not there.
	"""
	if fieldname and doc.meta.has_field(fieldname):
		doc.set(fieldname, value)
