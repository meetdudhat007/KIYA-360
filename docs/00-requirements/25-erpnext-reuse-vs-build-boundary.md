# KIYA 360 — ERPNext Reuse vs. Build Boundary Analysis

## 1. Status, Purpose, and Governance Boundary

- **Document ID:** 25-erpnext-reuse-vs-build-boundary
- **Phase:** Phase 0B-1D — ERPNext Workflow Reverse Engineering & KIYA Alignment
- **Status:** Complete / Strategic Boundary Assessment
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026)
- **Technical Evidence Base:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md`, `22-erpnext-kiya-workflow-alignment-matrix.md`, `23-erpnext-kiya-domain-mapping.md`, and `24-erpnext-kiya-gap-analysis.md`
- **Controlling Principles:** `AGENTS.md`, `.kiya/AI-DECISIONS.md` (DEC-002: Technology Neutrality; DEC-005: Technology Deferral)

### Mandatory Strategic Direction
This document is **NOT an approved architecture decision** or an implementation blueprint. 
- It preserves the strategic direction established in `docs/00-requirements/18-erpnext-fappe-feasibility-assessment.md`: **Frappe Framework + selective/isolated ERPNext reuse is a candidate direction, NOT an approved architecture.**
- ERPNext must **NEVER** become KIYA's product boundary or raw public API.
- KIYA must strictly own its product boundaries, unified data model, SaaS control plane, AI governance, analytics strategy, billing/subscription systems, and security policies.

---

## 2. Boundary Classification Taxonomy

Every major functional capability is categorized under one of the following seven boundary classifications:

| Classification | Definition | Architectural Implication |
|---|---|---|
| **Direct Reuse Candidate** | Mature, highly aligned ERPNext/Frappe domain logic that can be utilized with standard configuration without modifying upstream code. | Encapsulate within custom app; avoid fork. |
| **Isolated Reuse / Adaptation** | ERPNext domain logic provides valuable transactional mechanisms, but requires dedicated adapter layers, custom hooks, or workflow extensions to conform to KIYA requirements. | Strict isolation behind clean facade interfaces. |
| **Reference Only** | ERPNext implementation demonstrates how a mature ERP handles the domain, but technical, structural, or conceptual mismatch prevents direct code reuse. | Use as a design reference when building KIYA-owned components. |
| **KIYA-Owned (Mandatory Build)** | Capabilities core to KIYA's competitive differentiation, enterprise SaaS model, proprietary AI, or areas completely missing from ERPNext. | Designed, engineered, and maintained 100% by KIYA. |
| **Requires PoC** | Architectural feasibility is plausible, but decisive empirical evidence regarding performance, offline sync, or upgrade resilience is missing. | Blocked pending PoC execution (`20-erpnext-poc-plan.md`). |
| **Requires Legal Review** | Upstream licensing (GPLv3 in ERPNext v17 develop tree) poses potential copyleft risks for proprietary distribution or SaaS commercialization. | Requires formal legal counsel review before finalizing commercial structure. |
| **TBD** | Business rules or requirement specifications are currently unresolved in the BRD baseline. | Blocked pending approved Clarification Decision (`CD-###`). |

---

## 3. Major Capability Boundary Analysis Matrix

