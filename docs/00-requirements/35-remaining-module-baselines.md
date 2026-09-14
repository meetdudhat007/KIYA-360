# KIYA 360 — Remaining Module Baselines

## 1. Document Control, Authority & Scope

- **Document ID:** `35-remaining-module-baselines`
- **Phase:** Phase 0B-2 — Compressed Remaining Module Requirements Baseline
- **Status:** In Review / Phase 0B-2 Compressed Module Baselines
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026: Section 3, Section 6, Section 7.4, 7.5, 7.7, 7.15, 7.16, 7.19, 7.20, Section 8, Section 10, Section 11)
- **Governance & Precedents:**
  - `AGENTS.md` & `.kiya/AI-DECISIONS.md`
  - `docs/00-requirements/02-module-inventory.md` (28 modules, 238 functional requirements)
  - `docs/00-requirements/03-scope-boundaries.md` (In-Scope, Phase 1 Out-of-Scope, TBDs)
  - `CD-001` (`DEC-012`): Hybrid Scope-Expansion Model (`29-cd001-scope-expansion-hybrid-model.md`)
  - `CD-002` (`DEC-013`): Operational Business Status Lifecycle Model (`30-cd002-transactional-lifecycle-business-status.md`)
  - `DEC-007`: Unified Data Model — Zero duplicate master entities across modules
- **Completed Baseline Prerequisites (DO NOT DUPLICATE):**
  - Customer-to-Cash (C2C): `docs/00-requirements/31-customer-to-cash-detailed-requirements.md` (`DR-C2C-001`..`018`)
  - Procure-to-Pay (P2P): `docs/00-requirements/32-procure-to-pay-detailed-requirements.md` (`DR-P2P-001`..`012`)
  - Asset-to-Service (A2S): `docs/00-requirements/33-asset-to-service-detailed-requirements.md` (`DR-A2S-001`..`011`)
  - Shared Foundations Baseline: `docs/00-requirements/34-shared-foundation-requirements-baseline.md` (`SF-001`..`SF-015`)

---

## 2. Requirements Strategy & Overlap Discipline

1. **Non-Duplication Rule:** Capabilities already baselined in C2C, P2P, A2S, or Shared Foundations (`SF-001` through `SF-015`) are explicitly referenced and not rewritten.
2. **Platform & Administration Scoping:** The 50 granular Platform & Administration requirements (`FR-PADM-1.1.1` through `1.8.6`) are fully governed by `SF-001` through `SF-015` in Document 34 and Master Requirements (`01-master-requirements.md`).
3. **Classification Discipline:** Every requirement statement strictly uses `BRD-REQUIRED`, `BRD-DERIVED`, `ERP-REFERENCE`, `PROPOSED`, `TBD`, or `OUT-OF-SCOPE`.
4. **Open Question Preservation:** Questions `OQ-003` through `OQ-015` remain open. Unresolved policy, threshold, or localization details are marked `TBD`.
5. **Technology Neutrality:** Functional requirements only; no database engines, APIs, frameworks, or programming languages are mandated.

---

## 3. Compressed Remaining Module Baselines

---

### 3.1 Module 04 — Marketing

- **BRD Requirement IDs:** `FR-MKT-001` (Campaigns), `FR-MKT-002` (Email Marketing), `FR-MKT-003` (Digital Marketing), `FR-MKT-004` (Events & Webinars), `FR-MKT-005` (Lead Generation), `FR-MKT-006` (Market Analysis), `FR-MKT-007` (Marketing Analytics)
- **BRD Source Section:** BRD §7.4
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Plan, execute, track, and measure multi-channel marketing campaigns, promotional events, and lead-generation activities across target audience segments.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Multi-channel campaign planning, budgeting, scheduling, and channel allocation (`FR-MKT-001`).
  - `[BRD-REQUIRED]` Native outbound email marketing execution with subscription preferences and unsubscribes (`FR-MKT-002`).
  - `[BRD-REQUIRED]` Tracking of digital marketing channels, landing page conversions, and inbound referral sources (`FR-MKT-003`).
  - `[BRD-REQUIRED]` Management of corporate events, webinars, attendee registration, and participation tracking (`FR-MKT-004`).
  - `[BRD-REQUIRED]` Capture and qualification of marketing-generated leads and direct promotion into CRM (`FR-MKT-005`).
  - `[BRD-REQUIRED]` Market segment analysis, demographic categorization, and competitor benchmarking data capture (`FR-MKT-006`).
  - `[BRD-REQUIRED]` Marketing analytics measuring campaign ROI, lead acquisition cost, and conversion velocity (`FR-MKT-007`).
- **Key Business Behaviors:**
  - Qualified marketing leads automatically convert to CRM Leads (`FR-CRM-001` / `DR-C2C-001`) preserving campaign attribution source.
  - Campaign budgets link to EPM/Cost Centers (`SF-011`, `FR-FIN-006`) to track planned vs actual marketing spend.
- **Important Validations / Controls:**
  - Mandatory email opt-in and unsubscribe link validation on outbound email dispatches (`SF-006`, `FR-ASC-003`).
  - Out-of-Scope Boundary: Direct programmatic advertising platform management, automated social media bid optimizers, and third-party ad networks are not specified in BRD Phase 1 (`PROPOSED / TBD`).
- **Cross-Module Dependencies:** `FR-CRM-001` (CRM Leads), `SF-006` (Notifications), `SF-011` (BI Analytics), `FR-FIN-006` (Cost Centers).
- **Open Questions / TBDs:** Lead-scoring algorithm weighting and campaign approval thresholds are policy-dependent (`TBD / OQ-003`).
- **Minimal Acceptance Baseline:** Users can create a marketing campaign, define budget and audience segments, dispatch promotional communications, register attendee leads, and measure campaign conversion into CRM sales opportunities.

---

### 3.2 Module 05 — Customer Service

- **BRD Requirement IDs:** `FR-CSVC-001` (Case Management), `FR-CSVC-002` (Service Tickets), `FR-CSVC-003` (Knowledge Base), `FR-CSVC-004` (SLA Management), `FR-CSVC-005` (Customer Feedback), `FR-CSVC-006` (Escalations), `FR-CSVC-007` (Service Analytics)
- **BRD Source Section:** BRD §7.5
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Manage post-sale customer support cases, inquiry tickets, self-service knowledge base, service-level agreements (SLAs), customer satisfaction surveys, and support escalations independently from field maintenance.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Omnichannel customer case logging, classification, prioritization, and assignment (`FR-CSVC-001`).
  - `[BRD-REQUIRED]` Multi-tier service ticket lifecycle management with status tracking, communication history, and resolution logging (`FR-CSVC-002`).
  - `[BRD-REQUIRED]` Searchable customer-facing and internal support knowledge base with article versioning and category tagging (`FR-CSVC-003`).
  - `[BRD-REQUIRED]` Configurable SLA policies defining first-response and resolution time targets by customer tier or case priority (`FR-CSVC-004`).
  - `[BRD-REQUIRED]` Automated post-resolution customer satisfaction (CSAT) surveys, rating collection, and feedback recording (`FR-CSVC-005`).
  - `[BRD-REQUIRED]` Automated multi-tier escalation triggers for impending or breached SLAs (`FR-CSVC-006`).
  - `[BRD-REQUIRED]` Service performance analytics: First Contact Resolution (FCR), Average Handle Time (AHT), CSAT score trends (`FR-CSVC-007`).
