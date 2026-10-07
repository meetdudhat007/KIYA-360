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
	//: Shown in place of the framework's own About dialog, which lists the
	//: vendor's website, GitHub, blog, forum and five social accounts, then
	//: every installed app by name, then the vendor's copyright line.
	//:
	//: MIT asks that the copyright and permission notice travel with the
	//: software. They do: every source file keeps its header and Frappe's
	//: LICENSE is untouched. MIT does not require a host application to
	//: display them in its interface, which is what makes this replacement --
	//: rather than the removal of a notice -- the thing being done here.
	replace_about_dialog() {
		if (!frappe.ui || !frappe.ui.misc) {
			console.warn("KNIT 360: frappe.ui.misc not found; the About dialog was left alone.");
			return;
		}

		frappe.ui.misc.about = function () {
			if (knit360.branding.about_dialog) {
				knit360.branding.about_dialog.show();
				return;
			}

			const dialog = new frappe.ui.Dialog({ title: __("KNIT 360") });
			$(dialog.body).html(
				`<div>
					<p>${__("KNIT 360 — unified CRM and ERP platform.")}</p>
					<p class="text-muted" id="knit360-version">${__("Loading version...")}</p>
				</div>`
			);
			knit360.branding.about_dialog = dialog;

			// Only this product's version. get_versions returns every installed
			// app, and naming the others here would put back what the dialog
			// was replaced to leave out.
			frappe.call({
				method: "frappe.utils.change_log.get_versions",
				callback: (r) => {
					const app = (r.message || {}).knit360_core;
					const text = app
						? __("Version {0}", [app.branch_version || app.version])
						: __("Version unavailable");
					$(dialog.body).find("#knit360-version").text(text);
				},
			});

			dialog.show();
		};
	},

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

	suppress_search_bar_vendor_entries() {
		// Two things the search bar offers that are not ours to offer.
		//
		// The first is "Search for ...", which opens the framework's own index.
		// That index only ever holds fields a doctype marks for it, no KNIT 360
		// field does, and so it has always returned nothing. KNIT 360 now
		// supplies the bar with its own results through the awesomebar_search
		// hook, so the empty one is removed rather than left to disappoint.
		//
		// The second is "Install ... from Marketplace", which links to the
		// framework vendor's commercial store.
		if (!frappe.search || !frappe.search.AwesomeBar) {
			console.warn(
				"KNIT 360: frappe.search.AwesomeBar not found, so the vendor search " +
					"entries could not be suppressed. Check awesome_bar.js after an upgrade."
			);
			return;
		}

		frappe.search.AwesomeBar.prototype.make_global_search = function () {
			// Deliberately nothing. KNIT 360's own results come from the
			// awesomebar_search hook -- see knit360_core/search/api.py.
		};

		if (frappe.search.utils) {
			frappe.search.utils.get_marketplace_apps = function () {
				return [];
			};
		}
	},
};

knit360.branding.suppress_vendor_banners();
knit360.branding.suppress_search_bar_vendor_entries();
knit360.branding.replace_about_dialog();
