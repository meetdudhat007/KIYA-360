"""KNIT 360 Item Price - FR-SALES-004.

One item's price on one list. For an ordinary item the rate is typed.

**A main product's rate is worked out, never typed (DEC-048).** It is the
material cost -- each raw material's price on the buying list named in Raw
Material Prices From, times its count -- plus the margin. Whatever is typed
into Rate for a main product is replaced.

**A raw material's price change reaches every product.** Saving or deleting
a price reprices every main product that uses that item, directly or through
another group. Those repricings are saved as ordinary edits, so each
product price's history shows what moved it.
"""

import frappe
from frappe.model.document import Document
from frappe.utils import flt

from knit360_core.inventory import grouping


class KNIT360ItemPrice(Document):
	def validate(self):
		self.is_main_product = 1 if grouping.is_product(self.item_code) else 0
		if not self.is_main_product:
			for field in ("cost_price_list", "material_cost", "margin", "unpriced_materials"):
				self.set(field, None)
			return

		grouping.price_product(self)
		# A repricing set off by another price must not block that price
		# being changed or deleted; the nil rate and the unpriced list on this
		# row say what happened. Typed by hand, a nil product price is refused.
		if flt(self.rate) <= 0 and not self.flags.knit360_repricing:
			frappe.throw(
				f"{self.item_code} is priced from its raw materials, and none of them "
				f"has a price on {self.cost_price_list}, so its rate works out at nil. "
				f"Price the raw materials on that list first."
			)
		if self.unpriced_materials and not self.flags.knit360_repricing:
			missing = self.unpriced_materials.split("\n")
			frappe.msgprint(
				f"{len(missing)} raw material(s) of {self.item_code} have no price on "
				f"{self.cost_price_list}, so the rate leaves them out: "
				f"{', '.join(missing[:10])}{' ...' if len(missing) > 10 else ''}",
				title="Some raw materials are not priced",
				indicator="orange",
			)

	def on_update(self):
		if not self.flags.knit360_repricing:
			grouping.reprice_users(self.item_code, skip=self.name)

	def after_delete(self):
		grouping.reprice_users(self.item_code)
