# KIYA 360 — Asset-to-Service (A2S) Detailed Requirements Expansion (Batch 3)

## 1. Document Control, Authority & Scope

- **Document ID:** `33-asset-to-service-detailed-requirements`
- **Phase:** Phase 0B-2 — Detailed Requirements Expansion (Batch 3: Asset-to-Service)
- **Status:** In Review / Detailed Functional Requirements Baseline
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026: Section 6.1, Section 6.3, Section 7.5, 7.8, 7.9, 7.13, 7.14, 7.17, 7.18, 7.22, Section 8, Section 10)
- **Approved Clarification Decisions:**
  - `CD-001` (`DEC-012`): Hybrid Scope-Expansion Approach — Fully detail the complete BRD A2S core flow; use proven ERP-standard behavior as a traceable reference baseline for non-specified standard mechanics; zero automatic ERPNext coupling; explicit KIYA differentiators and documented exceptions (`docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md`).
  - `CD-002` (`DEC-013`): Operational Business Status Model — Use Business Status representing operational progression; reject ERPNext's dual `docstatus` technical model; progress statuses organically (`docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md`).
- **Dependencies Governed:** `DEP-002` (Inventory/Warehouse to Service), `DEP-004` (Manufacturing to Service/Quality), `DEP-005` (Order/Service to Billing & Accounting), `DEP-008` (Service to Finance & Tax), `DEP-011` (Asset Management to Maintenance & Field Service).
- **Reference Evidence Baseline:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` through `27-erpnext-analysis-review.md`.

---

### 1.1 Classification Discipline & Working Principles

In strict compliance with repository governance (`AGENTS.md`, `docs/00-requirements/12-requirement-status-legend.md`, and `CD-001`), this detailed expansion enforces five discrete levels of requirements authority:

1. **`BRD-REQUIRED`:** Core capabilities, functional entities, and flow stages explicitly mandated by BRD v2.0 (e.g., Asset / Machine, Installation, Warranty, Service Request, Technician Assignment, Spare Parts, Service Work Order, Maintenance Execution, Service Invoice, Payment, Asset History).
2. **`BRD-DERIVED`:** Behaviors and rules that are necessary logical consequences of an explicit BRD mandate (e.g., decrementing inventory balances upon spare parts consumption in field service, checking active warranty status during service triage, updating equipment service timelines upon work order closure), where the exact mechanism is not explicitly dictated by the BRD.
3. **`ERP-REFERENCE`:** Proven enterprise/ERP standard patterns (reverse-engineered from ERPNext in Docs 21–27) adopted as a baseline to accelerate functional definition. These are reference baselines and **must never silently become binding KIYA requirements** without formal ratification.
4. **`PROPOSED`:** Reasonable candidate business rules, field validations, configuration thresholds, or high-value differentiators (such as skills-based technician dispatch matching, automated truck-stock replenishment, or equipment telemetry ingestion) designed to complete the functional specification, pending formal stakeholder confirmation.
5. **`TBD`:** Functional ambiguities, statutory mechanics, or policy choices requiring formal stakeholder clarification (e.g., open questions `OQ-003` through `OQ-015`) before they can be treated as confirmed requirements.

**Operational Business Status Discipline (`CD-002`):**
In accordance with `CD-002` (`DEC-013`), KIYA 360 uses operational **Business Status** as its primary lifecycle model, discarding ERPNext's technical `docstatus` (Draft/Submitted/Cancelled) paradigm. The status values listed under each stage below represent **Candidate Operational Lifecycles (`PROPOSED`)** subject to final tenant workflow configuration; they are not rigid, frozen database enumerations.

**Unified Data Model Discipline (`DEC-007`):**
Master entities (`Customer Master`, `Item Master`, `Warehouse Master`, `Company Master`, `Tax Template`, `Chart of Accounts`, `Currency Master`, `UOM Master`) are strictly unified across all 11 stages and must never be duplicated across module boundaries.

---

## 2. Asset-to-Service Flow Overview & Architectural Spine

The Asset-to-Service (A2S) business flow is the after-sales operational and asset lifecycle backbone of KIYA 360. As mandated by BRD §6.1 and §6.3, it spans 11 distinct stages across 6 functional modules, unifying Asset Management, Field Service & Maintenance, Warehouse/Inventory, Financial Invoicing, Statutory Tax, and Asset Analytics:

```
+------------------+     +--------------------+     +-------------+     +-------------------+
| 1. Asset/Machine | --> | 2. Installation &  | --> | 3. Warranty | --> | 4. Service Request|
| (Installed Base) |     |    Commissioning   |     |  Entitlement|     |    (Incident)     |
+------------------+     +--------------------+     +-------------+     +-------------------+
                                                                                  |
+--------------------------+     +--------------------+     +---------------------+
| 7. Field Service Work Ord| <-- | 6. Spare Parts &   | <-- | 5. Technician Assign|
|    (Service Execution)   |     |    Truck Stock     |     |    & Dispatch       |
+--------------------------+     +--------------------+     +---------------------+
          |
          v
+--------------------------+     +--------------------+     +---------------------+
| 8. Maintenance Execution | --> | 9. Service Invoice | --> | 10. Customer Payment|
| (Preventive / Breakdown) |     |  (Labor & Parts)   |     |    & Settlement     |
+--------------------------+     +--------------------+     +---------------------+
          |                                                            |
          +------------------------------------------------------------+
                                        |
                                        v
                         +-----------------------------+
                         | 11. Complete Asset History  |
                         |     (360-Degree Lifecycle)  |
                         +-----------------------------+
