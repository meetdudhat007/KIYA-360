// The look every CRM list shares (DEC-056 on the lead list, DEC-059 on the
// rest). Each CRM list's script calls knit360.crm_list.setup in its onload.
//
// List Settings, where a list's columns are chosen, is a button beside Add
// rather than an item in the menu, and the menu's three dots are Frappe's gear
// (DEC-051). Frappe offers List Settings to System Managers only, and so does
// the button. The gear has no Customize or Toggle Sidebar, and the page has no
// sidebar toggle, so the sidebar is always shown -- or, for a list that asks,
// never.
//
// Frappe gives every column the same width, so on an ordinary screen nearly
// every value was cut short. Here each column is as wide as what it holds and
// at least as wide as its heading; the first column takes any room left over.
// When the columns need more room than the screen has, the grid scrolls
// sideways, and its heading stays in view as it scrolls down.

frappe.provide("knit360.crm_list");

knit360.crm_list = {
	WIDTHS: { Select: 160, Link: 190, Date: 110, Datetime: 150, Currency: 120, Float: 110, Int: 90, Check: 80 },

	CSS: `
		body.no-list-sidebar .knit-crm-list .layout-side-section { display: block; }
		.knit-crm-list.knit-no-sidebar .layout-side-section,
		body.no-list-sidebar .knit-crm-list.knit-no-sidebar .layout-side-section { display: none; }
		.knit-crm-list.knit-no-sidebar .layout-main-section-wrapper { flex: 1; max-width: 100%; }
		/* A phone shows only the first column, as Frappe has it. */
		@media (min-width: 768px) {
			.knit-crm-list .result { max-height: calc(100vh - 230px); overflow: auto; }
			.knit-crm-list .result .list-row-head, .knit-crm-list .result .list-row-container { min-width: max-content; }
			.knit-crm-list .list-row .level-left, .knit-crm-list .list-row-head .level-left { flex: 1 0 auto; min-width: 0; }
			.knit-crm-list .list-row .level-right, .knit-crm-list .list-row-head .level-right { flex: 0 0 110px; min-width: 110px; }
			.knit-crm-list .list-row-col { margin-right: 12px; }
			.knit-crm-list .result .list-row-head { position: sticky; top: 0; z-index: 3; }
		}
	`,

	setup(listview, { sidebar = true } = {}) {
		// A Report view has its own column picker and grid; it is left as it is.
		if (listview.view !== "List") return;
		frappe.dom.set_style(this.CSS, "knit360-crm-list");
		listview.page.wrapper.addClass("knit-crm-list").toggleClass("knit-no-sidebar", !sidebar);
		this.settings_menu(listview);
		this.grid(listview);
	},

	settings_menu(listview) {
		const page = listview.page;
		const label = __("List Settings", null, "Button in list view menu");
		const unwanted = [
			label,
			__("Customize", null, "Button in list view menu"),
			__("Toggle Sidebar", null, "Button in list view menu"),
		];
		page.menu
			.find(".menu-item-label")
			.filter((i, el) => unwanted.includes($(el).text().trim()))
			.closest("li")
			.remove();
		// Their keyboard shortcuts go with them.
		["ctrl+j", "ctrl+k"].forEach((shortcut) => frappe.ui.keys.off(shortcut, page));
		page.wrapper.find(".page-head .sidebar-toggle-btn").remove();

		if (frappe.user.has_role("System Manager")) {
			// On a phone the button shrinks to its icon, so it names itself on hover.
			page.set_secondary_action(label, () => listview.show_list_settings(), "table").attr("title", label);
		}
		page.menu_btn_group.find(".menu-btn-group-label use").attr("href", "#icon-setting-gear");
		page.menu_btn_group
			.find("[data-toggle=dropdown]")
			.attr({ "aria-label": __("Settings"), title: __("Settings") });
	},

	column_width(col) {
		const df = col.df || {};
		let width = this.WIDTHS[df.fieldtype] || 180;
		if (col.type === "Subject") width = 220;
		else if (df.fieldname === "name") width = 130;
		else if (/email/.test(df.fieldname)) width = 220;
		// About 7.5px a letter at the heading's size, plus room to breathe.
		const heading = Math.ceil(__(df.label || col.type).length * 7.5) + 20;
		return Math.max(width, heading);
	},

	// Sets the width of a row's cells, which come in the order of the list's
	// columns, as Frappe builds them.
	size_cells(listview, $cells) {
		$cells.each((i, cell) => {
			const col = listview.columns[i];
			if (col && col.type !== "Tag") {
				cell.style.flex = `${col.type === "Subject" ? 1 : 0} 0 ${this.column_width(col)}px`;
			}
		});
	},

	sized(listview, html, cells_of) {
		const $html = $("<div>").html(html);
		this.size_cells(listview, cells_of($html));
		return $html.html();
	},

	grid(listview) {
		const row = listview.get_left_html.bind(listview);
		listview.get_left_html = (doc) => this.sized(listview, row(doc), ($html) => $html.children(".list-row-col"));
		const header = listview.get_header_html.bind(listview);
		const heading_cells = ($html) => $html.find(".level-left").first().children(".list-row-col");
		listview.get_header_html = () => this.sized(listview, header(), heading_cells);
		// The heading is drawn before this runs, so it is sized where it stands.
		this.size_cells(listview, heading_cells(listview.$result.find(".list-row-head")));
	},
};
