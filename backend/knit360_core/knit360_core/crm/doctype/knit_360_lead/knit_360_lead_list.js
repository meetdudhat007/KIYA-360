// The lead list without Frappe's likes, at the owner's request (DEC-047).
//
// Frappe draws a heart on every list row and a "Liked by me" heart in the
// header, with no setting to turn them off. Both come from the list's own
// HTML builders, so this list's copies of those builders leave the hearts out
// -- along with the dot Frappe puts between the comment count and the heart.
// Every other list keeps Frappe's likes.
//
// List Settings, where the list's columns are chosen, is moved out of the menu
// onto a button of its own beside Add, and the menu's three dots become
// Frappe's gear (DEC-051). Frappe offers List Settings to System Managers only,
// and so does the button.
//
// Above the list is a filter bar of the owner's design (DEC-053, in place of
// DEC-052's lone Filter button): one search box that finds a lead by any word
// in it, then dropdowns for Business Status, Stage Detail and Assigned To.
// Frappe's Filter button stays after them for anything rarer, such as dates.

const KNIT360_LEAD = "KNIT 360 Lead";
const KNIT360_DROPDOWNS = ["knit360_business_status", "stage_detail", "assigned_to"];

frappe.listview_settings["KNIT 360 Lead"] = {
	onload(listview) {
		knit360_list_settings_button(listview);
		knit360_filter_bar(listview);
		knit360_sidebar_without_assignments(listview);

		const without = (html, selector) => {
			const $html = $("<div>").html(html);
			$html.find(selector).remove();
			return $html.html();
		};

		const header = listview.get_header_html.bind(listview);
		listview.get_header_html = () => without(header(), ".list-liked-by-me");

		const meta = listview.get_meta_html.bind(listview);
		listview.get_meta_html = (doc) =>
			without(meta(doc), ".list-row-like, .list-row-activity .mx-2");

		// The header is drawn before onload runs, so take its heart out here.
		listview.$result.find(".list-liked-by-me").remove();
	},
};

function knit360_list_settings_button(listview) {
	// The Report view of leads has its own column picker; leave it as it is.
	if (listview.view !== "List") return;
	const page = listview.page;
	const label = __("List Settings", null, "Button in list view menu");

	page.menu
		.find(".menu-item-label")
		.filter((i, el) => $(el).text().trim() === label)
		.closest("li")
		.remove();
	if (frappe.user.has_role("System Manager")) {
		// On a phone the button shrinks to its icon, so it names itself on hover.
		page.set_secondary_action(label, () => listview.show_list_settings(), "table").attr("title", label);
	}

	page.menu_btn_group.find(".menu-btn-group-label use").attr("href", "#icon-setting-gear");
	page.menu_btn_group
		.find("[data-toggle=dropdown]")
		.attr({ "aria-label": __("Settings"), title: __("Settings") });
}

function knit360_filter_bar(listview) {
	const area = listview.filter_area;
	if (!area || !area.standard_filters_wrapper) return;
	const page = listview.page;

	// Frappe's own row -- ID, Organization Name and every field marked as a
	// standard filter -- is built before this runs, and replaced here. The
	// filters the list starts with, saved from the last visit, are put back
	// afterwards: read from the list rather than from the row, which may still
	// be taking them in.
	const starting = (listview.filters || []).slice();
	Object.keys(page.fields_dict).forEach((fieldname) => delete page.fields_dict[fieldname]);
	const $bar = area.standard_filters_wrapper.empty();

	knit360_search_box(listview, $bar);

	// The dropdowns are added the way Frappe adds its row, so Frappe treats
	// them as its own: kept between visits, set from a link, cleared by the x.
	// A filter on any other field goes to the Filter button.
	const dropdowns = KNIT360_DROPDOWNS.map((fieldname) => {
		const df = frappe.meta.get_docfield(KNIT360_LEAD, fieldname);
		return page.add_field(
			{
				fieldtype: "Select",
				fieldname,
				label: __(df.label),
				// A blank first, which is "any".
				options: ["", ...(df.fieldtype === "Select" ? df.options.split("\n") : [])].filter(
					(option, i) => i === 0 || option
				),
				condition: "=",
				onchange: () => area.debounced_refresh_list_view(),
			},
			$bar
		);
	});

	// Each goes into its dropdown, or under the Filter button if it has none
	// (one already there is left alone). The list may already be loading
	// without them, so it loads again once they are in.
	if (starting.length) area.set(starting).then(() => listview.refresh());

	// Assigned To lists employees by name, which takes a call. Until the names
	// are back the dropdown cannot show a value it is given -- kept, or from a
	// link -- and Frappe reads a dropdown by what it shows, so it would count
	// as empty. It answers with the value it holds instead, and shows it once
	// the names arrive.
	const assigned = dropdowns[KNIT360_DROPDOWNS.indexOf("assigned_to")];
	const shown = assigned.get_value.bind(assigned);
	let named = false;
	assigned.get_value = () => (named ? shown() : assigned.value);
	frappe.xcall("knit360_core.crm.lead_search.assignees").then((employees) => {
		assigned.df.options = [{ label: "", value: "" }].concat(
			employees.map((e) => ({
				label: e.is_active ? e.employee_name : __("{0} (left)", [e.employee_name]),
				value: e.name,
			}))
		);
		assigned.set_options();
		named = true;
		if (assigned.value) assigned.set_input(assigned.value);
	});
}

// One box, any words: each word must appear somewhere in the lead, in any
// order (crm.lead_search keeps every lead's words). The search is not one of
// Frappe's filters -- they hold one value per field, and this is a condition
// per word -- so it is added to the list's query here, and leaves the address
// bar alone.
function knit360_search_box(listview, $bar) {
	const page = listview.page;
	const area = listview.filter_area;
	const box = page.add_field(
		{ fieldtype: "Data", fieldname: "knit360_search", label: __("Search leads by any word") },
		$bar
	);
	delete page.fields_dict.knit360_search;
	$(box.wrapper).removeClass("col-md-2").css({ flex: "1 1 220px", "max-width": "340px" });

	const words = () => (box.get_value() || "").split(/\s+/).filter(Boolean);
	const filters = listview.get_filters_for_args.bind(listview);
	listview.get_filters_for_args = () =>
		filters().concat(words().map((word) => [KNIT360_LEAD, "search_keywords", "like", `%${word}%`]));
	if (listview.get_search_params) {
		const params = listview.get_search_params.bind(listview);
		listview.get_search_params = () => {
			const out = params();
			out.delete("search_keywords");
			return out;
		};
	}
	box.$input.on("input", frappe.utils.debounce(() => area.refresh_list_view(), 300));

	// The x beside the Filter button empties the box too.
	const clear = area.clear.bind(area);
	area.clear = (...args) => {
		box.set_input("");
		return clear(...args);
	};
}

// The sidebar's Assigned To lists Frappe's to-do assignments, which leads do
// not use (DEC-048); beside the bar's Assigned To it would only mislead.
function knit360_sidebar_without_assignments(listview) {
	const group_by = listview.list_sidebar && listview.list_sidebar.list_group_by;
	if (!group_by) return;
	const render = group_by.render_group_by_items.bind(group_by);
	group_by.render_group_by_items = () => {
		group_by.group_by_fields = group_by.group_by_fields.filter((f) => f !== "assigned_to");
		render();
	};
	group_by.render_group_by_items();
	group_by.setup_dropdown();
}