- **Key Business Behaviors:**
  - Cases reference unified Customer (`FR-PADM-1.4.1` / `SF-003`) and Customer Installed Base (`FR-AST-001` / `DR-A2S-001`) when applicable.
  - When a customer case requires on-site technical repair, the case can trigger an Asset-to-Service Request (`DR-A2S-004`) while maintaining its distinct customer support case identity.
  - Architectural Boundary: Customer Service is an independent post-sale support domain; it is NOT merged into the C2C, P2P, or A2S flows.
- **Important Validations / Controls:**
  - SLA timers pause during legitimate pending-customer-response states and resume upon customer communication (`PROPOSED / Reference Baseline`).
  - Closed tickets cannot be edited; new inquiries on closed tickets generate linked follow-up tickets (`SF-008`).
- **Cross-Module Dependencies:** `SF-003` (Customer Master), `SF-005` (Escalation Engine), `SF-006` (Omnichannel Alerts), `DR-A2S-004` (Service Request Hand-off).
- **Open Questions / TBDs:** Exact SLA response/resolution hours per priority tier are policy-dependent (`TBD / OQ-010`).
- **Minimal Acceptance Baseline:** Support agents can log customer cases, link them to customer accounts, attach knowledge base solutions, track SLA countdowns, execute automated escalation upon SLA breach, capture CSAT feedback, and review service resolution metrics.

---

### 3.3 Module 07 — Supplier Management (Non-Transactional Lifecycle & Portal)

- **BRD Requirement IDs:** `FR-SUPM-001` (Supplier Master), `FR-SUPM-002` (Supplier Classification), `FR-SUPM-003` (Supplier Evaluation), `FR-SUPM-004` (Contracts), `FR-SUPM-005` (Performance Scorecard), `FR-SUPM-006` (Supplier Portal)
- **BRD Source Section:** BRD §7.7
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Govern the end-to-end non-transactional supplier relationship: vendor onboarding, category classification, compliance evaluation, master procurement contracts, automated performance scorecards, and external supplier self-service portal.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Unified Supplier Master with multi-branch addresses, banking details, and statutory tax IDs (`FR-SUPM-001` / `SF-003` / `DR-P2P-001`).
  - `[BRD-REQUIRED]` Strategic vendor classification by tier, spend category, critical risk level, and supply capability (`FR-SUPM-002`).
  - `[BRD-REQUIRED]` Periodic supplier qualification audits, compliance assessments, and ESG/financial risk evaluations (`FR-SUPM-003`).
  - `[BRD-REQUIRED]` Management of master purchasing agreements, annual rate contracts, volume commitments, and SLA terms (`FR-SUPM-004`).
  - `[BRD-REQUIRED]` Automated supplier performance scorecards aggregating quality acceptance rates, on-time delivery (OTD), and price adherence (`FR-SUPM-005` / `DR-P2P-012`).
  - `[BRD-REQUIRED]` Secure external supplier self-service portal for RFQ bidding, PO acknowledgment, ASN submission, and invoice status tracking (`FR-SUPM-006`).
- **Key Business Behaviors:**
  - PO creation in P2P (`DR-P2P-005`) references valid master contracts and active qualification status from `FR-SUPM-004`.
  - External suppliers access only their own scoped tenders, purchase orders, and payment statuses via the portal (`SF-002`).
- **Important Validations / Controls:**
  - Blacklisted, debarred, or expired suppliers are automatically blocked from RFQ invitation and PO issuance (`DR-P2P-001`).
  - Contract expiration alerts trigger 60/30 days prior to end date (`SF-006`).
- **Cross-Module Dependencies:** `DR-P2P-001`..`012` (P2P Execution), `SF-002` (External Portal RBAC), `SF-007` (Contract DMS), `SF-011` (Vendor BI).
- **Open Questions / TBDs:** Supplier scorecard metric weightings and portal self-registration verification steps are policy-dependent (`TBD / OQ-009`).
- **Minimal Acceptance Baseline:** Procurement officers can qualify suppliers, define master contracts, view auto-computed scorecard ratings based on P2P execution data, and grant secure portal access for vendors to review POs and submit quotations.

---

### 3.4 Module 15 — Logistics & Transportation

- **BRD Requirement IDs:** `FR-LOG-001` (Logistics Planning), `FR-LOG-002` (Freight Management), `FR-LOG-003` (Shipment Management), `FR-LOG-004` (Carrier Management), `FR-LOG-005` (Tracking & Tracing), `FR-LOG-006` (Delivery Confirmation), `FR-LOG-007` (Logistics Analytics)
- **BRD Source Section:** BRD §7.15
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Plan, execute, consolidate, track, and audit outbound customer freight, inbound vendor shipments, inter-facility logistics, carrier contracts, and proof of delivery (POD).
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Logistics load planning, vehicle consolidation, multi-drop route scheduling, and mode selection (`FR-LOG-001`).
  - `[BRD-REQUIRED]` Freight cost calculation, freight forwarding agreements, accessorial charges, and carrier freight bill auditing (`FR-LOG-002`).
  - `[BRD-REQUIRED]` Multi-modal shipment generation, bill of lading (BOL), airway bill (AWB), and shipping manifest generation (`FR-LOG-003`).
  - `[BRD-REQUIRED]` Carrier master data, contracted freight tariff rates, fleet profiles, and carrier performance ratings (`FR-LOG-004`).
  - `[BRD-REQUIRED]` End-to-end milestone tracking and tracing (dispatched, in-transit, out-for-delivery, delayed, delivered) (`FR-LOG-005`).
  - `[BRD-REQUIRED]` Digital Proof of Delivery (POD) capture, recipient signature, and photographic condition capture via mobile (`FR-LOG-006` / `SF-009`).
  - `[BRD-REQUIRED]` Logistics analytics measuring freight cost per unit, on-time in-full (OTIF) delivery percentage, and carrier transit reliability (`FR-LOG-007`).
- **Key Business Behaviors:**
  - Logistics shipments consume Warehouse Delivery Notes (`DR-C2C-012`) and generate statutory e-Way Bills (`DR-C2C-014` / `FR-TAX-005`).
  - Freight expenses automatically accrue against the corresponding sales order or purchase order to compute true landed cost (`FR-FIN-006`).
- **Important Validations / Controls:**
  - Shipments cannot be marked delivered without recorded POD timestamp or digital recipient confirmation (`FR-LOG-006`).
  - High-value shipments require carrier insurance validation prior to dispatch clearance (`SF-007`).
