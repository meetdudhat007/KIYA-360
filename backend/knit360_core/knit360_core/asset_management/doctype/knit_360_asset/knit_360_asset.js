// The unit's whole life, drawn from knit360_core.asset_management.history.
// Read fresh each time the form opens; nothing here is stored.

frappe.ui.form.on("KNIT 360 Asset", {
	refresh(frm) {
		const field = frm.get_field("service_history");
		if (!field) return;
		if (frm.is_new()) {
			field.$wrapper.html("");
			return;
		}
		frappe.call({
			method: "knit360_core.asset_management.history.asset_history",
			args: { asset: frm.doc.name },
			callback: (r) => field.$wrapper.html(knit360_asset_history(r.message || {})),
		});
	},
});

function knit360_asset_history(data) {
	const esc = frappe.utils.escape_html;
	const t = data.totals || {};
	const money = (v) => format_currency(v || 0);
	const figures = [
		[__("Service requests"), t.service_requests || 0],
		[__("Breakdown repairs"), t.breakdown_repairs || 0],
		[__("Planned visits"), t.preventive_visits || 0],
		[__("Labour hours"), (t.labour_hours || 0).toFixed(1)],
		[__("Parts used (cost)"), money(t.parts_cost)],
		[__("of which under warranty"), money(t.warranty_parts_cost)],
		[__("Billed for service"), money(t.billed)],
	];
	const summary = figures
		.map(([label, value]) => `<div class="col-sm-3 col-6" style="margin-bottom:8px">
			<div class="text-muted small">${label}</div><div class="bold">${esc(String(value))}</div></div>`)
		.join("");

	const events = data.events || [];
	const rows = events.length
		? events
				.map(
					(e) => `<tr>
				<td style="white-space:nowrap">${esc(e.when)}</td>
				<td>${esc(e.what)}</td>
				<td>${esc(e.detail)}</td>
				<td style="white-space:nowrap">${esc(e.status)}</td>
				<td><a href="/app/${frappe.router.slug(e.doctype)}/${encodeURIComponent(e.name)}">${esc(e.name)}</a></td>
			</tr>`
				)
				.join("")
		: `<tr><td colspan="5" class="text-muted">${__("Nothing has happened to this unit yet.")}</td></tr>`;

	return `<div class="row">${summary}</div>
		<div class="table-responsive"><table class="table table-bordered table-condensed">
		<thead><tr><th>${__("Date")}</th><th>${__("What")}</th><th>${__("Detail")}</th>
		<th>${__("Status")}</th><th>${__("Document")}</th></tr></thead>
		<tbody>${rows}</tbody></table></div>`;
}