```

---

### 2.1 Critical Architectural Seams & Boundaries

The analysis of ERPNext reference architecture (Docs 21–27) identified two critical domain hazards that KIYA 360 explicitly resolves:

1. **Customer Installed Base vs. Internal Capital Fixed Asset (`Doc 22 §3.3`, `Doc 23 §4.4`, `Doc 24 §08`):**
   - In ERPNext, the `Asset` module is strictly an accounting tool for *company-owned capitalized property* subject to balance sheet depreciation (`assets/doctype/asset/`). Customer equipment is not an `Asset` record; it is represented solely as a `Serial No` string on delivery notes or support tickets.
   - KIYA 360 establishes a first-class **Customer Installed Equipment / Asset** entity in the Asset Management domain (`FR-AST-001`, `FR-AST-003`). This entity maintains full physical hierarchy, operating site location, customer ownership, configuration BOM, service contract coverage, and lifetime telemetry, completely decoupled from corporate capital depreciation schedules.
2. **Field Service Work Order vs. Factory Manufacturing Work Order (`Doc 22 §3.3`, `Doc 23 §4.4`, `Doc 24 §08`):**
   - In ERPNext, `Work Order` belongs strictly to the *Manufacturing* module (`manufacturing/doctype/work_order/`), driving discrete factory production, bill of materials explosion, and shop-floor Job Cards.
   - To avoid catastrophic schema collision, KIYA 360 strictly establishes a distinct **Field Service Work Order** entity (`FR-MFS-002`, `FR-MFS-007`) governing on-site technician labor, field travel, customer sign-off checklists, and truck-stock spare parts consumption. Manufacturing Work Orders remain strictly isolated to the factory floor (C2C Stage 9).

---

## 3. Detailed Requirements per A2S Stage

---

### Stage 1: Asset / Installed Equipment Registry
- **Requirement ID:** `DR-A2S-001`
- **Phase 0A Baseline ID:** `FR-AST-001` (Asset Master), `FR-AST-002` (Asset Classification), `FR-AST-003` (Asset Tracking)
- **Module:** Asset Management | **Sub-Module:** Installed Base & Equipment Master
- **BRD Source:** BRD §6.1, §6.3, §7.13; FR-AST-001, FR-AST-002, FR-AST-003; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Core Flow Anchor & Asset Identity)
- **1. Purpose & Objective:** Establish and maintain an authoritative master record for every piece of serialized equipment, machine, or complex system installed at customer sites, tracking its identity, customer ownership, installation site, configuration, and serviceability.
- **2. Actors & Roles:** Asset Administrator, Field Service Coordinator, Quality Engineer, Customer Support Lead.
- **3. Preconditions:** Customer Master active (`DEC-007`); Item Master active with serialization/traceability enabled (`FR-INV-003`); Company Master configured.
- **4. Inputs:** Asset/Machine identifier, asset name/model, Item Master link, Serial Number, MAC address / IoT identifier (optional), Customer link, Installation site address, contact person, commissioning date, operating parameters, parent equipment link (for sub-assemblies).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Maintains a comprehensive registry of installed assets and machinery (`FR-AST-001`).
  - `[BRD-REQUIRED]` Categorizes assets by technical classification, product line, and criticality (`FR-AST-002`).
  - `[BRD-REQUIRED]` Tracks physical operating location, customer site, and operational environment (`FR-AST-003`).
  - `[BRD-DERIVED]` Links installed assets directly to serialized items delivered through the Customer-to-Cash flow (`DR-C2C-012` Dispatch) or registered directly upon legacy site onboarding.
  - `[PROPOSED / Differentiator]` Supports multi-tier parent-child asset hierarchy (e.g. Turbine → Generator → Bearing Assembly) to enable granular component-level maintenance tracking.
- **6. Business Rules:**
  - `[BRD-REQUIRED / Data Model Separation]` **Installed Base Rule:** Customer-installed equipment records are operational service assets and are maintained independently from corporate financial fixed assets subject to balance-sheet depreciation (`FR-AST-004`).
  - `[PROPOSED / Reference Baseline]` Unique Serial Rule: An active serial number must be globally unique across all active installed assets for a given product line.
  - `[PROPOSED Policy / TBD]` Customer Transfer Rule: Reassigning an installed asset to a new customer entity must archive prior warranty history and require service contract re-baseline (`TBD`).
- **7. Validations:** Serial Number format must conform to Item Master serialization mask; Customer Master and site location must be active records.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Status (`PROPOSED`):* `Registered` → `Commissioned / Operational` → `Under Maintenance` → `Degraded / Limited` → `Decommissioned` (or `Scrapped`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext `Asset` (`assets/doctype/asset/`) tracks company-owned capitalized property with monthly depreciation GL entries (`EWF-10`). Customer equipment is tracked merely as a `Serial No` string (`stock/doctype/serial_no/`) without dedicated asset hierarchy or field maintenance linkages.
  - *Architectural Gap (Doc 21 §WF-15, Doc 23 §34, Doc 24 §08):* ERPNext lacks a dedicated customer installed base domain entity.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA establishes a unified `Customer Installed Asset` record linking serial tracking, customer location, warranty contracts, and maintenance history into a single operational 360-degree view (`FR-AST-001`, `FR-AST-003`).
- **10. Cross-Module Handoffs:** Generates installation milestones (Stage 2); establishes warranty baselines (Stage 3); anchors incoming Service Requests (Stage 4) (`DEP-011`).
- **11. Audit & Security:** All ownership transfers, site location edits, and operational status transitions recorded in immutable audit log (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Alerts field service coordinator upon asset registration from warehouse delivery note.
- **13. Documents & Attachments:** Operating manuals, engineering schematics, P&ID drawings, factory acceptance test (FAT) certificates (`FR-DMS-001`).
- **14. Cancellation & Deactivation:** Decommissioned assets are retained in the registry with historical audit trails intact; serial numbers are retired from active dispatch.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Duplicate serial detection during registration triggers validation block and alerts asset administrator.
- **16. Reporting & KPI Implications:** Installed base by territory, asset uptime/downtime percentages, asset failure rates by product batch (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Given an active customer and serialized item, when registered, the system creates a distinct installed asset record tracking its physical location and customer ownership.
  - System enforces separation between customer-installed equipment and corporate capitalized fixed assets.

---

### Stage 2: Installation & Commissioning
- **Requirement ID:** `DR-A2S-002`
- **Phase 0A Baseline ID:** `FR-MFS-001` (Maintenance Planning), `FR-MFS-007` (Field Service)
- **Module:** Maintenance & Field Service | **Sub-Module:** Site Commissioning & Handover
- **BRD Source:** BRD §6.1, §6.3, §7.14; FR-MFS-001, FR-MFS-007; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage in BRD §6.1)
- **1. Purpose & Objective:** Manage on-site delivery staging, technical installation, calibration, safety testing, and formal customer commissioning handover for newly delivered or relocated equipment.
- **2. Actors & Roles:** Commissioning Lead, Field Service Engineer, Site Project Manager, Customer Site Representative.
- **3. Preconditions:** Installed Asset record created (Stage 1); dispatch/delivery confirmed at customer site (`DR-C2C-012`); commissioning resources assigned.
- **4. Inputs:** Asset reference, Customer site address, delivery note reference, target commissioning date, assigned commissioning technician, installation protocol checklist, baseline operating parameters.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Coordinates field service deployment for equipment installation (`FR-MFS-007`).
  - `[BRD-DERIVED]` Captures actual commissioning date and operational verification sign-off.
  - `[PROPOSED / Business Workflow]` Executes digital installation checklists (power supply verification, mechanical alignment, environmental compliance).
  - `[BRD-DERIVED]` Transitions installed asset status from `Registered` to `Commissioned / Operational`.
  - `[BRD-DERIVED]` Triggers the activation of standard manufacturer warranty coverage (Stage 3).
- **6. Business Rules:**
  - `[BRD-DERIVED / Warranty Activation Rule]` Warranty start date defaults to the customer-signed commissioning handover date, or dispatch date + grace period if commissioning is unconfirmed per tenant policy (`TBD / OQ-011`).
  - `[PROPOSED / Reference Baseline]` Commissioning sign-off requires recorded customer representative acknowledgement (digital signature or sign-off certificate).
- **7. Validations:** Commissioning date cannot precede equipment physical dispatch date; if an installation checklist is configured as applicable, all mandatory items in that configured checklist must be completed before commissioning can be completed.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Commissioning Lifecycle (`PROPOSED`):* `Scheduled` → `In Progress` → `Site Acceptance Testing` → `Commissioned / Handed Over` (or `Rejected / Stalled`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext `Installation Note` (`selling/doctype/installation_note/`) lists delivered serial numbers and provides a simple submit action.
  - *Architectural Gap (Doc 21 §Structural Inventory, Doc 22 §3.3):* ERPNext Installation Note is a static sales-log document. It lacks technician dispatch integration, commissioning workflows, site acceptance checklists, and dynamic warranty activation hooks.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA integrates installation as an active operational field service event executing commissioning verification, customer handover, and downstream warranty triggering (`FR-MFS-001`, `FR-MFS-007`).
- **10. Cross-Module Handoffs:** Activates warranty coverage in Contract/Warranty Management (Stage 3); updates Installed Asset operational status (Stage 1) (`DEP-011`).
- **11. Audit & Security:** Timestamped commissioning checklists, engineer sign-offs, and customer signature images logged in audit history (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Automated alert sent to customer and account manager upon successful commissioning completion.
- **13. Documents & Attachments:** Site Acceptance Test (SAT) reports, customer handover certificate, installation photos, calibration records (`FR-DMS-001`).
- **14. Cancellation & Abort:** Aborted commissioning resets asset status to `Staged / Pending Installation` and records cause of site failure.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Failed commissioning generates a technical Punch List task requiring resolution prior to warranty activation.
- **16. Reporting & KPI Implications:** Commissioning cycle time, first-time installation pass rate, installation defect metrics (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System captures commissioning milestones, checklist execution, and customer handover details for an installed asset.
  - Completing the commissioning event transitions the asset to operational status and sets the baseline warranty activation date.

---

### Stage 3: Warranty & Service Contract Management
- **Requirement ID:** `DR-A2S-003`
- **Phase 0A Baseline ID:** `FR-AST-003` (Asset Tracking), `FR-MFS-006` (Service Contracts)
- **Module:** Maintenance & Field Service / Asset Mgmt | **Sub-Module:** Warranty & Contract Entitlements
- **BRD Source:** BRD §6.1, §6.3, §7.13, §7.14; FR-AST-003, FR-MFS-006; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage & Entitlement Engine)
- **1. Purpose & Objective:** Define, track, and validate warranty coverage, Annual Maintenance Contracts (AMC), and Comprehensive Service Contracts (CMC) against installed assets to govern service entitlement and billing treatment.
- **2. Actors & Roles:** Service Contract Specialist, Warranty Administrator, Customer Service Lead.
- **3. Preconditions:** Installed Asset registered (Stage 1); Commissioning recorded or standard dispatch completed (Stage 2); Customer Master active.
- **4. Inputs:** Asset reference, Item Master warranty template, Contract type (Standard Warranty, Extended Warranty, AMC, CMC), Start date, End date, Coverage terms (parts covered, labor covered, travel covered), Exclusions, SLA tier (optional).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages service contracts and warranty records linked to installed equipment (`FR-MFS-006`).
  - `[BRD-DERIVED]` Calculates coverage validity period based on commissioning date or delivery terms.
  - `[BRD-REQUIRED]` Validates warranty coverage entitlement during service request triage (Stage 4) to distinguish free warranty service from billable repairs (`FR-MFS-006`).
  - `[PROPOSED / Reference Baseline]` Tracks contract renewals, generating advance expiration warnings prior to coverage lapse.
- **6. Business Rules:**
  - `[BRD-DERIVED / Entitlement Rule]` If service request incident date falls within active warranty start and end dates, labor and parts covered under the warranty template are flagged as non-billable (`FR-MFS-006`).
  - `[PROPOSED Policy / TBD]` Warranty Exclusion Rule: Customer abuse, unauthorized tampering, or external force voids warranty entitlement upon technical inspection confirmation (`TBD`).
  - `[PROPOSED Policy / TBD]` Grace Period Policy: Handling warranty claims submitted within a configured buffer window (e.g. 7 days post-expiration) is governed by company service policy (`TBD`).
- **7. Validations:** Coverage end date must be strictly later than start date; warranty template must exist in master configuration.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Warranty/Contract Status (`PROPOSED`):* `Draft` → `Active / In Coverage` → `Expiring Soon` → `Expired` (or `Voided / Terminated`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext stores warranty period in days on `Item` and sets `warranty_expiry_date` on `Serial No`. Customer claims log against `Warranty Claim` (`support/doctype/warranty_claim/`). AMC contracts are tracked under `Maintenance Schedule`.
  - *Architectural Gap (Doc 21 §WF-16, Doc 22 §3.3):* ERPNext provides static expiry dates on serial numbers. It lacks dynamic entitlement engines capable of evaluating multi-tier coverage (e.g., parts-only vs comprehensive labor+parts) and contract renewal pipelines.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA establishes a formal Service Contract & Warranty Entitlement engine (`FR-MFS-006`) that dynamically determines billing treatment for both parts and labor during service triage and work order generation.
- **10. Cross-Module Handoffs:** Informs Service Request warranty determination (Stage 4); feeds coverage parameters into Service Invoice calculation (Stage 9) (`DEP-011`).
- **11. Audit & Security:** All warranty extensions, policy overrides, and voiding actions logged to immutable audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Automated notifications dispatched to customer 30/60 days prior to warranty/contract expiration.
  - `[PROPOSED / Subject to OQ-003]` Management approval required to grant goodwill warranty coverage for expired assets.
- **13. Documents & Attachments:** Signed service contract agreements, warranty certificates, terms and conditions documents (`FR-DMS-001`).
- **14. Cancellation & Termination:** Early contract termination calculates pro-rata credit or unearned revenue reversal based on configured accounting policy (`TBD`).
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Ambiguous warranty status flags request for manual entitlement review by the warranty administrator.
- **16. Reporting & KPI Implications:** Active warranty coverage ratios, warranty claim cost per asset model, contract renewal rates (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System calculates and displays active warranty and contract coverage status for any installed asset based on its commissioning date and contract terms.
  - System identifies whether requested service activities and replacement parts fall under active warranty entitlement or require customer commercial billing.

---

### Stage 4: Service Request (Customer Incident & Triage)
- **Requirement ID:** `DR-A2S-004`
- **Phase 0A Baseline ID:** `FR-MFS-004` (Breakdown Maintenance), `FR-MFS-007` (Field Service)
- **Module:** Maintenance & Field Service | **Sub-Module:** Service Intake & Incident Triage
- **BRD Source:** BRD §6.1, §6.3, §7.14; FR-MFS-004, FR-MFS-007; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage in BRD §6.1)
- **1. Purpose & Objective:** Capture after-sales service requests, machine breakdown reports, and maintenance calls from customers, link them to the specific installed asset, triage symptoms, and evaluate warranty entitlement.
- **2. Actors & Roles:** Customer Support Representative, Service Helpdesk Engineer, Service Dispatcher, Customer Contact.
- **3. Preconditions:** Customer Master active; Installed Asset record exists (Stage 1) or un-cataloged serial intake permitted under exception.
- **4. Inputs:** Request timestamp, Customer reference, Installed Asset / Serial No, Problem description, Fault symptom code, Urgency/Priority indicator, Contact details, Site access constraints.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Logs customer service requests and breakdown incidents (`FR-MFS-004`).
  - `[BRD-REQUIRED]` Associates the incident directly with the specific installed asset and operating site (`FR-AST-003`).
  - `[BRD-DERIVED]` Evaluates active warranty / AMC entitlement from Stage 3, displaying coverage status to the service intake agent.
  - `[BRD-DERIVED]` Reviews prior asset maintenance history (Stage 11) to identify recurring faults or recent repairs.
  - `[BRD-DERIVED]` Converts qualified service incidents into downstream Technician Assignment (Stage 5) and Field Service Work Orders (Stage 7).
- **6. Business Rules:**
  - `[DEC-010 Alignment Rule]` Service Request in A2S represents field-maintenance and operational machine dispatch (`FR-MFS-004`, `FR-MFS-007`). Customer Service Helpdesk module (`FR-CSVC-001–005`) remains decoupled unless explicitly mapped.
  - `[PROPOSED / Reference Baseline]` Duplicate Check Rule: System warns if an open, unresolved service request already exists for the same installed asset.
  - `[PROPOSED Policy / TBD]` Service SLA Windows: Incident response and resolution time targets are configurable parameters based on customer contract tier (`TBD`).
- **7. Validations:** Problem description is mandatory; asset reference must correspond to an active installed asset owned by or leased to the customer.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Request Lifecycle (`PROPOSED`):* `Logged / Open` → `Triaged` → `Dispatched / Scheduled` → `Work In Progress` → `Resolved` → `Closed` (or `Cancelled`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext uses `Issue` (`support/doctype/issue/`) or `Warranty Claim` (`support/doctype/warranty_claim/`). `Issue` has basic SLA clocks (`service_level_agreement.py`) and customer links.
  - *Architectural Gap (Doc 21 §WF-17, Doc 22 §3.3):* ERPNext `Issue` is a generic support ticket decoupled from field technician dispatching and asset telemetry. It does not natively bridge to field maintenance execution.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA's Service Request natively bridges customer incident logging to field service work order generation, spare parts staging, and asset telemetry logging (`FR-MFS-004`, `FR-MFS-007`).
- **10. Cross-Module Handoffs:** Feeds incident details to Technician Assignment (Stage 5) and Field Service Work Order (Stage 7) (`DEP-011`).
- **11. Audit & Security:** All communication logs, severity changes, and status transitions recorded in audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Immediate ticket receipt confirmation sent to customer via SMS/Email.
- **13. Documents & Attachments:** Customer fault photos, error log files, alarm printouts (`FR-DMS-001`).
- **14. Cancellation & Closure:** Requests closed without on-site visit require customer confirmation of remote fault resolution.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Unregistered asset reported by customer routes to asset onboarding exception queue for rapid validation.
- **16. Reporting & KPI Implications:** Service response/acknowledgement time, Mean Time to Repair (MTTR), service request volume by fault category, first-contact resolution rate (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System captures service request with symptom description and links it directly to the designated installed asset.
  - System displays active warranty coverage status for the asset and permits generation of a field dispatch task.

---

### Stage 5: Technician Assignment & Dispatch
- **Requirement ID:** `DR-A2S-005`
- **Phase 0A Baseline ID:** `FR-MFS-007` (Field Service), `FR-MFS-001` (Maintenance Planning)
- **Module:** Maintenance & Field Service | **Sub-Module:** Resource Scheduling & Field Dispatch
- **BRD Source:** BRD §6.1, §6.3, §7.14; FR-MFS-007; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage in BRD §6.1)
- **1. Purpose & Objective:** Assign qualified service technicians or field engineering teams to approved service requests based on geographical territory, technical skills, and schedule availability, dispatching them to the customer site.
- **2. Actors & Roles:** Service Dispatcher, Field Service Supervisor, Field Service Technician.
- **3. Preconditions:** Service Request triaged and approved for on-site dispatch (Stage 4); Technician profiles and territories configured.
- **4. Inputs:** Service Request reference, Asset technical model, Customer site location/GPS coordinates, Required technical competencies, Scheduled appointment date/time slot, Assigned technician identifier.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages field service technician dispatching and service assignments (`FR-MFS-007`).
  - `[PROPOSED / Candidate Mechanics]` Filters candidate technicians by service territory, required equipment skill certifications, and current calendar availability.
  - `[BRD-DERIVED]` Dispatches assignment details to the technician's mobile application (`FR-MOB-002`), including site address, contact person, asset history, and reported symptoms.
  - `[PROPOSED / Reference Baseline]` Supports reassignment and rescheduling in response to emergency breakdown escalations.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline Policy]` Competency Gating: Regulated or hazardous equipment maintenance must only be assigned to technicians holding active safety and skill certifications.
  - `[PROPOSED Policy / TBD]` Dispatch Optimization: Automated route sequencing, travel distance optimization, and dynamic GPS proximity dispatching are candidate enhancements governed by field service policy (`TBD / OQ-013`).
