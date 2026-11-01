// The lead list without Frappe's likes, at the owner's request (DEC-047).
//
// Frappe draws a heart on every list row and a "Liked by me" heart in the
// header, with no setting to turn them off. Both come from the list's own
// HTML builders, so this list's copies of those builders leave the hearts out
// -- along with the dot Frappe puts between the comment count and the heart.
// Every other list keeps Frappe's likes.

frappe.listview_settings["KNIT 360 Lead"] = {
	onload(listview) {
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
