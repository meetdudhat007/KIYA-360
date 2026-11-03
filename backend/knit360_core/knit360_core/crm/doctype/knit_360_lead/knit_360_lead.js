// The people on a lead as ordinary form fields, one block per person, with an
// Add New Contact button under the last one (DEC-046).
//
// The people are still rows of Contact Persons -- the list columns, search and
// conversion all read them there -- but the owner did not want them typed into
// a table. Frappe's grid for that field is kept out of sight and each row is
// drawn here instead, in the form's two columns, with Frappe's own controls
// bound to the row: typing in a block is typing into its row, with the same
// checks and the same unsaved-changes marker as any other field.
//
// The Assignment section decides who may open the lead (DEC-048); the rules
// are in knit360_core.crm.lead_access, and the panel beside it shows their
// result for the values on screen. Others With Access is drawn the same way as
// the people: its grid is out of sight, and each row is an employee dropdown
// with Read Only and Read & Write as radio buttons, as the owner asked.

const KNIT360_PERSONS = "contact_persons";
const KNIT360_PERSON = "KNIT 360 Lead Person";
// Left column, then right column, of each person's block.
const KNIT360_PERSON_LAYOUT = [
	["person_name", "designation", "department"],
	["email", "phone", "address"],
];
const KNIT360_ACCESS = "lead_access";
const KNIT360_ACCESS_LEVELS = ["Read Only", "Read & Write"];

frappe.ui.form.on("KNIT 360 Lead", {
	setup(frm) {
		// Only people still with the company can be given a lead.
		const active = () => ({ filters: { is_active: 1 } });
		frm.set_query("assigned_to", active);
		frm.set_query("employee", "lead_access", active);
	},

	refresh(frm) {
		knit360_stage_details(frm);
		knit360_contact_blocks(frm);
		knit360_access_rows(frm);
		knit360_access_summary(frm);
		knit360.tasks.panel(frm);
		knit360_comment_type(frm);
		// Frappe's own Assign and Share in the sidebar would grant access the
		// Assignment section knows nothing of, and its next save would take
		// that access away again. So on this form the section is the one way.
		// Tags, the like heart and Follow are left off at the owner's request
		// (DEC-058).
		frm.sidebar?.sidebar
			?.find(".form-assignments, .form-shared, .form-tags, .form-stats-likes, .form-stats-likes + .mx-2, .form-follow")
			.addClass("hidden");
	},

	assigned_to: (frm) => knit360_access_summary(frm),
	lead_access_remove: (frm) => knit360_access_summary(frm),

	validate(frm) {
		// A block opened with Add New Contact and left empty is dropped rather
		// than refused, as long as one block stays to be filled in.
		const rows = frm.doc[KNIT360_PERSONS] || [];
		const fields = KNIT360_PERSON_LAYOUT.flat();
		const empty = rows.filter((row) => fields.every((f) => !row[f]));
		const drop = empty.length === rows.length ? empty.slice(1) : empty;
		if (drop.length) {
			drop.forEach((row) => frappe.model.clear_doc(row.doctype, row.name));
			frm.refresh_field(KNIT360_PERSONS);
			knit360_contact_blocks(frm);
		}

		// Likewise a person added under Others With Access but never picked.
		const unpicked = (frm.doc[KNIT360_ACCESS] || []).filter((row) => !row.employee);
		if (unpicked.length) {
			unpicked.forEach((row) => frappe.model.clear_doc(row.doctype, row.name));
			frm.refresh_field(KNIT360_ACCESS);
			knit360_access_rows(frm);
		}
	},
});

