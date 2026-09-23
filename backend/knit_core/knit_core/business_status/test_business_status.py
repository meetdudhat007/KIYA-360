"""Tests for the CD-002 status model.

model.py imports nothing from frappe, so these run without a site:

    python -m unittest knit_core.business_status.test_business_status

Engine tests need a bench and are not included; the value here is pinning the
transition matrix against the architecture diagram so a later edit that drifts
from it fails loudly.
"""

import unittest

from knit_core.business_status import model

# Transcribed independently from the state diagram in
# docs/02-architecture/04-target-architecture.md section 6.1.
DIAGRAM = {
	"Draft": {"Pending Approval", "Cancelled"},
	"Pending Approval": {"Approved", "Rejected", "Cancelled"},
	"Rejected": {"Draft"},
	"Approved": {"In Progress", "Cancelled"},
	"In Progress": {"Partially Completed", "Completed", "Cancelled"},
	"Partially Completed": {"Completed"},
	"Completed": {"Closed"},
	"Closed": set(),
	"Cancelled": set(),
}


class TestStatusModel(unittest.TestCase):
	def test_matrix_matches_architecture_diagram(self):
		self.assertEqual(model.TRANSITIONS, DIAGRAM)

	def test_every_state_has_a_transition_entry(self):
		self.assertEqual(set(model.STATES), set(model.TRANSITIONS))

	def test_every_target_is_a_known_state(self):
		for source, targets in model.TRANSITIONS.items():
			for target in targets:
				self.assertIn(target, model.STATES, f"{source} -> {target}")

	def test_terminal_states_have_no_exits(self):
		for state in model.TERMINAL_STATES:
			self.assertEqual(model.TRANSITIONS[state], set())

	def test_no_state_is_both_draft_and_submitted_backed(self):
		self.assertEqual(model.DRAFT_BACKED & model.SUBMITTED_BACKED, set())

	def test_every_state_has_a_docstatus(self):
		covered = model.DRAFT_BACKED | model.SUBMITTED_BACKED | {model.CANCELLED}
		self.assertEqual(covered, set(model.STATES))

	def test_cancelling_before_approval_stays_a_draft(self):
		# Nothing was posted, so there is nothing for Frappe to reverse, and
		# Frappe cannot cancel a draft in any case.
		self.assertEqual(model.required_docstatus(model.CANCELLED, 0), 0)

	def test_cancelling_after_approval_reverses(self):
		self.assertEqual(model.required_docstatus(model.CANCELLED, 1), 2)

	def test_post_approval_states_share_one_docstatus(self):
		# Approved -> In Progress -> Partially Completed -> Completed -> Closed
		# must not re-submit; they advance by field update alone.
		for state in model.SUBMITTED_BACKED:
			self.assertEqual(model.required_docstatus(state, 1), 1)

	def test_unknown_status_rejected(self):
		with self.assertRaises(ValueError):
			model.required_docstatus("Invented", 0)
		self.assertFalse(model.is_allowed("Invented", model.DRAFT))


class TestLifecycleRegistry(unittest.TestCase):
	"""Every registered lifecycle, not just the default."""

	def all_lifecycles(self):
		return [model.DEFAULT] + list(model.REGISTRY.values())

	def test_unregistered_doctype_gets_the_default(self):
		self.assertIs(model.for_doctype("Some Doctype With No Lifecycle"), model.DEFAULT)

	def test_registered_doctypes_get_their_own(self):
		self.assertIs(model.for_doctype("KNIT Lead"), model.LEAD)
		self.assertIs(model.for_doctype("KNIT Opportunity"), model.OPPORTUNITY)

	def test_initial_state_is_a_state(self):
		for lc in self.all_lifecycles():
			self.assertIn(lc.initial, lc.states, lc.name)

	def test_targets_are_known_states(self):
		for lc in self.all_lifecycles():
			for source, targets in lc.transitions.items():
				for target in targets:
					self.assertIn(target, lc.states, f"{lc.name}: {source} -> {target}")

	def test_every_state_has_a_docstatus(self):
		for lc in self.all_lifecycles():
			covered = lc.draft_states | lc.submitted_states | lc.cancelling_states
			self.assertEqual(covered, set(lc.states), lc.name)

	def test_docstatus_categories_do_not_overlap(self):
		for lc in self.all_lifecycles():
			self.assertEqual(lc.draft_states & lc.submitted_states, set(), lc.name)
			self.assertEqual(lc.draft_states & lc.cancelling_states, set(), lc.name)

	def test_lead_happy_path_matches_dr_c2c_001(self):
		# "New -> Contacted -> Qualified -> Converted"
		path = ["New", "Contacted", "Qualified", "Converted"]
		for a, b in zip(path, path[1:]):
			self.assertTrue(model.LEAD.is_allowed(a, b), f"{a} -> {b}")
		self.assertEqual(model.LEAD.terminal_states, {"Converted", "Disqualified", "Lost"})

	def test_opportunity_happy_path_matches_dr_c2c_002(self):
		# "Open -> In Negotiation -> Proposal Sent -> Won"
		path = ["Open", "In Negotiation", "Proposal Sent", "Won"]
		for a, b in zip(path, path[1:]):
			self.assertTrue(model.OPPORTUNITY.is_allowed(a, b), f"{a} -> {b}")
		self.assertEqual(model.OPPORTUNITY.terminal_states, {"Won", "Lost"})

	def test_non_submittable_lifecycles_never_leave_docstatus_zero(self):
		"""A Lead posts nothing, so no state of it may submit or cancel."""
		for lc in (model.LEAD, model.OPPORTUNITY):
			for state in lc.states:
				self.assertEqual(lc.required_docstatus(state, 0), 0, f"{lc.name}.{state}")

	def test_lifecycles_reject_each_others_states(self):
		self.assertFalse(model.LEAD.is_allowed("New", model.APPROVED))
		with self.assertRaises(ValueError):
			model.LEAD.required_docstatus(model.APPROVED, 0)


if __name__ == "__main__":
	unittest.main()