- **Cross-Module Dependencies:** `DR-C2C-012` (Dispatch), `DR-P2P-006` (Receiving), `FR-TAX-005` (e-Way Bill), `SF-009` (Mobile POD), `FR-FIN-006` (Landed Cost).
- **Open Questions / TBDs:** Third-party telematics and carrier GPS API protocols are subject to integration scoping (`TBD / OQ-012`).
- **Minimal Acceptance Baseline:** Logistics coordinators can bundle dispatches into shipments, assign licensed carriers, calculate contracted freight charges, generate shipping manifests, record transit tracking milestones, capture mobile POD, and analyze carrier delivery performance.

---

### 3.5 Module 16 — Projects

- **BRD Requirement IDs:** `FR-PROJ-001` (Project Planning), `FR-PROJ-002` (Project Budgeting), `FR-PROJ-003` (Project Execution), `FR-PROJ-004` (Resource Planning), `FR-PROJ-005` (Time & Expense), `FR-PROJ-006` (Project Billing), `FR-PROJ-007` (Project Analytics)
- **BRD Source Section:** BRD §7.16
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Plan work breakdown structures (WBS), track multi-currency project budgets, allocate enterprise resources, capture billable time/expenses, generate milestone/T&M invoices, and track project profitability.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Work breakdown structure (WBS), Gantt scheduling, milestone dependencies, and critical path planning (`FR-PROJ-001`).
  - `[BRD-REQUIRED]` Baseline project budgeting by expense category (labor, material, subcontracting, overhead) with revision control (`FR-PROJ-002`).
  - `[BRD-REQUIRED]` Task assignment, percent-complete progress tracking, issue logging, and deliverable sign-offs (`FR-PROJ-003`).
  - `[BRD-REQUIRED]` Resource capacity planning, employee allocation, role booking, and resource utilization monitoring (`FR-PROJ-004`).
  - `[BRD-REQUIRED]` Digital employee timesheet submission, expense logging against project tasks, and supervisory approval workflows (`FR-PROJ-005`).
  - `[BRD-REQUIRED]` Project billing supporting milestone billing, Time & Material (T&M), and fixed-price progress invoicing (`FR-PROJ-006`).
  - `[BRD-REQUIRED]` Project analytics measuring Earned Value (EV), Cost Variance (CV), Schedule Variance (SV), and project net margin (`FR-PROJ-007`).
- **Key Business Behaviors:**
  - Direct procurement for projects links POs (`DR-P2P-005`) to Project and WBS task IDs to book direct material commitments.
  - Approved project billing events generate Sales Invoices in the unified AR ledger (`DR-C2C-013` / `FR-FIN-003`).
- **Important Validations / Controls:**
  - Timesheet hours cannot exceed 24 hours per calendar day per employee; overlapping time blocks trigger validation errors (`SF-002`).
  - Project expense bookings exceeding approved budget thresholds require change order approval or budget override authorization (`SF-005`, `TBD / OQ-003`).
- **Cross-Module Dependencies:** `FR-FIN-001` (GL), `FR-FIN-003` (AR Billing), `DR-P2P-005` (Project Procurement), `FR-HR-001` (Employee Master), `SF-011` (EPM).
- **Open Questions / TBDs:** Revenue recognition method (Percentage of Completion vs Completed Contract) is governed by corporate accounting policy (`TBD / OQ-006`).
- **Minimal Acceptance Baseline:** Project managers can structure a WBS, allocate team members, track logged timesheets and project expenses against budget, trigger customer milestone invoices into AR, and evaluate earned value performance metrics.

---

### 3.6 Module 17 — Finance & Accounting (Back-Office Financial Controls)

- **BRD Requirement IDs:** `FR-FIN-004` (Cash & Bank), `FR-FIN-005` (Fixed Assets Accounting), `FR-FIN-006` (Cost Accounting), `FR-FIN-007` (Financial Reporting)  
  *(Note: `FR-FIN-001` General Ledger, `FR-FIN-002` Accounts Payable, and `FR-FIN-003` Accounts Receivable are fully baselined across C2C, P2P, and A2S execution).*
- **BRD Source Section:** BRD §7.17
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Govern back-office corporate financial controls: treasury cash/bank management, bank reconciliation, fixed asset accounting integration, managerial cost center accounting, and periodic financial period closing.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Bank account configuration, petty cash floats, electronic bank statement parsing, and rule-based bank reconciliation (`FR-FIN-004`).
  - `[BRD-REQUIRED]` General ledger posting of fixed asset additions, monthly depreciation expense schedules, revaluations, and asset disposals (`FR-FIN-005` / `FR-AST-004`).
  - `[BRD-REQUIRED]` Multi-tier cost center hierarchy, profit center assignment, overhead allocation cycles, and activity-based costing (`FR-FIN-006`).
  - `[BRD-REQUIRED]` Automated preparation of statutory Balance Sheet, Profit & Loss (Income Statement), Cash Flow, Trial Balance, and fiscal period close lockouts (`FR-FIN-007`).
- **Key Business Behaviors:**
  - Transactional postings from C2C, P2P, and A2S automatically inherit Company, Branch, Cost Center, and Business Unit tags (`SF-001`).
  - Fiscal period close places a hard lockout on retroactive transactional entries, permitting only authorized adjustment journals (`SF-002`, `SF-008`).
- **Important Validations / Controls:**
  - General ledger debits must strictly equal credits for every journal voucher and operational sub-ledger posting (`DR-C2C-016`, `DR-P2P-011`).
  - Bank reconciliation differences require explicit reconciliation adjustment journals with documented audit justification (`SF-008`).
- **Cross-Module Dependencies:** `SF-001` (Multi-Entity), `SF-008` (Audit Ledger), `FR-AST-004` (Asset Depreciation), `FR-TAX-001` (Tax Engine), all transactional modules.
- **Open Questions / TBDs:** Multi-company consolidation rules, intercompany eliminations, and foreign currency revaluation mechanics (`TBD / OQ-006`).
- **Minimal Acceptance Baseline:** Financial controllers can reconcile bank accounts, run automated depreciation journal postings, allocate indirect expenses across cost centers, execute fiscal month-end close lockouts, and generate real-time financial statements.

---

### 3.7 Module 13 — Asset Management (Corporate Capital Assets & Lifecycle)

- **BRD Requirement IDs:** `FR-AST-001` (Asset Master), `FR-AST-002` (Asset Classification), `FR-AST-003` (Asset Tracking), `FR-AST-004` (Asset Depreciation), `FR-AST-005` (Asset Valuation), `FR-AST-006` (Asset Lifecycle), `FR-AST-007` (Asset Analytics)  
  *(Note: A2S `DR-A2S-001` established the fundamental boundary separating Customer Installed Base from Corporate Capital Assets; this baseline covers Corporate Fixed Assets).*