| # | Major Capability Area | ERPNext / Frappe Baseline Reference | Boundary Classification | Detailed Rationale & Boundary Constraints | Mandatory KIYA-Owned Ownership Seams |
|---|---|---|---|---|---|
| **1** | **General Ledger & Accounting Engine** | `accounts/` (`GL Entry`, `general_ledger.py`, `taxes_and_totals.py`, multi-currency) | **Direct Reuse Candidate** | World-class double-entry financial core, perpetual inventory posting, exchange adjustments, and immutable ledger entries. Rebuilding this from scratch introduces extreme delivery and audit risk. | KIYA wraps GL in financial facade; owns multi-entity consolidated balance sheets and financial analytics. |
| **2** | **Accounts Receivable (AR) & Billing** | `accounts/` (`Sales Invoice`, `Payment Entry`, `Payment Ledger Entry`) | **Isolated Reuse / Adaptation** | Core invoicing, debit notes, and cash allocation are mature. Must be adapted to enforce KIYA's strict C2C sequence (mandatory physical dispatch before billing). | KIYA owns customer credit management policy, dunning rules, and self-service billing portal. |
| **3** | **Accounts Payable (AP) & Disbursements** | `accounts/` (`Purchase Invoice`, 3-way matching, `Payment Entry`, bank feeds) | **Direct Reuse Candidate** | 3-way matching against PO and PR is robust. Bank reconciliation via Plaid is verified. | KIYA owns multi-tier payment approval matrices and bank payment gateway integrations. |
| **4** | **Discrete Manufacturing & BOM** | `manufacturing/` (`BOM`, `Work Order`, `Job Card`, `Operation`, `Routing`) | **Direct Reuse Candidate** | Multi-level BOM explosion, scrap tracking, costing rollups, and shop-floor job card timing align directly with BRD discrete manufacturing requirements. | KIYA owns machine IoT telemetry ingestion, real-time dispatch dashboards, and OEE analytics. |
| **5** | **MRP & Material Planning** | `manufacturing/` (`Production Plan`, `Master Production Schedule`, `Sales Forecast`) | **Isolated Reuse / Adaptation** | Material requisition explosion from SO demand is usable. However, finite capacity scheduling (APS) and complex bottleneck sequencing are absent. | KIYA owns finite capacity planning heuristics, multi-plant scheduling, and constraint simulation. |
| **6** | **Core Inventory & Stock Ledger** | `stock/` (`Stock Ledger Entry`, `Stock Entry`, `Bin`, `Serial and Batch Bundle`) | **Direct Reuse Candidate** | Immutable transactional stock ledger, moving average/FIFO valuation, and serial/batch bundling are exceptionally mature and reliable. | KIYA owns inventory holding cost optimization, stock health analytics, and reservation policies. |
| **7** | **Inventory Reservation & ATP** | `stock/` (`Stock Reservation Entry`, `reservation.py`) | **Requires PoC / TBD** | SRE exists as an optional voucher. KIYA reservation timing, hard vs. soft holds, and shortage resolution rules remain unresolved (OQ-007). | KIYA must validate SRE concurrency under high-volume order booking via PoC-01. |
| **8** | **Physical Warehouse Management (WMS)** | `stock/` (`Warehouse`, `Pick List`, `Packing Slip`) | **Reference Only / KIYA-Owned** | ERPNext `Warehouse` is an accounting node and `Bin` is an item-balance cache. Completely lacks physical aisle/rack/bin coordinates, 3D slotting, and directed putaway. | KIYA must build a dedicated WMS engine managing physical coordinates, wave picking, and mobile scanning. |
| **9** | **Procurement Sourcing (RFQ & RFP)** | `buying/` (`Request for Quotation`, `Supplier Quotation`, `Purchase Order`) | **Isolated Reuse / Adaptation** | RFQ and PO mechanics are reusable for commercial purchasing. However, RFP DocType is absent; multi-attribute technical/commercial bid scoring must be added. | KIYA owns RFP entity, weighted scoring evaluation matrices, and supplier portal bidding interfaces. |
| **10** | **Supplier Performance & Onboarding** | `buying/` (`Supplier`, `Supplier Scorecard`) | **Isolated Reuse / Adaptation** | Supplier master and scorecard scheduler hook are reusable. ERPNext scoring formulas are hardcoded; vendor onboarding compliance workflows are missing. | KIYA owns vendor self-onboarding portal, compliance certificate verification, and dynamic scorecard engine. |
| **11** | **CRM Pipeline & Opportunities** | `crm/` (`Lead`, `Opportunity`, `Prospect`, `Campaign`) | **Isolated Reuse / Adaptation** | B2B lead and opportunity tracking are functional. Lacks omnichannel WhatsApp/social intake queues and predictive lead scoring. | KIYA owns omnichannel lead ingestion, AI lead scoring algorithms, and customer 360 profile aggregators. |
| **12** | **Sales Quotation & Order Booking** | `selling/` (`Quotation`, `Sales Order`) | **Isolated Reuse / Adaptation** | Commercial quoting and sales orders are reusable. Missing Enquiry DocType must be introduced. Complex CPQ rules must be built. | KIYA owns Enquiry DocType, CPQ configuration rules, and enterprise discount approval hierarchies. |
| **13** | **Customer Support & Ticketing** | `support/` (`Issue`, `Service Level Agreement`, `Warranty Claim`) | **Isolated Reuse / Adaptation** | Issue tracking and SLA clocks are usable for basic support. Completely segregated from Asset-to-Service maintenance flow per DEC-010. | KIYA owns customer service omnichannel routing (WhatsApp/Chat), CSAT engine, and knowledge base. |
| **14** | **Internal Capital Asset Management** | `assets/` (`Asset`, `Asset Depreciation Schedule`, `Asset Capitalization`) | **Direct Reuse Candidate** | Depreciation posting, fixed asset capitalization, asset transfers, and scrapping are highly mature and comply with standard accounting. | KIYA wraps asset accounting; owns fixed asset physical tagging and mobile audit verification. |
| **15** | **Field Service & Customer Equipment** | `maintenance/` (`Maintenance Schedule`, `Maintenance Visit`), `assets/` (`Asset Repair`) | **Reference Only / KIYA-Owned** | ERPNext separates internal assets from customer serial numbers. Maintenance Visit lacks mobile GPS tracking, technician dispatch boards, and truck-stock spare consumption. | KIYA must build a dedicated Field Service management suite (Customer Equipment, Dispatch Board, Mobile App). |
| **16** | **Quality Inspection & Testing** | `stock/` (`Quality Inspection`) | **Direct Reuse Candidate** | Quality Inspection covers Incoming, Outgoing, and In-Process checks with numeric reading parameters and reading tolerances. | KIYA owns statistical sampling plans (AQL) and mandatory inspection gate enforcement hooks. |
| **17** | **Non-Conformance (NCR) & CAPA** | `quality_management/` (`Non Conformance`, `Quality Action`) | **Reference Only / KIYA-Owned** | Non Conformance is an isolated text document in ERPNext with no automated trigger from Quality Inspection rejection. | KIYA must engineer the automated state machine linking inspection rejection to quarantine stock and CAPA. |
| **18** | **Project Management & Timesheets** | `projects/` (`Project`, `Task`, `Timesheet`) | **Direct Reuse Candidate** | WBS hierarchical tasks, Gantt tracking, employee billable timesheets, and timesheet billing to Sales Invoice align directly with BRD. | KIYA owns Earned Value Management (EVM) analytics, project portfolio dashboards, and milestone billing. |
| **19** | **HR & Payroll Processing** | `setup/` (`Employee`). Full HR removed to external app. | **Requires Legal Review / KIYA-Owned** | Core HRMS and payroll are absent from the ERPNext develop repository. Sourcing from Frappe HRMS requires separate license and architectural review. | KIYA must either integrate Frappe HRMS under strict license review or build a KIYA-owned payroll engine. |
| **20** | **Global Tax & Statutory Compliance** | `accounts/` (`Tax Rule`, `Sales Taxes and Charges Template`) | **Reference Only / KIYA-Owned** | India GST was stripped from ERPNext develop (`remove_india_localisation.py`). Generic tax tables cannot handle real-time statutory e-filing. | KIYA must build or integrate a dedicated Global Tax Engine and India GST / E-Invoicing / E-Way Bill service. |
| **21** | **E-Commerce & Customer Portal** | `portal/` (`Item` web filters, shopping cart, customer portal) | **Isolated Reuse / Adaptation** | Basic B2B self-service ordering is usable. Modern multi-marketplace synchronization (Amazon, Shopify) and headless APIs require external build. | KIYA owns headless e-commerce API gateway, multi-marketplace connectors, and consumer checkout UX. |
| **22** | **Enterprise Document Management (DMS)**| Frappe core `File` DocType | **Reference Only / KIYA-Owned** | Frappe handles basic file attachments on disk/S3. Completely lacks OCR indexing, check-in/out versioning, legal hold, and digital signatures. | KIYA must engineer an Enterprise DMS microservice with OCR pipelines and cryptographic e-signatures. |
| **23** | **Business Intelligence (BI)** | Frappe core `Dashboard`, `Dashboard Chart`, `Report` | **Reference Only / KIYA-Owned** | Frappe reports execute live SQL against transactional tables, creating extreme concurrency and locking risks at scale. Lacks OLAP cubes and semantic metrics. | KIYA must own an analytical data warehouse (ClickHouse/PostgreSQL OLAP) and semantic metric layer. |
| **24** | **Enterprise Performance Mgmt (EPM)** | `accounts/doctype/budget/` (`budget_controller.py`) | **Reference Only / KIYA-Owned** | ERPNext Budget is a simple spending ceiling on accounts. Lacks multi-scenario financial modeling, rolling cash flows, and balance sheet consolidation. | KIYA must design and build a proprietary EPM engine for enterprise planning and driver-based forecasting. |
| **25** | **Workflow & Universal Approvals** | Frappe core `Workflow`, `Workflow State`, `Workflow Action` | **Isolated Reuse / Adaptation** | State machine is usable for linear document status transitions. Lacks visual DAG builder, dynamic value thresholds, parallel voting, and escalation. | KIYA owns the Universal Approval Engine, multi-tier value threshold evaluator, and delegation rules. |
| **26** | **AI & Intelligent Automation** | None in reference repository | **KIYA-Owned (Mandatory Build)** | Completely absent from ERPNext. BRD mandates AI Insights, Predictive Models, RPA automation, and Conversational Assistant. | KIYA 100% owns AI architecture, model training pipelines, external LLM gateways, and AI governance. |
| **27** | **Integration & API Gateway** | Frappe core REST API, webhooks, hooks (`hooks.py`) | **Isolated Reuse / Adaptation** | Frappe REST/RPC is powerful for internal app communication. Exposing raw DocTypes externally violates API ownership. | KIYA owns the Enterprise API Gateway, OpenAPI 3.0 external contracts, rate limiting, and event broker (Kafka). |
| **28** | **Native Mobile Applications** | Frappe web responsive interface | **Requires PoC / KIYA-Owned** | ERPNext is a web app. Native mobile apps with offline local databases (SQLite) and conflict-free background synchronization do not exist. | KIYA must build native Flutter/React Native apps backed by an offline synchronization engine. |
| **29** | **Audit, Security & Compliance** | Frappe core `Version`, `Activity Log`, user sessions | **Isolated Reuse / Adaptation** | Field-level change tracking is useful. Lacks tamper-evident cryptographic audit chains, automated SoD validation, and field-level encryption. | KIYA owns cryptographic audit log verification, Segregation of Duties (SoD) engine, and compliance exports. |
| **30** | **Multi-Tenant SaaS Control Plane** | Frappe bench / multi-site architecture | **KIYA-Owned (Mandatory Build)** | Frappe supports site-per-tenant isolation, but has no automated SaaS provisioning, tenant billing, subscription quotas, or global control plane. | KIYA 100% owns SaaS Tenant Provisioning, Subscription Billing, Control Plane, and Cross-Tenant Telemetry. |

