"""knit360_core -- the KNIT 360 product app.

Track B. Runs on bare Frappe. Must never import from erpnext, hrms or
knit360_demo, and must never reference a doctype those apps own. Anything here
has to work on a site where Frappe is the only installed app.

bench new-app generates its own hooks.py; merge these entries into it.
"""

app_name = "knit360_core"
app_title = "KNIT 360"
app_publisher = "KNIT 360"
app_description = "KNIT 360 platform. Built to the BRD on the Frappe framework."
app_email = "TBD"
app_license = "TBD"

# --- Branding -----------------------------------------------------------
# Hooks are only the fallback: Website Settings and Navbar Settings take
# precedence, so knit360_core.branding writes those too.
app_logo_url = "/assets/knit360_core/images/knit360-logo.svg"

website_context = {
	"favicon": "/assets/knit360_core/images/knit360-logo.svg",
	"splash_image": "/assets/knit360_core/images/knit360-logo.svg",
	"brand_html": "KNIT 360",
}

# --- Desk UI ------------------------------------------------------------
# The business status field is read-only everywhere, so the Desk had no way to
# move a document along its lifecycle -- only the three stages on /knit360
# could be moved at all. This renders a button per legal move on every form,
# asking the engine what is legal rather than deciding for itself.
# Named *.bundle.js so Frappe's bundler emits it with a content hash. Served
# from a fixed path it was cached by the browser forever, and every change to
# it needed a hard refresh on every machine.
app_include_js = [
	"business_status.bundle.js",
	# Suppresses Frappe's own product adverts in the list sidebar. Our CRM
	# module triggers one for a competing CRM product; see the file.
	"branding.bundle.js",
]

after_install = [
	"knit360_core.branding.after_install",
	"knit360_core.desk.after_migrate",
	"knit360_core.dashboards.after_migrate",
]
after_migrate = [
	"knit360_core.branding.after_migrate",
	# Desk shows nothing for a module until a Workspace exists for it.
	"knit360_core.desk.after_migrate",
	# Charts and number cards go on top of those workspaces.
	"knit360_core.dashboards.after_migrate",
	# A default account field added after a company was created would otherwise
	# stay empty for ever; setup() will not re-enter an existing chart. DEC-021.
	"knit360_core.finance.chart_of_accounts.backfill_defaults",
	# Indexes any document that has no search row yet. Cheap when there is
	# nothing missing, and self-healing after an import or a restore; a full
	# rebuild stays an explicit command.
	"knit360_core.search.index.top_up",
]

# --- Printing -------------------------------------------------------------
# The print formats break tax into its components, which means calling the
# same function the posting code calls rather than a second copy of the rule
# written in Jinja. A print format that computes its own tax is a print format
# that will one day disagree with the ledger.
jinja = {
	# The function keeps its own name in the template; Frappe takes the
	# name from the function, not from an alias.
	"methods": ["knit360_core.pricing.totals.tax_lines"],
}

# --- Search ---------------------------------------------------------------
# The framework's own index only holds fields a doctype marks for it, and no
# KNIT 360 field did, so the bar found nothing. This adds our index as a source.
awesomebar_search = ["knit360_core.search.api.awesomebar"]

# --- Lifecycle integrity -------------------------------------------------
# CD-002 makes the business status the lifecycle. These refuse a submit or
# cancel that did not come through the adapter, on any doctype that has a
# registered lifecycle. See knit360_core/business_status/guard.py.
doc_events = {
	"*": {
		"before_submit": "knit360_core.business_status.guard.before_submit",
		"before_cancel": "knit360_core.business_status.guard.before_cancel",
		# --- Search -----------------------------------------------------
		# One index row per document, kept current by the document's own
		# lifecycle rather than by a scheduled job, so a document is findable
		# the moment it exists. The handlers ignore anything that is not a
		# KNIT 360 parent document. See knit360_core/search/index.py.
		"after_insert": "knit360_core.search.index.index_document",
		"on_update": "knit360_core.search.index.index_document",
		# A status moves by db_set, which fires on_change rather than
		# on_update. Without this the bar described a paid invoice as Overdue.
		"on_change": "knit360_core.search.index.index_document",
		"after_rename": "knit360_core.search.index.rename_document",
		"on_trash": "knit360_core.search.index.remove_document",
	}
}
