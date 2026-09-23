"""The KNIT Customer-to-Cash workspace, served at /knit.

Deliberately a Frappe website page rather than a separately hosted single-page
app. Two things come free that way and are not worth reimplementing yet: the
session cookie set by the KNIT-branded /login, and the CSRF token Frappe
injects into the '<!-- csrf_token -->' marker in index.html.

The page itself is framework-free HTML, CSS and JavaScript, so nothing here
pre-empts the front-end technology decision for the eventual product UI. That
decision has not been taken (no ADR covers it) and AGENTS.md bars an agent from
taking it. What this page proves is the seam, not the stack: every call it makes
goes to knit_core.api.c2c, never to Frappe's generic /api/resource endpoints.
"""

import frappe

no_cache = 1


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/knit"
		raise frappe.Redirect

	# Frappe's page renderer substitutes the '<!-- csrf_token -->' marker from
	# the session, but it only reads the token -- it does not create one. Only
	# the Desk boot does that, so a standalone page has to ask for it here or
	# the marker renders as "None" and every POST is rejected.
	frappe.sessions.get_csrf_token()

	context.no_cache = 1
	context.user = frappe.session.user
	return context
