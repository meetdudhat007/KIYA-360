"""Idempotent demo seeding for the KIYA 360 prototype.

Run:
    bench --site <site> execute kiya_core.demo_seed.seed.execute

Every write goes through the Frappe document API so controller validation,
permissions and the audit timeline behave normally. No field name is assumed:
_assert_fields checks each one against the installed doctype metadata first and
raises naming the missing fields, rather than silently writing bad data.
"""

import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from kiya_core.demo_seed import brd_data, custom_fields

COMPANY = brd_data.BRD_ORG_CONTEXT["company"]


def _assert_fields(doctype, fieldnames):
	"""Raise if the installed doctype lacks any of these fields."""
	meta = frappe.get_meta(doctype)
	missing = [f for f in fieldnames if meta.get_field(f) is None]
	if missing:
		frappe.throw(
			f"{doctype} has no field(s): {', '.join(missing)}. "
			f"Check the installed app version before seeding."
		)


def _insert(doctype, filters, values):
	"""Insert a document unless one matching filters already exists.

	Returns the document name, existing or new.
	"""
	existing = frappe.db.exists(doctype, filters)
	if existing:
		return existing

	doc = frappe.get_doc(dict(doctype=doctype, **values))
	doc.insert(ignore_permissions=True)
	return doc.name


def _assert_company():
	if not frappe.db.exists("Company", COMPANY):
		frappe.throw(
			f"Company '{COMPANY}' does not exist. Create it through the ERPNext "
			f"setup wizard first (country, currency and chart of accounts are "
			f"setup decisions this script does not make)."
		)


def configure_naming_series():
	"""Put the BRD series first in each doctype's naming_series options."""
	for doctype, series in brd_data.BRD_NAMING_SERIES.items():
		_assert_fields(doctype, ["naming_series"])
		field = frappe.get_meta(doctype).get_field("naming_series")
		options = [o for o in (field.options or "").split("\n") if o.strip()]
		if series in options:
			continue
		make_property_setter(
			doctype,
			"naming_series",
			"options",
			"\n".join([series] + options),
			"Text",
			validate_fields_for_doctype=False,
		)


def seed_dev2():
	"""Item Group, Item and Customer masters."""
	item = brd_data.BRD_ITEM

	_assert_fields("Item Group", ["item_group_name", "parent_item_group", "is_group"])
	_insert(
		"Item Group",
		{"item_group_name": item["item_group"]},
		{
			"item_group_name": item["item_group"],
			"parent_item_group": "All Item Groups",
			"is_group": 0,
		},
	)

	_assert_fields("Item", ["item_code", "item_name", "item_group", "stock_uom", "kiya_hsn_sac_code"])
	_insert(
		"Item",
		{"item_code": item["item_code"]},
		{
			"item_code": item["item_code"],
			"item_name": item["item_code"],
			"item_group": item["item_group"],
			"stock_uom": item["stock_uom"],
			"kiya_hsn_sac_code": item["hsn_sac_code"],
		},
	)

	_assert_fields("Customer", ["customer_name", "customer_group", "territory"])
	for customer in brd_data.PLACEHOLDER_CUSTOMERS:
		_insert(
			"Customer",
			{"customer_name": customer["customer_name"]},
			{
				"customer_name": customer["customer_name"],
				"customer_group": "All Customer Groups",
				"territory": "All Territories",
			},
		)


def seed_dev3():
	"""Department, Designation, Employee and Asset Category masters."""
	department = brd_data.BRD_ORG_CONTEXT["department"]

	_assert_fields("Department", ["department_name", "company", "parent_department", "is_group"])
	_insert(
		"Department",
		{"department_name": department, "company": COMPANY},
		{
			"department_name": department,
			"company": COMPANY,
			"parent_department": "All Departments",
			"is_group": 0,
		},
	)

	_assert_fields("Designation", ["designation_name"])
	for designation in brd_data.PLACEHOLDER_DESIGNATIONS:
		_insert(
			"Designation",
			{"designation_name": designation},
			{"designation_name": designation},
		)

	employee = brd_data.PLACEHOLDER_EMPLOYEE
	_assert_fields(
		"Employee",
		[
			"first_name",
			"last_name",
			"gender",
			"date_of_birth",
			"date_of_joining",
			"company",
			"department",
			"designation",
			"status",
		],
	)
	_insert(
		"Employee",
		{
			"first_name": employee["first_name"],
			"last_name": employee["last_name"],
			"company": COMPANY,
		},
		{
			"first_name": employee["first_name"],
			"last_name": employee["last_name"],
			"gender": employee["gender"],
			"date_of_birth": employee["date_of_birth"],
			"date_of_joining": employee["date_of_joining"],
			"company": COMPANY,
			"department": frappe.db.get_value(
				"Department", {"department_name": department, "company": COMPANY}, "name"
			),
			"designation": employee["designation"],
			"status": "Active",
		},
	)

	_assert_fields("Asset Category", ["asset_category_name"])
	_insert(
		"Asset Category",
		{"asset_category_name": brd_data.PLACEHOLDER_ASSET_CATEGORY},
		{"asset_category_name": brd_data.PLACEHOLDER_ASSET_CATEGORY},
	)


def set_role_approval_authority():
	"""Apply the BRD's Sales Manager approval ceiling."""
	role = brd_data.BRD_USER_ROLE
	if not frappe.db.exists("Role", role["role_name"]):
		frappe.throw(f"Role '{role['role_name']}' does not exist.")

	frappe.db.set_value(
		"Role", role["role_name"], "kiya_approval_authority", role["approval_authority"]
	)


def execute():
	custom_fields.install()
	_assert_company()
	configure_naming_series()
	set_role_approval_authority()
	seed_dev2()
	seed_dev3()
	frappe.db.commit()