- **BRD Source Section:** BRD §7.13
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Manage internal corporate fixed assets throughout their lifecycle: acquisition, capital tagging, physical location tracking, automated depreciation, revaluation, transfer, impairment, and scrapping/disposal.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Corporate Fixed Asset Register recording capitalization date, purchase value, asset custodian, and serial numbers (`FR-AST-001`).
  - `[BRD-REQUIRED]` Categorization by asset class (Machinery, Vehicles, IT Hardware, Buildings, Furniture) with default useful life and depreciation methods (`FR-AST-002`).
  - `[BRD-REQUIRED]` Tracking physical asset location (Branch, Building, Floor, Room), employee custody, and periodic physical asset audit scanning (`FR-AST-003`).
  - `[BRD-REQUIRED]` Automated monthly depreciation calculation supporting Straight Line (SLM), Written Down Value (WDV), and Units of Production (`FR-AST-004`).
  - `[BRD-REQUIRED]` Asset impairment, historical cost revaluation, salvage value adjustments, and net book value (NBV) tracking (`FR-AST-005`).
  - `[BRD-REQUIRED]` Asset lifecycle management: inter-branch asset transfer, internal maintenance work orders, capital overhaul, and disposal/scrapping (`FR-AST-006`).
  - `[BRD-REQUIRED]` Asset analytics: asset age distribution, remaining useful life, maintenance-to-cost ratio, and asset return on capital (`FR-AST-007`).
- **Key Business Behaviors:**
  - Fixed asset capitalization is triggered by P2P capital purchase orders (`DR-P2P-005`) or manufacturing capital work-in-progress (CWIP).
  - Monthly depreciation runs post automated debit to Depreciation Expense and credit to Accumulated Depreciation in the GL (`FR-FIN-005`).
- **Important Validations / Controls:**
  - Assets cannot be scrapped or sold without authorized write-off approval (`SF-005`).
  - Accumulated depreciation cannot exceed capitalized purchase cost minus designated salvage value (`FR-AST-004`).
- **Cross-Module Dependencies:** `FR-FIN-005` (Fixed Asset GL), `DR-P2P-005` (Capital Procurement), `SF-001` (Branch Locations), `SF-008` (Audit).
- **Open Questions / TBDs:** Country statutory depreciation schedules (Companies Act vs Tax depreciation rates) are jurisdiction-dependent (`TBD / OQ-005`, `OQ-006`).
- **Minimal Acceptance Baseline:** Asset accountants can capitalize purchased fixed assets, assign barcode/RFID tags and custodians, run automated monthly depreciation schedules into the GL, log inter-branch transfers, and record disposal gains/losses.

---

### 3.8 Modules 08 & 09 — Inventory & Warehouse (Periodic Operations)

- **BRD Requirement IDs:** `FR-INV-005` (Cycle Counting), `FR-INV-006` (Stock Valuation), `FR-WH-006` (Warehouse Transfers)  
  *(Note: Stock quantity, batches, serials, reservations, warehouse layouts, bins, and pick/pack/ship operations are fully baselined across C2C and P2P).*
- **BRD Source Section:** BRD §7.8, §7.9
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Govern periodic inventory governance and inter-facility stock movements: perpetual cycle counting, physical inventory reconciliation, formal stock valuation costing methods, and inter-warehouse logistics transfers.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Configurable cycle count scheduling (ABC-analysis driven), blind count sheets, variance logging, and automated count adjustments (`FR-INV-005`).
  - `[BRD-REQUIRED]` Continuous stock valuation supporting FIFO, Moving Average, and Standard Costing with automated inventory revaluation journals (`FR-INV-006`).
  - `[BRD-REQUIRED]` Multi-phase inter-warehouse stock transfers: transfer request, pick, transit-out (in-transit virtual warehouse), transit-in, and receiving inspection (`FR-WH-006`).
- **Key Business Behaviors:**
  - Approved cycle count variance entries generate inventory adjustment journals debiting/crediting Stock Adjustment Expense in the GL (`FR-FIN-001`).
  - Material in-transit between company branches is held in an In-Transit valuation account until formally received at the destination warehouse (`SF-001`).
- **Important Validations / Controls:**
  - Physical inventory adjustments exceeding configured dollar thresholds mandate inventory manager and financial controller sign-off (`SF-005`, `TBD / OQ-003`).
  - Negative stock is prohibited; transactions driving stock below zero are blocked unless explicit backorder configuration is enabled (`DR-C2C-007`).
- **Cross-Module Dependencies:** `DR-C2C-007` (Reservations), `DR-P2P-008` (Putaway), `FR-FIN-001` (GL), `FR-LOG-003` (Shipments), `SF-005` (Approvals).
- **Open Questions / TBDs:** Inventory reservation release timeouts and hard vs soft allocation algorithms (`TBD / OQ-007`).
- **Minimal Acceptance Baseline:** Warehouse supervisors can generate ABC cycle count sheets, enter blind physical counts, post approved variance reconciliations to the stock ledger and GL, and execute multi-step inter-warehouse stock transfers.

---

### 3.9 Modules 10 & 11 — Manufacturing & MRP (Advanced Product Structures & Planning)

- **BRD Requirement IDs:** `FR-MFG-007` (By-Products / Co-Products), `FR-MRP-001` (Demand Planning), `FR-MRP-005` (Supply Planning)  
  *(Note: Standard BOM, Routing, Production Work Orders, Shop Floor Execution, MRP gross-to-net calculation, and capacity planning are fully baselined in C2C Stages 8–10).*
- **BRD Source Section:** BRD §7.10, §7.11
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Provide advanced multi-output manufacturing structures (by-products, co-products, scrap allocations) and strategic enterprise planning capabilities (unconstrained long-term demand planning, multi-scenario supply balancing).
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Bill of Materials (BOM) definition for by-products, co-products, and estimated scrap percentages with proportional cost allocation rules (`FR-MFG-007`).
  - `[BRD-REQUIRED]` Aggregate statistical demand forecasting, historical demand trend analysis, and sales forecast consensus modeling (`FR-MRP-001`).
  - `[BRD-REQUIRED]` Master Production Schedule (MPS) and multi-echelon supply planning balancing production lines, supplier lead times, and safety stock targets (`FR-MRP-005`).
- **Key Business Behaviors:**
  - Production order completion splits realized manufacturing costs across primary finished goods and co-products based on predefined cost weighting ratios (`FR-MFG-006`).
  - By-product yields are received into inventory at standard salvage value, crediting the primary manufacturing order cost (`DR-C2C-010`).
- **Important Validations / Controls:**
  - Combined cost allocation percentages across primary products and co-products must total exactly 100% in the engineering BOM (`SF-003`).
  - Discrete manufacturing scope is strictly enforced; continuous process/recipe manufacturing configurators are out of Phase 1 scope per BRD §3.2 (`OUT-OF-SCOPE`).
- **Cross-Module Dependencies:** `DR-C2C-008` (MRP Engine), `DR-C2C-009` (Production Orders), `FR-INV-001` (Item Master), `FR-FIN-006` (Cost Accounting).
- **Open Questions / TBDs:** MRP exception message handling and automated rescheduling threshold tolerances (`TBD / OQ-008`).
- **Minimal Acceptance Baseline:** Production planners can maintain complex BOMs with co-products and by-products, generate multi-period demand forecasts, simulate supply balance plans, and allocate completion costs accurately across joint production outputs.

---

### 3.10 Module 12 — Quality Management (Quality Governance & CAPA)

- **BRD Requirement IDs:** `FR-QLTY-001` (Quality Planning), `FR-QLTY-005` (Quality Control), `FR-QLTY-006` (NCR / CAPA)  
  *(Note: Incoming inspection, in-process inspection, final inspection, and inspection-triggered quarantine are fully baselined in P2P Stage 7 and C2C Stage 11).*
