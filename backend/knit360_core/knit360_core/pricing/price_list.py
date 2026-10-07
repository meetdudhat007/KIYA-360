"""What an item costs, read from the masters -- FR-SALES-004 / FR-INV-004.

The Price List and Item Price masters have existed since Phase 0B-2 and have
been populated on every demonstration site. Until now no document read them:
every rate on every quotation, order and invoice was typed by hand. So the
masters were decoration, and two people quoting the same item on the same day
could quote two different prices with nothing to say which was right.

**Where a rate comes from.** The first of these that answers:

    1. the line's own rate, if somebody typed one
    2. the Item Price for this item on this document's price list, valid on
       this document's date
    3. nothing -- the line stays at what it was, and the document's own
       validate decides whether a nil line is acceptable

A typed rate is never overwritten. Prices are a starting point, not a cage:
the salesperson in front of the customer may know something the master does
not. What the master knows is kept as well, in `price_list_rate`, so the
difference between the list and what was actually charged is visible on the
document rather than lost.

**Which list.** Also the first that answers: the list named on the document,
then the party's own default (`default_price_list` on the customer), then the
company-wide default for this side of the business. A selling document will
not price from a buying list, and that is refused rather than quietly used --
selling at cost is a mistake worth stopping.

**Validity is a window, not a date.** An Item Price with no `valid_from` has
always applied; one with no `valid_upto` still applies. Where two prices both
apply, the one that started later wins, because that is the newer decision. A
price quoted in a specific unit of measure beats one quoted without, because
it is the more specific statement about the same thing.

This module reads masters and returns figures. It writes nothing to the
ledger and stores no price of its own.
"""

import frappe
from frappe.utils import flt, getdate, nowdate

ITEM_PRICE = "KNIT 360 Item Price"
PRICE_LIST = "KNIT 360 Price List"

SELLING = "Selling"
BUYING = "Buying"

#: The field on each document that holds the chosen list, where it has one.
PRICE_LIST_FIELD = "price_list"

#: The read-only line field that records what the master said.
LINE_PRICE_FIELD = "price_list_rate"


def default_for(applies_to):
	"""The company's default list for this side of the business, or None.

	Two lists marked default for the same side is a master-data error rather
	than something to guess about, so the older one is used and the condition
	is reported by an acceptance check rather than hidden here.
	"""
	names = frappe.get_all(
		PRICE_LIST,
		filters={"applies_to": applies_to, "is_default": 1, "disabled": 0},
		pluck="name",
		order_by="creation asc",
	)
	return names[0] if names else None


def party_default(doc):
	"""The customer's own list, where the document has a customer that has one."""
	customer = doc.get("customer")
	if not customer:
		return None
	return frappe.db.get_value("KNIT 360 Customer", customer, "default_price_list")


def for_document(doc, applies_to):
	"""Which list this document prices from. Returns a name, or None.

	None is a legitimate answer: a site with no price lists at all still
	works, with every rate typed, exactly as it did before this module.
	"""
	named = doc.get(PRICE_LIST_FIELD) if doc.meta.has_field(PRICE_LIST_FIELD) else None
	if named:
		_check_side(named, applies_to, doc)
		return named

	chosen = party_default(doc) if applies_to == SELLING else None
	if chosen:
		_check_side(chosen, applies_to, doc)
		return chosen

	return default_for(applies_to)


def _check_side(name, applies_to, doc):
	"""Refuse a list that belongs to the other side of the business."""
	row = frappe.db.get_value(PRICE_LIST, name, ["applies_to", "disabled"], as_dict=True)
	if not row:
		frappe.throw(f"Price list {name} does not exist.")
	if row.disabled:
		frappe.throw(
			f"Price list {name} is disabled, so it cannot price {doc.doctype}. "
			f"Choose another list, or enable it."
		)
	if row.applies_to != applies_to:
		frappe.throw(
			f"{name} is a {row.applies_to} price list, and {doc.doctype} is a "
			f"{applies_to.lower()} document. Pricing a sale from a buying list "
			f"would sell at cost."
		)


def rate_for(item_code, price_list, on_date=None, uom=None):
	"""The rate the master holds for this item on this date, or None.

	The candidate rows are read and then filtered here rather than in SQL.
	The set is one item on one list -- a handful of rows -- and the rule for
	choosing between them reads as the rule rather than as a query.
	"""
	if not item_code or not price_list:
		return None

	when = getdate(on_date or nowdate())
	rows = frappe.get_all(
		ITEM_PRICE,
		filters={"item_code": item_code, "price_list": price_list},
		fields=["name", "rate", "uom", "valid_from", "valid_upto"],
	)

	applicable = [
		row for row in rows
		if (not row.valid_from or getdate(row.valid_from) <= when)
		and (not row.valid_upto or getdate(row.valid_upto) >= when)
	]

	# A line that does not say which unit it means is counted in the item's
	# own stock unit -- that is what the quantity column means everywhere else
	# in the system, so it is what the price must be read in.
	wanted = uom or frappe.db.get_value("KNIT 360 Item", item_code, "stock_uom")
	if wanted:
		applicable = [row for row in applicable if row.uom == wanted] or [
			row for row in applicable if not row.uom
		]
	else:
		applicable = [row for row in applicable if not row.uom]

	if not applicable:
		return None

	applicable.sort(
		key=lambda row: (
			getdate(row.valid_from) if row.valid_from else getdate("1900-01-01"),
			row.name,
		),
		reverse=True,
	)
	return flt(applicable[0].rate)


def apply(doc, shape, applies_to, date_field=None):
	"""Stamp the list rate on every line, and fill a rate nobody typed.

	Called from the document's validate before the totals are computed, so
	the arithmetic sees the rate that was actually used. Returns how many
	lines were priced from the master, which the acceptance checks read.
	"""
	price_list = for_document(doc, applies_to)
	if not price_list:
		return 0

	if doc.meta.has_field(PRICE_LIST_FIELD) and not doc.get(PRICE_LIST_FIELD):
		doc.set(PRICE_LIST_FIELD, price_list)

	when = doc.get(date_field) if date_field else None
	filled = 0

	for row in doc.get(shape.table) or []:
		rate = rate_for(row.get("item_code"), price_list, when, row.get("uom"))
		if rate is None:
			continue
		if row.meta.has_field(LINE_PRICE_FIELD):
			row.set(LINE_PRICE_FIELD, rate)
		if not flt(row.get(shape.rate)):
			row.set(shape.rate, rate)
			filled += 1

	return filled
