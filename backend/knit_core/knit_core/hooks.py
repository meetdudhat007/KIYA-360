"""knit_core -- the KNIT product app.

Track B. Runs on bare Frappe. Must never import from erpnext, hrms or
knit_demo, and must never reference a doctype those apps own. Anything here
has to work on a site where Frappe is the only installed app.

bench new-app generates its own hooks.py; merge these entries into it.
"""

app_name = "knit_core"
app_title = "KNIT"
app_publisher = "KNIT"
app_description = "KNIT platform. Built to the BRD on the Frappe framework."
app_email = "TBD"
app_license = "TBD"

# --- Branding -----------------------------------------------------------
# Hooks are only the fallback: Website Settings and Navbar Settings take
# precedence, so knit_core.branding writes those too.
app_logo_url = "/assets/knit_core/images/knit-logo.svg"

website_context = {
	"favicon": "/assets/knit_core/images/knit-logo.svg",
	"splash_image": "/assets/knit_core/images/knit-logo.svg",
	"brand_html": "KNIT",
}

after_install = "knit_core.branding.after_install"
after_migrate = "knit_core.branding.after_migrate"
