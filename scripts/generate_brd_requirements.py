"""Regenerate knit360_core/brd_requirements.py from the approved BRD inventory.

The app runs from a bench that mounts `backend/` and not `docs/`, so it cannot
read the inventory at runtime. This copies it in as data.

Run from the repository root after docs/00-requirements/02-module-inventory.md
changes:

    python scripts/generate_brd_requirements.py

It refuses to write unless it finds exactly the expected number of
requirements, so a parse that silently matched half the table cannot overwrite
a good file with a short one.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "docs" / "00-requirements" / "02-module-inventory.md"
TARGET = ROOT / "backend" / "knit360_core" / "knit360_core" / "brd_requirements.py"

#: The approved inventory holds 238 functional requirements across 28 modules.
#: Both are asserted rather than discovered, so a bad parse fails loudly.
EXPECTED_REQUIREMENTS = 238
EXPECTED_MODULES = 28

MODULE = re.compile(r"^## Module (\d+) — (.+)$")
ROW = re.compile(r"^\|\s*(FR-[A-Z0-9.\-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


def parse():
	rows, modules, module = [], {}, None
	for line in INVENTORY.read_text(encoding="utf-8").splitlines():
		heading = MODULE.match(line.strip())
		if heading:
			module = (int(heading.group(1)), heading.group(2).strip())
			modules[module[0]] = module[1]
			continue
		row = ROW.match(line)
		if row and module:
			rows.append((row.group(1), row.group(2).strip(), module[0], row.group(3).strip()))
	return rows, modules


def render(rows, modules):
	head = TARGET.read_text(encoding="utf-8").split('"""')
	docstring = head[1] if len(head) > 2 else " The BRD requirement inventory, as data. "

	out = ['"""' + docstring + '"""', ""]
	out += ["#: module number -> module name. 28 modules.", "MODULES = {"]
	out += [f"\t{n}: {modules[n]!r}," for n in sorted(modules)]
	out += ["}", "", "#: (requirement id, name, module number, classification). 238 rows.",
	        "REQUIREMENTS = ["]
	out += [f"\t({r[0]!r}, {r[1]!r}, {r[2]}, {r[3]!r})," for r in rows]
	out += ["]", ""]
	return "\n".join(out)


def main():
	if not INVENTORY.exists():
		sys.exit(f"inventory not found at {INVENTORY}")

	rows, modules = parse()
	if len(rows) != EXPECTED_REQUIREMENTS or len(modules) != EXPECTED_MODULES:
		sys.exit(
			f"refusing to write: parsed {len(rows)} requirements across "
			f"{len(modules)} modules, expected {EXPECTED_REQUIREMENTS} and "
			f"{EXPECTED_MODULES}. The inventory's table format has probably changed."
		)

	TARGET.write_text(render(rows, modules), encoding="utf-8")
	print(f"wrote {TARGET.relative_to(ROOT)}: {len(rows)} requirements, {len(modules)} modules")


if __name__ == "__main__":
	main()
