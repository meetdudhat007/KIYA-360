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

	def test_brd_requirement_inventory_is_intact(self):
		"""The copied BRD inventory still has the shape it is supposed to.

		brd_requirements.py is generated from
		docs/00-requirements/02-module-inventory.md by
		scripts/generate_brd_requirements.py. The app cannot see the docs tree
		at runtime, so this cannot catch a *stale* copy -- but it does catch a
		truncated or corrupted one, which is the failure that would quietly
		understate coverage in front of a client.
		"""
		import re

		from knit360_core import brd_requirements

		self.assertEqual(len(brd_requirements.REQUIREMENTS), 238)
		self.assertEqual(len(brd_requirements.MODULES), 28)

		ids = [row[0] for row in brd_requirements.REQUIREMENTS]
		self.assertEqual(len(ids), len(set(ids)), "duplicate requirement ids")

		pattern = re.compile(r"^FR-[A-Z]+-[0-9]+(\.[0-9]+)*$")
		for req_id, name, module_no, classification in brd_requirements.REQUIREMENTS:
			self.assertRegex(req_id, pattern, f"{req_id} is not a requirement id")
			self.assertTrue(name.strip(), f"{req_id} has no name")
			self.assertIn(module_no, brd_requirements.MODULES, f"{req_id} cites module {module_no}")
			self.assertTrue(classification.strip(), f"{req_id} has no classification")

	def test_every_proven_requirement_exists(self):
		"""traceability.PROVEN_BY is hand-maintained, so it is checked.

		A line claiming a requirement is proven by a check that does not exist,
		or naming a requirement that is not in the BRD, would put a false green
		in front of a client. Both are refused here.
		"""
		from knit360_core import acceptance, brd_requirements, traceability

		known = {row[0] for row in brd_requirements.REQUIREMENTS}
		check_names = {name for _group, name, _fn in acceptance.CHECKS}

		for req_id, check in traceability.PROVEN_BY.items():
			self.assertIn(req_id, known, f"{req_id} is claimed proven but is not in the BRD")
			self.assertIn(
				check,
				check_names,
				f"{req_id} claims to be proven by '{check}', which is not an acceptance check",
			)

	def test_every_doctype_declares_how_it_is_named(self):
		"""A document with no naming rule is named with a random hash.

		This test exists because four tree masters -- Item Group, Territory,
		Customer Group and Supplier Group -- shipped without one. Nothing
		complained, because the tables were empty; the first record inserted
		was called 'b497tuqe2q'. A master named like that is unusable in a
		Link field, unreadable in a report and impossible to refer to from
		outside the system.

		A naming rule may live in the JSON as `autoname`, or in the controller
		as an autoname() method when the name is built from several fields
		(KNIT 360 Account qualifies its name with the company abbreviation,
		because two companies both need an account called Debtors).
		"""
		for path in self.files:
			d = load(path)
			if d.get("istable") or d.get("issingle"):
				continue
			controller = path.with_suffix(".py")
			in_code = (
				controller.exists()
				and "def autoname" in controller.read_text(encoding="utf-8")
			)
			self.assertTrue(
				d.get("autoname") or in_code,
				f"{d['name']} declares no autoname and has no autoname() method, "
				f"so its records will be named with a random hash",
			)

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
		#: Modules that implement no BRD requirement, and why. A module is only
		#: exempt because the capability genuinely appears nowhere in the 238 --
		#: not because a trace was hard to find. Inventing an FR- to satisfy
		#: this test would be inventing a requirement, which AGENTS.md forbids.
		INFRASTRUCTURE = {
			"Business Status": "CD-002 lifecycle plumbing; the BRD names no audit-log record",
			"Search": "no requirement among the 238 mentions search, lookup or find",
		}
		for path in self.files:
			d = load(path)
			if d["module"] in INFRASTRUCTURE:
				continue
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
