// Tasks on leads (DEC-058): a user's own calls, meetings and emails, each for a
// date and a time, like Salesforce's and HubSpot's tasks.
//
// The lead page lists the user's tasks on that lead beside Activity, with a
// form to add one. The CRM page's My Tasks block shows the user's tasks on one
// day, across all their leads, with a date box to pick another day. A task is ticked
// done in either place. The server side, which also rings the bell when a task
// is due, is knit360_core.crm.lead_tasks.

frappe.provide("knit360.tasks");

knit360.tasks = {
	DOCTYPE: "KNIT 360 Task",
	LEAD: "KNIT 360 Lead",
	API: "knit360_core.crm.lead_tasks",

	// For both places. The CRM block draws inside a shadow root, which Frappe's
	// desk styles reach but the page's own <style> elements do not, so these
	// are added to whichever root a task is drawn in.
	CSS: `
		.knit-task { display: flex; gap: var(--padding-sm); align-items: flex-start;
			padding: var(--padding-sm) 0; border-bottom: 1px solid var(--border-color); }
		.knit-task:last-child { border-bottom: 0; }
		.knit-task input[type="checkbox"] { margin-top: 3px; flex: none; }
		.knit-task-body { flex: 1; min-width: 0; }
		.knit-task-when { display: flex; flex-wrap: wrap; align-items: center;
			gap: var(--padding-xs); font-size: var(--text-sm); color: var(--text-muted); }
		.knit-task-what { display: block; color: var(--text-color); white-space: pre-wrap;
			word-break: break-word; cursor: pointer; }
		.knit-task-what:hover { text-decoration: underline; }
		.knit-task-lead { font-size: var(--text-sm); }
		.knit-task.is-done .knit-task-what { text-decoration: line-through; color: var(--text-muted); }
		.knit-tasks-empty { color: var(--text-muted); font-size: var(--text-sm); }
	`,

	style(root, id, css) {
		if (root.querySelector(`style[data-knit="${id}"]`)) return;
		const style = document.createElement("style");
		style.dataset.knit = id;
		style.textContent = css;
		(root === document ? document.head : root).appendChild(style);
	},

	time(value) {
		return moment(value, "H:mm:ss").format("HH:mm");
	},

	// One task: a tick box, when, its type and what to do -- the text opens the
	// task, to change or delete it. On the CRM page, under a heading naming the
	// day, it gives only the time, and which lead it is for, linked to the lead.
	item(task, { show_lead, changed }) {
		const esc = frappe.utils.escape_html;
		const overdue =
			!task.done &&
			moment(`${task.due_date} ${task.due_time}`, "YYYY-MM-DD H:mm:ss").isBefore(moment());
		const $item = $(`<div class="knit-task ${task.done ? "is-done" : ""}"></div>`);
		$(`<input type="checkbox">`)
			.prop("checked", !!task.done)
			.attr("title", task.done ? __("Mark as not done") : __("Mark as done"))
			.on("change", (e) =>
				frappe.db
					.set_value(this.DOCTYPE, task.name, "done", e.target.checked ? 1 : 0)
					.then(changed)
			)
			.appendTo($item);
		const $body = $(`<div class="knit-task-body"></div>`).appendTo($item);
		$(`<div class="knit-task-when ${overdue ? "text-danger" : ""}">
				<span>${show_lead ? "" : esc(frappe.datetime.str_to_user(task.due_date))} ${esc(this.time(task.due_time))}</span>
				<span class="indicator-pill gray">${esc(__(task.task_type))}</span>
				${overdue ? `<span>${__("Overdue")}</span>` : ""}
			</div>`).appendTo($body);
		$(`<a class="knit-task-what"></a>`)
			.text(task.description)
			.attr("title", __("Open task"))
			.on("click", () => frappe.set_route("Form", this.DOCTYPE, task.name))
			.appendTo($body);
		if (show_lead) {
			$(`<a class="knit-task-lead"></a>`)
				.text(`${task.organization_name || ""} · ${task.lead}`)
				.attr("href", `/app/${frappe.router.slug(this.LEAD)}/${encodeURIComponent(task.lead)}`)
				.on("click", (e) => {
					e.preventDefault();
					frappe.set_route("Form", this.LEAD, task.lead);
				})
				.appendTo($body);
		}
		return $item;
	},

	// --- the lead page -----------------------------------------------------

	PANEL_CSS: `
		.after-save.knit-with-tasks { display: grid; column-gap: var(--margin-xl);
			grid-template-columns: minmax(0, 1fr) 340px; }
		.after-save.knit-with-tasks > .comment-box { grid-column: 1 / -1; }
		.after-save.knit-with-tasks > .new-timeline { grid-column: 1; grid-row: 2; }
		.after-save.knit-with-tasks > .knit-tasks { grid-column: 2; grid-row: 2; }
		/* Level with Activity's heading, which Frappe draws 60px tall after 20px of space. */
		.knit-tasks { padding-top: 20px; }
		.knit-tasks h4 { display: flex; align-items: center; min-height: 60px; margin: 0; font-weight: 700; }
		.knit-task-fields { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
			gap: 0 var(--padding-sm); }
		.knit-task-form { margin-bottom: var(--margin-md); }
		/* On a narrow screen, Tasks above Activity. */
		@media (max-width: 991px) {
			.after-save.knit-with-tasks { grid-template-columns: minmax(0, 1fr); }
			.after-save.knit-with-tasks > .knit-tasks { grid-column: 1; grid-row: 2; }
			.after-save.knit-with-tasks > .new-timeline { grid-row: 3; }
		}
	`,

	// The user's tasks on this lead, beside Activity, and a form to add one.
	panel(frm) {
		const $after = frm.$wrapper.find(".form-footer .after-save");
		$after.children(".knit-tasks").remove();
		if (frm.is_new()) return;
		this.style(document, "tasks", this.CSS);
		this.style(document, "task-panel", this.PANEL_CSS);
		$after.addClass("knit-with-tasks");

		const $panel = $(`<div class="knit-tasks"><h4>${__("Tasks")}</h4></div>`).appendTo($after);
		const $form = $(`<div class="knit-task-form"></div>`).appendTo($panel);
		const $fields = $(`<div class="knit-task-fields"></div>`).appendTo($form);
		const control = (df, $parent) => {
			const field = frappe.ui.form.make_control({ df, parent: $parent, render_input: true });
			field.refresh();
			return field;
		};
		const types = (frm.doc.__onload && frm.doc.__onload.task_types) || [];
		const type = control({ fieldtype: "Select", label: __("Type"), options: types }, $fields);
		const date = control({ fieldtype: "Date", label: __("Date") }, $fields);
		const time = control({ fieldtype: "Time", label: __("Time") }, $fields);
		const description = control({ fieldtype: "Small Text", label: __("Description") }, $form);
		// Frappe draws a Small Text 150px tall; a task needs a line or two.
		description.$input.css("height", "64px");
		type.set_value(types[0]);
		date.set_value(frappe.datetime.get_today());

		const $list = $(`<div class="knit-task-list"></div>`).appendTo($panel);
		const list = () =>
			frappe.xcall(`${this.API}.for_lead`, { lead: frm.doc.name }).then((tasks) => {
				$list.empty();
				if (!tasks.length) {
					$list.append(`<p class="knit-tasks-empty">${__("No tasks on this lead yet.")}</p>`);
				}
				tasks.forEach((task) => $list.append(this.item(task, { changed: list })));
			});

		$(`<button type="button" class="btn btn-sm btn-primary"></button>`)
			.text(__("Add Task"))
			.on("click", () => {
				const values = {
					task_type: type.get_value(),
					due_date: date.get_value(),
					due_time: time.get_value(),
					description: (description.get_value() || "").trim(),
				};
				const missing = [
					[values.due_date, __("Date")],
					[values.due_time, __("Time")],
					[values.description, __("Description")],
				].filter(([value]) => !value);
				if (missing.length) {
					frappe.msgprint(__("Please fill in {0}.", [missing.map(([, label]) => label).join(", ")]));
					return;
				}
				frappe.db.insert({ doctype: this.DOCTYPE, lead: frm.doc.name, ...values }).then(() => {
					time.set_value("");
					description.set_value("");
					frappe.show_alert({ message: __("Task added"), indicator: "green" });
					list();
				});
			})
			.appendTo($form);
		list();
	},

	// --- the CRM page --------------------------------------------------------

	BOARD_CSS: `
		.knit-board { padding: var(--padding-md) 0; }
		.knit-board-head { display: flex; flex-wrap: wrap; align-items: center; gap: var(--padding-sm);
			margin-bottom: var(--margin-sm); }
		.knit-board-head h4 { flex: 1; margin: 0; }
		.knit-board-head .frappe-control { width: 150px; margin: 0; }
		.knit-day-title { font-weight: 600; color: var(--text-color); margin-bottom: var(--margin-xs); }
	`,

	// The user's tasks on one day, across all their leads: today to begin
	// with, any other day from the date box, which opens the same calendar as
	// every date field in the system.
	board(root) {
		// Drawn in the page itself rather than inside the block's shadow root,
		// where the date box's calendar would not open as it does elsewhere.
		root.appendChild(document.createElement("slot"));
		$(root.host).empty();
		this.style(document, "tasks", this.CSS);
		this.style(document, "task-board", this.BOARD_CSS);
		const $root = $(`
			<div class="knit-board">
				<div class="knit-board-head">
					<h4>${__("My Tasks")}</h4>
					<span class="knit-day-pick"></span>
					<button type="button" class="btn btn-xs btn-default knit-today">${__("Today")}</button>
				</div>
				<div class="knit-day-title"></div>
				<div class="knit-day-tasks"></div>
			</div>`).appendTo(root.host);

		const today = frappe.datetime.get_today();
		const draw = () => {
			const day = picker.get_value() || today;
			$root.find(".knit-day-title").text(`${moment(day).format("dddd")}, ${frappe.datetime.str_to_user(day)}`);
			frappe.xcall(`${this.API}.on_day`, { date: day }).then((tasks) => {
				const $list = $root.find(".knit-day-tasks").empty();
				if (!tasks.length) {
					$list.append(`<p class="knit-tasks-empty">${__("No tasks on this day.")}</p>`);
				}
				tasks.forEach((task) => $list.append(this.item(task, { show_lead: true, changed: draw })));
			});
		};
		const picker = frappe.ui.form.make_control({
			df: { fieldtype: "Date", fieldname: "knit_task_day", placeholder: __("Date"), change: draw },
			parent: $root.find(".knit-day-pick"),
			render_input: true,
			only_input: true,
		});
		picker.refresh();
		picker.set_value(today);
		$root.find(".knit-today").on("click", () => picker.set_value(today));
		draw();
	},
};
