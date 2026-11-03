// Every contact of the customer, listed on its page (DEC-049).
//
// The customer's own Email and Phone are its first person's; everyone else it
// deals with is a KNIT 360 Contact. Read fresh each time the page opens, and
// each name opens that contact.

frappe.ui.form.on("KNIT 360 Customer", {
	refresh(frm) {
		const field = frm.get_field("contacts_html");
		if (!field) return;
		if (frm.is_new()) {
			field.$wrapper.html("");
			return;
		}
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "KNIT 360 Contact",
				filters: { customer: frm.doc.name },
				fields: ["name", "contact_name", "designation", "department", "email", "phone", "is_primary"],
				order_by: "is_primary desc, creation asc",
				limit_page_length: 0,
			},
			callback: (r) => field.$wrapper.html(knit360_customer_contacts(r.message || [])),
		});
	},
});

function knit360_customer_contacts(contacts) {
	const esc = frappe.utils.escape_html;
	if (!contacts.length) {
		return `<p class="text-muted">${__("No contacts yet.")}</p>`;
	}
	const rows = contacts
		.map(
			(c) => `<tr>
			<td><a href="/app/knit-360-contact/${encodeURIComponent(c.name)}">${esc(c.contact_name)}</a>
				${c.is_primary ? `<span class="indicator-pill green" style="margin-left: 6px">${__("Primary")}</span>` : ""}</td>
			<td>${esc(c.designation || "")}</td>
			<td>${esc(c.department || "")}</td>
			<td>${esc(c.email || "")}</td>
			<td style="white-space: nowrap">${esc(c.phone || "")}</td>
		</tr>`
		)
		.join("");
	return `<div class="table-responsive"><table class="table table-bordered table-condensed">
		<thead><tr><th>${__("Name")}</th><th>${__("Designation")}</th><th>${__("Department")}</th>
		<th>${__("Email")}</th><th>${__("Phone")}</th></tr></thead>
		<tbody>${rows}</tbody></table></div>`;
}
