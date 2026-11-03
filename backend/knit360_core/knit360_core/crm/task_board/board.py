"""The CRM page's My Tasks block (DEC-058).

A Custom HTML Block -- Frappe's own way to put something of one's own on a
workspace -- holding only a place to draw. The calendar and the day's tasks are
drawn by knit360.tasks.board in public/js/tasks.bundle.js, the same code that
draws the lead page's Tasks panel, so the two never disagree.

Put at the top of the CRM workspace on every migrate, after knit360_core.desk
has rebuilt the workspace's blocks and knit360_core.dashboards has put its
cards above them.
"""

import json

import frappe

BLOCK = "KNIT 360 My Tasks"
WORKSPACE = "CRM"


def install():
	if not frappe.db.exists("Workspace", WORKSPACE):
		return

	if frappe.db.exists("Custom HTML Block", BLOCK):
		block = frappe.get_doc("Custom HTML Block", BLOCK)
	else:
		block = frappe.new_doc("Custom HTML Block")
		block.name = BLOCK
	block.update(
		{
			"html": '<div class="knit-task-board"></div>',
			"script": "knit360.tasks.board(root_element);",
			"style": "",
			"private": 0,
		}
	)
	block.save(ignore_permissions=True)

	workspace = frappe.get_doc("Workspace", WORKSPACE)
	# The page finds a block by its row's label, so the label is the block's name.
	workspace.custom_blocks = [row for row in workspace.custom_blocks if row.custom_block_name != BLOCK]
	workspace.append("custom_blocks", {"custom_block_name": BLOCK, "label": BLOCK})
	others = [
		b
		for b in json.loads(workspace.content or "[]")
		if not (b.get("type") == "custom_block" and b.get("data", {}).get("custom_block_name") == BLOCK)
	]
	mine = {"id": "knittaskboard", "type": "custom_block", "data": {"custom_block_name": BLOCK, "col": 12}}
	workspace.content = json.dumps([mine, *others])
	workspace.save(ignore_permissions=True)
	frappe.db.commit()
