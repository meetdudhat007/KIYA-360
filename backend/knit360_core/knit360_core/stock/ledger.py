"""The stock ledger -- FR-INV-002 Stock Quantity, FR-INV-006 Stock Valuation.

Everything that moves stock goes through post(). Nothing else writes a
KNIT 360 Stock Ledger Entry.

**A quantity is never stored as the truth.** The stock of an item in a
warehouse is the sum of the signed movements against it, exactly as an account
balance is the sum of its postings and a leave balance is the sum of its
entries. There is no `qty` field on Item, and no quantity on Bin -- a Bin is a
place, aisle and rack and shelf, and it tells you where to walk, not what you
own.

**Valuation is FIFO, decided in DEC-023.** Ind AS 2 paragraph 25 permits only
FIFO and weighted average, so LIFO is not offered: it would be a setting that
puts the client in breach. The cost of what leaves is computed by replaying the
layers that came in, oldest first, rather than by keeping a running queue --
same reason as everywhere else in this system. A stored queue is a second copy
of the truth, and when it disagrees with the movements behind it nothing can
say which is right.

Paragraph 25 also requires one formula per class of similar inventory rather
than one for the whole company, which is why `valuation_method` lives on the
Item.

**What this does not do.** Ind AS 2 also requires stock to be carried at the
lower of cost and net realisable value. Nothing here writes stock down, and
deciding when to is a judgement about the client's market, item by item. That
is `OQ-026`, raised and still open -- recorded rather than quietly skipped.
"""

import frappe
from frappe.utils import flt, getdate

SLE = "KNIT 360 Stock Ledger Entry"
ITEM = "KNIT 360 Item"

#: Rounding tolerance, matching the general ledger's.
TOLERANCE = 0.005

#: What Item.valuation_method may say. LIFO is absent on purpose -- Ind AS 2
#: paragraph 25 does not permit it.
METHODS = ("FIFO", "Moving Average")
DEFAULT_METHOD = "FIFO"


def method_for(item_code):
	"""The cost formula for one item, defaulting to FIFO."""
	declared = (frappe.db.get_value(ITEM, item_code, "valuation_method") or "").strip()
	return declared if declared in METHODS else DEFAULT_METHOD


# --- reading ------------------------------------------------------------


def _movements(item_code, warehouse=None, company=None, upto=None, before=None):
	"""Live movements in the order they happened."""
	conditions = ["item_code = %(item_code)s", "is_cancelled = 0"]
	values = {"item_code": item_code}
	if warehouse:
		conditions.append("warehouse = %(warehouse)s")
		values["warehouse"] = warehouse
	if company:
		conditions.append("company = %(company)s")
		values["company"] = company
	if upto:
		conditions.append("posting_date <= %(upto)s")
		values["upto"] = getdate(upto)
	if before:
		conditions.append("name != %(before)s")
		values["before"] = before

	return frappe.db.sql(
		f"""SELECT name, posting_date, actual_qty, rate, value_change
		    FROM `tab{SLE}` WHERE {" AND ".join(conditions)}
		    ORDER BY posting_date, creation, name""",
		values,
		as_dict=True,
	)


def balance(item_code, warehouse=None, company=None, upto=None):
	"""How many of an item are in a warehouse. Derived, never stored."""
	return flt(sum(flt(row.actual_qty) for row in _movements(item_code, warehouse, company, upto)))


def value(item_code, warehouse=None, company=None, upto=None):
	"""What that stock is carried at."""
	return flt(sum(flt(row.value_change) for row in _movements(item_code, warehouse, company, upto)))


def layers(item_code, warehouse, company=None, upto=None, before=None):
	"""The unconsumed receipts, oldest first, as [qty, rate] pairs.

	This is the FIFO queue, rebuilt from the movements each time it is needed
	rather than carried along. An issue eats the oldest layers; a reversal of
	an issue puts a layer back at its own rate.
	"""
	queue = []
	for row in _movements(item_code, warehouse, company, upto, before):
		qty = flt(row.actual_qty)
		if qty > 0:
			queue.append([qty, flt(row.rate)])
			continue

		# An issue consumes from the front.
		remaining = -qty
		while remaining > TOLERANCE and queue:
			if queue[0][0] > remaining + TOLERANCE:
				queue[0][0] -= remaining
				remaining = 0
			else:
				remaining -= queue[0][0]
				queue.pop(0)
	return queue


