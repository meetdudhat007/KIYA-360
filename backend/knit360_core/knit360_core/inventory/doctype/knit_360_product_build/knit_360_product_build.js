// KNIT 360 Product Build (DEC-048). Only a main product can be built, and the
// stores belong to the build's company.

frappe.ui.form.on("KNIT 360 Product Build", {
	setup(frm) {
		frm.set_query("product", () => ({ filters: { is_main_product: 1, disabled: 0 } }));
		for (const field of ["source_warehouse", "target_warehouse"]) {
			frm.set_query(field, () => ({
				filters: frm.doc.company ? { company: frm.doc.company } : {},
			}));
		}
	},
});
