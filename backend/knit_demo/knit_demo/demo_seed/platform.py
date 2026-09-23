"""Day 3-4: Sales Order approval workflow and the stand-in dashboard.

    bench --site <site> execute knit_demo.demo_seed.platform.install_workflow
    bench --site <site> execute knit_demo.demo_seed.platform.install_dashboard

install_workflow uses Frappe's Workflow doctype, which drives docstatus.
CD-002 (document 30) rejects the docstatus model, so this demonstrates the
framework feature, not the approved KNIT lifecycle.

Run install_workflow AFTER flows.run_c2c, or the Sales Order there will stop
at Pending Approval instead of submitting.
"""

import json

import frappe

from knit_core import brd_data
from knit_demo.demo_seed._util import insert_if_absent, require

WORKFLOW_NAME = "KNIT Sales Order Approval"
APPROVER_ROLE = brd_data.BRD_USER_ROLE["role_name"]
REQUESTER_ROLE = "Sales User"

# Draft and Pending Approval hold docstatus 0; Approved submits the document.
STATES = [
	("Draft", 0, REQUESTER_ROLE),
	("Pending Approval", 0, APPROVER_ROLE),
	("Approved", 1, APPROVER_ROLE),
]

# Blocks approval above the role's BRD approval ceiling (FR-PADM-1.2.4).
APPROVAL_CONDITION = (
	'doc.grand_total <= frappe.db.get_value("Role", "{role}", "knit_approval_authority")'
).format(role=APPROVER_ROLE)

TRANSITIONS = [
	("Draft", "Submit for Approval", "Pending Approval", REQUESTER_ROLE, None),
	("Pending Approval", "Approve", "Approved", APPROVER_ROLE, APPROVAL_CONDITION),
]


def install_workflow():
	require("Role", APPROVER_ROLE, "It ships with ERPNext.")
	require("Role", REQUESTER_ROLE, "It ships with ERPNext.")

	for state, _doc_status, _role in STATES:
		insert_if_absent("Workflow State", state, {"workflow_state_name": state})
	for _state, action, _next_state, _role, _condition in TRANSITIONS:
		insert_if_absent("Workflow Action Master", action, {"workflow_action_name": action})

	if frappe.db.exists("Workflow", WORKFLOW_NAME):
		return WORKFLOW_NAME

	workflow = frappe.get_doc(
		{
			"doctype": "Workflow",
			"workflow_name": WORKFLOW_NAME,
			"document_type": "Sales Order",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"send_email_alert": 0,
			"states": [
				{"state": state, "doc_status": doc_status, "allow_edit": role}
				for state, doc_status, role in STATES
			],
			"transitions": [
				{
					"state": state,
					"action": action,
					"next_state": next_state,
					"allowed": role,
					"condition": condition,
				}
				for state, action, next_state, role, condition in TRANSITIONS
			],
		}
	)
	# Frappe adds the workflow_state custom field to Sales Order on save.
	workflow.insert(ignore_permissions=True)
	frappe.db.commit()
	return workflow.name


CARDS = [
	{
		"name": "KNIT Open Sales Orders",
		"label": "Open Sales Orders",
		"document_type": "Sales Order",
		"function": "Count",
		"filters_json": json.dumps([["Sales Order", "status", "not in", ["Closed", "Completed"]]]),
	},
	{
		"name": "KNIT Low Stock Bins",
		"label": "Low Stock Bins",
		"document_type": "Bin",
		"function": "Count",
		"filters_json": json.dumps([["Bin", "actual_qty", "<", 1]]),
	},
	{
		"name": "KNIT Pending Leave Requests",
		"label": "Pending Leave Requests",
		"document_type": "Leave Application",
		"function": "Count",
		"filters_json": json.dumps([["Leave Application", "status", "=", "Open"]]),
	},
	{
		"name": "KNIT Recent Changes",
		"label": "Recent Changes",
		"document_type": "Version",
		"function": "Count",
		"filters_json": json.dumps([["Version", "creation", ">", "Today"]]),
	},
]

DASHBOARD_NAME = "KNIT Overview"


def install_dashboard():
	"""Number Cards plus one Dashboard. Stands in for the BI module."""
	for card in CARDS:
		insert_if_absent(
			"Number Card",
			card["name"],
			{
				"__newname": card["name"],
				"label": card["label"],
				"type": "Document Type",
				"document_type": card["document_type"],
				"function": card["function"],
				"filters_json": card["filters_json"],
				"is_public": 1,
			},
		)

	dashboard = insert_if_absent(
		"Dashboard",
		DASHBOARD_NAME,
		{
			"__newname": DASHBOARD_NAME,
			"dashboard_name": DASHBOARD_NAME,
			"is_default": 0,
			"cards": [{"card": card["name"]} for card in CARDS],
		},
	)
	frappe.db.commit()
	return dashboard
