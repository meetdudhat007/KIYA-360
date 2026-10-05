// Filters for the requirement coverage report.
//
// All three default to empty, so the report opens showing every requirement
// including the ones nothing has been built for. "Only the gaps" is there so a
// planning conversation can get to the list of what is missing in one click.

frappe.query_reports["KNIT 360 Requirement Coverage"] = {
	filters: [
		{
			fieldname: "module",
			label: __("BRD Module"),
			fieldtype: "Select",
			options: [""],
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: ["", "Proven", "Modelled", "Not started"],
		},
		{
			fieldname: "only_gaps",
			label: __("Only the gaps"),
			fieldtype: "Check",
			default: 0,
		},
	],

	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "status" && data) {
			const colour = {
				Proven: "green",
				Modelled: "blue",
				"Not started": "gray",
			}[data.status];
			if (colour) {
				value = `<span class="indicator-pill ${colour}">${data.status}</span>`;
			}
		}
		return value;
	},

	onload(report) {
		// The module list is read from the data rather than written out a
		// second time here, so a change to the BRD inventory cannot leave this
		// dropdown stale.
		frappe.call({
			method: "knit360_core.traceability.summary",
			callback: (r) => {
				const filter = report.get_filter("module");
				if (!filter) return;
				const modules = ((r.message || {}).per_module || []).map((m) => m.module);
				filter.df.options = [""].concat(modules);
				filter.refresh();
			},
		});
	},
};