---

## 4. Mandatory KIYA-Owned Strategic Seams

To prevent architectural decay, vendor lock-in, and legal entanglement, KIYA must establish an unyielding boundary around the following eight strategic seams:

```
+-------------------------------------------------------------------------+
|                       KIYA 360 UNIFIED PLATFORM                         |
+-------------------------------------------------------------------------+
| 1. Product & Domain Boundaries (KIYA Unified Business Model & Schemas)  |
| 2. Proprietary UX & Frontend Applications (Web, Mobile, Portals)        |
| 3. Enterprise API Gateway & External Contracts (OpenAPI 3.0, GraphQL)   |
| 4. SaaS Multi-Tenant Control Plane, Billing & Subscription Operations    |
| 5. AI & Automation Governance (LLM Gateway, ML Models, RPA Workers)     |
| 6. Enterprise BI & EPM Layer (ClickHouse/OLAP, Metric Semantic Layer)   |
| 7. Security Policy, Cryptographic Audit Ledger & Compliance Controls    |
| 8. Universal Integration Hub & Event-Driven Message Broker (Kafka/RMQ) |
+-------------------------------------------------------------------------+
                                    |
                    [ Clean Facade / Adapter Layer ]
                                    |
+-------------------------------------------------------------------------+
|                  ISOLATED TRANSACTIONAL ERP ENGINE                      |
| (Selected Frappe Framework + Reusable ERPNext GL/Stock/Mfg/Assets/Buy)  |
+-------------------------------------------------------------------------+
```