def outgoing_rate(item_code, warehouse, qty, company=None, upto=None):
	"""What `qty` leaving now costs, and nothing about whether it may.

	FIFO walks the layers oldest first. Moving Average divides the value held
	by the quantity held. Both are permitted by Ind AS 2 paragraph 25; which
	one applies is the Item's own setting, because the standard requires one
	formula per class of similar inventory rather than one per company.
	"""
	qty = flt(qty)
	if qty <= 0:
		return 0.0

	if method_for(item_code) == "Moving Average":
		held = balance(item_code, warehouse, company, upto)
		if held <= TOLERANCE:
			return 0.0
		return flt(value(item_code, warehouse, company, upto) / held)

	queue = layers(item_code, warehouse, company, upto)
	taken, cost = 0.0, 0.0
	for layer_qty, layer_rate in queue:
		if taken >= qty - TOLERANCE:
			break
		use = min(layer_qty, qty - taken)
		cost += use * layer_rate
		taken += use

	if taken <= TOLERANCE:
		return 0.0
	# Short of stock, the rate of what there was is the best honest answer;
	# whether the issue is allowed at all is check_can_issue's business.
	return flt(cost / taken)


def statement(item_code, warehouse=None, company=None):
	"""Every movement with a running quantity, for showing on a screen."""
	running, out = 0.0, []
	for row in _movements(item_code, warehouse, company):
		running += flt(row.actual_qty)
		entry = frappe.db.get_value(
			SLE, row.name, ["voucher_type", "voucher_no", "warehouse"], as_dict=True
		)
		out.append(
			{
				"entry": row.name,
				"posting_date": row.posting_date,
				"warehouse": entry.warehouse,
				"voucher_type": entry.voucher_type,
				"voucher_no": entry.voucher_no,
				"qty": flt(row.actual_qty),
				"rate": flt(row.rate),
				"value_change": flt(row.value_change),
				"balance": flt(running),
			}
		)
	return out


# --- refusals -----------------------------------------------------------


def check_can_issue(item_code, warehouse, qty, company=None):
	"""Refuse an issue that would drive stock negative.

	Negative stock is not a smaller problem than a blocked delivery note. It
	means the books claim goods that are not there, every valuation after it is
	wrong, and nobody finds out until a stock count months later. So the
	document is refused now and somebody receives the goods properly.
	"""
	held = balance(item_code, warehouse, company)
	if flt(qty) - held > TOLERANCE:
		frappe.throw(
			f"{warehouse} holds {held:g} of {item_code} and this issues {flt(qty):g}. "
			f"Receive the stock first, or reduce the quantity -- stock is not "
			f"allowed to go negative, because every valuation after it would be wrong."
		)
	return held


# --- writing ------------------------------------------------------------


