"""Product grouping -- DEC-048, a client change request that is not in the BRD.

The client makes control boards (ITC, SL, 133/2 ...) from a shared stock of
raw materials. One raw material goes into many boards, so it belongs to many
groups -- which is why this is not the Item's Category: an item has one
category, and it can be in any number of groups.

**A group is the main product's own list.** A KNIT 360 Item ticked Main
Product carries a Raw Materials table: an item and a count on each line. A
line may itself be a main product, so a group can sit inside another group.
Nothing else stores the relationship, so "where used" is read from those
tables when asked rather than kept as a second copy that could drift.

**Price.** A main product's price is what its raw materials cost plus a
margin. A raw material's cost is its price on a buying list; a line that is
itself a main product costs what its own materials cost, so a change to one
raw material's price reaches every product above it, however deep. The
margin's form -- percentage or fixed, one for all or per product -- is TBD
with the client (DEC-048); both forms are offered per price row until they
decide.

**Building** takes the group's raw materials out of stock and puts the
product in. That is KNIT 360 Product Build, which posts through the stock
ledger like every other movement.

**Not the BOM.** The BOM is handled later and separately (DEC-048). When it
is built it should read these groups rather than keep a second parts list.
"""

import frappe
from frappe.utils import flt, nowdate

from knit360_core.pricing import price_list as pricing

ITEM = "KNIT 360 Item"
LINE = "KNIT 360 Item Raw Material"
ITEM_PRICE = "KNIT 360 Item Price"

#: How deep a group may nest. Loops are refused when a group is saved, so
#: this only stops a corrupted table from hanging a request.
MAX_DEPTH = 25

PERCENTAGE = "Percentage"
AMOUNT = "Amount"


# --- reading the groups ---------------------------------------------------


def is_product(item_code):
	return bool(item_code and frappe.db.get_value(ITEM, item_code, "is_main_product"))


def lines(product):
	"""A main product's raw materials, in the order they were listed."""
	return frappe.get_all(
		LINE,
		filters={"parenttype": ITEM, "parentfield": "raw_materials", "parent": product},
		fields=["item_code", "qty"],
		order_by="idx asc",
	)


def _direct_users(item_code):
	"""Main products that list this item on their own group."""
	return frappe.get_all(
		LINE,
		filters={"parenttype": ITEM, "parentfield": "raw_materials", "item_code": item_code},
		fields=["parent", "qty"],
	)


def contains(product, item_code):
	"""Whether `item_code` is anywhere inside `product`'s group, at any depth."""
	frontier, seen = [product], set()
	while frontier:
		current = frontier.pop()
		if current in seen:
			continue
		seen.add(current)
		if len(seen) > 10 * MAX_DEPTH * MAX_DEPTH:
			break
		for row in lines(current):
			if row.item_code == item_code:
				return True
			frontier.append(row.item_code)
	return False


def where_used(item_code):
	"""Every main product this item goes into, directly or through another group.

	Returns one row per product: how many of this item one of that product
	takes in total, whether it is listed on the product's own group, and the
	groups it arrives through when it is not. Counts multiply down the chain:
	3 in a sub-board that the product uses twice is 6.
	"""
	found = {}
	frontier = [(item_code, 1.0, None, 0)]
	while frontier:
		code, multiplier, through, depth = frontier.pop()
		if depth >= MAX_DEPTH:
			continue
		for row in _direct_users(code):
			units = multiplier * flt(row.qty)
			entry = found.setdefault(
				row.parent, {"product": row.parent, "qty": 0.0, "direct": False, "through": []}
			)
			entry["qty"] += units
			if through is None:
				entry["direct"] = True
			elif through not in entry["through"]:
				entry["through"].append(through)
			frontier.append((row.parent, units, row.parent, depth + 1))
	return sorted(found.values(), key=lambda row: row["product"])


@frappe.whitelist()
def where_used_rows(item_code):
	"""For the Where Used list on the Item form."""
	frappe.has_permission(ITEM, "read", throw=True)
	rows = where_used(item_code)
	names = dict(
		frappe.get_all(
			ITEM,
			filters={"name": ["in", [row["product"] for row in rows] or [""]]},
			fields=["name", "item_name"],
			as_list=True,
		)
	)
	for row in rows:
		row["item_name"] = names.get(row["product"]) or ""
	return rows


# --- checking a group -------------------------------------------------------