1. **KIYA Product & Domain Boundary:** ERPNext's internal DocType structures must never dictate KIYA's unified business model. All cross-module entities are defined by KIYA domain specifications.
2. **KIYA SaaS Control Plane:** Tenant lifecycle, tenant database provisioning, subscription quotas, license metering, and operational telemetry must be 100% KIYA-owned.
3. **Enterprise API Gateway:** External consumers, partners, mobile apps, and third parties communicate strictly with KIYA's API Gateway. Raw ERPNext REST endpoints (`/api/resource/...`) must never be exposed externally.
4. **AI & Automation Boundary:** AI models, prompt governance, data access boundaries, and human-in-the-loop review policies remain completely independent of the ERP backend.
5. **Enterprise Analytics Strategy (BI & EPM):** Transactional reporting can use ERPNext; all multi-dimensional OLAP analytics, executive dashboards, and financial planning models belong to an independent analytical data warehouse.
6. **Proprietary UX & Mobile Layer:** Native mobile offline applications (iOS/Android) and enterprise web portals are owned and built by KIYA, consuming backend services via governed APIs.
7. **Security, Cryptographic Audit & Compliance:** Enterprise compliance controls (cryptographic ledger sealing, SoD conflict enforcement, field encryption) reside in KIYA's governance tier.
8. **Statutory Tax & India Compliance:** Tax jurisdiction determination, e-invoicing, e-way bills, and statutory filing engines are managed via dedicated KIYA microservices or certified third-party integrations.