def post(voucher_type, voucher_no, company, posting_date, movements):
	"""Write one document's stock movements. The only writer.

	`movements` is a list of dicts: item_code, warehouse, qty (signed), and for
	a receipt, rate. An issue's rate is not supplied -- it is what the stock
	already cost, which is this module's job to work out and not the calling
	document's.
	"""
	if not movements:
		frappe.throw(f"{voucher_type} {voucher_no}: nothing to move.")

	written = []
	for move in movements:
		qty = flt(move["qty"])
		if abs(qty) <= TOLERANCE:
			continue

		item_code, warehouse = move["item_code"], move["warehouse"]
		if not frappe.db.exists(ITEM, item_code):
			frappe.throw(f"{voucher_type} {voucher_no}: there is no item called {item_code}.")
		if not frappe.db.exists("KNIT 360 Warehouse", warehouse):
			frappe.throw(f"{voucher_type} {voucher_no}: there is no warehouse called {warehouse}.")

		if qty > 0:
			rate = flt(move.get("rate"))
			if rate <= 0:
				frappe.throw(
					f"{voucher_type} {voucher_no}: {item_code} is coming in at a rate of "
					f"{rate}. Stock received for nothing cannot be valued, and every "
					f"issue after it would be costed wrongly."
				)
			value_change = flt(qty * rate)
		else:
			check_can_issue(item_code, warehouse, -qty, company)
			rate = outgoing_rate(item_code, warehouse, -qty, company)
			value_change = flt(qty * rate)

		entry = frappe.get_doc(
			{
				"doctype": SLE,
				"item_code": item_code,
				"warehouse": warehouse,
				"company": company,
				"posting_date": posting_date,
				"actual_qty": qty,
				"rate": rate,
				"value_change": value_change,
				"voucher_type": voucher_type,
				"voucher_no": voucher_no,
				"is_cancelled": 0,
				"remarks": move.get("remarks"),
			}
		).insert(ignore_permissions=True)
		written.append(entry.name)

	if not written:
		frappe.throw(f"{voucher_type} {voucher_no}: every line is for nil quantity.")
	return written


def reverse(voucher_type, voucher_no, posting_date=None):
	"""Undo a document's movements by writing their mirror.

	The originals are flagged rather than deleted, like the general ledger's.
	A reversed issue puts the stock back at the rate it left at, so the value
	returns to where it was rather than at today's cost.
	"""
	existing = frappe.get_all(
		SLE,
		filters={"voucher_type": voucher_type, "voucher_no": voucher_no, "is_cancelled": 0},
		fields=["name", "item_code", "warehouse", "company", "posting_date",
		        "actual_qty", "rate", "value_change"],
	)
	if not existing:
		return []

	written = []
	for row in existing:
		mirror = frappe.get_doc(
			{
				"doctype": SLE,
				"item_code": row.item_code,
				"warehouse": row.warehouse,
				"company": row.company,
				"posting_date": posting_date or row.posting_date,
				"actual_qty": -flt(row.actual_qty),
				"rate": flt(row.rate),
				"value_change": -flt(row.value_change),
				"voucher_type": voucher_type,
				"voucher_no": voucher_no,
				"is_cancelled": 1,
				"remarks": f"Reversal of {voucher_type} {voucher_no}",
			}
		).insert(ignore_permissions=True)
		frappe.db.set_value(SLE, row.name, "is_cancelled", 1, update_modified=False)
		written.append(mirror.name)
	return written


def voucher_movements(voucher_type, voucher_no, include_cancelled=0):
	"""What one document did to stock, for showing on that document."""
	filters = {"voucher_type": voucher_type, "voucher_no": voucher_no}
	if not int(include_cancelled or 0):
		filters["is_cancelled"] = 0
	return frappe.get_all(
		SLE,
		filters=filters,
		fields=["name", "item_code", "warehouse", "posting_date", "actual_qty",
		        "rate", "value_change", "is_cancelled"],
		order_by="creation",
	)


@frappe.whitelist()
def stock_on_hand(company=None, warehouse=None):
	"""Every item holding stock, with its quantity and value.

	Derived on every call. There is nowhere this figure is kept.
	"""
	conditions = ["is_cancelled = 0"]
	values = {}
	if company:
		conditions.append("company = %(company)s")
		values["company"] = company
	if warehouse:
		conditions.append("warehouse = %(warehouse)s")
		values["warehouse"] = warehouse

	rows = frappe.db.sql(
		f"""SELECT item_code, warehouse, SUM(actual_qty) AS qty,
		           SUM(value_change) AS value
		    FROM `tab{SLE}` WHERE {" AND ".join(conditions)}
		    GROUP BY item_code, warehouse
		    HAVING ABS(SUM(actual_qty)) > {TOLERANCE}
		    ORDER BY item_code, warehouse""",
		values,
		as_dict=True,
	)
	for row in rows:
		row["rate"] = flt(row.value / row.qty) if row.qty else 0.0
		row["method"] = method_for(row.item_code)
	return rows
