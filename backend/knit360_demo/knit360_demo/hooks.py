"""knit360_demo -- the ERPNext-based client demo.

Track A. Exists to stand up the three-week pitch on ERPNext + HRMS. It is
throwaway demo scaffolding, not the product: nothing in knit360_core may import
from here. The dependency runs one way only, knit360_demo -> knit360_core.

bench new-app generates its own hooks.py; merge these entries into it.
"""

app_name = "knit360_demo"
app_title = "KNIT 360 Demo"
app_publisher = "KNIT 360"
app_description = "Demo seeding and branding over ERPNext and HRMS. Not the KNIT 360 product."
app_email = "TBD"
app_license = "TBD"

required_apps = ["erpnext", "hrms", "knit360_core"]

# Business status transition UI on ERPNext's Sales Order. The whitelisted
# methods it calls live in knit360_core.business_status.engine.
doctype_js = {"Sales Order": "public/js/sales_order_business_status.js"}