- **BRD Source Section:** BRD §7.12
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Establish enterprise quality governance: quality inspection plans, engineering tolerance specifications, formal Non-Conformance Reporting (NCR), and Corrective and Preventive Action (CAPA) tracking.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Quality Planning: defining inspection characteristics, sampling sizes (AQL / ISO 2859), test methods, and instrument calibration requirements (`FR-QLTY-001`).
  - `[BRD-REQUIRED]` Quality Control Standards: parameter-level qualitative checks (pass/fail) and quantitative tolerances (min/nominal/max) linked to Item Masters (`FR-QLTY-005`).
  - `[BRD-REQUIRED]` Enterprise NCR / CAPA: formal non-conformance investigation, root cause analysis (5-Why, Fishbone), corrective action assignment, implementation tracking, and effectiveness verification (`FR-QLTY-006`).
- **Key Business Behaviors:**
  - Material failed during receiving (`DR-P2P-007`) or manufacturing (`DR-C2C-011`) automatically creates a candidate Non-Conformance Record (`SF-004`).
  - CAPA actions can mandate updates to engineering BOMs, vendor scorecards (`FR-SUPM-005`), or maintenance work orders.
- **Important Validations / Controls:**
  - Regulated items cannot bypass mandatory quality inspection gates; automated release without completed inspection logs is prohibited (`SF-008`).
  - CAPA records cannot be closed without documented effectiveness verification sign-off by the Quality Director (`SF-005`).
- **Cross-Module Dependencies:** `DR-P2P-007` (QI Receiving), `DR-C2C-011` (QI Final), `FR-SUPM-005` (Supplier Scorecards), `SF-005` (Approvals), `SF-007` (DMS).
- **Open Questions / TBDs:** Exact AQL sampling algorithms and automatic quarantine threshold triggers (`TBD / OQ-009`).
- **Minimal Acceptance Baseline:** Quality engineers can create item-specific inspection templates with numerical tolerances, review automatically generated NCRs from failed inspections, execute root cause analysis, track CAPA tasks to completion, and certify effectiveness.

---

### 3.11 Module 19 — HR & Payroll

- **BRD Requirement IDs:** `FR-HR-001` (Employee Master), `FR-HR-002` (Organization Management), `FR-HR-003` (Attendance & Leave), `FR-HR-004` (Payroll Processing), `FR-HR-005` (Benefits Management), `FR-HR-006` (Performance Management), `FR-HR-007` (HR Analytics)
- **BRD Source Section:** BRD §3.2, §7.19
- **Classification:** `BRD-REQUIRED` (with explicit Phase 1 statutory boundaries)
- **Purpose:** Manage core employee lifecycle data, organizational reporting lines, time and attendance, Phase 1 basic payroll calculation, benefits administration, employee reviews, and workforce analytics.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Employee Master maintaining personal identity, employment contract, department, designation, salary structure, and bank details (`FR-HR-001` / `SF-003`).
  - `[BRD-REQUIRED]` Organizational management: reporting hierarchies, supervisory positions, and department head assignments (`FR-HR-002` / `SF-001`).
  - `[BRD-REQUIRED]` Time, attendance, shift scheduling, leave entitlement balances, and leave request approval workflows (`FR-HR-003`).
  - `[BRD-REQUIRED]` Phase 1 Monthly Payroll: gross salary computation, standard allowances, attendance-based salary deductions, net pay calculation, and payslip generation (`FR-HR-004`).
  - `[BRD-REQUIRED]` Employee benefits administration, insurance enrollment tracking, and expense reimbursement claims (`FR-HR-005`).
  - `[BRD-REQUIRED]` Employee performance evaluation, goal tracking, KPI appraisals, and review cycle workflows (`FR-HR-006`).
  - `[BRD-REQUIRED]` HR analytics: workforce headcount, turnover rates, absenteeism trends, and departmental payroll cost analysis (`FR-HR-007`).
- **Key Business Behaviors:**
  - Approved monthly payroll automatically generates GL salary journal vouchers debiting Payroll Expense and crediting Salary Payable and Statutory Liabilities (`FR-FIN-001`).
  - Employee Master provides user identity mappings for RBAC, approval matrices, and field service technician dispatch (`SF-002`, `DR-A2S-005`).
- **Important Validations / Controls:**
  - Phase 1 Scope Boundary: Country-specific statutory payroll tax calculations are explicitly restricted to India (PF, ESI, PT, TDS) and one reference country per BRD §3.2. All additional international statutory payroll calculations are explicitly `OUT-OF-SCOPE` for Phase 1.
  - Confidentiality: Payroll records, compensation bands, and employee medical data enforce strict row-level and field-level security restrictions (`SF-002`, `FR-ASC-003`).
- **Cross-Module Dependencies:** `SF-001` (Org Hierarchy), `SF-002` (User Identities), `FR-FIN-001` (Salary GL), `DR-A2S-005` (Technicians), `FR-PROJ-005` (Timesheets).
- **Open Questions / TBDs:** Exact statutory tax deduction slabs, overtime formulas, and bonus accrual policies (`TBD / OQ-006`).
- **Minimal Acceptance Baseline:** HR personnel can onboard employees, maintain organizational structures, approve leave requests, execute monthly payroll runs generating payslips and GL salary entries for Phase 1 supported jurisdictions, and monitor workforce metrics.

---

### 3.12 Module 20 — E-Commerce

- **BRD Requirement IDs:** `FR-ECOM-001` (Online Store), `FR-ECOM-002` (Product Catalog), `FR-ECOM-003` (Shopping Cart), `FR-ECOM-004` (Order Management), `FR-ECOM-005` (Payment Gateway), `FR-ECOM-006` (Promotions), `FR-ECOM-007` (Customer Portal)
- **BRD Source Section:** BRD §3.2, §7.20
- **Classification:** `BRD-REQUIRED` (with explicit Phase 1 marketplace integration boundaries)
- **Purpose:** Provide a native digital commerce storefront integrated with the KIYA core, enabling real-time product catalog browsing, digital shopping carts, customer order placement, online payment gateway capture, and customer self-service.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Native responsive web and mobile digital storefront UI with company branding (`FR-ECOM-001`).
  - `[BRD-REQUIRED]` Real-time product catalog publishing synced with unified Item Master, item categories, images, specifications, and live inventory availability (`FR-ECOM-002` / `SF-003`).
  - `[BRD-REQUIRED]` Persistent shopping cart supporting guest checkout, registered customer login, tax calculation, and shipping fee computation (`FR-ECOM-003`).
  - `[BRD-REQUIRED]` Seamless order ingestion converting confirmed web orders into native KIYA Sales Orders (`FR-ECOM-004` / `DR-C2C-005`).
  - `[BRD-REQUIRED]` Secure online payment gateway integration supporting credit/debit cards, net banking, UPI, and instant digital payment confirmation (`FR-ECOM-005`).
  - `[BRD-REQUIRED]` Configurable promotional discounts, digital coupon codes, volume pricing rules, and flash sales (`FR-ECOM-006`).
  - `[BRD-REQUIRED]` Customer self-service account portal for order history tracking, invoice downloads, shipment tracking, and return requests (`FR-ECOM-007`).