- **7. Validations:** Scheduled dispatch window must be future-dated; assigned technician must have active employment/contractor status.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Dispatch Status (`PROPOSED`):* `Unassigned` → `Assigned` → `Dispatched / En Route` → `On Site` → `Work Started` (or `Reassigned` / `Rescheduled`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext `Maintenance Visit` (`maintenance/doctype/maintenance_visit/`) has a simple `assigned_to` user field.
  - *Architectural Gap (Doc 21 §WF-16, Doc 22 §3.3):* ERPNext lacks skills-based matching, technician calendar scheduling, territory dispatching, GPS route guidance, and mobile field service dispatch workflows.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA provides dedicated Field Service resource scheduling and mobile technician dispatching (`FR-MFS-007`, `FR-MOB-002`).
- **10. Cross-Module Handoffs:** Establishes labor assignee for Field Service Work Order (Stage 7); reserves field technician calendar (`DEP-011`).
- **11. Audit & Security:** Technician assignment changes, dispatch timestamps, and mobile status updates logged in audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[BRD-DERIVED]` Mobile push notification and work order pack dispatched to assigned technician (`FR-MOB-002`).
  - `[PROPOSED / Subject to OQ-004]` Appointment arrival window alert transmitted to customer contact.
- **13. Documents & Attachments:** Site access permits, health & safety protocols, route directions (`FR-DMS-001`).
- **14. Cancellation & Reassignment:** Reassignment reopens schedule slot for original technician and triggers schedule updates to customer.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Technician unavailability or delay alerts the dispatcher to reassign or notify customer of revised ETA.
- **16. Reporting & KPI Implications:** Dispatch response time, technician utilization rates, schedule adherence, travel-to-work ratios (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System assigns an active technician to a service incident and dispatches work order details to their mobile service profile.
  - System records dispatch progression timestamps (Assigned, En Route, On Site).

---

### Stage 6: Spare Parts & Service Materials Management
- **Requirement ID:** `DR-A2S-006`
- **Phase 0A Baseline ID:** `FR-MFS-005` (Spare Parts Management), `FR-INV-001` (Inventory Master & Stock Tracking)
- **Module:** Maintenance & Field Service / Inventory | **Sub-Module:** Field Spares & Truck Stock
- **BRD Source:** BRD §6.1, §6.3, §7.8, §7.14; FR-MFS-005, FR-INV-001; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage & Inventory Seam)
- **1. Purpose & Objective:** Identify required replacement components, verify stock availability across central warehouses or mobile van stock (truck stock), stage/reserve parts for service, track field consumption, and handle return of unused or defective parts.
- **2. Actors & Roles:** Field Service Technician, Warehouse Parts Clerk, Service Planner.
- **3. Preconditions:** Item Master active with spare parts flagged; Service Work Order created (Stage 7) or Incident triaged (Stage 4); Warehouse/Van stock locations configured.
- **4. Inputs:** Asset reference, Item Master spare parts list, Required quantities, Source warehouse / Mobile van location, Defective part return flag, Warranty entitlement flag.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages spare parts inventory and service materials allocation (`FR-MFS-005`).
  - `[BRD-DERIVED]` Queries real-time stock balances across regional service warehouses and technician mobile truck stock (`FR-INV-001`).
  - `[PROPOSED / Reference Baseline]` Reserves required spare parts against the service incident to prevent stock exhaustion.
  - `[BRD-DERIVED]` Records spare parts consumption against the Field Service Work Order, updating Stock Ledger balances (`DR-C2C-007 / EWF-02`).
  - `[BRD-DERIVED]` Tracks replacement of serialized/batched components, updating the Installed Asset's configuration records (Stage 1).
  - `[PROPOSED / Reference Baseline]` Logs return of unused good parts to stock and routes removed defective parts to quality quarantine or vendor warranty return.
- **6. Business Rules:**
  - `[BRD-REQUIRED / Unified Item Master DEC-007]` Spare parts must utilize the unified Item Master (`FR-INV-001`); independent service parts catalogs are prohibited.
  - `[BRD-DERIVED / Accounting Integrity]` Spare parts consumption generates inventory reduction entries in the Stock Ledger; commercial valuation and COGS vs warranty expense posting is governed by warranty entitlement (`Stage 3 / DEP-005`).
  - `[PROPOSED Policy / TBD]` Mobile Truck Stock Replenishment: Automated min-max reordering for mobile technician van stock is a configurable operational policy (`TBD`).
- **7. Validations:** Consumed quantity cannot exceed available stock in the issuing warehouse/van location; serialized spare parts require valid serial number entry.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Material Reservation Status (`PROPOSED`):* `Draft / Requested` → `Reserved` → `Issued / Staged` → `Consumed in Field` (or `Returned to Stock`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext uses `Stock Entry` (Material Transfer / Material Issue) to move items. `Maintenance Visit Purpose` has an item table listing items inspected or replaced.
  - *Architectural Gap (Doc 21 §WF-16, Doc 22 §3.3):* ERPNext Maintenance Visit does NOT natively execute mobile truck-stock replenishment or automated Stock Ledger Entry (SLE) consumption from field technician mobile devices. Parts logging in Maintenance Visit is disconnected from live stock decrement unless manual Stock Entries are submitted.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA natively couples Field Service Work Orders to mobile stock issuance, truck-stock consumption, and reverse logistics for defective cores (`FR-MFS-005`, `FR-INV-001`).
- **10. Cross-Module Handoffs:** Issues parts to Field Service Work Order (Stage 7); posts inventory cost and consumption to Stock Ledger (`DEP-002`, `DEP-005`); provides billable parts lines to Service Invoice (Stage 9).
- **11. Audit & Security:** All parts movements, technician truck-stock transfers, and serial adjustments logged in immutable inventory audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Low stock warning triggered when critical spare part falls below reorder threshold.
- **13. Documents & Attachments:** Material transfer dockets, defective core tags, parts delivery receipts (`FR-DMS-001`).
- **14. Cancellation & Restocking:** Cancelled service work unwinds parts reservations and returns issued items to available stock.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Stock shortage triggers emergency inter-branch transfer or purchase requisition (`DR-P2P-002`).
- **16. Reporting & KPI Implications:** Spare parts consumption rate, truck-stock inventory turn, parts availability percentage at first visit (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System checks and displays spare parts stock availability across target warehouse or van locations.
  - Logging parts consumption against a service order updates stock balances and flags billable vs warranty treatment.

---

### Stage 7: Field Service / Maintenance Work Order Execution
- **Requirement ID:** `DR-A2S-007`
- **Phase 0A Baseline ID:** `FR-MFS-002` (Work Orders), `FR-MFS-007` (Field Service)
- **Module:** Maintenance & Field Service | **Sub-Module:** Field Execution & Job Tracking
- **BRD Source:** BRD §6.1, §6.3, §7.14; FR-MFS-002, FR-MFS-007; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage & Critical Architectural Seam)
- **1. Purpose & Objective:** Authorize, execute, and record on-site field maintenance or workshop repair activities, tracking technician labor hours, travel time, work performed, checklist compliance, spare parts consumed, and customer formal sign-off.
- **2. Actors & Roles:** Field Service Technician, Service Supervisor, Customer Site Manager.
- **3. Preconditions:** Service Request triaged (Stage 4); Technician assigned (Stage 5); Spare parts staged or verified (Stage 6).
- **4. Inputs:** Work Order ID, Service Request reference, Asset identifier, Assigned technician, Planned work start/end, Standard operating procedures (SOP), Actual labor hours, Travel hours, Checklist tasks, Findings/Action notes, Customer signature.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Generates and manages Maintenance & Field Service Work Orders (`FR-MFS-002`).
  - `[BRD-REQUIRED]` Manages on-site field service execution, technician tracking, and job completion (`FR-MFS-007`).
  - `[BRD-DERIVED]` Captures actual labor hours and technician travel time via mobile timesheet logging (`FR-MOB-002`).
  - `[BRD-DERIVED]` Records consumed spare parts and replaces sub-assembly serial numbers on the installed asset (Stage 1).
  - `[PROPOSED / Business Workflow]` Enforces completion of step-by-step technical safety checklists and machine operating parameter captures (voltage, pressure, temperature).
  - `[BRD-DERIVED]` Captures digital customer acknowledgement (electronic signature and satisfaction rating) upon job completion.
- **6. Business Rules:**
  - `[CRITICAL ARCHITECTURAL SEAM / Collision Prevention]` **Service Work Order Isolation Rule:** The Field Service Work Order entity (`FR-MFS-002`) is strictly an operational maintenance and field service execution document. It must **never** be conflated with the Discrete Manufacturing Work Order (`DR-C2C-009`, `FR-MFG-002`), which is strictly dedicated to factory BOM assembly.
  - `[BRD-DERIVED / Entitlement Application]` Labor and spare parts line items on the service work order are tagged with entitlement indicators (`Warranty Covered`, `Contract Covered`, `Billable to Customer`) inherited from Stage 3.
  - `[PROPOSED / Reference Baseline]` Closure Sign-Off Rule: Work order cannot transition to `Completed` without captured customer sign-off or recorded supervisor exception waiver.
- **7. Validations:** Actual end timestamp must be greater than start timestamp; labor hours must be greater than zero; mandatory checklist steps must be recorded.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Work Order Status (`PROPOSED`):* `Scheduled` → `In Progress` → `Pending Parts / On Hold` → `Work Complete` → `Customer Signed Off` → `Closed` (or `Cancelled`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext uses `Maintenance Visit` (`maintenance/doctype/maintenance_visit/`) for customer equipment and `Asset Repair` (`assets/doctype/asset_repair/`) for internal assets. In ERPNext, `Work Order` belongs strictly to *Manufacturing* (`manufacturing/doctype/work_order/`) (Doc 21 §WF-09).
  - *Critical Architectural Distinction (Doc 21 §WF-16, Doc 22 §3.3, Doc 23 §36):* Attempting to reuse ERPNext's manufacturing `Work Order` for field service corrupts discrete production logic.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA establishes a dedicated, first-class `Field Service Work Order` entity (`FR-MFS-002`, `FR-MFS-007`) tailored for mobile execution, technician labor, and field parts replacement.
- **10. Cross-Module Handoffs:** Feeds completed labor and parts to Service Invoice (Stage 9); updates Asset History (Stage 11); decrements inventory balances via Stock Ledger (Stage 6) (`DEP-002`, `DEP-005`, `DEP-011`).
- **11. Audit & Security:** GPS capture of arrival/departure, technician mobile timestamp logs, and customer digital signatures preserved in audit trail (`FR-PADM-1.8.2`, `FR-MOB-002`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Work completion summary report and signed service report automatically emailed to customer.
- **13. Documents & Attachments:** Signed Field Service Report (FSR), before/after equipment photos, vibration/thermal test readings (`FR-DMS-001`).
- **14. Cancellation & Incomplete Work:** If work cannot be completed, work order is placed `On Hold - Awaiting Parts` or rescheduled, retaining logged hours.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Discovery of secondary catastrophic machine damage generates a supplementary work order and alerts the service coordinator.
- **16. Reporting & KPI Implications:** First-Time Fix Rate (FTFR), Mean Time to Repair (MTTR), labor productivity, field service profitability (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System creates a dedicated Field Service Work Order tracking technician labor, activities performed, parts consumed, and customer sign-off.
  - Entity is architecturally distinct from factory manufacturing work orders.

---

### Stage 8: Maintenance Execution (Preventive & Corrective)
- **Requirement ID:** `DR-A2S-008`
- **Phase 0A Baseline ID:** `FR-MFS-003` (Preventive Maintenance), `FR-MFS-004` (Breakdown Maintenance)
- **Module:** Maintenance & Field Service | **Sub-Module:** Maintenance Programs & Calibration
- **BRD Source:** BRD §6.1, §6.3, §7.14; FR-MFS-003, FR-MFS-004; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage in BRD §6.1)
- **1. Purpose & Objective:** Schedule, trigger, and govern recurring preventive maintenance programs, condition-based servicing, safety calibrations, and corrective breakdown repairs across the installed asset base.
- **2. Actors & Roles:** Maintenance Planner, Reliability Engineer, Field Service Supervisor.
- **3. Preconditions:** Installed Asset operational (Stage 1); Maintenance plans or breakdown events established.
- **4. Inputs:** Asset reference, Maintenance schedule template, Trigger rules (calendar interval, operating hours, run cycles), Maintenance tasks/checklists, Service contract linkage.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages scheduled preventive maintenance programs (`FR-MFS-003`).
  - `[BRD-REQUIRED]` Manages unscheduled breakdown and corrective maintenance activities (`FR-MFS-004`).
  - `[PROPOSED / Reference Baseline]` Automatically generates upcoming maintenance visits or work orders based on configured calendar recurrence (e.g. monthly, quarterly, annual).
  - `[PROPOSED / Differentiator]` Ingests machine operating hours or IoT run-cycle counters to trigger usage-based maintenance tasks (`FR-AST-003`).
  - `[BRD-DERIVED]` Records findings, component wear measurements, and replacement recommendations post-maintenance.
  - `[BRD-DERIVED]` Automatically reschedules next preventive maintenance due date upon completion of current maintenance cycle.
- **6. Business Rules:**
  - `[BRD-REQUIRED / FR-MFS-003]` Preventive Maintenance Policy: Preventive maintenance tasks must execute according to configured asset service schedules.
  - `[PROPOSED Policy / TBD]` Maintenance Tolerance Windows: Execution buffer days (e.g. +/- 5 days around due date) before flagging asset maintenance as overdue are governed by tenant policy (`TBD`).
- **7. Validations:** Maintenance schedule must define at least one valid task frequency or run-threshold; target asset must be in active operating status.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Program Status (`PROPOSED`):* `Scheduled` → `Due` → `Overdue` → `Work Order Generated` → `Completed` (or `Skipped / Deferred`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext provides `Maintenance Schedule` (`maintenance/doctype/maintenance_schedule/`) for customer AMC visits and `Asset Maintenance` (`assets/doctype/asset_maintenance/`) for internal fixed assets.
  - *Architectural Gap (Doc 21 §WF-16, Doc 22 §3.3):* ERPNext's customer maintenance schedule generates static visit rows based strictly on calendar days. It lacks dynamic condition-based triggering, IoT counter integration, and predictive maintenance capabilities.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA unifies preventive and breakdown maintenance execution, supporting both calendar-based and usage/condition-based maintenance triggers linked to customer installed equipment (`FR-MFS-003`, `FR-MFS-004`).
- **10. Cross-Module Handoffs:** Triggers Field Service Work Orders (Stage 7); updates Asset History (Stage 11); adjusts asset reliability scores (`DEP-011`).
- **11. Audit & Security:** All schedule modifications, deferred maintenance approvals, and completion logs recorded in audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Advance reminders sent to customer and service dispatcher 7 days prior to preventive maintenance due date.
  - `[PROPOSED / Subject to OQ-003]` Deferral of safety-critical preventive maintenance requires formal service manager approval.
- **13. Documents & Attachments:** Calibration certificates, lubricant analysis reports, statutory safety compliance forms (`FR-DMS-001`).
- **14. Cancellation & Deferral:** Deferring a maintenance cycle requires recorded justification and sets a mandatory revised target date.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Overdue maintenance triggers alert badges on customer 360 view and installed asset dashboard.
- **16. Reporting & KPI Implications:** Preventive Maintenance Compliance (PMC) percentage, breakdown vs preventive ratio, MTBF, asset health index (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System schedules and tracks recurring preventive maintenance tasks for installed assets.
  - Completing a maintenance task records the execution history and calculates the next scheduled maintenance date.

---

### Stage 9: Service Invoicing & Billing
- **Requirement ID:** `DR-A2S-009`
- **Phase 0A Baseline ID:** `FR-MFS-006` (Service Contracts), `FR-ACC-002` (Invoicing & Billing), `FR-TAX-001` (Tax Engine)
- **Module:** Finance & Accounting / Maintenance | **Sub-Module:** Service Billing & Accounts Receivable
- **BRD Source:** BRD §6.1, §6.3, §7.14, §7.17, §7.18; FR-MFS-006, FR-ACC-002, FR-TAX-001; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Core Financial Flow Stage)
- **1. Purpose & Objective:** Formulate and issue commercial Service Invoices to customers for billable field services, technician labor hours, travel charges, and non-warranty replacement parts, applying statutory taxes and booking Accounts Receivable.
- **2. Actors & Roles:** Billing Specialist, Finance Controller, Field Service Supervisor.
- **3. Preconditions:** Field Service Work Order completed and customer signed-off (Stage 7); Warranty entitlements verified (Stage 3); Chart of Accounts and Tax templates configured (`DEC-007`).
- **4. Inputs:** Work Order reference, Customer billing account, Billable labor hours and rates, Billable spare parts quantities and unit prices, Travel/ancillary charges, Warranty deduction lines, Applicable statutory tax template.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Generates commercial customer invoices for completed service activities (`FR-ACC-002`).
  - `[BRD-REQUIRED]` Distinguishes between warranty-covered activities (billed at zero rate or absorbed by warranty provision) and customer-billable line items (`FR-MFS-006`).
  - `[BRD-REQUIRED]` Invokes the Global Tax Engine (`FR-TAX-001`, `DR-C2C-014`) to compute applicable statutory GST/VAT on service labor and spare parts.
  - `[BRD-DERIVED]` Posts double-entry accounting records upon invoice submission: debits Customer Accounts Receivable, credits Service Revenue (labor) and Spare Parts Revenue (materials), and credits Statutory Tax Liability (`DEP-005`, `DEP-008`).
  - `[BRD-DERIVED]` Updates billing reference on source Field Service Work Order and Service Request.
- **6. Business Rules:**
  - `[UNIFIED FINANCE GOVERNANCE RULE]` **Invoicing Consistency Rule:** Service Invoicing must strictly utilize the platform's unified Sales/Commercial Invoicing engine and Chart of Accounts (`FR-ACC-002`, `DEC-007`). Creating an isolated, independent billing model for service is prohibited.
  - `[BRD-REQUIRED / Tax Determination]` Tax determination on service labor and physical spare parts must execute via the Global Tax Engine based on customer state/jurisdiction and SAC/HSN codes (`FR-TAX-001`).
  - `[PROPOSED Policy / TBD]` Fixed-Fee vs Time-and-Materials: System supports both fixed contract call-out pricing and actual time-and-materials billing based on service contract configuration (`TBD`).
- **7. Validations:** Customer must have an active billing account; billable totals must be non-negative; invoice date must fall within an open financial fiscal period.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Invoice Status (`PROPOSED`):* `Draft` → `Pending Approval` → `Issued / Unpaid` → `Partially Paid` → `Paid / Settled` (or `Cancelled / Credited`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* In ERPNext, billing service work requires creating a standard `Sales Invoice` manually from a `Maintenance Visit` or linking a `Timesheet` (`projects/doctype/timesheet/`) (`EWF-12`).
  - *Architectural Gap (Doc 21 §WF-03, Doc 22 §3.3):* ERPNext lacks automated service billing logic that aggregates warranty-exempt parts, billable labor hours, and travel allowances from a single field service work order into a consolidated invoice.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA provides consolidated service billing rules that seamlessly parse Field Service Work Order lines, verify warranty coverage exemptions, apply statutory tax codes, and generate Accounts Receivable postings (`FR-MFS-006`, `FR-ACC-002`).
- **10. Cross-Module Handoffs:** Generates Accounts Receivable ledger entry (Stage 10); feeds service revenue metrics into BI & EPM (`DEP-005`, `DEP-008`).
- **11. Audit & Security:** All invoice creation, discount overrides, and credit adjustments logged in immutable financial audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Digital invoice transmitted to customer billing email with online payment link.
  - `[PROPOSED / Subject to OQ-003]` Invoice credit notes or disputed amount write-offs require financial controller approval.
- **13. Documents & Attachments:** Service Invoice PDF, attached signed Field Service Report (FSR), parts replacement breakdown (`FR-DMS-001`).
- **14. Cancellation & Credit:** Voiding or cancelling a service invoice requires issuing a formal Credit Note, reversing GL entries and reopening the work order for re-billing.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Disputed service charges place the invoice on `Billing Hold` pending service manager resolution.
- **16. Reporting & KPI Implications:** Days Sales Outstanding (DSO) for service, service billing realization rate, warranty absorption cost (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System generates a service invoice from a completed work order, accurately separating billable items from warranty-covered items.
  - Submitting the invoice posts Accounts Receivable and revenue entries to the General Ledger and calculates applicable statutory taxes.

---

### Stage 10: Customer Payment Collection & GL Settlement
- **Requirement ID:** `DR-A2S-010`
- **Phase 0A Baseline ID:** `FR-ACC-004` (Payments & Bank Reconciliation), `FR-ACC-001` (General Ledger)
- **Module:** Finance & Accounting | **Sub-Module:** Cash Receipts & AR Settlement
- **BRD Source:** BRD §6.1, §6.3, §7.17; FR-ACC-004, FR-ACC-001; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Core Financial Flow Stage)
- **1. Purpose & Objective:** Process customer payment collections against outstanding service invoices, reconcile bank receipts, manage partial payments or advances, and settle Accounts Receivable balances in the General Ledger.
- **2. Actors & Roles:** Accounts Receivable Specialist, Cashier, Finance Controller.
- **3. Preconditions:** Service Invoice issued (Stage 9); Customer remittance or electronic payment received; Corporate bank accounts active (`DEC-007`).
- **4. Inputs:** Payment voucher reference, Customer link, Payment date, Remittance amount, Payment instrument / mode (NEFT/RTGS, Credit Card, Electronic Gateway, Check), Target bank account, Allocated invoice references.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Records customer payments and settles outstanding service invoices (`FR-ACC-004`).
  - `[BRD-REQUIRED]` Posts double-entry general ledger settlement: debits Bank/Cash account and credits Customer Accounts Receivable (`FR-ACC-001`).
  - `[BRD-DERIVED]` Supports partial payments, advance payment allocations, and multi-invoice settlement.
  - `[BRD-DERIVED]` Updates `outstanding_amount` and marks invoice as `Paid` upon full settlement (`DR-C2C-015`).
  - `[PROPOSED / Reference Baseline]` Reconciles electronic payment gateway transactions against corporate bank statements (`FR-ACC-004`).
- **6. Business Rules:**
  - `[UNIFIED FINANCIAL MODEL RULE]` **Shared Payment Engine:** Payment processing for Asset-to-Service must strictly reuse the unified platform Payment Entry mechanism established in Customer-to-Cash (`DR-C2C-015`, `EWF-04`). Creating an independent payment engine for service is prohibited.
  - `[PROPOSED / Reference Baseline]` Unallocated Receipts: Payments received without invoice allocation remain as unallocated customer advance balances on the ledger until manually matched.
- **7. Validations:** Payment amount must be greater than zero; allocated payment cannot exceed the total outstanding balance of target invoices; payment date must fall in an open fiscal period.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Payment Status (`PROPOSED`):* `Draft` → `Payment Received` → `Cleared / Reconciled` (or `Rejected / Bounced` / `Reversed`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Payment Entry` (`accounts/doctype/payment_entry/`) (`EWF-04`) handles receipts, invoice reconciliation, exchange rate adjustments, and GL ledger updates.
  - *Adoption Assessment:* Core payment entry structure, bank allocation, and AR clearing mechanisms are directly adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Core Requirement:* Unification of payment transactions across commercial sales and after-sales service billing (`DEC-007`).
- **10. Cross-Module Handoffs:** Clears AR balance in General Ledger; updates customer credit profile in Customer 360 (`DEP-005`, `DEP-008`).
- **11. Audit & Security:** All payment receipts, bank clearing timestamps, and transaction reversals logged in immutable financial audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Payment acknowledgement receipt automatically dispatched to customer upon settlement.
- **13. Documents & Attachments:** Bank advice slips, payment gateway settlement receipts, check scans (`FR-DMS-001`).
- **14. Cancellation & Reversal:** Payment cancellation voids GL entries, restores outstanding balance on the service invoice, and updates customer ledger.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Bounced checks or failed gateway settlements trigger immediate reversal of provisional AR settlement and flag customer account.
- **16. Reporting & KPI Implications:** Cash collection efficiency, service overdue AR aging, payment method breakdown (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System captures payment against a service invoice, reducing the outstanding balance and posting debit to bank and credit to accounts receivable.
  - Payment model operates seamlessly using the unified platform payment engine.

---

### Stage 11: Asset History & Lifecycle Intelligence
- **Requirement ID:** `DR-A2S-011`
- **Phase 0A Baseline ID:** `FR-AST-006` (Asset Lifecycle), `FR-AST-007` (Asset Analytics)
- **Module:** Asset Management / BI | **Sub-Module:** 360-Degree Asset Timeline & Reliability Analytics
- **BRD Source:** BRD §6.1, §6.3, §7.13, §7.22; FR-AST-006, FR-AST-007; Business Flows §3
- **Stage Classification:** `BRD-REQUIRED` (Core Flow Destination & Analytics Closure)
- **1. Purpose & Objective:** Aggregate, synthesize, and present a complete, tamper-evident chronological lifecycle timeline of every installed asset—spanning installation, warranty events, service calls, technician visits, parts replacements, service costs, and operating downtime.
- **2. Actors & Roles:** Reliability Engineer, Head of Field Service, Product Quality Manager, Asset Owner / Customer.
- **3. Preconditions:** Installed Asset record active (Stage 1); historical transactional events generated across Stages 2–10.
- **4. Inputs:** Asset identifier, Serial Number, Chronological event stream (Installation, Warranties, Service Requests, Work Orders, Maintenance Inspections, Spare Parts, Invoices, Payments).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Tracks end-to-end asset lifecycle from commissioning through retirement (`FR-AST-006`).
  - `[BRD-REQUIRED]` Generates comprehensive asset intelligence and operational analytics (`FR-AST-007`).
  - `[BRD-DERIVED]` Synthesizes an interactive 360-degree chronological timeline detailing all lifecycle milestones for the asset.
  - `[BRD-DERIVED]` Computes lifetime maintenance spend (parts + labor costs) vs. initial purchase price to track Total Cost of Ownership (TCO).
  - `[PROPOSED / Differentiator]` Computes standard equipment reliability metrics: Mean Time Between Failures (MTBF), Mean Time to Repair (MTTR), and Availability Index.
  - `[PROPOSED / Feedback Loop]` Feeds asset failure rates and component defect data back to Manufacturing Quality (`FR-QLTY-002`) and R&D for engineering continuous improvement.
- **6. Business Rules:**
  - `[BRD-REQUIRED / DEC-007]` Lifecycle Integrity Rule: The asset timeline is an immutable chronological record derived directly from approved operational transactions; manual retroactive manipulation is prohibited.
  - `[PROPOSED Policy / TBD]` Reliability Calculation Windows: MTBF/MTTR metrics are calculated across configurable rolling timeframes (e.g. 12 months, lifetime) per industry standard (`TBD`).
- **7. Validations:** Asset record must exist; event chronology is preserved based on recorded transaction/event business timestamps, ensuring that delayed data entry or approved historical onboarding records do not invalidate historical sequence while maintaining full auditability.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Asset Health State (`PROPOSED`):* `Optimal` → `Normal Wear` → `Attention Required / High Failure Rate` → `End of Economic Life` (or `Retired / Archived`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext provides an `Asset` dashboard showing depreciation GL entries and repairs for internal assets, and a `Serial No` status history log for serialized items.
  - *Architectural Gap (Doc 21 §WF-15, Doc 22 §3.3):* ERPNext lacks a unified customer equipment health dashboard that integrates warranty entitlements, field service visits, spare parts consumption, and automated reliability calculations (MTBF/MTTR).
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA establishes a dedicated Asset Lifecycle Intelligence hub (`FR-AST-006`, `FR-AST-007`) that consolidates full after-sales service history, component degradation trends, and field reliability analytics into an actionable 360-degree view.
- **10. Cross-Module Handoffs:** Feeds asset reliability metrics into BI & EPM (`DEP-009`); provides component failure intelligence to Manufacturing & Quality (`DEP-004`).
- **11. Audit & Security:** All timeline queries, export actions, and health score adjustments logged in audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Automated alert dispatched to account manager when an asset's cumulative maintenance cost exceeds configured replacement threshold (e.g. 60% of asset value).
- **13. Documents & Attachments:** Historical service reports, warranty certificates, calibration audit trails, engineering change notices (`FR-DMS-001`).
- **14. Cancellation & Archival:** Retired or scrapped assets retain permanent searchable read-only history for legal and compliance audit.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Inconsistent operational data (e.g. missing work order dates) flags data integrity review on the asset record.
- **16. Reporting & KPI Implications:** Asset availability rate, Total Cost of Ownership (TCO), fleet failure Pareto analysis, warranty recovery ratio (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System renders an integrated, chronological lifecycle timeline for any designated installed asset, displaying all historical installations, service requests, work orders, parts consumed, and financial invoices.
  - System aggregates operational downtime and maintenance expenditures to report on equipment health and reliability metrics.

---

## 4. Traceability & Classification Summary Matrix

| Req ID | A2S Stage | Baseline ID | Module | Primary Stage Classification | Explicit KIYA Differentiators & Candidate Enhancements | Dependency | Current Status |
|---|---|---|---|---|---|---|---|
| **DR-A2S-001** | Stage 1: Asset / Installed Base | `FR-AST-001` / `AST-003` | Asset Mgmt | `BRD-REQUIRED` | **Dedicated Customer Installed Base Entity** (`BRD-REQUIRED / Architectural Seam`); Parent-child asset hierarchy (`PROPOSED`) | `DEP-011` | Cleaned Baseline |
| **DR-A2S-002** | Stage 2: Installation & Commissioning | `FR-MFS-001` / `MFS-007` | Field Service | `BRD-REQUIRED` | Commissioning handover & digital SAT checklists (`BRD-REQUIRED`); Dynamic warranty trigger (`BRD-DERIVED`) | `DEP-011` | Cleaned Baseline |
| **DR-A2S-003** | Stage 3: Warranty & Contracts | `FR-AST-003` / `MFS-006` | Asset / Service | `BRD-REQUIRED` | **Dynamic Entitlement Engine** (`BRD-REQUIRED`); Multi-tier coverage validation (`PROPOSED / TBD`) | `DEP-011` | Cleaned Baseline |
| **DR-A2S-004** | Stage 4: Service Request | `FR-MFS-004` / `MFS-007` | Field Service | `BRD-REQUIRED` | Asset-linked service incident intake (`BRD-REQUIRED`); SLA priority clocks (`ERP-REFERENCE / TBD`) | `DEP-011` | Cleaned Baseline |
| **DR-A2S-005** | Stage 5: Technician Dispatch | `FR-MFS-007` / `MOB-002` | Field Service | `BRD-REQUIRED` | **Mobile Technician Dispatching** (`BRD-REQUIRED`); Skills/territory matching & GPS routing (`PROPOSED`) | `DEP-011` | Cleaned Baseline |
| **DR-A2S-006** | Stage 6: Spare Parts | `FR-MFS-005` / `INV-001` | Service / Inv | `BRD-REQUIRED` | **Unified Spares & Truck-Stock Consumption** (`BRD-REQUIRED`); Defective core reverse logistics (`PROPOSED`) | `DEP-002`, `DEP-005` | Cleaned Baseline |
| **DR-A2S-007** | Stage 7: Service Work Order | `FR-MFS-002` / `MFS-007` | Field Service | `BRD-REQUIRED` | **Dedicated Field Service Work Order** (`BRD-REQUIRED / Collision Resolution`); Customer mobile sign-off (`BRD-DERIVED`) | `DEP-002`, `DEP-011` | Cleaned Baseline |
| **DR-A2S-008** | Stage 8: Maintenance Execution | `FR-MFS-003` / `MFS-004` | Field Service | `BRD-REQUIRED` | Calendar & Usage-based preventive maintenance (`BRD-REQUIRED`); IoT run-cycle counters (`PROPOSED`) | `DEP-011` | Cleaned Baseline |
| **DR-A2S-009** | Stage 9: Service Invoice | `FR-ACC-002` / `MFS-006` | Finance / Tax | `BRD-REQUIRED` | **Consolidated Service Billing** (`BRD-REQUIRED`); Warranty vs billable split & Global Tax engine (`BRD-REQUIRED`) | `DEP-005`, `DEP-008` | Cleaned Baseline |
| **DR-A2S-010** | Stage 10: Payment Settlement | `FR-ACC-004` / `ACC-001` | Finance & Acct | `BRD-REQUIRED` | Unified payment collection & AR settlement (`BRD-REQUIRED`); Multi-channel electronic gateway (`ERP-REFERENCE`) | `DEP-005`, `DEP-008` | Cleaned Baseline |
| **DR-A2S-011** | Stage 11: Asset History | `FR-AST-006` / `AST-007` | Asset / BI | `BRD-REQUIRED` | **360-Degree Asset Lifecycle Intelligence Hub** (`BRD-REQUIRED`); Automated MTBF/MTTR calculation (`PROPOSED`) | `DEP-004`, `DEP-009` | Cleaned Baseline |

---

## 5. Explicit KIYA Gaps & Differentiators Summary

In strict compliance with `CD-001` and anti-hallucination discipline, the following 5 key areas represent explicit KIYA differentiators where standard ERPNext behavior was rejected, found absent, or expanded beyond standard ERP conventions:

1. **Customer Installed Base vs. Capital Fixed Asset (DR-A2S-001) — `BRD-REQUIRED (Seam Resolution)`:**
   In ERPNext, `Asset` is strictly a corporate capitalized property entity subject to depreciation. Customer equipment is merely tracked as a `Serial No` string under Stock. KIYA explicitly establishes a dedicated `Customer Installed Equipment / Asset` entity maintaining site location, configuration hierarchy, warranty entitlements, and lifetime service history (`FR-AST-001`, `FR-AST-003`), decoupled from balance-sheet asset accounting.
2. **Dedicated Field Service Work Order vs. Factory Manufacturing Work Order (DR-A2S-007) — `BRD-REQUIRED (Collision Resolution)`:**
   In ERPNext, `Work Order` belongs strictly to factory manufacturing. Reusing it for field maintenance would cause severe architectural and logic corruption. KIYA establishes a first-class `Field Service Work Order` entity tailored for field dispatch, technician labor logging, checklist execution, and truck-stock spare parts consumption (`FR-MFS-002`, `FR-MFS-007`).
3. **Consolidated Service Billing with Warranty-Entitlement Parsing (DR-A2S-003, DR-A2S-009) — `BRD-REQUIRED (Engine) / PROPOSED (Tolerances)`:**
   ERPNext lacks automated service billing that merges field technician timesheets, travel allowances, and replacement parts into a single invoice while dynamically exempting warranty-covered items. KIYA integrates a consolidated service billing engine that validates entitlement against active warranty/AMC terms, applies Global Tax Engine rules, and books Accounts Receivable seamlessly (`FR-MFS-006`, `FR-ACC-002`).
4. **Mobile Truck-Stock Integration & Field Spares Logistics (DR-A2S-006) — `BRD-REQUIRED (Spares) / PROPOSED (Truck Stock Mechanics)`:**
   While ERPNext requires manual `Stock Entry` transactions, KIYA natively links field service execution to mobile technician truck-stock locations, enabling real-time parts consumption, batch/serial tracking, and reverse logistics for defective components directly from the technician mobile app (`FR-MFS-005`, `FR-MOB-002`).
5. **360-Degree Asset Lifecycle Intelligence & Reliability Analytics (DR-A2S-011) — `BRD-REQUIRED (Timeline) / PROPOSED (MTBF Algorithms)`:**
   ERPNext stores fragmented maintenance visit logs without unified equipment reliability dashboards. KIYA provides a dedicated Asset Lifecycle Intelligence hub synthesizing commissioning records, complete maintenance timelines, parts consumption, total maintenance spend, and automated reliability metrics (MTBF, MTTR, Availability) (`FR-AST-006`, `FR-AST-007`).

---

## 6. Cross-Module Interactions & Data Flow Architecture

The Asset-to-Service flow exhibits extensive horizontal integration across the enterprise platform:

1. **Upstream Asset Seeding (C2C Fulfillment to Asset Registry):**
   - Serialized equipment manufactured in Production (`DR-C2C-009`) and dispatched via Delivery Note (`DR-C2C-012`) automatically feeds the Installed Asset Registry (`DR-A2S-001`), establishing customer ownership and initial site location (`DEP-002`, `DEP-011`).
2. **Operational Commissioning to Entitlement (Field Service to Contracts):**
   - Installation and commissioning completion (`DR-A2S-002`) establishes the formal operational handover and activates the manufacturer warranty coverage period (`DR-A2S-003`).
3. **Service Incident to Mobile Field Execution (Incident to Dispatch to Work Order):**
   - Service Requests (`DR-A2S-004`) evaluate warranty entitlement, schedule qualified technicians (`DR-A2S-005`), stage spare parts (`DR-A2S-006`), and generate Field Service Work Orders (`DR-A2S-007`) dispatched to mobile field technicians (`FR-MOB-002`).
4. **Materials & Financial Settlement (Work Order to Warehouse to Invoicing to AR):**
   - Parts consumed during service execution decrement warehouse or truck-stock balances in the Stock Ledger (`DR-A2S-006`, `DEP-002`).
   - Completed work orders feed billable labor and non-warranty parts into Service Invoicing (`DR-A2S-009`).
   - Global Tax Engine computes statutory GST/VAT (`FR-TAX-001`), and customer payments (`DR-A2S-010`) clear Accounts Receivable in the General Ledger (`DEP-005`, `DEP-008`).
5. **Closed-Loop Reliability & Quality Feedback (History to BI and Manufacturing):**
   - Every completed work order, maintenance visit, and component replacement continuously streams into Asset History (`DR-A2S-011`).
   - Aggregated failure analytics and component defect trends feed back to Manufacturing Quality (`FR-QLTY-002`) to drive continuous engineering enhancements (`DEP-004`, `DEP-009`).

---

## 7. Document Metadata & Governance

- **Prepared By:** Antigravity Enterprise Requirements Architect
- **Creation Date:** 14 September 2026 | **Correction Pass:** 14 September 2026
- **Status:** Baseline Detailed Requirements Package (Final QC Correction Pass Completed)
- **Traceability Chain:** `source/KIYA360_BRD.pdf v2.0` → `docs/00-requirements/01-master-requirements.md` → `docs/00-requirements/04-business-flows.md` → `docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md` → `docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md` → `docs/00-requirements/33-asset-to-service-detailed-requirements.md`.
- **Immediate Next Action:** Update `docs/PROJECT-STATE.md`, `.kiya/AI-HANDOFF.md`, and `.kiya/AI-CHANGELOG.md`. Await stakeholder review of A2S. Phase 0B-2 core flow functional expansions (C2C, P2P, A2S) are now complete.
