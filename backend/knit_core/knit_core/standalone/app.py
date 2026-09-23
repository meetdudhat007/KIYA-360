"""Standalone preview of the CD-002 lifecycle.

This is NOT ERPNext. It exists so the approved business status model can be
seen working without a bench, and it imports the real product modules --
knit_core.business_status.model and knit_core.brd_data -- rather
than reimplementing them. A rule broken here is broken in the Frappe adapter
too.

    python backend/run_preview.py
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from knit_core.business_status import model
from knit_core import brd_data
from knit_core.standalone import store

STATIC = Path(__file__).parent / "static"
DEMO_USER = brd_data.BRD_USER_ROLE["user_full_name"]

app = FastAPI(title="KNIT — Business Status Preview")


class NewOrder(BaseModel):
	customer: str
	qty: int = 1
	rate: float = float(brd_data.PLACEHOLDER_DEMO_RATE)


class Transition(BaseModel):
	to_status: str
	reason: str | None = None


@app.on_event("startup")
def _startup():
	store.init()


@app.get("/api/context")
def context():
	"""BRD-sourced values, straight from brd_data."""
	return {
		"company": brd_data.BRD_ORG_CONTEXT["company"],
		"branch": brd_data.BRD_ORG_CONTEXT["branch"],
		"location": brd_data.BRD_ORG_CONTEXT["location"],
		"user": DEMO_USER,
		"role": brd_data.BRD_USER_ROLE["role_name"],
		"approval_authority": brd_data.BRD_USER_ROLE["approval_authority"],
		"item": brd_data.BRD_ITEM,
		"states": model.STATES,
	}


@app.get("/api/orders")
def list_orders():
	return store.list_orders()


@app.post("/api/orders")
def create_order(payload: NewOrder):
	name = store.next_name("SO", 2025)
	return store.create_order(
		name,
		payload.customer,
		brd_data.BRD_ITEM["item_code"],
		payload.qty,
		payload.rate,
		model.DRAFT,
		model.required_docstatus(model.DRAFT, 0),
	)


@app.get("/api/orders/{name}")
def get_order(name: str):
	order = store.get_order(name)
	if not order:
		raise HTTPException(404, f"Sales Order {name} not found")
	return {
		"order": order,
		"allowed_next": sorted(model.TRANSITIONS.get(order["business_status"], set())),
		"log": store.get_log(name),
	}


@app.post("/api/orders/{name}/transition")
def transition(name: str, payload: Transition):
	order = store.get_order(name)
	if not order:
		raise HTTPException(404, f"Sales Order {name} not found")

	from_status = order["business_status"]
	to_status = payload.to_status

	if to_status not in model.STATES:
		raise HTTPException(400, f"Unknown business status: {to_status}")

	if not model.is_allowed(from_status, to_status):
		allowed = sorted(model.TRANSITIONS.get(from_status, set())) or ["(terminal)"]
		raise HTTPException(
			400,
			f"'{from_status}' -> '{to_status}' is not an allowed transition. "
			f"Allowed: {', '.join(allowed)}.",
		)

	from_docstatus = order["docstatus"]
	to_docstatus = model.required_docstatus(to_status, from_docstatus)

	# Same invariant the Frappe adapter enforces: 0->1 and 1->2 only.
	if to_docstatus != from_docstatus and (from_docstatus, to_docstatus) not in {(0, 1), (1, 2)}:
		raise HTTPException(
			400,
			f"Cannot move docstatus {from_docstatus} -> {to_docstatus}. "
			f"Reverse the posted document instead of rewriting it.",
		)

	store.apply_transition(
		name, to_status, to_docstatus, from_status, from_docstatus, payload.reason, DEMO_USER
	)
	return get_order(name)


app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
	return FileResponse(STATIC / "index.html")