function knit360_contact_blocks(frm) {
	const field = frm.get_field("contact_editor");
	if (!field) return;
	const editable = frm.has_perm("write");

	// A new lead opens with one person ready to fill in.
	if (editable && !(frm.doc[KNIT360_PERSONS] || []).length) {
		frm.add_child(KNIT360_PERSONS);
	}
	const rows = frm.doc[KNIT360_PERSONS] || [];

	const redraw = () => {
		frm.dirty();
		frm.refresh_field(KNIT360_PERSONS);
		knit360_contact_blocks(frm);
	};

	const $editor = $(`<div class="knit-contacts" style="margin-bottom: var(--margin-md)"></div>`);
	rows.forEach((row, i) => {
		const $block = $(`<div class="knit-contact"></div>`).appendTo($editor);
		if (i > 0) {
			$block.css({
				"border-top": "1px dashed var(--border-color)",
				"padding-top": "var(--padding-sm)",
			});
		}
		if (rows.length > 1) {
			const $head = $(`<div class="flex justify-between align-center"></div>`)
				.append(`<span class="text-muted small">${__("Contact {0}", [i + 1])}</span>`)
				.appendTo($block);
			if (editable) {
				$(`<button type="button" class="btn btn-link btn-xs text-muted"></button>`)
					.text(__("Remove"))
					.on("click", () => {
						frappe.model.clear_doc(row.doctype, row.name);
						redraw();
					})
					.appendTo($head);
			}
		}

		const $row = $(`<div class="row"></div>`).appendTo($block);
		KNIT360_PERSON_LAYOUT.forEach((fieldnames) => {
			const $column = $(`<div class="col-sm-6"></div>`).appendTo($row);
			fieldnames.forEach((fieldname) => {
				const control = frappe.ui.form.make_control({
					df: frappe.meta.get_docfield(KNIT360_PERSON, fieldname, row.name),
					parent: $column,
					frm,
					doc: row,
					doctype: KNIT360_PERSON,
					docname: row.name,
					render_input: true,
				});
				control.refresh();
				knit360.field_help.iconise(control);
			});
		});
	});

	if (editable) {
		$(`<button type="button" class="btn btn-xs btn-secondary"></button>`)
			.text(__("+ Add New Contact"))
			.on("click", () => {
				frm.add_child(KNIT360_PERSONS);
				redraw();
				field.$wrapper.find(".knit-contact").last().find("input").first().focus();
			})
			.appendTo($editor);
	}

	field.$wrapper.empty().append($editor);
}

frappe.ui.form.on("KNIT 360 Lead Access", {
	employee: (frm) => knit360_access_summary(frm),
	access: (frm) => knit360_access_summary(frm),
});

function knit360_access_rows(frm) {
	const field = frm.get_field("access_editor");
	if (!field) return;
	const editable = frm.has_perm("write");
	const rows = frm.doc[KNIT360_ACCESS] || [];
	const df = frm.get_docfield(KNIT360_ACCESS);

	const redraw = () => {
		frm.dirty();
		frm.refresh_field(KNIT360_ACCESS);
		knit360_access_rows(frm);
		knit360_access_summary(frm);
	};

	const $editor = $(`<div class="knit-access" style="margin-bottom: var(--margin-md)"></div>`);
	const $label = $(`<div class="control-label" style="margin-bottom: var(--margin-xs)"></div>`)
		.text(__(df.label))
		.appendTo($editor);
	if (df.description) {
		$label.append(" ").append(knit360.field_help.icon(df.label, df.description));
	}
	if (!rows.length && !editable) {
		$editor.append(`<p class="text-muted small">${__("No one else.")}</p>`);
	}

	rows.forEach((row) => {
		const $row = $(`<div class="knit-access-row"></div>`).appendTo($editor);
		const $line = $(`<div class="flex align-center" style="gap: var(--padding-sm)"></div>`).appendTo($row);
		const $pick = $(`<div style="flex: 1; min-width: 0"></div>`).appendTo($line);
		const control = frappe.ui.form.make_control({
			// No label of its own: the section's label says what it is.
			// No required marker either: a person never picked is dropped on save.
			df: Object.assign({}, frappe.meta.get_docfield(row.doctype, "employee", row.name), {
				label: "",
				reqd: 0,
				placeholder: __("Pick an employee"),
				get_query: () => ({ filters: { is_active: 1 } }),
				// The dropdown shows the employee's name, not their number. A
				// field on the form is redrawn after a pick, which teaches it
				// that name; this one is not on the form, so it redraws itself.
				// Otherwise leaving the field read the name back as a number,
				// found no such employee, and emptied the pick.
				change() {
					this.refresh();
				},
			}),
			parent: $pick,
			frm,
			doc: row,
			doctype: row.doctype,
			docname: row.name,
			render_input: true,
		});
		control.refresh();
		control.$wrapper.find(".control-label").first().addClass("hidden");
		if (editable) {
			$(`<button type="button" class="btn btn-link btn-xs text-muted"></button>`)
				.text(__("Remove"))
				.on("click", () => {
					frappe.model.clear_doc(row.doctype, row.name);
					redraw();
				})
				.appendTo($line);
		}

		const $levels = $(`<div class="flex" style="gap: var(--padding-lg); margin: calc(-1 * var(--margin-sm)) 0 var(--margin-md)"></div>`)
			.appendTo($row);
		KNIT360_ACCESS_LEVELS.forEach((level) => {
			const $input = $(`<input type="radio">`)
				.attr("name", `knit-access-${row.name}`)
				.val(level)
				.prop("checked", (row.access || KNIT360_ACCESS_LEVELS[0]) === level)
				.prop("disabled", !editable)
				.on("change", () => frappe.model.set_value(row.doctype, row.name, "access", level));
			$(`<label class="flex align-center" style="gap: var(--padding-xs); margin: 0; font-weight: normal"></label>`)
				.append($input)
				.append($("<span>").text(__(level)))
				.appendTo($levels);
		});
	});

	if (editable) {
		$(`<button type="button" class="btn btn-xs btn-secondary"></button>`)
			.text(__("+ Add Person"))
			.on("click", () => {
				frm.add_child(KNIT360_ACCESS, { access: KNIT360_ACCESS_LEVELS[0] });
				redraw();
				field.$wrapper.find(".knit-access-row").last().find("input[type=text], input:not([type])").first().focus();
			})
			.appendTo($editor);
	}

	field.$wrapper.empty().append($editor);
}

