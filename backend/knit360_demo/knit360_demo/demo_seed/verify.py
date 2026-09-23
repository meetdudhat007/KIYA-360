"""Read-only green/red check on the demo state.

    bench --site <site> execute knit360_demo.demo_seed.verify.run

Writes nothing, so it is safe to run on freeze day, each rehearsal morning and
immediately before the client demo. Every check is isolated: one failure does
not stop the rest, so a single run tells you everything that is broken.
"""

import frappe

from knit360_core.business_status import model as bs_model
from knit360_core.business_status.engine import FIELD as BS_FIELD
from knit360_core.business_status.engine import LOG_DOCTYPE, conflicting_workflow
from knit360_core import brd_data
from knit360_demo.demo_seed import platform

COMPANY = brd_data.BRD_ORG_CONTEXT["company"]
CHECKS = []


def check(label):
	def register(fn):
		CHECKS.append((label, fn))
		return fn

	return register


def _submitted(doctype, filters=None):
	"""Name of one submitted document, or None."""
	return frappe.db.get_value(doctype, dict(docstatus=1, **(filters or {})), "name")


def _require_submitted(doctype):
	name = _submitted(doctype)
	if not name:
		raise AssertionError(f"no submitted {doctype}")
	return name


@check("Company and naming series")
def _company():
	if not frappe.db.exists("Company", COMPANY):
		raise AssertionError(f"Company '{COMPANY}' missing")
	wrong = []
	for doctype, series in brd_data.BRD_NAMING_SERIES.items():
		options = (frappe.get_meta(doctype).get_field("naming_series").options or "").split("\n")
		if series not in options:
			wrong.append(doctype)
	if wrong:
		raise AssertionError(f"BRD series not applied to: {', '.join(wrong)}")
	return COMPANY


@check("knit360_core custom fields")
def _custom_fields():
	missing = []
	for doctype, fieldname in (
		("Role", "knit360_approval_authority"),
		("Item", "knit360_hsn_sac_code"),
	):
		if frappe.get_meta(doctype).get_field(fieldname) is None:
			missing.append(f"{doctype}.{fieldname}")
	if missing:
		raise AssertionError(f"missing: {', '.join(missing)}")
	authority = frappe.db.get_value(
		"Role", brd_data.BRD_USER_ROLE["role_name"], "knit360_approval_authority"
	)
	if not authority:
		raise AssertionError("Sales Manager approval authority not set")
	return f"approval authority {authority}"


@check("BRD item IF-1500")
def _item():
	item = brd_data.BRD_ITEM
	if not frappe.db.exists("Item", item["item_code"]):
		raise AssertionError(f"Item {item['item_code']} missing")
	hsn = frappe.db.get_value("Item", item["item_code"], "knit360_hsn_sac_code")
	if hsn != item["hsn_sac_code"]:
		raise AssertionError(f"HSN/SAC is '{hsn}', expected '{item['hsn_sac_code']}'")
	return f"{item['item_code']} HSN {hsn}"


@check("Customer-to-Cash chain")
def _c2c():
	found = {}
	for doctype in (
		"Quotation",
		"Sales Order",
		"Delivery Note",
		"Sales Invoice",
	):
		found[doctype] = _require_submitted(doctype)
	if not frappe.db.exists("Lead", {"company_name": brd_data.PLACEHOLDER_LEAD["company_name"]}):
		raise AssertionError("demo Lead missing")
	if not _submitted("Payment Entry", {"payment_type": "Receive"}):
		raise AssertionError("no submitted inbound Payment Entry")
	return f"{len(found) + 2} documents"


@check("Procure-to-Pay chain")
def _p2p():
	for doctype in (
		"Material Request",
		"Request for Quotation",
		"Supplier Quotation",
		"Purchase Order",
		"Purchase Receipt",
		"Purchase Invoice",
		"Quality Inspection",
	):
		_require_submitted(doctype)
	if not _submitted("Payment Entry", {"payment_type": "Pay"}):
		raise AssertionError("no submitted outbound Payment Entry")
	return "8 documents"


@check("Production and HR")
def _operations():
	_require_submitted("BOM")
	if not frappe.db.exists("Work Order", {"production_item": brd_data.BRD_ITEM["item_code"]}):
		raise AssertionError("Work Order missing")
	if not frappe.db.exists("Salary Slip", {}):
		raise AssertionError("Salary Slip missing")
	if not frappe.db.exists("Leave Application", {}):
		raise AssertionError("Leave Application missing")
	return "BOM, Work Order, Salary Slip, Leave Application"


@check("Asset and maintenance")
def _assets():
	asset = frappe.db.get_value("Asset", {"company": COMPANY}, "name")
	if not asset:
		raise AssertionError("Asset missing")
	if not frappe.db.exists("Asset Maintenance", {"asset_name": asset}):
		raise AssertionError("Asset Maintenance missing")
	return asset


@check("Sales Order approval workflow")
def _workflow():
	if not frappe.db.exists("Workflow", platform.WORKFLOW_NAME):
		raise AssertionError(f"Workflow '{platform.WORKFLOW_NAME}' missing")
	if not frappe.db.get_value("Workflow", platform.WORKFLOW_NAME, "is_active"):
		raise AssertionError("workflow exists but is not active")
	return platform.WORKFLOW_NAME


@check("Dashboard")
def _dashboard():
	if not frappe.db.exists("Dashboard", platform.DASHBOARD_NAME):
		raise AssertionError(f"Dashboard '{platform.DASHBOARD_NAME}' missing")
	missing = [c["name"] for c in platform.CARDS if not frappe.db.exists("Number Card", c["name"])]
	if missing:
		raise AssertionError(f"missing cards: {', '.join(missing)}")
	return f"{len(platform.CARDS)} cards"


@check("CD-002 business status adapter")
def _business_status():
	if frappe.get_meta("Sales Order").get_field(BS_FIELD) is None:
		raise AssertionError(f"Sales Order.{BS_FIELD} missing")
	if not frappe.db.exists("DocType", LOG_DOCTYPE):
		raise AssertionError(f"{LOG_DOCTYPE} doctype not installed")
	clash = conflicting_workflow("Sales Order")
	if clash:
		raise AssertionError(
			f"Frappe Workflow '{clash}' is active on Sales Order and fights the adapter "
			f"for docstatus. Run only one of them in the demo."
		)
	states = frappe.db.count(LOG_DOCTYPE)
	return f"{len(bs_model.STATES)} states, {states} logged transitions"


def run():
	results = []
	failures = 0
	for label, fn in CHECKS:
		try:
			detail = fn()
			results.append(("PASS", label, detail or ""))
		except Exception as exc:
			failures += 1
			results.append(("FAIL", label, str(exc)))

	width = max(len(label) for _, label, _ in results)
	for status, label, detail in results:
		print(f"{status}  {label.ljust(width)}  {detail}")
	print(f"\n{len(results) - failures}/{len(results)} checks passed")
	return {"passed": len(results) - failures, "failed": failures, "results": results}
