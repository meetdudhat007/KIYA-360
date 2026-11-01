"""KNIT 360 Work Order - FR-MFG-003.

DR-C2C-009 Shop Floor Production Execution. Distinct from the field-service work
order (DR-A2S-007); doc 33 requires the two not share a schema.

DR-C2C-009 acceptance: "Completing production posts inventory ledger
deductions for raw materials and creates an uninspected finished goods
receipt." So on Completed, in this order, because the second needs the first's
answer:

    materials       out of Raw Materials From, each at what it cost (FIFO)
    finished goods  into Finished Goods To, at the materials' total cost
                    divided by the quantity made

**No general ledger posting.** Both legs are stock: what leaves as material
arrives as finished goods, at the same value, and the chart carries one Stock
In Hand account for both. The stock ledger moves; the accounts do not change.

**Not built.** The finished goods carry material cost only. Labour and factory
overhead are not added to it, which Ind AS 2 paragraph 12 includes in the cost
of conversion; production costing (FR-MFG-006) is the work that would add them
-- DEC-040. Transfer to work-in-progress and job cards (DR-C2C-009 Stages 9A
and 9B) are not built either: materials leave stock when production is
completed, not when it starts.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate

from knit360_core.stock import ledger as stock_ledger

BOM = "KNIT 360 BOM"
COMPLETED = "Completed"
CANCELLED = "Cancelled"


class KNIT360WorkOrder(Document):
	def validate(self):
		if flt(self.qty_to_produce) <= 0:
			frappe.throw("Say how many to make.")
		bom = frappe.get_doc(BOM, self.bom)
		if bom.item_code != self.production_item:
			frappe.throw(f"{self.bom} is the recipe for {bom.item_code}, not {self.production_item}.")
		if not bom.is_active:
			frappe.throw(f"{self.bom} is not marked Is Active. Use the current recipe, or tick it if this is the one.")
		if self.docstatus == 0:
			self._explode(bom)

	def _explode(self, bom):
		"""The materials for the quantity to make, from the BOM. Never typed."""
		batch = flt(bom.quantity) or 1
		self.set("materials", [])
		for row in bom.items:
			qty = flt(row.qty) * flt(self.qty_to_produce) / batch
			if qty <= stock_ledger.TOLERANCE:
				frappe.throw(f"{bom.name} line {row.idx}: {row.item_code} works out at a quantity of nil.")
			self.append("materials", {"item_code": row.item_code, "required_qty": qty})

	def before_business_status(self, from_status, to_status):
		if to_status == COMPLETED:
			if not (self.source_warehouse and self.target_warehouse):
				frappe.throw("Say which store the materials come from and which the finished goods go to.")
			needed = {}
			for row in self.materials:
				needed[row.item_code] = needed.get(row.item_code, 0.0) + flt(row.required_qty)
			for item, qty in needed.items():
				stock_ledger.check_can_issue(item, self.source_warehouse, qty, self.company)
		if to_status == CANCELLED and self.docstatus == 1:
			held = stock_ledger.balance(self.production_item, self.target_warehouse, self.company)
			if held + stock_ledger.TOLERANCE < flt(self.qty_to_produce):
				frappe.throw(
					f"Only {held:g} of the {flt(self.qty_to_produce):g} {self.production_item} made "
					f"on this order are still in {self.target_warehouse}; the rest have left. "
					f"Bring them back before cancelling, or the books would show goods that are not there."
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
					"remarks": f"Used on {self.name}",
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

		unit_cost = total / flt(self.qty_to_produce)
		stock_ledger.post(
			self.doctype,
			self.name,
			self.company,
			date,
			[
				{
					"item_code": self.production_item,
					"warehouse": self.target_warehouse,
					"qty": flt(self.qty_to_produce),
					"rate": unit_cost,
					"remarks": f"Made on {self.name}",
				}
			],
		)
		self.db_set("total_material_cost", total, update_modified=False)
		self.db_set("produced_unit_cost", unit_cost, update_modified=False)

	def on_cancel(self):
		stock_ledger.reverse(self.doctype, self.name)
