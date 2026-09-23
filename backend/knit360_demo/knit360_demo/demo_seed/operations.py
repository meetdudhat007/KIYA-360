"""Day 3-4: HRMS payroll, production and asset/quality demo records.

Run after seed.execute():
    bench --site <site> execute knit360_demo.demo_seed.operations.run_all
"""

import frappe
from frappe.utils import add_days, nowdate

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip

from knit360_core import brd_data
from knit360_demo.demo_seed import flows
from knit360_demo.demo_seed._util import assert_fields, insert_if_absent, require, submit_new

COMPANY = brd_data.BRD_ORG_CONTEXT["company"]


def _employee():
	employee = brd_data.PLACEHOLDER_EMPLOYEE
	name = frappe.db.get_value(
		"Employee",
		{
			"first_name": employee["first_name"],
			"last_name": employee["last_name"],
			"company": COMPANY,
		},
		"name",
	)
	if not name:
		frappe.throw("Demo Employee not found. Run knit360_demo.demo_seed.seed.execute first.")
	return name


def seed_hr():
	"""Leave allocation, leave application, salary structure and salary slip."""
	employee = _employee()
	leave_type = brd_data.PLACEHOLDER_LEAVE_TYPE
	insert_if_absent("Leave Type", leave_type, {"leave_type_name": leave_type})

	assert_fields(
		"Leave Allocation",
		["employee", "leave_type", "from_date", "to_date", "new_leaves_allocated"],
	)
	allocation = insert_if_absent(
		"Leave Allocation",
		{"employee": employee, "leave_type": leave_type, "docstatus": 1},
		{
			"employee": employee,
			"leave_type": leave_type,
			"from_date": nowdate(),
			"to_date": add_days(nowdate(), 365),
			"new_leaves_allocated": 10,
			"docstatus": 1,
		},
	)

	leave_from = add_days(nowdate(), 1)
	leave_to = add_days(nowdate(), brd_data.PLACEHOLDER_LEAVE_DAYS)
	application = insert_if_absent(
		"Leave Application",
		{"employee": employee, "leave_type": leave_type},
		{
			"employee": employee,
			"leave_type": leave_type,
			"from_date": leave_from,
			"to_date": leave_to,
			"company": COMPANY,
			"status": "Approved",
			"docstatus": 1,
		},
	)

	salary = brd_data.PLACEHOLDER_SALARY
	for component, component_type in (
		(salary["earning_component"], "Earning"),
		(salary["deduction_component"], "Deduction"),
	):
		insert_if_absent(
			"Salary Component",
			component,
			{"salary_component": component, "type": component_type},
		)

	structure_name = salary["structure_name"]
	if not frappe.db.exists("Salary Structure", structure_name):
		structure = frappe.get_doc(
			{
				"doctype": "Salary Structure",
				"__newname": structure_name,
				"company": COMPANY,
				"payroll_frequency": "Monthly",
				"currency": frappe.db.get_value("Company", COMPANY, "default_currency"),
				"earnings": [
					{"salary_component": salary["earning_component"], "amount": salary["base"]}
				],
				"deductions": [
					{"salary_component": salary["deduction_component"], "amount": 0}
				],
			}
		)
		submit_new(structure)

	insert_if_absent(
		"Salary Structure Assignment",
		{"employee": employee, "salary_structure": structure_name, "docstatus": 1},
		{
			"employee": employee,
			"salary_structure": structure_name,
			"from_date": nowdate(),
			"base": salary["base"],
			"company": COMPANY,
			"docstatus": 1,
		},
	)

	slip = make_salary_slip(structure_name, employee=employee)
	slip.insert(ignore_permissions=True)

	frappe.db.commit()
	return {
		"Leave Allocation": allocation,
		"Leave Application": application,
		"Salary Structure": structure_name,
		"Salary Slip": slip.name,
	}