function knit360_access_summary(frm) {
	const field = frm.get_field("access_summary");
	if (!field) return;
	frappe.call({
		method: "knit360_core.crm.lead_access.who_can_open",
		args: {
			assigned_to: frm.doc.assigned_to || null,
			access: (frm.doc.lead_access || []).map((r) => ({ employee: r.employee, access: r.access })),
		},
		callback: (r) => field.$wrapper.html(knit360_access_html(r.message || [])),
	});
}

// A plain list, one person to a line: who, at what level, and why.
function knit360_access_html(entries) {
	const esc = frappe.utils.escape_html;
	const people = entries
		.map((e) => {
			let note = "";
			if (!e.active) note = __("No longer active, so no access");
			else if (!e.has_login) note = __("No login yet; access starts once one is linked on their Employee page");
			return `<div style="margin-bottom: var(--margin-sm)">
				<div><span class="bold">${esc(e.employee_name)}</span> &middot; ${esc(__(e.access))}</div>
				<div class="text-muted small">${esc(e.why)}</div>
				${note ? `<div class="text-warning small">${esc(note)}</div>` : ""}
			</div>`;
		})
		.join("");
	const body =
		people || `<p class="text-muted small">${__("No one is assigned yet. Only whoever created this lead can open it.")}</p>`;
	return `<div class="control-label" style="margin-bottom: var(--margin-xs)">${__("Who Can Open This Lead")}</div>
		${body}
		<p class="text-muted small">${__("System Managers can open every lead.")}</p>`;
}

// A comment can say what it reports on -- a Call, Meeting, Email or Other, the
// types a task has -- picked beside the Comments heading (DEC-059). The type
// is written in bold above the text; Activity shows when it was written.
function knit360_comment_type(frm) {
	const box = frm.comment_box;
	if (!box || box.knit360_typed) return;
	box.knit360_typed = true;
	const types = (frm.doc.__onload && frm.doc.__onload.task_types) || [];
	const $type = $(`<select class="form-control input-xs" style="width: auto; display: inline-block"></select>`)
		.append($("<option>").val("").text(__("Type")))
		.append(types.map((type) => $("<option>").val(type).text(__(type))));
	frm.$wrapper
		.find(".comment-box .comment-input-header")
		.addClass("flex justify-between align-center")
		.append($type);
	const submit = box.on_submit;
	box.on_submit = (comment) => {
		const type = $type.val();
		$type.val("");
		submit(type ? `<p><strong>${frappe.utils.escape_html(__(type))}</strong></p>${comment}` : comment);
	};
}

// Stage Detail offers only the steps of the stage the lead is at (DEC-050).
// The steps come from knit360_core.crm.lead_stages, sent with the lead.
function knit360_stage_details(frm) {
	const all = (frm.doc.__onload && frm.doc.__onload.stage_details) || {};
	const steps = all[frm.doc.knit360_business_status] || [];
	frm.set_df_property("stage_detail", "options", ["", ...steps]);
}
