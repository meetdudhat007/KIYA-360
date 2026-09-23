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

after_install = "knit360_core.branding.after_install"
after_migrate = "knit360_core.branding.after_migrate"
