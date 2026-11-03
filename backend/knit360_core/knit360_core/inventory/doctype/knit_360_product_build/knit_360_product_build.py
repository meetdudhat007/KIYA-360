"""KNIT 360 Product Build -- DEC-054, a client change request that is not in the BRD.

Building a main product. The raw materials come from the product's group on
the Item, times the quantity to build; they are never typed here.

**What it posts, on Built.** In this order, because the second needs the
first's answer:

    raw materials  out of Raw Materials From, each at what it cost (FIFO
                   or the item's own method -- the stock ledger decides)
    product        into Finished Product To, at the raw materials' total
                   cost divided by the quantity built

Stock stays per raw material: every movement is one item in one warehouse,
exactly like a Work Order's.

**Warnings and refusals, as the owner asked (DEC-054).**

    about to run out  a raw material this build would leave below its
                      Safety Stock is named in a warning, on save and again
                      when it is built. The build goes ahead.
    not enough        a raw material with less in stock than the build needs
                      stops the build. The error names every short item, what
                      is needed, what is held and the shortfall, so one
                      reading says everything to receive.

**Not the BOM or the Work Order.** The Work Order builds from a BOM; this
builds from the product's group. DEC-054 keeps the BOM separate for now.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.inventory import grouping
from knit360_core.stock import ledger as stock_ledger

BUILT = "Built"
CANCELLED = "Cancelled"


def _fmt(qty):
	return f"{flt(qty):g}"


class KNIT360ProductBuild(Document):
	def validate(self):
		if flt(self.qty) <= 0:
			frappe.throw("Say how many to build.")
		if not grouping.is_product(self.product):
			frappe.throw(
				f"{self.product} is not a main product. Tick Main Product on the item "
				f"and list its raw materials before building it."
			)
		if self.docstatus == 0:
			self._explode()
			self._warn(on_save=True)

	def _explode(self):
		"""The raw materials for the quantity to build, from the product's group."""
		rows = grouping.lines(self.product)
		if not rows:
			frappe.throw(
				f"{self.product} has no raw materials listed in its group yet, so there "
				f"is nothing to build it from. Add them on the item first."
			)
		self.set("materials", [])
		for row in rows:
			if flt(row.qty) * flt(self.qty) <= stock_ledger.TOLERANCE:
				frappe.throw(f"{row.item_code} works out at a quantity of nil for this build.")
			self.append(
				"materials",
				{
					"item_code": row.item_code,
					"per_unit_qty": flt(row.qty),
					"required_qty": flt(row.qty) * flt(self.qty),
					"available_qty": self._held(row.item_code),
				},
			)

	def _held(self, item_code):
		if not self.source_warehouse:
			return 0
		return stock_ledger.balance(item_code, self.source_warehouse, self.company)

	def _shortfalls(self):
		"""(item, needed, held) for every raw material there is not enough of."""
		short = []
		for row in self.materials:
			held = self._held(row.item_code)
			if flt(row.required_qty) - held > stock_ledger.TOLERANCE:
				short.append((row.item_code, flt(row.required_qty), held))
		return short

	def _running_low(self, posted=False):
		"""(item, left, safety stock) for every raw material this build leaves below its safety stock.

		Before posting, what is left is what is held less what the build needs;
		once posted, the ledger already holds the answer.
		"""
		low = []
		for row in self.materials:
			safety = flt(frappe.db.get_value("KNIT 360 Item", row.item_code, "safety_stock"))
			if safety <= 0:
				continue
			left = self._held(row.item_code) - (0 if posted else flt(row.required_qty))
			if -stock_ledger.TOLERANCE <= left < safety:
				low.append((row.item_code, left, safety))
		return low

	def _shortfall_message(self, short, lead="Cannot build"):
		lines = "".join(
			f"<li>{item}: needs {_fmt(needed)}, has {_fmt(held)} ({_fmt(needed - held)} short)</li>"
			for item, needed, held in short
		)
		return (
			f"{lead} {_fmt(self.qty)} × {self.product}: {self.source_warehouse} "
			f"does not hold enough of {len(short)} raw material(s).<ul>{lines}</ul>"
			f"Receive the missing stock, or build fewer."
		)

	def _warn(self, on_save=False):
		if not self.source_warehouse:
			return
		if on_save:
			short = self._shortfalls()
			if short:
				frappe.msgprint(
					self._shortfall_message(
						short, "This build will be refused until the stock arrives. Cannot build"
					),
					title="Not enough stock",
					indicator="red",
				)
				return
		low = self._running_low(posted=not on_save)
		if low:
			lines = "".join(
				f"<li>{item}: {_fmt(left)} left, safety stock {_fmt(safety)}</li>"
				for item, left, safety in low
			)
			when = "After this build" if on_save else "This build has left"
			frappe.msgprint(
				f"{when} {len(low)} raw material(s) in {self.source_warehouse} "
				f"below safety stock. Reorder soon.<ul>{lines}</ul>",
				title="Stock about to run out",
				indicator="orange",
			)

	def before_business_status(self, from_status, to_status):
		if to_status == BUILT:
			if not (self.source_warehouse and self.target_warehouse):
				frappe.throw("Say which store the raw materials come from and which the product goes to.")
			short = self._shortfalls()
			if short:
				frappe.throw(self._shortfall_message(short), title="Not enough stock")
		if to_status == CANCELLED and self.docstatus == 1:
			held = stock_ledger.balance(self.product, self.target_warehouse, self.company)
			if held + stock_ledger.TOLERANCE < flt(self.qty):
				frappe.throw(
					f"Only {_fmt(held)} of the {_fmt(self.qty)} {self.product} built here "
					f"are still in {self.target_warehouse}; the rest have left. Bring them "
					f"back before cancelling, or the books would show goods that are not there."
				)

	def on_submit(self):
		date = self.posting_date or nowdate()
		used = stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			date,
			[
				{
					"item_code": row.item_code,
					"warehouse": self.source_warehouse,
					"qty": -flt(row.required_qty),
					"remarks": f"Used to build {self.product} on {self.name}",
				}
				for row in self.materials
			],
		)

		total = 0.0
		for row, entry in zip(self.materials, used):
			move = frappe.db.get_value(stock_ledger.SLE, entry, ["rate", "value_change"], as_dict=True)
			row.db_set("valuation_rate", flt(move.rate), update_modified=False)
			row.db_set("cost_amount", abs(flt(move.value_change)), update_modified=False)
			total += abs(flt(move.value_change))

		unit_cost = total / flt(self.qty)
		stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			date,
			[
				{
					"item_code": self.product,
					"warehouse": self.target_warehouse,
					"qty": flt(self.qty),
					"rate": unit_cost,
					"remarks": f"Built on {self.name}",
				}
			],
		)
		self.db_set("total_material_cost", total, update_modified=False)
		self.db_set("unit_cost", unit_cost, update_modified=False)
		self._warn()

	def on_cancel(self):
		stock_ledger.reverse(self.doctype, self.name)
