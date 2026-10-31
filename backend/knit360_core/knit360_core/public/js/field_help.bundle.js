// A field's description behind an info icon instead of as text under the
// input (DEC-045).
//
// Frappe prints every description as small grey text below its field. On a
// form people fill in every day that text is read once and then only takes
// space, so on the forms listed here it moves behind an info icon, in the slot
// Frappe keeps beside the label for help (`span.help`, where it puts a field's
// documentation link). Hovering or tapping the icon shows the text; nothing is
// lost, and the descriptions themselves are unchanged.

frappe.provide("knit360.field_help");

knit360.field_help = {
	// The owner asked for this on the Lead form first. Adding a doctype here
	// gives its form the same treatment.
	DOCTYPES: new Set(["KNIT 360 Lead"]),

	// Frappe's own info icon is a solid blue disc; the owner asked for an
	// outline one with no fill (DEC-046). Drawn in the line style of Frappe's
	// help icon, in the label's grey.
	ICON: `<svg class="icon icon-sm" viewBox="0 0 20 20" aria-hidden="true"
		style="fill: none; stroke: currentColor">
		<circle cx="10" cy="10" r="7"/>
		<path d="M10 9.25v4.5" stroke-linecap="round"/>
		<circle cx="10" cy="6.6" r="0.4" style="fill: currentColor"/>
	</svg>`,

	apply(frm) {
		if (!frm || !this.DOCTYPES.has(frm.doctype)) return;
		Object.values(frm.fields_dict).forEach((field) => this.iconise(field));
	},

	iconise(field) {
		const text = field.df && field.df.description;
		if (!text || !field.$wrapper) return;

		// set_description re-renders only when the description differs from
		// _description, so clearing the text once keeps it clear on refresh.
		if (field.set_empty_description) field.set_empty_description();
		field._description = field.df.description;

		const $slot = field.$wrapper.find("span.help").first();
		if (!$slot.length || $slot.find(".knit-field-info").length) return;

		const label = __(field.df.label || "");
		const $icon = $(
			`<span class="knit-field-info text-muted" role="button" tabindex="0"></span>`
		)
			.attr("aria-label", __("About {0}", [label]))
			.html(this.ICON)
			.appendTo($slot);

		$icon.popover({
			trigger: "hover focus",
			placement: "top",
			html: false,
			content: () => __(text),
		});
	},
};

$(document).on("form-refresh", (e, frm) => knit360.field_help.apply(frm));
