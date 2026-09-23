"""knit_demo -- the ERPNext-based client demo.

Track A. Exists to stand up the three-week pitch on ERPNext + HRMS. It is
throwaway demo scaffolding, not the product: nothing in knit_core may import
from here. The dependency runs one way only, knit_demo -> knit_core.

bench new-app generates its own hooks.py; merge these entries into it.
"""

app_name = "knit_demo"
app_title = "KNIT Demo"
app_publisher = "KNIT"
app_description = "Demo seeding and branding over ERPNext and HRMS. Not the KNIT product."
app_email = "TBD"
app_license = "TBD"

required_apps = ["erpnext", "hrms", "knit_core"]

# Business status transition UI on ERPNext's Sales Order. The whitelisted
# methods it calls live in knit_core.business_status.engine.
doctype_js = {"Sales Order": "public/js/sales_order_business_status.js"}
