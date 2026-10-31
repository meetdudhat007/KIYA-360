"""Contract tests for the Desk's Convert and Raise Quotation buttons.

Runs without a site:
    python -m unittest knit360_core.api.test_c2c_contract

knit360_core.api.c2c imports frappe, so this reads the doctypes it names out of
its source with ast instead of importing it. What it checks is structural: that
those doctypes exist and are lifecycle-governed, and that conversion moves a
lead on a transition the matrix allows.

Tests for the /knit360 page's own endpoints went with the page on
31 October 2026 (DEC-044).
"""

import ast
import json
import pathlib
import unittest

APP = pathlib.Path(__file__).resolve().parent.parent

import sys

sys.path.insert(0, str(APP.parent))
from knit360_core.business_status import model  # noqa: E402  (after sys.path setup)


def named_doctypes():
	"""LEAD and OPPORTUNITY from c2c.py, without importing frappe."""
	tree = ast.parse((APP / "api" / "c2c.py").read_text(encoding="utf-8"))
	found = {
		node.targets[0].id: ast.literal_eval(node.value)
		for node in tree.body
		if isinstance(node, ast.Assign)
		and isinstance(node.targets[0], ast.Name)
		and node.targets[0].id in ("LEAD", "OPPORTUNITY")
	}
	if set(found) != {"LEAD", "OPPORTUNITY"}:
		raise AssertionError(f"c2c.py no longer defines LEAD and OPPORTUNITY: {found}")
	return found


def doctype_names():
	names = set()
	for path in APP.glob("*/doctype/*/*.json"):
		data = json.loads(path.read_text(encoding="utf-8"))
		if data.get("doctype") == "DocType":
			names.add(data["name"])
	return names


class TestC2CContract(unittest.TestCase):
	def test_named_doctypes_exist(self):
		existing = doctype_names()
		for doctype in named_doctypes().values():
			self.assertIn(doctype, existing)

	def test_named_doctypes_have_a_registered_lifecycle(self):
		"""The buttons sit beside status buttons drawn from the lifecycle; a
		doctype falling back to DEFAULT would offer states it does not have."""
		for doctype in named_doctypes().values():
			self.assertIn(doctype, model.REGISTRY, f"{doctype} has no lifecycle of its own")

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