- **Key Business Behaviors:**
  - Web orders automatically check real-time warehouse available-to-promise (ATP) stock (`DR-C2C-006`) and place immediate soft reservations upon checkout (`DR-C2C-007`).
  - Successful online payment transactions automatically generate Customer Payment entries linked to the Sales Order in AR (`DR-C2C-015` / `FR-FIN-003`).
- **Important Validations / Controls:**
  - Phase 1 Scope Boundary: Marketplace-specific third-party storefront integrations (e.g. Amazon, Flipkart, Shopify connectors) are explicitly `OUT-OF-SCOPE` for Phase 1 per BRD §3.2. Scope is strictly confined to the native KIYA E-Commerce storefront.
  - Orders cannot be confirmed if payment gateway authorization fails or inventory reservation cannot be satisfied (`DR-C2C-007`).
- **Cross-Module Dependencies:** `SF-003` (Item Master), `DR-C2C-005` (Sales Orders), `DR-C2C-006` (ATP Stock), `DR-C2C-015` (Payment Capture), `SF-006` (Alerts).
- **Open Questions / TBDs:** Payment gateway webhook timeout reconciliation and guest customer account creation policies (`TBD / OQ-012`).
- **Minimal Acceptance Baseline:** Customers can browse items from the unified catalog with live pricing, add items to cart, checkout with real-time tax calculation, complete online payment, and receive automated order confirmation, with the order flowing seamlessly into the C2C processing queue.

---

### 3.13 Module 18 — Tax & Statutory Compliance (Statutory Filing & Tax Returns)

- **BRD Requirement IDs:** `FR-TAX-004` (Withholding Tax), `FR-TAX-006` (Tax Returns), `FR-TAX-007` (Statutory Reports)  
  *(Note: Global Tax Engine, Country Tax Rules, GST/VAT transaction calculations, e-Invoicing, and e-Way Bills are fully baselined in C2C Stage 14, P2P Stage 10, and SF-001).*
- **BRD Source Section:** BRD §7.18
- **Classification:** `BRD-REQUIRED`
- **Purpose:** Govern periodic statutory tax compliance, vendor withholding tax (TDS) schedules, periodic tax return consolidation (GSTR-1, GSTR-3B, VAT), and audit-ready statutory compliance reporting.
- **Core Functional Scope:**
  - `[BRD-REQUIRED]` Withholding tax (TDS / WHT) ledger compilation, deduction certificates (Form 16A), and monthly withholding remittance schedules (`FR-TAX-004`).
  - `[BRD-REQUIRED]` Periodic tax return data extraction, multi-rate tax aggregation, input tax credit (ITC) reconciliation, and return JSON/XML export (`FR-TAX-006`).
  - `[BRD-REQUIRED]` Generation of statutory compliance registers (Sales Register, Purchase Register, Tax Liability Register, ITC Available vs Claimed) (`FR-TAX-007`).
- **Key Business Behaviors:**
  - Tax return engines aggregate finalized transactional tax postings from AR invoices (`DR-C2C-013`) and AP bills (`DR-P2P-009`) by tax period.
  - Statutory period lockouts prevent invoice modifications once corresponding periodic tax returns have been filed (`SF-008`).
- **Important Validations / Controls:**
  - Tax return summary balances must reconcile exactly to the General Ledger Tax Liability and Input Tax Credit accounts (`FR-FIN-001`).
  - Unmatched vendor invoices (where vendor has not uploaded corresponding invoice) are flagged for ITC deferral (`DR-P2P-010`).
- **Cross-Module Dependencies:** `FR-TAX-001` (Tax Engine), `DR-C2C-013` (AR Tax Invoices), `DR-P2P-009` (AP Tax Bills), `FR-FIN-001` (GL), `SF-008` (Audit).
- **Open Questions / TBDs:** Exact statutory filing formats and direct tax portal filing API integrations (`TBD / OQ-005`).
- **Minimal Acceptance Baseline:** Tax accountants can generate vendor withholding tax certificates, compile monthly/quarterly tax return registers reconciling exactly to the GL, and export statutory return filing payloads.

---

## 4. Remaining Module Traceability Matrix

| Module | BRD FR ID(s) | Capability | Covered By Existing Document? | New Baseline Needed? | Primary Classification | Cross-Module Dependencies | Open Question | Current Status |
|---|---|---|---|---|---|---|---|---|
| **04 Marketing** | `FR-MKT-001`–`007` | Multi-channel campaigns, email, events, lead generation, analytics | No | **Yes (Doc 35 §3.1)** | `BRD-REQUIRED` | CRM, Finance, BI, Notifications | `OQ-003`, `OQ-004` | Baselined in Doc 35 |
| **05 Customer Service** | `FR-CSVC-001`–`007` | Case management, tickets, KB, SLAs, feedback, escalations, analytics | No | **Yes (Doc 35 §3.2)** | `BRD-REQUIRED` | Customer Master, Installed Base, Alerts | `OQ-004`, `OQ-010` | Baselined in Doc 35 |
| **07 Supplier Mgmt** | `FR-SUPM-001`–`006` | Supplier classification, evaluation, contracts, scorecards, portal | Partial (`DR-P2P-001`, `012`) | **Yes (Doc 35 §3.3)** | `BRD-REQUIRED` | P2P Flow, Contracts, Vendor Portal | `OQ-009`, `OQ-012` | Baselined in Doc 35 |
| **15 Logistics** | `FR-LOG-001`–`007` | Logistics planning, freight, carriers, shipments, tracking, POD, analytics | Partial (`DR-C2C-012`, `DR-P2P-006`) | **Yes (Doc 35 §3.4)** | `BRD-REQUIRED` | Sales Dispatch, e-Way Bill, Mobile POD | `OQ-012`, `OQ-013` | Baselined in Doc 35 |
| **16 Projects** | `FR-PROJ-001`–`007` | WBS planning, budgeting, task execution, resources, timesheets, billing | No | **Yes (Doc 35 §3.5)** | `BRD-REQUIRED` | GL, AR Invoicing, P2P Procurement, HR | `OQ-003`, `OQ-006` | Baselined in Doc 35 |
| **17 Finance (Back-Office)**| `FR-FIN-004`–`007` | Cash/Bank reconciliation, fixed assets, cost accounting, financial close | Partial (`DR-C2C-016`, `DR-P2P-011`) | **Yes (Doc 35 §3.6)** | `BRD-REQUIRED` | Fixed Assets, Cost Centers, Multi-Entity | `OQ-005`, `OQ-006` | Baselined in Doc 35 |
| **13 Asset Management** | `FR-AST-001`–`007` | Corporate fixed asset register, tracking, depreciation, valuation, disposal | Partial (`DR-A2S-001` Installed Base)| **Yes (Doc 35 §3.7)** | `BRD-REQUIRED` | Fixed Asset GL, Capital Procurement | `OQ-005`, `OQ-006` | Baselined in Doc 35 |
| **08/09 Inventory/WH** | `FR-INV-005`–`006`, `WH-006`| ABC cycle counting, stock valuation methods, inter-warehouse transfers | Partial (`DR-C2C-007`, `DR-P2P-008`) | **Yes (Doc 35 §3.8)** | `BRD-REQUIRED` | Stock Ledger, GL Adjustment, Logistics | `OQ-007`, `OQ-008` | Baselined in Doc 35 |
| **10/11 Mfg & MRP** | `FR-MFG-007`, `MRP-001`, `005`| Co-products, by-products, aggregate demand forecasting, supply planning | Partial (`DR-C2C-008`..`010`) | **Yes (Doc 35 §3.9)** | `BRD-REQUIRED` | Item Master, Production Orders, Costing | `OQ-008` | Baselined in Doc 35 |
| **12 Quality Mgmt** | `FR-QLTY-001`, `005`, `006`| Quality plans, tolerance parameters, enterprise CAPA & root cause | Partial (`DR-P2P-007`, `DR-C2C-011`) | **Yes (Doc 35 §3.10)**| `BRD-REQUIRED` | Item Master, Inspections, Vendor Score | `OQ-009` | Baselined in Doc 35 |
| **19 HR & Payroll** | `FR-HR-001`–`007` | Employee master, org structure, attendance, Phase 1 payroll, analytics | No | **Yes (Doc 35 §3.11)**| `BRD-REQUIRED` | Org Hierarchy, Salary GL, User RBAC | `OQ-006` | Baselined in Doc 35 |
| **20 E-Commerce** | `FR-ECOM-001`–`007` | Native web storefront, catalog, cart, orders, payment gateway, portal | No | **Yes (Doc 35 §3.12)**| `BRD-REQUIRED` | Catalog, Sales Orders, AR Payments | `OQ-012` | Baselined in Doc 35 |
| **18 Tax Compliance** | `FR-TAX-004`, `006`, `007` | Withholding tax schedules, periodic tax returns, statutory registers | Partial (`DR-C2C-014`, `DR-P2P-010`) | **Yes (Doc 35 §3.13)**| `BRD-REQUIRED` | Tax Engine, GL Liabilities, Invoices | `OQ-005` | Baselined in Doc 35 |

