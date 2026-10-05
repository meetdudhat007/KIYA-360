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
    grand total   = net total + tax + any document-level additions

The additions exist for one case, recorded as DEC-020: a supplier's bill
carries freight and statutory tax outside the line items, and the amount
payable is everything printed on that bill.

Copying that into thirteen controllers would mean thirteen places to get
rounding wrong. So it lives here once, and each controller declares the field
names it happens to use. The field names genuinely differ between documents
(Quotation Item calls its rate `unit_rate`, Sales Order Item calls it `rate`),
and a declaration is cheaper and safer than renaming columns that already exist.

Tax is read from KNIT 360 Tax Template, component by component. Since DEC-021
a component can name the account it posts to, so tax_lines() returns the
components rather than only their sum -- a posting document needs one GL line
per account, not one lump. This module still never touches the ledger: it
computes figures and names accounts, and where they are posted stays the
posting document's business.
"""

import frappe
from frappe.utils import flt

TAX_TEMPLATE_ROW = "KNIT 360 Tax Template Row"


class TaxLine:
	"""One tax component of one document.

	`account` is whatever the template row named, which may be nothing. The
	fallback is deliberately not resolved here: it depends on whether the
	document charges tax or pays it, and only the document knows that.
	"""

	def __init__(self, component, rate, amount, account=None):
		self.component = component
		self.rate = flt(rate)
		self.amount = flt(amount)
		self.account = account


class Shape:
	"""Which fields on a document and its lines hold the money.

	Only `table` and `rate` are required. Everything else is optional, so a
	document that has no discount column or no tax template still totals.
	"""

	def __init__(self, table="items", rate="rate", qty="qty", amount="amount",
	             discount=None, net_total="net_total", tax_total="total_taxes",
	             grand_total="grand_total", tax_template="tax_template",
	             additions=()):
		self.table = table
		self.rate = rate
		self.qty = qty
		self.amount = amount
		self.discount = discount
		self.net_total = net_total
		self.tax_total = tax_total
		self.grand_total = grand_total
		self.tax_template = tax_template
		#: Document-level fields whose values add to the grand total.
		self.additions = tuple(additions)


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


def tax_lines(net, template):
	"""The template's components, each applied to the net total.

	Returns an empty list for no template and for a nil net, so a document
	without tax simply has no tax lines rather than a zero one.
	"""
	if not template or not net:
		return []
	rows = frappe.get_all(
		TAX_TEMPLATE_ROW,
		filters={"parent": template},
		fields=["tax_component", "rate", "tax_account"],
		order_by="idx asc",
	)
	return [
		TaxLine(
			component=row.tax_component,
			rate=row.rate,
			amount=flt(net) * flt(row.rate) / 100.0,
			account=row.tax_account,
		)
		for row in rows
	]


def tax_amount(net, template):
	"""The tax total: the sum of the components, and nothing else.

	Derived from tax_lines rather than computed separately, so the figure a
	document stores can never disagree with the lines it posts.
	"""
	return flt(sum(line.amount for line in tax_lines(net, template)))


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

	# Document-level charges outside the lines -- DEC-020.
	additions = flt(sum(flt(doc.get(field)) for field in shape.additions))

	_set(doc, shape.net_total, net)
	_set(doc, shape.tax_total, tax)
	_set(doc, shape.grand_total, flt(net + tax + additions))
	return flt(net + tax + additions)


def _set(doc, fieldname, value):
	"""Set a total only if the doctype actually declares the field.

	This lets one Shape describe documents at different stages of build-out --
	a document with no tax column simply does not get a tax total, rather than
	raising on a field that is not there.
	"""
	if fieldname and doc.meta.has_field(fieldname):
		doc.set(fieldname, value)