---

## 5. Licensing & Commercialization Boundary (GPLv3 vs. Proprietary)

- **Baseline Fact:** The ERPNext reference repository (`references/erpnext-develop/`) is licensed under **GNU General Public License v3 (GPLv3)** (`erpnext/hooks.py`), while Frappe Framework is licensed under **MIT**.
- **Legal Risk Standard:** Direct modification of ERPNext core source code or tight in-process coupling with proprietary KIYA components creates legal exposure regarding copyleft obligations under GPLv3.
- **Architectural Boundary Enforcement:**
  - **Zero-Core-Modification Policy:** Under no circumstances will ERPNext core codebase be modified.
  - **Independent Application Isolation:** All KIYA-specific functionality, domain models, APIs, and business rules must reside in separate custom Frappe apps or standalone microservices communicating over network boundaries (REST/RPC).
  - **Mandatory Legal Counsel:** Final commercial packaging, customer delivery models (hosted SaaS vs. on-premises deployment), and license compatibility require formal legal review before technical implementation commences.

---

## 6. Document Metadata & Traceability

- **Created:** 14 September 2026
- **Baseline Document Reference:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md`, `docs/00-requirements/22-erpnext-kiya-workflow-alignment-matrix.md`, `docs/00-requirements/23-erpnext-kiya-domain-mapping.md`, `docs/00-requirements/24-erpnext-kiya-gap-analysis.md`
- **Output Artifacts:** Feeds directly into `docs/00-requirements/26-erpnext-workflow-reference-catalog.md` and `27-erpnext-analysis-review.md`.
