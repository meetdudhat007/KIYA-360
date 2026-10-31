"""KNIT 360 Delivery Note - FR-SALES-005 / FR-INV-002.

DR-C2C-012 Dispatch and Delivery Note. Goods leave, so stock falls and the
cost of what left is charged to profit.

**What it posts.** Two things, in this order, because the second needs the
first's answer:

    stock   each line out of the shipping warehouse, at what it cost
    ledger  debit Cost of Goods Sold, credit Stock In Hand -- that same cost

The cost is **not** on this document and is never typed. It is what the stock
ledger says those units cost, worked out by FIFO over the receipts that
actually brought them in -- DEC-023. A dispatch is a quantity decision; what
it cost was settled when the goods were bought.

**Why it refuses to over-issue.** Stock is not allowed to go negative. The
alternative is books that claim goods nobody has, every later valuation wrong,
and nobody finding out until a count months later. Better a blocked delivery
note today.

This posts no revenue. The invoice does that, and the two are deliberately
separate: goods can leave before they are billed.

**Against an order** it may not dispatch more of an item than the order still
has outstanding (DR-C2C-012). **Serial-tracked items** carry one serial number
per unit, and each unit dispatched is registered as an installed asset for
the order's customer -- the start of its warranty and service history
(DR-A2S-001, FR-INV-003).
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.finance import ledger
from knit360_core.stock import ledger as stock_ledger

COMPANY = "KNIT 360 Company"
ITEM = "KNIT 360 Item"
ASSET = "KNIT 360 Asset"
SALES_ORDER = "KNIT 360 Sales Order"
REGISTERED = "Registered"


def serials(text):
	"""Serial numbers typed one per line, or separated by commas."""
	return [s.strip() for s in (text or "").replace(",", "\n").splitlines() if s.strip()]


def ordered_and_dispatched(sales_order, exclude=None, include_drafts=False):
	"""item -> (ordered, already dispatched) for one sales order."""
	ordered = {}
	for row in frappe.get_all("KNIT 360 Sales Order Item", filters={"parent": sales_order},
	                          fields=["item_code", "qty"]):
		ordered[row.item_code] = ordered.get(row.item_code, 0.0) + flt(row.qty)

	statuses = "(dn.docstatus = 1 OR (dn.docstatus = 0 AND dn.knit360_business_status = 'Draft'))" \
		if include_drafts else "dn.docstatus = 1"
	sent = frappe.db.sql(
		f"""SELECT item.item_code, SUM(item.qty) AS qty
		    FROM `tabKNIT 360 Delivery Note Item` item
		    JOIN `tabKNIT 360 Delivery Note` dn ON dn.name = item.parent
		    WHERE dn.sales_order = %(order)s AND dn.name != %(exclude)s AND {statuses}
		    GROUP BY item.item_code""",
		{"order": sales_order, "exclude": exclude or ""},
		as_dict=True,
	)
	dispatched = {row.item_code: flt(row.qty) for row in sent}
	return {item: (qty, dispatched.get(item, 0.0)) for item, qty in ordered.items()}, dispatched


class KNIT360DeliveryNote(Document):
	def validate(self):
		if not self.items:
			frappe.throw("A delivery note with no lines dispatches nothing.")
		for row in self.items:
			if flt(row.qty) <= 0:
				frappe.throw(f"Line {row.idx}: a dispatch of {flt(row.qty)} is not a dispatch.")
			if self.docstatus == 0:
				# Shown while it is still a draft, so somebody sees the refusal
				# in time to do something about it.
				stock_ledger.check_can_issue(
					row.item_code, self.source_warehouse, row.qty, self.company
				)
		if self.sales_order and self.docstatus == 0:
			self._within_the_order()

	def _within_the_order(self):
		balance, _sent = ordered_and_dispatched(self.sales_order, exclude=self.name)
		here = {}
		for row in self.items:
			here[row.item_code] = here.get(row.item_code, 0.0) + flt(row.qty)
		for item, qty in here.items():
			if item not in balance:
				frappe.throw(f"{item} is not on {self.sales_order}.")
			ordered, sent = balance[item]
			if qty - (ordered - sent) > stock_ledger.TOLERANCE:
				frappe.throw(
					f"{self.sales_order} ordered {ordered:g} of {item} and {sent:g} have already "
					f"been dispatched, so {ordered - sent:g} can go now, not {qty:g}."
				)

	def before_submit(self):
		for row in self.items:
			if not frappe.db.get_value(ITEM, row.item_code, "is_serial_tracked"):
				continue
			numbers = serials(row.serial_numbers)
			if flt(row.qty) != int(flt(row.qty)) or len(numbers) != int(flt(row.qty)):
				frappe.throw(
					f"Line {row.idx}: {row.item_code} is tracked by serial number, so dispatching "
					f"{flt(row.qty):g} needs {flt(row.qty):g} serial numbers, one per unit. "
					f"{len(numbers)} given."
				)
			if len(set(numbers)) != len(numbers):
				frappe.throw(f"Line {row.idx}: a serial number is repeated.")
			for number in numbers:
				known = frappe.db.get_value(ASSET, {"item_code": row.item_code, "serial_number": number}, "name")
				if known:
					frappe.throw(f"Line {row.idx}: {row.item_code} serial {number} has already been delivered as {known}.")

	def on_submit(self):
		movements = stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.delivery_note_date or nowdate(),
			[
				{
					"item_code": row.item_code,
					"warehouse": self.source_warehouse,
					"qty": -flt(row.qty),
					"remarks": f"Dispatched on {self.name}",
				}
				for row in self.items
			],
		)
		self._record_cost(movements)
		self._post_cost_of_sales()
		self._register_units()

	def on_cancel(self):
		units = self._registered_units()
		moved_on = [u.name for u in units if u.knit360_business_status != REGISTERED]
		if moved_on:
			frappe.throw(
				f"{', '.join(moved_on)} delivered on this note have been put into service. "
				f"Their history depends on this dispatch, so it cannot be cancelled."
			)
		stock_ledger.reverse(self.doctype, self.name)
		ledger.reverse(self.doctype, self.name)
		# The dispatch did not happen, so neither did the delivery of these units.
		for unit in units:
			frappe.delete_doc(ASSET, unit.name, ignore_permissions=True)

	def _registered_units(self):
		return frappe.get_all(ASSET, filters={"delivery_note": self.name},
		                      fields=["name", "knit360_business_status"])

	def _register_units(self):
		customer = frappe.db.get_value(SALES_ORDER, self.sales_order, "customer") if self.sales_order else None
		for row in self.items:
			if not frappe.db.get_value(ITEM, row.item_code, "is_serial_tracked"):
				continue
			name = frappe.db.get_value(ITEM, row.item_code, "item_name") or row.item_code
			for number in serials(row.serial_numbers):
				frappe.get_doc(
					{
						"doctype": ASSET,
						"asset_name": name,
						"item_code": row.item_code,
						"serial_number": number,
						"company": self.company,
						"customer": customer,
						"delivery_note": self.name,
						"sales_order": self.sales_order,
						"site_address": self.ship_to_address,
					}
				).insert(ignore_permissions=True)

	def _record_cost(self, movements):
		"""Copy what the ledger worked out back onto the lines, to be read.

		A figure shown on the document and a figure in the ledger must come
		from one place, so these are written from the movement rather than
		recomputed here.
		"""
		by_item = {}
		for name in movements:
			row = frappe.db.get_value(
				stock_ledger.SLE, name, ["item_code", "rate", "value_change"], as_dict=True
			)
			by_item[row.item_code] = row

		for line in self.items:
			move = by_item.get(line.item_code)
			if not move:
				continue
			line.db_set("valuation_rate", flt(move.rate), update_modified=False)
			line.db_set("stock_value", abs(flt(move.value_change)), update_modified=False)

	def _post_cost_of_sales(self):
		"""Charge what left to Cost of Goods Sold and take it off Stock In Hand."""
		cost = abs(
			flt(sum(flt(m.value_change) for m in
			        stock_ledger.voucher_movements(self.doctype, self.name)))
		)
		if cost <= stock_ledger.TOLERANCE:
			return

		accounts = frappe.db.get_value(
			COMPANY, self.company, ["default_cogs_account", "default_stock_account"], as_dict=True
		)
		if not accounts.default_cogs_account or not accounts.default_stock_account:
			frappe.throw(
				f"{self.company} has no Default Cost of Goods Sold Account or no "
				f"Default Stock Account, so the cost of this dispatch has nowhere "
				f"to go. Set them before dispatching."
			)

		ledger.post(
			self.doctype,
			self.name,
			self.company,
			self.delivery_note_date or nowdate(),
			[
				ledger.Line(account=accounts.default_cogs_account, debit=cost),
				ledger.Line(account=accounts.default_stock_account, credit=cost),
			],
			remarks=f"Cost of goods dispatched on {self.name}",
		)
