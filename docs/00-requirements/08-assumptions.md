# KIYA 360 — Assumptions & Constraints

| ID | Assumption / Constraint | Source | Status | Impact |
| --- | --- | --- | --- | --- |
| AC-001 | India is the primary Phase 1 tax jurisdiction (GST); the Global Tax Engine architecture supports incremental addition of further country tax rule sets. | BRD §12 | BRD-stated assumption / constraint | Defines initial tax jurisdiction scope; country expansion detail is TBD. |
| AC-002 | Existing company, branch, customer, supplier, item, and employee master data will be imported via Master Data Management before go-live. | BRD §12 | BRD-stated assumption | Prerequisite for go-live; migration/cutover services from named legacy suites are separately out of scope. |
| AC-003 | Users have stable internet connectivity for the cloud platform; Mobile Application provides offline sync for intermittent connectivity. | BRD §12 | BRD-stated assumption / constraint | Establishes connectivity expectation and mobile offline requirement. |
| AC-004 | Enterprise-suite comparison is directional internal stakeholder communication, not a feature-parity guarantee. | BRD §12 | BRD-stated constraint | Prevents treating positioning comparison as functional requirements. |

No proposed engineering assumptions are introduced in Phase 0A.
