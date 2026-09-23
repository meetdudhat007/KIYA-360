"""SQLite persistence for the standalone preview.

Mirrors what engine.py does inside Frappe: a document carries a business
status and a docstatus, and every transition appends an immutable log row.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "knit_preview.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sales_order (
	name TEXT PRIMARY KEY,
	customer TEXT NOT NULL,
	item_code TEXT NOT NULL,
	qty INTEGER NOT NULL,
	rate REAL NOT NULL,
	business_status TEXT NOT NULL,
	docstatus INTEGER NOT NULL,
	created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS status_log (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	reference_name TEXT NOT NULL,
	from_status TEXT NOT NULL,
	to_status TEXT NOT NULL,
	from_docstatus INTEGER NOT NULL,
	to_docstatus INTEGER NOT NULL,
	reason TEXT,
	transitioned_by TEXT NOT NULL,
	transitioned_at TEXT NOT NULL
);
"""


def connect():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init():
	with connect() as conn:
		conn.executescript(SCHEMA)


def next_name(series_prefix, year):
	"""Next document number, matching the BRD's SO-2025-0001 format."""
	with connect() as conn:
		row = conn.execute(
			"SELECT COUNT(*) AS n FROM sales_order WHERE name LIKE ?",
			(f"{series_prefix}-{year}-%",),
		).fetchone()
	return f"{series_prefix}-{year}-{row['n'] + 1:04d}"


def list_orders():
	with connect() as conn:
		rows = conn.execute("SELECT * FROM sales_order ORDER BY created_at DESC").fetchall()
	return [dict(r) for r in rows]


def get_order(name):
	with connect() as conn:
		row = conn.execute("SELECT * FROM sales_order WHERE name = ?", (name,)).fetchone()
	return dict(row) if row else None


def create_order(name, customer, item_code, qty, rate, status, docstatus):
	with connect() as conn:
		conn.execute(
			"INSERT INTO sales_order "
			"(name, customer, item_code, qty, rate, business_status, docstatus, created_at) "
			"VALUES (?,?,?,?,?,?,?,?)",
			(name, customer, item_code, qty, rate, status, docstatus, datetime.now().isoformat()),
		)
	return get_order(name)


def apply_transition(name, to_status, to_docstatus, from_status, from_docstatus, reason, user):
	with connect() as conn:
		conn.execute(
			"UPDATE sales_order SET business_status = ?, docstatus = ? WHERE name = ?",
			(to_status, to_docstatus, name),
		)
		conn.execute(
			"INSERT INTO status_log "
			"(reference_name, from_status, to_status, from_docstatus, to_docstatus, "
			"reason, transitioned_by, transitioned_at) VALUES (?,?,?,?,?,?,?,?)",
			(
				name,
				from_status,
				to_status,
				from_docstatus,
				to_docstatus,
				reason,
				user,
				datetime.now().isoformat(),
			),
		)
	return get_order(name)


def get_log(name):
	with connect() as conn:
		rows = conn.execute(
			"SELECT * FROM status_log WHERE reference_name = ? ORDER BY id DESC", (name,)
		).fetchall()
	return [dict(r) for r in rows]