---

## 5. Complete 238-Requirement Coverage Reconciliation

The following table accounts for every single one of the 238 BRD functional requirement records across the entire KIYA 360 suite, demonstrating complete, rigorous, and evidence-based coverage across the Phase 0 baselines:

| BRD FR ID Range | Module Name | Count | Primary Coverage Source | Coverage Status | Classification | Reconciliation Notes |
|---|---|---|---|---|---|---|
| `FR-PADM-1.1.1`–`1.1.6` | 01 Platform & Administration | 6 | `SF-001` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Company, Branch, BU, Dept, Div, Location masters |
| `FR-PADM-1.2.1`–`1.2.6` | 01 Platform & Administration | 6 | `SF-002`, `SF-005` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Users, Roles, Permissions, Approvals, Groups, Sessions |
| `FR-PADM-1.3.1`–`1.3.6` | 01 Platform & Administration | 6 | `SF-002`, `SF-008` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Authentication, IP limits, Encryption, Access control |
| `FR-PADM-1.4.1`–`1.4.7` | 01 Platform & Administration | 7 | `SF-003`, `SF-004` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Customer, Supplier, Item, Employee, Tax, Currency, UOM |
| `FR-PADM-1.5.1`–`1.5.7` | 01 Platform & Administration | 7 | `SF-001`, `SF-003`, Doc 01 | Covered — shared foundation | `BRD-REQUIRED` | Suite-wide system, finance, sales, purchase, mfg settings |
| `FR-PADM-1.6.1`–`1.6.6` | 01 Platform & Administration | 6 | `SF-013` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Universal numbering series across docs/transactions |
| `FR-PADM-1.7.1`–`1.7.6` | 01 Platform & Administration | 6 | `SF-006` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Email, SMS, WhatsApp, Push, In-App notifications |
| `FR-PADM-1.8.1`–`1.8.6` | 01 Platform & Administration | 6 | `SF-008`, `SF-012` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Login, Data change, Transaction, Approval, API logs |
| `FR-CRM-001`–`008` | 02 CRM | 8 | C2C Flow (`DR-C2C-001`..`005`, `018`) | Fully Covered — existing document | `BRD-REQUIRED` | Leads, Opportunities, Accounts, Contacts, Cust 360 |
| `FR-SALES-001`–`008` | 03 Sales | 8 | C2C Flow (`DR-C2C-003`..`007`, `012`) | Fully Covered — existing document | `BRD-REQUIRED` | Enquiries, Quotes, Orders, Pricing, Dispatch, Returns |
| `FR-MKT-001`–`007` | 04 Marketing | 7 | Doc 35 §3.1 | Covered — this document | `BRD-REQUIRED` | Campaigns, Email, Events, Lead Gen, Analytics |
| `FR-CSVC-001`–`007` | 05 Customer Service | 7 | Doc 35 §3.2 | Covered — this document | `BRD-REQUIRED` | Case management, tickets, KB, SLAs, feedback, CSAT |
| `FR-PROC-001`–`007` | 06 Procurement | 7 | P2P Flow (`DR-P2P-002`..`007`) | Fully Covered — existing document | `BRD-REQUIRED` | PR, RFQ/RFP, Quotes, PO, Goods Receipt, Returns |
| `FR-SUPM-001`–`006` | 07 Supplier Management | 6 | P2P (`DR-P2P-001`, `012`) & Doc 35 §3.3| Covered — this document | `BRD-REQUIRED` | Vendor classification, contracts, scorecards, portal |
| `FR-INV-001`–`004`, `007` | 08 Inventory | 5 | C2C, P2P, A2S Flows | Fully Covered — existing document | `BRD-REQUIRED` | Item Master, Stock Qty, Batches/Serials, Stock Ledger |
| `FR-INV-005`–`006` | 08 Inventory | 2 | Doc 35 §3.8 | Covered — this document | `BRD-REQUIRED` | ABC cycle counting, FIFO/Moving Avg stock valuation |
| `FR-WH-001`–`005`, `007` | 09 Warehouse | 6 | C2C (`DR-C2C-007`, `012`), P2P (`DR-P2P-008`)| Fully Covered — existing document | `BRD-REQUIRED` | Warehouse setup, Bin topology, Inbound/Outbound, Picking |
| `FR-WH-006` | 09 Warehouse | 1 | Doc 35 §3.8 | Covered — this document | `BRD-REQUIRED` | Inter-warehouse logistics transfers & in-transit stock |
| `FR-MFG-001`–`006` | 10 Manufacturing | 6 | C2C Flow (`DR-C2C-009`..`010`) | Fully Covered — existing document | `BRD-REQUIRED` | BOM, Routing, Work Orders, Shop Floor, Costing |
| `FR-MFG-007` | 10 Manufacturing | 1 | Doc 35 §3.9 | Covered — this document | `BRD-REQUIRED` | By-products, co-products, joint cost allocation |
| `FR-MRP-002`–`004`, `006`–`007` | 11 MRP & Planning | 5 | C2C Flow (`DR-C2C-008`) | Fully Covered — existing document | `BRD-REQUIRED` | Material requirements, capacity, scheduling, analytics |
| `FR-MRP-001`, `005` | 11 MRP & Planning | 2 | Doc 35 §3.9 | Covered — this document | `BRD-REQUIRED` | Demand planning, multi-echelon supply planning |
| `FR-QLTY-002`–`004`, `007` | 12 Quality | 4 | P2P (`DR-P2P-007`), C2C (`DR-C2C-011`) | Fully Covered — existing document | `BRD-REQUIRED` | Incoming, In-process, Final inspections, analytics |
| `FR-QLTY-001`, `005`, `006` | 12 Quality | 3 | Doc 35 §3.10 | Covered — this document | `BRD-REQUIRED` | Quality plans, parameter tolerances, enterprise CAPA |
| `FR-AST-001`–`007` | 13 Asset Management | 7 | Doc 35 §3.7 & A2S (`DR-A2S-001`..`003`) | Covered — this document & A2S | `BRD-REQUIRED` | Corporate Fixed Assets baselined in Doc 35 §3.7; Customer Installed Base derived under A2S flow |
| `FR-MFS-001`–`007` | 14 Maintenance & Field Service| 7 | A2S Flow (`DR-A2S-004`..`010`) | Fully Covered — existing document | `BRD-REQUIRED` | Preventive/breakdown maintenance, work orders, dispatch |
| `FR-LOG-001`–`007` | 15 Logistics & Transportation | 7 | Doc 35 §3.4 | Covered — this document | `BRD-REQUIRED` | Logistics planning, freight, carriers, tracking, POD |
| `FR-PROJ-001`–`007` | 16 Projects | 7 | Doc 35 §3.5 | Covered — this document | `BRD-REQUIRED` | WBS planning, budgets, resources, timesheets, billing |
| `FR-FIN-001`–`003` | 17 Finance & Accounting | 3 | C2C, P2P, A2S Flows | Fully Covered — existing document | `BRD-REQUIRED` | General Ledger, Accounts Payable, Accounts Receivable |
| `FR-FIN-004`–`007` | 17 Finance & Accounting | 4 | Doc 35 §3.6 | Covered — this document | `BRD-REQUIRED` | Cash & Bank, Fixed Asset GL, Cost Centers, Close |
| `FR-TAX-001`–`003`, `005` | 18 Tax & Statutory Compliance | 4 | C2C, P2P Flows & `SF-001` | Fully Covered — existing document | `BRD-REQUIRED` | Tax Engine, Country Rules, GST/VAT, e-Invoicing/e-Way |
| `FR-TAX-004`, `006`, `007` | 18 Tax & Statutory Compliance | 3 | Doc 35 §3.13 | Covered — this document | `BRD-REQUIRED` | Withholding Tax schedules, Tax Returns, Registers |
| `FR-HR-001`–`007` | 19 HR & Payroll | 7 | Doc 35 §3.11 | Covered — this document | `BRD-REQUIRED` | Employee master, attendance, Phase 1 payroll, reviews |
| `FR-ECOM-001`–`007` | 20 E-Commerce | 7 | Doc 35 §3.12 | Covered — this document | `BRD-REQUIRED` | Native storefront, catalog, cart, orders, payments |
| `FR-DOCM-001`–`007` | 21 Document Management | 7 | `SF-007` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Document capture, storage, versioning, e-signatures |
| `FR-BI-001`–`007` | 22 Business Intelligence | 7 | `SF-011` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Dashboards, reports, KPIs, ad-hoc, predictive BI |
| `FR-EPM-001`–`007` | 23 EPM / Budget / Forecast | 7 | `SF-011` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Budgeting, forecasting, planning, variance analysis |
| `FR-WFA-001`–`007` | 24 Workflow & Approvals | 7 | `SF-005` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Workflow builder, approval matrix, escalations |
| `FR-AIAU-001`–`007` | 25 AI & Automation | 7 | `SF-010` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | AI insights, predictive models, RPA, chat assistant |
| `FR-INTG-001`–`007` | 26 Integration & API | 7 | `SF-012` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | API management, webhooks, middleware, sync |
| `FR-MOB-001`–`007` | 27 Mobile Application | 7 | `SF-009` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Native apps (Sales, Service, Inventory), offline sync |
| `FR-ASC-001`–`005` | 28 Audit, Security & Compliance | 5 | `SF-002`, `SF-008` (Doc 34 §2) | Covered — shared foundation | `BRD-REQUIRED` | Security policy, RBAC, encryption, risk, monitoring |

