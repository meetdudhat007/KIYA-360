// Keep other vendors' advertising out of the product -- CD-010 branding.
//
// Frappe's list sidebar appends promotional banners linking to Frappe's own
// commercial products. There are three, in frappe/public/js/frappe/list/
// list_sidebar.js:
//
//   add_crm_banner()       shows on any list whose doctype's module is "CRM",
//                          linking to frappe.io/crm with campaign tracking,
//                          captioned "Switch to Frappe CRM for smarter sales"
//   add_helpdesk_banner()  the same for a module named "Support"
//   add_insights_banner()  on any Report view, linking to Frappe Insights
//
// KNIT 360 has a module called CRM, because that is what BRD module 02 is
// called. The consequence was an advert for a competing CRM product sitting in
// the sidebar of our own Lead, Opportunity and Customer lists -- including in
// front of a client being shown the system.
//
// All three go through one helper, add_banner(), so that is what is overridden
// here. Doing it at the funnel rather than at each of the three also covers any
// further banner Frappe adds through the same path.
//
// On the licence: Frappe Framework is MIT. MIT requires that the copyright and
// permission notice be kept with copies of the software -- which it is, in the
// source files and in Frappe's LICENSE. It does not require a host application
// to display marketing links. Suppressing a banner is not removing a copyright
// notice, and nothing in Frappe's source is modified; this overrides a method
// at runtime from our own bundle. (Not legal advice -- see Y1 in the handover,
// where a real opinion on the licence position is still outstanding.)

frappe.provide("knit360.branding");

knit360.branding = {
	suppress_vendor_banners() {
		// Loaded after list.bundle.js, so the class exists by now. If Frappe
		// ever restructures this, say so in the console rather than failing
		// silently -- a returning advert should be findable.
		if (!frappe.views || !frappe.views.ListSidebar) {
			console.warn(
				"KNIT 360: frappe.views.ListSidebar not found, so vendor banners " +
					"could not be suppressed. Check list_sidebar.js after a Frappe upgrade."
			);
			return;
		}

		frappe.views.ListSidebar.prototype.add_banner = function () {
			// Deliberately nothing. See the note at the top of this file.
		};

		// The Insights banner also honours this flag, so set it as well: if the
		// override above ever stops matching, this still keeps that one away.
		try {
			localStorage.setItem("show_insights_banner", "false");
		} catch (error) {
			// Private browsing and blocked storage both throw here. The banner
			// is cosmetic, so a failure to set the flag is not worth surfacing.
		}
	},
};

knit360.branding.suppress_vendor_banners();
