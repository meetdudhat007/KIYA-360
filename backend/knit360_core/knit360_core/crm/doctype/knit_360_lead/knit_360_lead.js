// The people on a lead as ordinary form fields, one block per person, with an
// Add New Contact button under the last one (DEC-046).
//
// The people are still rows of Contact Persons -- the list columns, search and
// conversion all read them there -- but the owner did not want them typed into
// a table. Frappe's grid for that field is kept out of sight and each row is
// drawn here instead, in the form's two columns, with Frappe's own controls
// bound to the row: typing in a block is typing into its row, with the same
// checks and the same unsaved-changes marker as any other field.

const KNIT360_PERSONS = "contact_persons";
const KNIT360_PERSON = "KNIT 360 Lead Person";
// Left column, then right column, of each person's block.
const KNIT360_PERSON_LAYOUT = [
	["person_name", "designation", "department"],
	["email", "phone"],
];

frappe.ui.form.on("KNIT 360 Lead", {
	refresh(frm) {
		knit360_contact_blocks(frm);
	},

	validate(frm) {
		// A block opened with Add New Contact and left empty is dropped rather
		// than refused, as long as one block stays to be filled in.
		const rows = frm.doc[KNIT360_PERSONS] || [];
		const fields = KNIT360_PERSON_LAYOUT.flat();
		const empty = rows.filter((row) => fields.every((f) => !row[f]));
		const drop = empty.length === rows.length ? empty.slice(1) : empty;
		if (!drop.length) return;
		drop.forEach((row) => frappe.model.clear_doc(row.doctype, row.name));
		frm.refresh_field(KNIT360_PERSONS);
		knit360_contact_blocks(frm);
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