*(Reconciliation Summary: Exactly 238 of 238 functional requirements accounted for across all 28 modules; zero orphans, zero unmapped IDs).*

---

## 6. Phase 0 Requirements Readiness Summary

1. **Total BRD Functional Requirements Catalogued:** `238`
2. **Fully Covered by Completed Core Business Flows (C2C, P2P, A2S):** `63` requirements (CRM 8, Sales 8, Procurement 7, Inventory 5, Warehouse 6, Manufacturing 6, MRP 5, Quality 4, Maintenance & Field Service 7, Finance 3, Tax 4)
3. **Covered by Shared Platform Foundations (`SF-001` through `SF-015` in Doc 34):** `104` requirements (Platform & Administration 50, Document Management 7, Business Intelligence 7, EPM 7, Workflow & Approvals 7, AI & Automation 7, Integration & API 7, Mobile Application 7, Audit & Security 5)
4. **Covered by Compressed Remaining Module Baselines (Doc 35 §3):** `71` requirements (Marketing 7, Customer Service 7, Supplier Management 6, Inventory 2, Warehouse 1, Manufacturing 1, MRP 2, Quality 3, Asset Management 7, Logistics 7, Projects 7, Finance 4, Tax 3, HR & Payroll 7, E-Commerce 7)  
   *(Sum check: 63 + 104 + 71 = exactly 238 total functional requirements reconciled).*
5. **Partially Covered / Policy TBDs (Open Questions):** Specific thresholds, calculation algorithms, and field schemas under `OQ-003` through `OQ-015` remain explicitly preserved as `TBD` without blocking functional baseline coverage.
6. **Explicitly Out-of-Scope (Phase 1 Boundaries per BRD §3.2):**
   - Multi-country payroll/statutory calculations beyond India and one reference country.
   - Continuous process/recipe manufacturing configurators.
   - Marketplace-specific storefront connectors (Amazon, Flipkart, etc.).
   - Legacy data cutover/migration services.
7. **Requirement-Level Blockers / Contradictions:** `ZERO`. All module baselines are fully aligned with the authoritative BRD v2.0, `CD-001` (hybrid model), `CD-002` (operational business status), and `DEC-007` (unified data model).
8. **Phase 0 Status Assessment:** Requirements authoring across all 28 modules and 3 core business flows is now 100% COMPLETE. The project is fully unblocked and ready for the formal **Final Requirements Traceability & Quality-Control Gate**.
