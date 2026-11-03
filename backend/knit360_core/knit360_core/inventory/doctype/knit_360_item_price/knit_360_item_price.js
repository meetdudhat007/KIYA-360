// KNIT 360 Item Price -- a main product's price is worked out (DEC-048).
//
// This shows the figure as the margin or list changes. The server works it
// out again on save and its figure is the one stored.

frappe.ui.form.on("KNIT 360 Item Price", {
	setup(frm) {
		frm.set_query("cost_price_list", () => ({
			filters: { applies_to: "Buying", disabled: 0 },
		}));
	},
	item_code: knit360_preview_price,
	cost_price_list: knit360_preview_price,
	margin_type: knit360_preview_price,
	margin: knit360_preview_price,
});

function knit360_preview_price(frm) {
	if (!frm.doc.item_code) return;
	frappe.call({
		method: "knit360_core.inventory.grouping.preview_price",
		args: {
			item_code: frm.doc.item_code,
			cost_price_list: frm.doc.cost_price_list,
			margin_type: frm.doc.margin_type,
			margin: frm.doc.margin,
		},
		callback(r) {
			const out = r.message || {};
			frm.set_value("is_main_product", out.is_main_product ? 1 : 0);
			if (!out.is_main_product) return;
			if (!frm.doc.cost_price_list && out.cost_price_list) {
				frm.set_value("cost_price_list", out.cost_price_list);
			}
			frm.set_value("material_cost", out.material_cost);
			frm.set_value("unpriced_materials", out.unpriced_materials || "");
			frm.set_value("rate", out.rate);
		},
	});
}
