"""Contract tests for the Customer-to-Cash seam.

Runs without a site:
    python -m unittest knit360_core.api.test_c2c_contract

knit360_core.api.c2c imports frappe, so this reads the module's STAGES table out of
its source with ast instead of importing it. That keeps the test runnable in the
same place as the other structural tests, and what it checks is structural
anyway: that the seam's promises about doctypes and fields match the doctype
JSON and the lifecycle registry on disk.
"""

import ast
import json
import pathlib
import unittest

APP = pathlib.Path(__file__).resolve().parent.parent

import sys

sys.path.insert(0, str(APP.parent))
from knit360_core.business_status import model  # noqa: E402  (after sys.path setup)


def stages():
	"""STAGES from c2c.py, without importing frappe."""
	tree = ast.parse((APP / "api" / "c2c.py").read_text(encoding="utf-8"))
	for node in ast.walk(tree):
		if isinstance(node, ast.Assign) and node.targets[0].id == "STAGES":
			return list(ast.literal_eval(node.value))
	raise AssertionError("c2c.py no longer defines STAGES")


def doctype_json(name):
	for path in APP.glob("*/doctype/*/*.json"):
		data = json.loads(path.read_text(encoding="utf-8"))
		if data["name"] == name:
			return data
	raise AssertionError(f"no doctype JSON defines {name}")


class TestC2CContract(unittest.TestCase):
	def setUp(self):
		self.stages = stages()
		self.assertTrue(self.stages)

	def test_stage_keys_are_unique(self):
		keys = [s["key"] for s in self.stages]
		self.assertEqual(len(keys), len(set(keys)), f"duplicate stage keys: {keys}")

	def test_every_stage_doctype_exists(self):
		for stage in self.stages:
			doctype_json(stage["doctype"])

	def test_listed_fields_exist_on_the_doctype(self):
		"""documents() asks the database for these by name. A field renamed in
		the JSON and not here is a 500 at runtime, so it is caught here."""
		for stage in self.stages:
			data = doctype_json(stage["doctype"])
			declared = {f["fieldname"] for f in data["fields"]}
			declared.update({"name", "owner", "creation", "modified", "docstatus"})
			for fieldname in stage["fields"]:
				self.assertIn(
					fieldname,
					declared,
					f"{stage['doctype']} has no field '{fieldname}', "
					f"but c2c.STAGES lists it",
				)

	def test_title_field_exists_and_matches_the_doctype(self):
		for stage in self.stages:
			data = doctype_json(stage["doctype"])
			declared = {f["fieldname"] for f in data["fields"]}
			self.assertIn(stage["title_field"], declared)
			if data.get("title_field"):
				self.assertEqual(
					stage["title_field"],
					data["title_field"],
					f"{stage['doctype']}: the seam's title_field disagrees with "
					f"the doctype's own",
				)

	def test_title_field_is_returned_by_documents(self):
		"""documents() reads row[title_field], so it must be in the select."""
		for stage in self.stages:
			self.assertIn(stage["title_field"], stage["fields"])

	def test_every_stage_has_a_registered_lifecycle(self):
		"""A stage falling back to DEFAULT would offer the front end states its
		doctype's Select field does not have."""
		for stage in self.stages:
			self.assertIn(
				stage["doctype"],
				model.REGISTRY,
				f"{stage['doctype']} is exposed by the seam but has no lifecycle "
				f"of its own in the registry",
			)

	def test_stages_are_in_flow_order(self):
		"""Customer-to-Cash, BRD 6.1: Lead -> Opportunity -> Quotation."""
		self.assertEqual(
			[s["doctype"] for s in self.stages],
			["KNIT 360 Lead", "KNIT 360 Opportunity", "KNIT 360 Quotation"],
		)

	def test_conversion_target_status_is_in_the_lead_lifecycle(self):
		source = (APP / "crm" / "conversion.py").read_text(encoding="utf-8")
		tree = ast.parse(source)
		values = {
			node.targets[0].id: ast.literal_eval(node.value)
			for node in tree.body
			if isinstance(node, ast.Assign)
			and isinstance(node.targets[0], ast.Name)
			and isinstance(node.value, ast.Constant)
		}
		lifecycle = model.REGISTRY["KNIT 360 Lead"]
		self.assertIn(values["REQUIRED_STATUS"], lifecycle.states)
		self.assertIn(values["CONVERTED"], lifecycle.states)
		self.assertTrue(
			lifecycle.is_allowed(values["REQUIRED_STATUS"], values["CONVERTED"]),
			"conversion moves the lead on a transition the matrix forbids",
		)


if __name__ == "__main__":
	unittest.main()