def validate_group(item):
	"""Refusals for an Item's Raw Materials table. Called from Item.validate."""
	if not item.is_main_product:
		# Unticking Main Product empties the group, so no hidden table keeps
		# feeding where-used lists and prices.
		item.set("raw_materials", [])
		item.raw_material_count = 0
		item.total_units = 0
		return

	listed = set()
	for row in item.raw_materials:
		if not row.item_code:
			frappe.throw(f"Raw Materials line {row.idx}: choose the raw material.")
		if flt(row.qty) <= 0:
			frappe.throw(
				f"Raw Materials line {row.idx}: {row.item_code} has a count of "
				f"{flt(row.qty):g}. Say how many one {item.item_code} uses."
			)
		if row.item_code == item.item_code:
			frappe.throw(f"Raw Materials line {row.idx}: {item.item_code} cannot be made from itself.")
		if row.item_code in listed:
			frappe.throw(
				f"Raw Materials line {row.idx}: {row.item_code} is already listed. "
				f"Put the full count on one line, so the group says one thing about it."
			)
		listed.add(row.item_code)
		if contains(row.item_code, item.item_code):
			frappe.throw(
				f"Raw Materials line {row.idx}: {row.item_code} already contains "
				f"{item.item_code}, so {item.item_code} cannot contain {row.item_code}. "
				f"Each would need the other to be built first."
			)

	item.raw_material_count = len(item.raw_materials)
	item.total_units = sum(flt(row.qty) for row in item.raw_materials)


# --- pricing ----------------------------------------------------------------


def material_cost(product, cost_list, on_date=None, _depth=0):
	"""What one of `product` costs in raw materials, and what had no price.

	Returns (cost, unpriced). A raw material with no price on `cost_list` adds
	nothing and is named in `unpriced`, so the shortfall is visible rather
	than silently making the product look cheaper.
	"""
	total, unpriced = 0.0, []
	if _depth >= MAX_DEPTH:
		return total, unpriced
	for row in lines(product):
		if is_product(row.item_code):
			unit, missing = material_cost(row.item_code, cost_list, on_date, _depth + 1)
			unpriced.extend(missing)
		else:
			unit = pricing.rate_for(row.item_code, cost_list, on_date)
			if unit is None:
				unpriced.append(row.item_code)
				unit = 0.0
		total += flt(unit) * flt(row.qty)
	return total, unpriced


def cost_list_for(price):
	"""The buying list a product price reads its raw material prices from."""
	if price.cost_price_list:
		return price.cost_price_list
	chosen = pricing.default_for(pricing.BUYING)
	if not chosen:
		frappe.throw(
			f"{price.item_code} is priced from its raw materials, and no buying price "
			f"list says what they cost. Choose one in Raw Material Prices From, or "
			f"mark a buying price list as the default."
		)
	return chosen


def price_product(price):
	"""Fill a main product's Item Price: material cost, plus margin, is the rate."""
	price.cost_price_list = cost_list_for(price)
	cost, unpriced = material_cost(price.item_code, price.cost_price_list, nowdate())
	price.material_cost = cost
	price.unpriced_materials = "\n".join(sorted(set(unpriced)))

	margin = flt(price.margin)
	if price.margin_type == AMOUNT:
		added = margin
	else:
		price.margin_type = PERCENTAGE
		added = cost * margin / 100
	price.rate = flt(cost + added, price.precision("rate"))


@frappe.whitelist()
def preview_price(item_code, cost_price_list=None, margin_type=None, margin=None):
	"""For the Item Price form: what the rate would be, before saving."""
	frappe.has_permission(ITEM_PRICE, "read", throw=True)
	if not is_product(item_code):
		return {"is_main_product": 0}
	price = frappe.new_doc(ITEM_PRICE)
	price.update(
		{
			"item_code": item_code,
			"cost_price_list": cost_price_list,
			"margin_type": margin_type,
			"margin": margin,
		}
	)
	price_product(price)
	return {
		"is_main_product": 1,
		"cost_price_list": price.cost_price_list,
		"material_cost": price.material_cost,
		"unpriced_materials": price.unpriced_materials,
		"rate": price.rate,
	}


def reprice_users(item_code, include_self=False, skip=None):
	"""Recompute every product price that depends on this item.

	Called when a raw material's price changes, and when a product's group
	changes. Each affected price is saved, not written behind its back, so its
	version history shows what it was and what it became.
	"""
	products = [row["product"] for row in where_used(item_code)]
	if include_self and is_product(item_code):
		products.append(item_code)
	if not products:
		return []

	changed = []
	for name in frappe.get_all(ITEM_PRICE, filters={"item_code": ["in", products]}, pluck="name"):
		if name == skip:
			continue
		price = frappe.get_doc(ITEM_PRICE, name)
		before = (flt(price.rate), flt(price.material_cost), price.unpriced_materials or "")
		price_product(price)
		after = (flt(price.rate), flt(price.material_cost), price.unpriced_materials or "")
		if before != after:
			price.flags.knit360_repricing = True
			price.save(ignore_permissions=True)
			changed.append(name)
	return changed
