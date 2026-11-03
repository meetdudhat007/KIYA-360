"""Who may open a lead, and how -- DEC-048.

FR-PADM-1.3.6 Access Control and FR-PADM-1.2.3 Permission Management, applied
to FR-CRM-001 Leads.

Leads are private. A sales login sees the leads it created -- the Lead's role
permissions for Sales User and Sales Manager are "only if creator" -- and the
ones it has been given here. Access to a particular lead comes from three
places, as in the CRMs the owner pointed to (Salesforce and Zoho: the record's
owner, the role hierarchy above them, and manual sharing):

- the employee it is assigned to, who can read and change it;
- everyone above that employee through Reports To, who can read it;
- the people listed under Others With Access, at the level given there.

The grants are Frappe's own document shares, so Frappe's permission checks, its
list filtering and the form's read-only state all honour them with nothing
further here. They are worked out afresh from those three sources whenever a
lead is saved, and whenever an employee's login, manager or active flag
changes, so a share no longer justified by any of them is taken away.

An employee reaches a lead through their login (Employee.user). One with no
login yet, or no longer active, is listed but given nothing; linking a login
later grants the access at once.

System Managers see every lead whatever is set here; that comes from their role.
"""

import json

import frappe

LEAD = "KNIT 360 Lead"
ACCESS = "KNIT 360 Lead Access"
EMPLOYEE = "KNIT 360 Employee"
READ_ONLY = "Read Only"
READ_WRITE = "Read & Write"


def managers(employee):
	"""Everyone above an employee through Reports To, nearest first."""
	chain, seen = [], {employee}
	current = frappe.db.get_value(EMPLOYEE, employee, "reports_to")
	while current and current not in seen:
		chain.append(current)
		seen.add(current)
		current = frappe.db.get_value(EMPLOYEE, current, "reports_to")
	return chain


def below(employee):
	"""An employee and everyone under them through Reports To."""
	found, frontier = {employee}, [employee]
	while frontier:
		frontier = [
			e for e in frappe.get_all(EMPLOYEE, filters={"reports_to": ["in", frontier]}, pluck="name")
			if e not in found
		]
		found.update(frontier)
	return found


def describe(assigned_to, rows):
	"""Everyone with access to a lead, at the strongest level any source gives.

	rows -- (employee, access) pairs from Others With Access.
	Returns one dict per employee, in the order the sources are listed above:
	employee, employee_name, user, active, access, and why (plain words).
	"""
	entries = {}

	def name_of(employee):
		return frappe.db.get_value(EMPLOYEE, employee, "employee_name") or employee

	def give(employee, access, why):
		entry = entries.get(employee)
		if not entry:
			user, active = frappe.db.get_value(EMPLOYEE, employee, ["user", "is_active"]) or (None, 0)
			entry = entries[employee] = {
				"employee": employee,
				"employee_name": name_of(employee),
				"user": user,
				"active": bool(active),
				"access": access,
				"why": [],
			}
		if access == READ_WRITE:
			entry["access"] = READ_WRITE
		entry["why"].append(why)

	if assigned_to:
		give(assigned_to, READ_WRITE, "Assigned")
		assignee = name_of(assigned_to)
		for manager in managers(assigned_to):
			give(manager, READ_ONLY, f"{assignee} reports to them")
	for employee, access in rows:
		if employee:
			give(employee, READ_WRITE if access == READ_WRITE else READ_ONLY, "Added on this lead")

	for entry in entries.values():
		entry["why"] = "; ".join(entry["why"])
	return list(entries.values())


def sync(lead):
	"""Make the lead's shares exactly what describe() says, and nothing else."""
	wanted = {
		entry["user"]: entry["access"] == READ_WRITE
		for entry in describe(lead.assigned_to, [(r.employee, r.access) for r in lead.lead_access])
		if entry["user"] and entry["active"]
	}
	existing = frappe.get_all(
		"DocShare",
		filters={"share_doctype": LEAD, "share_name": lead.name, "everyone": 0},
		fields=["name", "user", "write"],
	)
	flags = {"ignore_share_permission": True}
	for share in existing:
		if share.user not in wanted:
			frappe.delete_doc("DocShare", share.name, ignore_permissions=True, flags=flags)
	for user, write in wanted.items():
		current = next((s for s in existing if s.user == user), None)
		if current and bool(current.write) == write:
			continue
		frappe.share.add_docshare(LEAD, lead.name, user, write=int(write), flags=flags)


def resync_for(employee):
	"""Rework every lead an employee's change can reach.

	Their own leads and those of everyone under them (a new manager, or a lost
	one, changes who reads those), and the leads they are listed on by name.
	"""
	leads = set(frappe.get_all(LEAD, filters={"assigned_to": ["in", list(below(employee))]}, pluck="name"))
	leads.update(
		frappe.get_all(ACCESS, filters={"employee": employee, "parenttype": LEAD}, pluck="parent")
	)
	for name in leads:
		sync(frappe.get_doc(LEAD, name))


@frappe.whitelist()
def who_can_open(assigned_to=None, access=None):
	"""describe() for the form's "Who Can Open This Lead" panel, from the form's
	current, possibly unsaved, values."""
	if not frappe.has_permission(LEAD, "read"):
		raise frappe.PermissionError
	rows = json.loads(access) if isinstance(access, str) else (access or [])
	return [
		{key: entry[key] for key in ("employee_name", "access", "why", "active")}
		| {"has_login": bool(entry["user"])}
		for entry in describe(assigned_to, [(r.get("employee"), r.get("access")) for r in rows])
	]
