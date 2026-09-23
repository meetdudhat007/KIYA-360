// Business status UI for Sales Order (CD-002).
//
// The field itself is read-only: every change goes through the whitelisted
// engine so the transition matrix is enforced and the audit entry is written.
// The form never sets the status directly.

frappe.provide("knit360.business_status");

const STATUS_COLOUR = {
	Draft: "gray",
	"Pending Approval": "orange",
	Approved: "blue",
	Rejected: "red",
	"In Progress": "blue",
	"Partially Completed": "yellow",
	Completed: "green",
	Closed: "green",
	Cancelled: "red",
};

// A reason is mandatory where the transition ends or reverses the lifecycle.
const REASON_REQUIRED = ["Rejected", "Cancelled"];

knit360.business_status.headline = function (frm, status) {
	const colour = STATUS_COLOUR[status] || "gray";
	const pill = `<span class="indicator-pill ${colour}">${frappe.utils.escape_html(status)}</span>`;
	frm.dashboard.clear_headline();
	frm.dashboard.set_headline(__("Business Status: {0}", [pill]));
};

knit360.business_status.confirm = function (frm, next) {
	frappe.prompt(
		[
			{
				fieldname: "reason",
				fieldtype: "Small Text",
				label: __("Reason"),
				reqd: REASON_REQUIRED.includes(next) ? 1 : 0,
			},
		],
		(values) => {
			frappe.call({
				method: "knit360_core.business_status.engine.transition",
				args: {
					reference_doctype: frm.doctype,
					reference_name: frm.doc.name,
					to_status: next,
					reason: values.reason,
				},
				freeze: true,
				freeze_message: __("Updating business status…"),
				callback: () => frm.reload_doc(),
			});
		},
		__("Move to {0}", [next]),
		__("Confirm")
	);
};

knit360.business_status.render = function (frm) {
	const status = frm.doc.knit360_business_status;
	if (!status) return;

	knit360.business_status.headline(frm, status);

	frappe.call({
		method: "knit360_core.business_status.engine.allowed_next",
		args: { reference_doctype: frm.doctype, reference_name: frm.doc.name },
		callback: (r) => {
			const next_states = r.message || [];
			if (!next_states.length) return;
			next_states.forEach((next) => {
				frm.add_custom_button(
					__(next),
					() => knit360.business_status.confirm(frm, next),
					__("Business Status")
				);
			});
		},
	});
};

frappe.ui.form.on("Sales Order", {
	refresh(frm) {
		if (frm.is_new()) return;
		knit360.business_status.render(frm);
	},
});