def seed_production():
	"""Raw material, BOM and Work Order for the BRD item IF-1500."""
	finished = brd_data.BRD_ITEM["item_code"]
	raw = brd_data.PLACEHOLDER_RAW_ITEM
	require("Item", finished, "Run knit360_demo.demo_seed.seed.execute first.")

	assert_fields("Item", ["item_code", "item_name", "item_group", "stock_uom"])
	insert_if_absent(
		"Item",
		{"item_code": raw["item_code"]},
		{
			"item_code": raw["item_code"],
			"item_name": raw["item_name"],
			"item_group": brd_data.BRD_ITEM["item_group"],
			"stock_uom": raw["stock_uom"],
		},
	)

	# Gives the raw material a valuation rate so the BOM costs at non-zero.
	flows.receive_stock(item_code=raw["item_code"], qty=brd_data.PLACEHOLDER_DEMO_QTY)

	bom_name = frappe.db.get_value("BOM", {"item": finished, "docstatus": 1}, "name")
	if not bom_name:
		bom = frappe.get_doc(
			{
				"doctype": "BOM",
				"item": finished,
				"quantity": 1,
				"company": COMPANY,
				"items": [{"item_code": raw["item_code"], "qty": 1}],
			}
		)
		bom_name = submit_new(bom)

	assert_fields(
		"Work Order",
		["production_item", "bom_no", "qty", "company", "wip_warehouse", "fg_warehouse"],
	)
	warehouse = flows._warehouse()
	work_order = insert_if_absent(
		"Work Order",
		{"production_item": finished, "bom_no": bom_name},
		{
			"production_item": finished,
			"bom_no": bom_name,
			"qty": brd_data.PLACEHOLDER_DEMO_QTY,
			"company": COMPANY,
			"wip_warehouse": warehouse,
			"fg_warehouse": warehouse,
			"planned_start_date": nowdate(),
		},
	)

	frappe.db.commit()
	return {"BOM": bom_name, "Work Order": work_order}


def seed_asset_and_quality():
	"""Quality Inspection Template, a capital Asset and its maintenance schedule.

	The Asset is left in draft: submitting it requires depreciation account
	mappings on the Asset Category, which the BRD does not specify.
	"""
	parameter = "Visual Inspection"
	insert_if_absent("Quality Inspection Parameter", parameter, {"parameter": parameter})

	template_name = "IF-1500 Incoming Inspection"
	template = insert_if_absent(
		"Quality Inspection Template",
		template_name,
		{
			"quality_inspection_template_name": template_name,
			"item_quality_inspection_parameter": [
				{"specification": parameter, "acceptance_formula": ""}
			],
		},
	)

	asset_item = brd_data.PLACEHOLDER_ASSET_ITEM
	asset_category = brd_data.PLACEHOLDER_ASSET_CATEGORY
	require(
		"Asset Category", asset_category, "Run knit360_demo.demo_seed.seed.execute first."
	)

	insert_if_absent(
		"Item",
		{"item_code": asset_item["item_code"]},
		{
			"item_code": asset_item["item_code"],
			"item_name": asset_item["item_name"],
			"item_group": brd_data.BRD_ITEM["item_group"],
			"stock_uom": asset_item["stock_uom"],
			"is_fixed_asset": 1,
			"is_stock_item": 0,
			"asset_category": asset_category,
		},
	)

	location = brd_data.BRD_ORG_CONTEXT["location"]
	insert_if_absent("Location", location, {"location_name": location})

	assert_fields(
		"Asset",
		["item_code", "asset_name", "asset_category", "company", "gross_purchase_amount"],
	)
	asset = insert_if_absent(
		"Asset",
		{"asset_name": asset_item["item_name"], "company": COMPANY},
		{
			"item_code": asset_item["item_code"],
			"asset_name": asset_item["item_name"],
			"asset_category": asset_category,
			"company": COMPANY,
			"location": location,
			"purchase_date": nowdate(),
			"available_for_use_date": nowdate(),
			"gross_purchase_amount": brd_data.PLACEHOLDER_ASSET_COST,
			"calculate_depreciation": 0,
		},
	)

	task = brd_data.PLACEHOLDER_MAINTENANCE_TASK
	maintenance = insert_if_absent(
		"Asset Maintenance",
		{"asset_name": asset},
		{
			"asset_name": asset,
			"item_code": asset_item["item_code"],
			"company": COMPANY,
			"asset_maintenance_tasks": [
				{
					"maintenance_task": task["maintenance_task"],
					"periodicity": task["periodicity"],
					"maintenance_type": task["maintenance_type"],
					"start_date": nowdate(),
					"assign_to": frappe.session.user,
				}
			],
		},
	)

	frappe.db.commit()
	return {
		"Quality Inspection Template": template,
		"Asset": asset,
		"Asset Maintenance": maintenance,
	}


def run_all():
	result = {}
	result.update(seed_production())
	result.update(seed_hr())
	result.update(seed_asset_and_quality())
	return result
