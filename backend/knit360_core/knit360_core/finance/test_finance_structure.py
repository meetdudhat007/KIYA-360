"""Structural tests for the Finance core.

Runs without a site:
    python -m unittest knit360_core.finance.test_finance_structure

These check the things that only fail at migrate time or, worse, at posting
time: a doctype with no controller module, a chart of accounts naming an
account_type its own doctype does not offer, a company default pointing at an
account the bootstrap never creates.
"""

import ast
import json
import pathlib
import sys
import unittest

APP = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP.parent))

from knit360_core.business_status import model  # noqa: E402


def load(path):
	return json.loads(path.read_text(encoding="utf-8"))


def literal(module_path, name):
	"""Read a module-level constant without importing frappe."""
	tree = ast.parse((APP / module_path).read_text(encoding="utf-8"))
	for node in tree.body:
		if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == name:
			return ast.literal_eval(node.value)
	raise AssertionError(f"{module_path} no longer defines {name}")


def account_options():
	d = load(APP / "finance/doctype/knit_360_account/knit_360_account.json")
	fields = {f["fieldname"]: f for f in d["fields"]}
	return (
		set(fields["root_type"]["options"].split("\n")),
		set(fields["account_type"]["options"].split("\n")),
	)


def flatten(nodes):
	for account_name, account_type, children in nodes:
		yield account_name, account_type, bool(children)
		yield from flatten(children)


class TestFinanceStructure(unittest.TestCase):
	def test_every_doctype_has_a_controller_module(self):
		"""A doctype JSON with no .py beside it fails bench migrate, not the
		test suite -- which is a slow way to find out."""
		missing = [
			str(path.relative_to(APP))
			for path in APP.glob("*/doctype/*/*.json")
			if not path.with_suffix(".py").exists()
		]
		self.assertEqual(missing, [], f"doctypes with no controller: {missing}")

	def test_every_doctype_folder_is_a_package(self):
		missing = [
			str(path.relative_to(APP))
			for path in APP.glob("*/doctype/*")
			if path.is_dir()
			and path.name != "__pycache__"
			and not (path / "__init__.py").exists()
		]
		self.assertEqual(missing, [])

	def test_chart_uses_only_declared_account_types(self):
		roots, types = account_options()
		tree = literal("finance/chart_of_accounts.py", "TREE")
		for root_name, (root_type, children) in tree.items():
			self.assertIn(root_type, roots, f"{root_name} has root_type '{root_type}'")
			for account_name, account_type, _ in flatten(children):
				if account_type is not None:
					self.assertIn(
						account_type, types,
						f"{account_name} has account_type '{account_type}', "
						f"which KNIT 360 Account does not offer",
					)

	def test_chart_gives_leaf_accounts_a_type(self):
		"""A group needs no type. A leaf without one cannot be resolved by a
		posting rule that selects on type."""
		tree = literal("finance/chart_of_accounts.py", "TREE")
		for _root, (_root_type, children) in tree.items():
			for account_name, account_type, is_group in flatten(children):
				if not is_group:
					self.assertIsNotNone(
						account_type, f"leaf account '{account_name}' has no account_type"
					)

	def test_company_defaults_exist_in_the_chart(self):
		"""Sales Invoice refuses to post without these, so the bootstrap has to
		actually create every account it promises to set."""
		tree = literal("finance/chart_of_accounts.py", "TREE")
		defaults = literal("finance/chart_of_accounts.py", "DEFAULTS")
		created = {root for root in tree}
		for _root, (_root_type, children) in tree.items():
			created.update(name for name, _t, _g in flatten(children))
		for field, leaf in defaults.items():
			self.assertIn(leaf, created, f"{field} points at '{leaf}', which the chart never creates")

	def test_company_declares_every_default_field(self):
		company = load(APP / "platform/doctype/knit_360_company/knit_360_company.json")
		fields = {f["fieldname"] for f in company["fields"]}
		for field in literal("finance/chart_of_accounts.py", "DEFAULTS"):
			self.assertIn(field, fields, f"KNIT 360 Company has no field '{field}'")
		self.assertIn("abbreviation", fields)

	def test_posting_doctypes_are_submittable_and_may_submit(self):
		"""A lifecycle with submitted states drives docstatus 1 through
		doc.submit(), which needs the submit permission to exist."""
		for folder in ("knit_360_journal_entry", "knit_360_sales_invoice"):
			d = load(APP / "finance/doctype" / folder / f"{folder}.json")
			lifecycle = model.for_doctype(d["name"])
			self.assertTrue(lifecycle.submitted_states, f"{d['name']} has no submitted states")
			self.assertEqual(d.get("is_submittable"), 1, f"{d['name']} is not submittable")
			self.assertTrue(
				any(p.get("submit") for p in d["permissions"]),
				f"{d['name']} has no role permitted to submit",
			)
			self.assertTrue(
				any(p.get("cancel") for p in d["permissions"]),
				f"{d['name']} has no role permitted to cancel",
			)

	def test_every_lifecycle_state_maps_to_a_docstatus(self):
		"""required_docstatus raises on a state left out of all three sets, and
		it would do so mid-transition, on a real document."""
		for doctype, lifecycle in model.REGISTRY.items():
			for state in lifecycle.states:
				for current in (0, 1):
					lifecycle.required_docstatus(state, current)

	def test_the_ledger_is_the_only_writer_of_gl_entries(self):
		"""GL Entry is created in exactly one module. If that stops being true,
		the invariants in ledger.post are no longer guaranteed."""
		writers = []
		for path in APP.rglob("*.py"):
			if "__pycache__" in path.parts or path.name.startswith("test_"):
				continue
			text = path.read_text(encoding="utf-8")
			if '"doctype": GL' in text or '"doctype": "KNIT 360 GL Entry"' in text:
				writers.append(path.relative_to(APP).as_posix())
		self.assertEqual(writers, ["finance/ledger.py"], f"GL Entry is written by {writers}")


if __name__ == "__main__":
	unittest.main()
