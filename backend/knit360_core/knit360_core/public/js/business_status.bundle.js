// Business status buttons for the Desk -- CD-002.
//
// Why this file exists.
//
// knit360_business_status is read-only on every governed doctype, because only
// business_status.engine.transition may write it. That is correct, and it is
// what stops a status being typed. But until this script existed there was no
// way to *call* the engine from the Desk: a Sales Invoice opened in /app showed
// "Posted / Unpaid" as read-only text and offered no way to move it on. Only
// the three stages on /knit360 (lead, opportunity, quotation) could be moved at
// all, which left Sales Order, Delivery Note, Sales Invoice, Journal Entry and
// the whole purchasing side with no reachable lifecycle.
//
// So this renders one button per legal move, straight from the engine. The
// front end never decides what is legal -- it asks, and draws what it is told.
//
// Loaded for every Desk page via app_include_js and attached to Frappe's own
// global "form-refresh" event. That event fires after refresh_header(), which
// is what clears custom buttons, so buttons added here survive. Frappe's own
// comment at form.js:600 says the ordering is deliberate for exactly this.

frappe.provide("knit360.business_status");

knit360.business_status = {
	FIELD: "knit360_business_status",

	// Statuses an available action reaches on its own, collected per form so
	// the plain status button for them can be left out. Without this a lead at
	// Qualified showed both "Converted" and "Convert to Customer +
	// Opportunity": the first marks it converted and creates nothing, which is
	// the one mistake this screen must not invite.
	claimed: {},

	attach(frm) {
		// A document that has never been saved has no status to move.
		if (!frm || !frm.doc || frm.is_new()) return;
		// Cheap local check first, so forms without a lifecycle cost no request.
		if (!frm.meta || !frm.meta.fields.some((f) => f.fieldname === this.FIELD)) return;

		// Actions first, so the statuses they claim are known before the plain
		// status buttons are drawn.
		frappe.call({
			method: "knit360_core.api.c2c.actions_for",
			args: { doctype: frm.doctype, name: frm.doc.name },
			callback: (r) => {
				this.render_actions(frm, (r && r.message) || []);
				frappe.call({
					method: "knit360_core.business_status.engine.next_steps",
					args: { reference_doctype: frm.doctype, reference_name: frm.doc.name },
					callback: (s) => this.render(frm, (s && s.message) || []),
				});
			},
		});

		// Moves within a stage are one thing; moves that create the next
		// document are another. Converting a lead and raising a quotation
		// existed only on /knit360 until now, so a Desk user could qualify a
		// lead and then had nowhere to take it.
	},

	//: Which seam method each action calls, and where it lands. The server
	//: decides *whether* an action is offered; this only knows how to run it.
	RUNNERS: {
		convert_lead: {
			method: "knit360_core.api.c2c.convert_lead",
			args: (frm) => ({ name: frm.doc.name }),
			open: (res) => ["KNIT 360 Opportunity", res.opportunity],
		},
		create_quotation: {
			method: "knit360_core.api.c2c.create_quotation",
			args: (frm) => ({ opportunity: frm.doc.name }),
			open: (res) => ["KNIT 360 Quotation", res.name],
		},
	},

	render_actions(frm, actions) {
		this.claimed[frm.doc.name] = {};
		actions.forEach((action) => {
			const runner = this.RUNNERS[action.key];
			if (!runner) return;
			if (!action.enabled) {
				// Say why rather than showing a button that refuses. The reason
				// comes from the server, so it is never a guess.
				if (action.reason) {
					frm.dashboard.add_comment(
						__("{0}: {1}", [action.label, action.reason]),
						"orange",
						true
					);
				}
				return;
			}
			if (action.produces_status) {
				this.claimed[frm.doc.name][action.produces_status] = true;
			}
			frm.add_custom_button(__(action.label), () => this.run(frm, action, runner));
			frm.change_custom_button_type(__(action.label), null, "primary");
		});
	},

	run(frm, action, runner) {
		frappe.call({
			method: runner.method,
			args: runner.args(frm),
			freeze: true,
			freeze_message: __("{0}...", [action.label]),
			callback: (r) => {
				const [doctype, name] = runner.open(r.message || {});
				if (!name) {
					frm.reload_doc();
					return;
				}
				frappe.show_alert({ message: __("Created {0}", [name]), indicator: "green" });
				frappe.set_route("Form", doctype, name);
			},
		});
	},

	render(frm, steps) {
		if (!steps.length) {
			// Terminal states are a real answer, not a missing one. Saying so
			// stops someone hunting for a button that should not exist.
			frm.dashboard.add_comment(
				__("This {0} has reached the end of its life. Nothing further happens to it.", [
					frm.doctype.replace("KNIT 360 ", ""),
				]),
				"blue",
				true
			);
			return;
		}

		const claimed = this.claimed[frm.doc.name] || {};
		steps.forEach((step) => {
			if (claimed[step.status]) return;
			frm.add_custom_button(__(step.status), () => this.confirm(frm, step));
			if (step.is_forward) {
				// The ordinary next step is the one most people want, so it is
				// the one that looks like the action.
				frm.change_custom_button_type(__(step.status), null, "primary");
			}
		});
	},

	confirm(frm, step) {
		// A move that can be undone needs no ceremony.
		if (!step.locks && !step.terminal) {
			this.move(frm, step.status, null);
			return;
		}

		const consequence = step.terminal
			? __("Nothing further happens to it after this.")
			: __("Its lines can no longer be changed after this.");

		if (step.terminal) {
			// Terminal moves are where "why" matters later, so they ask for it.
			frappe.prompt(
				[
					{
						fieldname: "reason",
						fieldtype: "Small Text",
						label: __("Reason (optional)"),
						description: __("Recorded against this change in the status history."),
					},
				],
				(values) => this.move(frm, step.status, values.reason),
				__("Move to {0}?", [step.status]),
				__("Move to {0}", [step.status])
			);
			return;
		}

		frappe.confirm(
			__("Move this to {0}? {1}", [step.status, consequence]),
			() => this.move(frm, step.status, null)
		);
	},

	move(frm, to_status, reason) {
		frappe.call({
			method: "knit360_core.business_status.engine.transition",
			args: {
				reference_doctype: frm.doctype,
				reference_name: frm.doc.name,
				to_status: to_status,
				reason: reason || null,
			},
			freeze: true,
			freeze_message: __("Moving to {0}...", [to_status]),
			callback: () => {
				frappe.show_alert({ message: __("Now {0}", [to_status]), indicator: "green" });
				frm.reload_doc();
			},
		});
	},
};

$(document).on("form-refresh", (event, frm) => {
	knit360.business_status.attach(frm);
});
