// KNIT 360 Item -- product grouping (DEC-048).
//
// The counts are recomputed here as lines change so the form never shows a
// stale figure; the server works them out again on save, and its figure is
// the one stored. Where Used is read from the server each time the form
// opens, because it is made of other products' groups, not this item's.

frappe.ui.form.on("KNIT 360 Item", {
	setup(frm) {
		frm.set_query("item_code", "raw_materials", () => ({
			filters: { name: ["!=", frm.doc.name || ""], disabled: 0 },
		}));
	},

	refresh(frm) {
		knit360_where_used(frm);
	},

	raw_materials_remove(frm) {
		knit360_recount(frm);
	},
});

frappe.ui.form.on("KNIT 360 Item Raw Material", {
	item_code(frm) {
		knit360_recount(frm);
	},
	qty(frm) {
		knit360_recount(frm);
	},
});

function knit360_recount(frm) {
	const rows = frm.doc.raw_materials || [];
	frm.set_value("raw_material_count", rows.filter((row) => row.item_code).length);
	frm.set_value(
		"total_units",
		rows.reduce((sum, row) => sum + (flt(row.qty) || 0), 0)
	);
}

function knit360_where_used(frm) {
	const field = frm.get_field("where_used_html");
	if (!field || frm.is_new()) return;

	field.$wrapper.html(`<p class="text-muted">${__("Loading...")}</p>`);
	frappe.call({
		method: "knit360_core.inventory.grouping.where_used_rows",
		args: { item_code: frm.doc.name },
		callback(r) {
			const rows = r.message || [];
			if (!rows.length) {
				field.$wrapper.html(
					`<p class="text-muted">${__("Not used in any main product yet.")}</p>`
				);
				return;
			}
			const esc = frappe.utils.escape_html;
			const body = rows
				.map((row) => {
					const how = [];
					if (row.direct) how.push(__("Listed directly"));
					if (row.through.length) {
						how.push(__("Through {0}", [row.through.map(esc).join(", ")]));
					}
					const href = `/app/knit-360-item/${encodeURIComponent(row.product)}`;
					return `<tr>
						<td><a href="${href}">${esc(row.product)}</a></td>
						<td>${esc(row.item_name || "")}</td>
						<td class="text-right">${format_number(row.qty, null, 2).replace(/\.00$/, "")}</td>
						<td>${how.join("; ")}</td>
					</tr>`;
				})
				.join("");
			field.$wrapper.html(`
				<p class="text-muted small">${__(
					"{0} main product(s) use this item. Count is how many one of that product takes.",
					[rows.length]
				)}</p>
				<table class="table table-bordered table-condensed">
					<thead><tr>
						<th>${__("Product")}</th><th>${__("Name")}</th>
						<th class="text-right">${__("Count")}</th><th>${__("How")}</th>
					</tr></thead>
					<tbody>${body}</tbody>
				</table>`);
		},
	});
}
