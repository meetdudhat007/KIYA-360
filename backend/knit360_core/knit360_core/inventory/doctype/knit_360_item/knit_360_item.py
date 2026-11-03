"""KNIT 360 Item - FR-INV-001 / FR-PADM-1.4.3.

Item Master. The BRD gives 'item code, category, HSN/SAC' (FR-PADM-1.4) and the worked example IF-1500 / Induction Furnace / HSN 8514 / UOM Nos.

**Product grouping (DEC-054, client change request).** An item ticked Main
Product lists the raw materials it is made from, with a count each. The rules
for that list, and the pricing and where-used logic that read it, are in
inventory/grouping.py. When a group changes, every price built from it is
worked out again.
"""

from frappe.model.document import Document

from knit360_core.inventory import grouping


class KNIT360Item(Document):
	def validate(self):
		grouping.validate_group(self)

	def on_update(self):
		before = self.get_doc_before_save()
		if self._group_signature(before) != self._group_signature(self):
			grouping.reprice_users(self.name, include_self=True)

	@staticmethod
	def _group_signature(doc):
		if not doc:
			return None
		return (
			bool(doc.is_main_product),
			tuple((row.item_code, float(row.qty or 0)) for row in doc.get("raw_materials") or []),
		)
