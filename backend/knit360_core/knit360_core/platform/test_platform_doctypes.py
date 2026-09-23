"""Structural tests for the knit360_core doctype definitions.

Runs without a site:
    python -m unittest knit360_core.platform.test_platform_doctypes

The test that matters is test_link_targets_are_bare_frappe_safe. knit360_core must
install on a site where Frappe is the only app, so a Link pointing at an
ERPNext or HRMS doctype is a broken build, not a style problem.
"""

import json
import pathlib
import unittest

APP = pathlib.Path(__file__).resolve().parent.parent

# Frappe framework doctypes knit360_core is allowed to depend on.
FRAPPE_CORE = {"User", "Role", "Currency", "Country", "DocType", "File", "Company Setup"}

# Doctypes ERPNext or HRMS own. A Link to any of these breaks bare Frappe.
FOREIGN = {
	"Company", "Customer", "Supplier", "Item", "Employee", "Department", "Branch",
	"Warehouse", "Sales Order", "Sales Invoice", "Purchase Order", "Asset",
	"Cost Center", "Fiscal Year", "Account", "BOM", "Work Order",
}


def doctype_files():
	return sorted(APP.glob("*/doctype/*/*.json"))


def load(path):
	return json.loads(path.read_text(encoding="utf-8"))


class TestDoctypeDefinitions(unittest.TestCase):
	def setUp(self):
		self.files = doctype_files()
		self.assertTrue(self.files, "no doctype JSON found")
		self.defined = {load(p)["name"] for p in self.files}

	def test_json_is_valid_and_named(self):
		for path in self.files:
			d = load(path)
			for key in ("name", "module", "doctype", "fields", "field_order", "permissions"):
				self.assertIn(key, d, f"{path.name} missing {key}")
			self.assertEqual(d["doctype"], "DocType", path.name)

	def test_field_order_matches_fields(self):
		for path in self.files:
			d = load(path)
			self.assertEqual(
				d["field_order"], [f["fieldname"] for f in d["fields"]], d["name"]
			)

	def test_no_duplicate_fieldnames(self):
		for path in self.files:
			d = load(path)
			names = [f["fieldname"] for f in d["fields"]]
			self.assertEqual(len(names), len(set(names)), f"{d['name']} has duplicate fieldnames")

	def test_autoname_and_title_fields_exist(self):
		for path in self.files:
			d = load(path)
			names = {f["fieldname"] for f in d["fields"]}
			if str(d.get("autoname", "")).startswith("field:"):
				self.assertIn(d["autoname"].split(":", 1)[1], names, d["name"])
			if d.get("title_field"):
				self.assertIn(d["title_field"], names, d["name"])

	def test_every_link_has_options(self):
		for path in self.files:
			d = load(path)
			for f in d["fields"]:
				if f["fieldtype"] in ("Link", "Table", "Table MultiSelect"):
					self.assertTrue(f.get("options"), f"{d['name']}.{f['fieldname']} has no options")

	def test_link_targets_are_bare_frappe_safe(self):
		"""knit360_core must not depend on ERPNext or HRMS."""
		for path in self.files:
			d = load(path)
			for f in d["fields"]:
				if f["fieldtype"] != "Link":
					continue
				target = f["options"]
				self.assertNotIn(
					target, FOREIGN,
					f"{d['name']}.{f['fieldname']} links to '{target}', which ERPNext/HRMS owns. "
					f"knit360_core must install on bare Frappe.",
				)
				self.assertTrue(
					target in FRAPPE_CORE or target in self.defined,
					f"{d['name']}.{f['fieldname']} links to unknown doctype '{target}'",
				)

	def test_modules_are_declared(self):
		declared = {
			line.strip()
			for line in (APP / "modules.txt").read_text(encoding="utf-8").splitlines()
			if line.strip()
		}
		for path in self.files:
			self.assertIn(load(path)["module"], declared, f"{path.name} module not in modules.txt")

	def test_every_field_is_traceable(self):
		"""Non-layout fields carry the BRD requirement they came from."""
		layout = {"Section Break", "Column Break", "Tab Break", "HTML"}
		for path in self.files:
			d = load(path)
			if d["module"] == "Business Status":
				continue  # infrastructure, not a BRD requirement
			for f in d["fields"]:
				if f["fieldtype"] in layout:
					continue
				self.assertTrue(
					f.get("description", "").startswith("FR-"),
					f"{d['name']}.{f['fieldname']} has no BRD trace in its description",
				)


	def test_status_field_options_match_the_registered_lifecycle(self):
		"""A doctype's Select options must equal its lifecycle in model.py.

		The states live in two places -- the lifecycle registry and the
		doctype JSON -- so this stops them drifting apart.
		"""
		from knit360_core.business_status import model

		FIELD = model.FIELD

		checked = 0
		for path in self.files:
			d = load(path)
			for f in d["fields"]:
				if f["fieldname"] != FIELD:
					continue
				lifecycle = model.for_doctype(d["name"])
				self.assertEqual(
					f["options"].split(chr(10)), lifecycle.states,
					f"{d['name']}.{FIELD} options do not match the '{lifecycle.name}' lifecycle",
				)
				self.assertEqual(f.get("default"), lifecycle.initial, d["name"])
				self.assertEqual(f.get("read_only"), 1,
					f"{d['name']}.{FIELD} must be read-only; transitions go through the engine")
				checked += 1
		self.assertTrue(checked, "no business status fields found to check")


if __name__ == "__main__":
	unittest.main()
