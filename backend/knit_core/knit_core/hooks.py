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
