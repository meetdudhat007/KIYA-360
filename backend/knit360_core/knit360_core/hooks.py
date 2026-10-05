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
app_include_js = "business_status.bundle.js"

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
]

# --- Lifecycle integrity -------------------------------------------------
# CD-002 makes the business status the lifecycle. These refuse a submit or
# cancel that did not come through the adapter, on any doctype that has a
# registered lifecycle. See knit360_core/business_status/guard.py.
doc_events = {
	"*": {
		"before_submit": "knit360_core.business_status.guard.before_submit",
		"before_cancel": "knit360_core.business_status.guard.before_cancel",
	}
}
