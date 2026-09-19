"""Demo seed values.

BRD_* values are quoted verbatim from source/KIYA360_BRD.pdf (v2.0).
PLACEHOLDER_* values are NOT in the BRD. The BRD carries worked examples only
in Section 1 (Platform & Administration); it gives no Customer, Employee,
Designation or Asset Category example. Confirm these with the client before
the demo.
"""

# BRD Section 1.1, "Example" row.
BRD_ORG_CONTEXT = {
	"company": "Kelvinotherm Induction LLP",
	"branch": "Ahmedabad",
	"business_unit": "Induction Furnace",
	"division": "Manufacturing",
	"department": "Production",
	"location": "Vatva GIDC, Ahmedabad",
}

# BRD Section 1.2, "Example" row.
# "Approval Authority: Up to Rs 10 Lakhs" -> 10,00,000 INR.
BRD_USER_ROLE = {
	"role_name": "Sales Manager",
	"user_full_name": "Ramesh Shah",
	"approval_authority": 1000000,
}

# BRD Section 1.4.2, "Example" row.
BRD_ITEM = {
	"item_code": "IF-1500",
	"item_group": "Induction Furnace",
	"hsn_sac_code": "8514",
	"stock_uom": "Nos",
}

# BRD Section 1.6, "Example" row: SO-2025-0001, INV-2025-0001, PO-2025-0001.
# Frappe naming-series syntax; ".####." yields the 4 digits the BRD shows.
BRD_NAMING_SERIES = {
	"Sales Order": "SO-.YYYY.-.####.",
	"Sales Invoice": "INV-.YYYY.-.####.",
	"Purchase Order": "PO-.YYYY.-.####.",
}

# --- Not BRD-sourced. Confirm before use. ---

PLACEHOLDER_CUSTOMERS = [
	{"customer_name": "Demo Customer A"},
	{"customer_name": "Demo Customer B"},
]

PLACEHOLDER_DESIGNATIONS = [
	"Production Manager",
	"Shop Floor Supervisor",
]

PLACEHOLDER_EMPLOYEE = {
	"first_name": "Demo",
	"last_name": "Employee",
	"gender": "Male",
	"date_of_birth": "1990-01-01",
	"date_of_joining": "2024-01-01",
	"designation": "Production Manager",
}

PLACEHOLDER_ASSET_CATEGORY = "Plant and Machinery"
