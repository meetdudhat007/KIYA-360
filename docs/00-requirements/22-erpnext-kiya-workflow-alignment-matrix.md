# KIYA 360 — ERPNext / KIYA Workflow Alignment Matrix

## 1. Status, Scope, and Authority Boundary

- **Document ID:** 22-erpnext-kiya-workflow-alignment-matrix
- **Phase:** Phase 0B-1D — ERPNext Workflow Reverse Engineering & KIYA Alignment
- **Status:** Complete / Reference Analysis
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026)
- **Primary Technical Evidence Baseline:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` (ERPNext reference tree `references/erpnext-develop/`, v17.0.0-dev, GPLv3)
- **Governance & Process Controls:** `AGENTS.md`, `.kiya/AI-CONTEXT.md`, `.kiya/AI-DECISIONS.md`, `docs/PROJECT-STATE.md`, `docs/00-requirements/04-business-flows.md`, `docs/00-requirements/06-open-questions.md`, `docs/00-requirements/15-critical-clarification-plan.md`

### Strict Anti-Hallucination & Evidence Rules
1. **Classification Standard:**
   - `BRD-REQUIRED`: Explicitly mandated by KIYA BRD v2.0.
   - `BRD-DERIVED`: A necessary, explained logical consequence of explicit BRD requirements.
   - `ERPNext-REFERENCE`: Observed workflow, document sequence, or mechanism in the ERPNext reference baseline (Document 21).
   - `ERPNext-SPECIFIC`: Mechanism, status, or design unique to ERPNext that must NOT automatically become a KIYA requirement.
   - `PROPOSED`: Potential implementation/architecture option; non-binding.
   - `TBD`: Gaps, missing rules, or unresolved business questions where evidence is insufficient.
   - `OUT-OF-SCOPE`: Explicitly excluded from Phase 1 by the BRD.
2. **Platform & Architecture Neutrality:** This document does NOT constitute an approved architecture decision or platform selection. ERPNext is an external reference system, not KIYA's specification.
3. **No Unilateral Approvals:** Open questions (OQ-001 through OQ-015) remain unresolved until formally approved via the Clarification Decision framework (`16-clarification-decision-register.md`).

---

## 2. Match Level Definitions

To maintain absolute precision in comparing KIYA requirements with ERPNext capabilities, the following match levels are strictly applied:

| Match Level | Definition |
| --- | --- |
| **Exact Match** | Document concepts, stages, and business intent align directly without structural modification (subject to KIYA naming/field governance). |
| **Partial Match** | Core transactional flow exists, but significant conceptual differences, missing documents, different stage sequencing, or unresolved KIYA business logic exist. |
| **Weak / Analogous Match** | High-level business intent is similar, but underlying mechanisms, doc types, or data structures are fundamentally different or decoupled. |
| **Missing / Absent** | Capability is required by the KIYA BRD but is absent from the analyzed ERPNext reference repository. |
| **Framework-Owned** | Capability belongs to Frappe Framework (outside the ERPNext repository) and is not provided directly by ERPNext business logic. |

---

## 3. Core Business Workflow Alignment

### 3.1 Customer-to-Cash (C2C) Flow Alignment

**BRD Baseline Sequence (`docs/00-requirements/04-business-flows.md` §1):**
`Lead → Opportunity → Enquiry → Quotation → Sales Order → Availability Check → Inventory → MRP / Planning → Production → Quality Check → Warehouse → Dispatch → Invoice → Tax → Payment → Accounting → Profitability → Customer History`

**ERPNext Reference Sequence (`docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` WF-01, WF-02, WF-03, WF-04, WF-08, WF-09, WF-10, WF-12, WF-13):**
`Lead → Opportunity → Quotation → Sales Order → [Stock Reservation Entry / Pick List] → Delivery Note → Sales Invoice → Payment Entry → GL Entry / Payment Ledger Entry` (with asynchronous/parallel links to Production Plan, Work Order, Stock Entry, and Quality Inspection).

#### Detailed Stage-by-Stage Comparison Matrix

| Flow Stage | KIYA BRD Requirement & Evidence | ERPNext Equivalent & Reference Evidence | Match Level | Key Differences & Missing Capabilities | Related KIYA OQs / CDs | Classification | Reuse Consideration |
|---|---|---|---|---|---|---|---|
| **1. Lead** | Capture prospective buyers, multi-channel intake, lead scoring (BRD §6.1, §7.2; FR-CRM-001, FR-CRM-002) | `Lead` (`crm/doctype/lead/`) mapped via `lead/mapper.py` (Doc 21 §WF-01) | Partial Match | ERPNext Lead has basic status/qualification; lacks KIYA advanced scoring, omnichannel campaign intake, and AI scoring out-of-the-box. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Candidate for isolated reuse/adaptation of Lead master. |
| **2. Opportunity** | Track qualified deal, value, pipeline stage, win probability (BRD §6.1, §7.2; FR-CRM-003) | `Opportunity` (`crm/doctype/opportunity/`) with `Opportunity Item` (Doc 21 §WF-01) | Exact Match | Conceptually identical; ERPNext tracks opportunity items, stage, and probability. Status updater maintains state. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for direct reuse with KIYA pipeline extensions. |
| **3. Enquiry** | Formal customer request for technical specs/quote (BRD §6.1, §7.3; FR-SALES-001) | **None.** No separate `Enquiry` DocType exists in ERPNext reference tree (Doc 21 §WF-01, structural inventory). ERPNext maps `Opportunity.name` into `Quotation.enq_no`. | Missing / Absent | Major structural gap. KIYA treats Enquiry as a distinct document stage between Opportunity and Quotation. ERPNext collapses Enquiry into Opportunity. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (absence) | KIYA must build a dedicated Enquiry entity/DocType or formally resolve enquiry semantics via CD. |
| **4. Quotation** | Multi-currency, tiered pricing, discount approvals, versioning (BRD §6.1, §7.3; FR-SALES-002) | `Quotation` (`selling/doctype/quotation/`) with `Quotation Item` (Doc 21 §WF-01) | Partial Match | ERPNext Quotation supports pricing, currency, expiry (`valid_till`), and tax templates. Lacks advanced multi-version comparison/revision history required by enterprise CRM. | OQ-001, OQ-002, OQ-003 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Candidate for reuse with custom pricing and approval logic. |
| **5. Sales Order** | Commercial commitment, credit check, order booking, delivery schedules (BRD §6.1, §7.3; FR-SALES-003) | `Sales Order` (`selling/doctype/sales_order/`) (Doc 21 §WF-01, WF-02) | Partial Match | ERPNext SO supports order items, sales team, delivery dates, and status map. Credit limits handled via Customer master, but approval matrices remain TBD. | OQ-001, OQ-002, OQ-003 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Candidate for core reuse; requires integration with KIYA universal approval engine. |
| **6. Availability Check** | Real-time stock reservation, ATP (Available-to-Promise), warehouse allocation (BRD §6.1, §7.8; FR-SALES-003, FR-INV-002) | `Stock Reservation Entry` (SRE) and `Bin` projected qty (`stock_reservation_entry.py`) (Doc 21 §WF-02, WF-13) | Partial Match | ERPNext SRE exists but is an optional decoupled document. Bin projected qty is a mathematical cache per Item+Warehouse, not a dynamic ATP engine across complex supply chains. | OQ-002, OQ-007 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | SRE pattern can be adapted, but KIYA reservation timing and shortage rules are unresolved (TBD). |
| **7. Inventory** | Stock deduction, batch/serial tracking, multi-warehouse balance (BRD §6.1, §7.8; FR-INV-001–004) | `Stock Ledger Entry` (SLE), `Serial and Batch Bundle`, `Bin` (`stock_ledger.py`) (Doc 21 §WF-12, WF-14) | Exact Match | ERPNext immutable SLE ledger and serial/batch bundling provide robust inventory tracking foundations. | OQ-002, OQ-007 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | High candidate for reuse as backend inventory transaction engine. |
| **8. MRP / Planning** | Material requirement explosion, work order demand, capacity planning (BRD §6.1, §7.11; FR-MRP-001–004) | `Production Plan`, `Master Production Schedule`, `Sales Forecast` (`production_plan.py`) (Doc 21 §WF-08) | Partial Match | ERPNext generates material requests and work orders from SO demand. However, it lacks advanced finite capacity scheduling (APS), constraint-based sequencing, and multi-facility optimization. | OQ-001, OQ-008 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Production Plan can be used as baseline planning document; advanced heuristics require KIYA-owned planning services. |
| **9. Production** | Discrete assembly, BOM execution, operation routing, job cards (BRD §6.1, §7.10; FR-MFG-001–005) | `BOM`, `Work Order`, `Job Card`, `Stock Entry` (Doc 21 §WF-09) | Exact Match | Discrete manufacturing flow in ERPNext is mature: BOM routing, Work Order release, material transfer/consumption, and Job Card time tracking. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for direct reuse for discrete/BOM manufacturing. |
| **10. Quality Check** | In-process & finished goods inspection, sampling, test parameters (BRD §6.1, §7.12; FR-QLTY-001–004) | `Quality Inspection` (`stock/doctype/quality_inspection/`) (Doc 21 §WF-10) | Partial Match | ERPNext supports QI against Job Card and Stock Entry (FG receipt). However, automated inspection gates and non-conformance linkage are weakly coupled. | OQ-001, OQ-009 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse QI structure; build tighter enforcement hooks and KIYA sample plans. |
| **11. Warehouse** | Physical bin management, staging, putaway, picking, packing (BRD §6.1, §7.9; FR-WH-001–004) | `Warehouse`, `Pick List`, `Packing Slip` (`stock/`) (Doc 21 §WF-02, WF-12) | Weak / Analogous Match | **Critical difference:** ERPNext `Warehouse` is a logical ledger node; `Bin` is an item-balance record, NOT a physical aisle/rack/bin location. ERPNext lacks true WMS physical location topologies, 3D slotting, and directed putaway/picking. | OQ-001, OQ-002, OQ-007 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` | ERPNext Warehouse handles accounting/stock ledger only. KIYA WMS bin/location capabilities must be KIYA-owned or heavily customized. |
| **12. Dispatch** | Delivery note generation, packaging, shipping, carrier tracking (BRD §6.1, §7.3, §7.15; FR-SALES-004, FR-LOG-001) | `Delivery Note`, `Delivery Trip` (`stock/doctype/delivery_note/`) (Doc 21 §WF-02) | Partial Match | ERPNext DN updates stock (`StatusUpdater`, SLE) and supports basic delivery trips. Lacks multi-carrier TMS integration, rate shopping, and route optimization. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse Delivery Note for commercial/stock fulfillment; TMS integration owned by KIYA. |
| **13. Invoice** | Commercial billing, progress billing, recurring billing (BRD §6.1, §7.3, §7.17; FR-SALES-005, FR-ACC-002) | `Sales Invoice` (`accounts/doctype/sales_invoice/`) (Doc 21 §WF-03) | Partial Match | ERPNext creates SI from DN or directly from SO (`skip_delivery_note`). Note: ERPNext direct SO→SI billing bypasses dispatch, whereas KIYA core C2C requires dispatch before invoice. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse Sales Invoice core accounting engine; enforce KIYA dispatch-before-billing sequence via workflow constraints. |
| **14. Tax** | Global tax engine, India GST (CGST/SGST/IGST), e-invoicing, e-way bill (BRD §6.1, §7.18; FR-TAX-001–007) | `Sales Taxes and Charges Template` (`taxes_and_totals.py`) (Doc 21 §WF-20) | Weak / Missing (India) | **Critical gap:** ERPNext tree removed India GST/e-invoicing localization (`remove_india_localisation.py`). Generic tax engine is rule/table-based, not an enterprise global rules engine with real-time tax jurisdiction APIs. | OQ-005 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (absence) | Generic tax table logic reusable; Global Tax Engine and India GST/compliance must be KIYA-owned custom app or integration. |
| **15. Payment** | Multi-channel collection, reconciliation, payment allocation (BRD §6.1, §7.17; FR-ACC-004) | `Payment Entry`, `Payment Ledger Entry` (`accounts/doctype/payment_entry/`) (Doc 21 §WF-04) | Exact Match | ERPNext Payment Entry handles AR reconciliation, deductions, advances, multi-currency write-offs, and payment ledger entries robustly. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for direct reuse for AR cash application and payment accounting. |
| **16. Accounting** | Double-entry GL posting, perpetual inventory GL, sub-ledgers (BRD §6.1, §7.17; FR-ACC-001) | `GL Entry`, `general_ledger.py` (`accounts/`) (Doc 21 §WF-04, WF-20) | Exact Match | Fully aligned. ERPNext posts automated debits/credits on SI submit and perpetual inventory postings on DN. Cancel reverses entries. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | High candidate for reuse as underlying GL transaction engine. |
| **17. Profitability** | Order/customer/product profitability, contribution margin (BRD §6.1, §7.22; FR-BI-003) | Standard reports (`gross_profit.py`, etc.) | Weak / Analogous Match | ERPNext provides basic SQL/script reports for gross profit. Lacks multi-dimensional cost allocation, activity-based costing (ABC), and EPM profitability models. | OQ-001, OQ-015 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Gross profit report usable as reference; enterprise profitability engine belongs to KIYA BI/EPM layer. |
| **18. Customer History** | 360-degree timeline, interaction logging, transactional summary (BRD §6.1, §7.2; FR-CRM-004) | `Customer` dashboard and Frappe timeline/activity log | Partial Match | Frappe framework provides document activity timeline. ERPNext Customer dashboard shows transaction counts. Lacks true omnichannel 360 view (support, IoT, field service, AI sentiment). | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Frappe timeline and dashboard can be extended; unified 360 model remains KIYA-owned. |

---

### 3.2 Procure-to-Pay (P2P) Flow Alignment

**BRD Baseline Sequence (`docs/00-requirements/04-business-flows.md` §2):**
`Supplier → RFQ / RFP → Supplier Quotation → Purchase Order → Goods Receipt → Quality Check → Inventory → Supplier Invoice → Tax → Payment → Accounting → Supplier Performance`

**ERPNext Reference Sequence (`docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` WF-05, WF-06, WF-07, WF-10, WF-12, WF-19, WF-20):**
`[Material Request] → Request for Quotation → Supplier Quotation → Purchase Order → Purchase Receipt → [Quality Inspection] → Purchase Invoice → Payment Entry → GL Entry → Supplier Scorecard`

#### Detailed Stage-by-Stage Comparison Matrix

| Flow Stage | KIYA BRD Requirement & Evidence | ERPNext Equivalent & Reference Evidence | Match Level | Key Differences & Missing Capabilities | Related KIYA OQs / CDs | Classification | Reuse Consideration |
|---|---|---|---|---|---|---|---|
| **1. Supplier** | Onboarding, compliance verification, bank details, multi-tier categorization (BRD §6.2, §7.7; FR-SUPM-001, FR-SUPM-002) | `Supplier` (`buying/doctype/supplier/`) | Exact Match | ERPNext Supplier master supports contacts, addresses, payment terms, default accounts, and supplier groups. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Candidate for direct reuse; extend with KIYA vendor onboarding and compliance workflows. |
| **2. RFQ / RFP** | Sourcing requests, complex technical bid evaluations, RFP scoring (BRD §6.2, §7.6; FR-PROC-001, FR-PROC-002) | `Request for Quotation` (`buying/doctype/request_for_quotation/`) (Doc 21 §WF-05) | Partial Match | **Critical difference:** ERPNext has RFQ (price quotation request sent to vendor list). **No RFP DocType** exists in the analyzed tree. RFQ cannot handle multi-envelope technical/commercial proposals or RFP weighted scoring matrices. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (absence of RFP) | RFQ reusable for simple price requests; RFP entity and complex sourcing evaluation must be KIYA-owned. |
| **3. Supplier Quotation** | Vendor proposal capture, comparison matrices, multi-currency quotes (BRD §6.2, §7.6; FR-PROC-003) | `Supplier Quotation` (`buying/doctype/supplier_quotation/`) (Doc 21 §WF-05) | Exact Match | ERPNext captures vendor bids and provides a `supplier_quotation_comparison` report. Supports multi-currency and lead times. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for direct reuse; comparison UI can be enhanced. |
| **4. Purchase Order** | Commercial commitment, approval tiers, budget reservation, milestone schedules (BRD §6.2, §7.6; FR-PROC-004) | `Purchase Order` (`buying/doctype/purchase_order/`) (Doc 21 §WF-05) | Partial Match | ERPNext PO tracks items, prices, required delivery, and status (`per_received`, `per_billed`). Budget checks exist via `budget_controller.py`. Approval limits require Frappe Workflow configuration. | OQ-001, OQ-002, OQ-003 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | High candidate for reuse as purchasing transaction backbone. |
| **5. Goods Receipt** | Inward gate entry, physical receipt, staging, shortage/damage logging (BRD §6.2, §7.6, §7.9; FR-PROC-005, FR-WH-001) | `Purchase Receipt` (`stock/doctype/purchase_receipt/`) (Doc 21 §WF-06) | Exact Match | ERPNext PR records received quantities, inward SLE, provisional accounting GL entries, and rejected warehouse movements. | OQ-001, OQ-002, OQ-007 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for reuse for inventory receiving and provisional accounting. |
| **6. Quality Check** | Receiving inspection, sampling (AQL), quarantine/hold, test certificates (BRD §6.2, §7.12; FR-QLTY-001–003) | `Quality Inspection` (`stock/doctype/quality_inspection/`) (Doc 21 §WF-06, WF-10) | Partial Match | ERPNext allows gating PR submission behind mandatory Quality Inspection (`inspection_required`). Rejection moves stock to rejected warehouse. Lacks statistical sampling (AQL) and skip-lot logic. | OQ-001, OQ-009 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse QI transaction gate; implement AQL sampling and vendor quarantine rules in KIYA. |
| **7. Inventory** | Putaway to storage location, stock valuation update, serial/batch activation (BRD §6.2, §7.8; FR-INV-001–003) | `Stock Ledger Entry` (SLE), `Serial and Batch Bundle` (Doc 21 §WF-12, WF-14) | Partial Match | ERPNext SLE updates inventory balance and moving average/FIFO valuation. Lacks automated WMS directed putaway to physical rack/bin. | OQ-001, OQ-002, OQ-007 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse stock ledger and serial/batch bundling; physical putaway managed separately. |
| **8. Supplier Invoice** | 3-way matching (PO-PR-PI), non-PO invoicing, payment terms, debit notes (BRD §6.2, §7.6, §7.17; FR-PROC-006, FR-ACC-003) | `Purchase Invoice` (`accounts/doctype/purchase_invoice/`) (Doc 21 §WF-07) | Exact Match | ERPNext supports 3-way matching via `po_detail` and `pr_detail` link fields and validation rules in `purchase_invoice.py`. Holds and debit notes supported. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for reuse for AP invoicing and 3-way matching. |
| **9. Tax** | Input Tax Credit (ITC), reverse charge (RCM), withholding tax/TDS, statutory returns (BRD §6.2, §7.18; FR-TAX-001–007) | `Purchase Taxes and Charges Template`, Withholding Tax DocTypes (Doc 21 §WF-20) | Weak / Missing (India) | **Critical gap:** India GST ITC, GSTR-2B reconciliation, and e-invoicing verification are absent from the analyzed ERPNext develop tree (`remove_india_localisation.py`). | OQ-005 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (absence) | Tax calculation engine reusable; statutory tax reconciliation and India localization must be built or integrated independently. |
| **10. Payment** | AP disbursement, bank integration, check printing, batch payments (BRD §6.2, §7.17; FR-ACC-004) | `Payment Entry` (`accounts/doctype/payment_entry/`) (Doc 21 §WF-04) | Exact Match | ERPNext Payment Entry debits supplier, credits bank, reconciles invoices, and handles payment clearing. Plaid sync available. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Strong candidate for direct reuse for AP disbursements and reconciliation. |
| **11. Accounting** | AP GL posting, accrual reversal, exchange gain/loss, trial balance (BRD §6.2, §7.17; FR-ACC-001) | `GL Entry` (`accounts/general_ledger.py`) (Doc 21 §WF-07, WF-20) | Exact Match | Standard double-entry posting: PR creates provisional stock accrual; PI reverses accrual and books AP; Payment clears AP against cash/bank. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | High candidate for reuse as AP accounting ledger engine. |
| **12. Supplier Performance** | Automated scorecard, OTIF (On-Time In-Full), quality ppm, compliance rating (BRD §6.2, §7.7; FR-SUPM-003, FR-SUPM-005) | `Supplier Scorecard` (`buying/doctype/supplier_scorecard/`) (Doc 21 §WF-19) | Partial Match | ERPNext has Supplier Scorecard with daily scheduler refresh. However, scoring variables are ERPNext-specific formulas; KIYA performance metrics and weights are unresolved (TBD). | OQ-001, OQ-010 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (formulas) | Reuse scorecard structure and scheduler hook; scoring algorithms must reflect KIYA CD decisions. |

---

### 3.3 Asset-to-Service (A2S) Flow Alignment

**BRD Baseline Sequence (`docs/00-requirements/04-business-flows.md` §3):**
`Asset / Machine → Installation → Warranty → Service Request → Technician Assignment → Spare Parts → Work Order → Maintenance → Service Invoice → Payment → Asset History`

**ERPNext Reference Sequence (`docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` WF-15, WF-16, WF-17, structural inventory):**
*Fragmented across three disconnected modules:*
- **Assets Module:** `Asset → Asset Depreciation Schedule → Asset Repair → Asset Maintenance Log → Asset Movement` (internal company assets).
- **Support Module:** `Warranty Claim → Issue → Service Level Agreement` (customer helpdesk/claims).
- **Maintenance Module:** `Maintenance Schedule → Maintenance Visit` (customer equipment servicing).
- **Selling Module:** `Installation Note` (delivery installation).

#### Detailed Stage-by-Stage Comparison Matrix

| Flow Stage | KIYA BRD Requirement & Evidence | ERPNext Equivalent & Reference Evidence | Match Level | Key Differences & Missing Capabilities | Related KIYA OQs / CDs | Classification | Reuse Consideration |
|---|---|---|---|---|---|---|---|
| **1. Asset / Machine** | Unified asset registry, serial tracking, internal vs customer asset distinction (BRD §6.3, §7.13; FR-AST-001, FR-AST-002) | `Asset` (`assets/doctype/asset/`) vs `Item` Serial No (Doc 21 §WF-15) | Partial Match | **Critical conceptual split:** ERPNext `Asset` is strictly a *company-owned capitalized asset* subject to depreciation. Customer equipment is tracked merely as a Serial No under Stock/Support, not as an Asset record. | OQ-001, OQ-002, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` | Internal asset lifecycle reusable; customer equipment/installed base model must be unified under KIYA domain model. |
| **2. Installation** | Delivery staging, site commissioning, installation checklist, sign-off (BRD §6.3, §7.14; FR-MFS-001) | `Installation Note` (`selling/doctype/installation_note/`) (Doc 21 structural inventory §Selling) | Weak / Analogous Match | ERPNext Installation Note is a simple selling document recording installed serial numbers from a Delivery Note. Lacks commissioning workflows, checklists, technician sign-off, or warranty activation triggers. | OQ-001, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Minimal reference; KIYA needs a robust Field Service Commissioning/Installation model. |
| **3. Warranty** | Warranty terms, AMC/contract management, coverage validation, expiry alerts (BRD §6.3, §7.13, §7.14; FR-AST-003, FR-MFS-002) | `Warranty Claim` (`support/doctype/warranty_claim/`) and Serial No warranty fields (Doc 21 §WF-17) | Partial Match | ERPNext tracks warranty period on Item/Serial No and records claims. AMC contracts tracked under Maintenance Schedule. Lacks dynamic entitlement checks and tiered SLA coverage. | OQ-001, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reusable data fields on Serial No; contract/warranty entitlement engine requires KIYA build. |
| **4. Service Request** | Multi-channel incident intake, customer portal, fault triage, SLA clock (BRD §6.3, §7.5, §7.14; FR-CS-001, FR-MFS-003) | `Issue` (`support/doctype/issue/`) or `Warranty Claim` (Doc 21 §WF-17) | Partial Match | ERPNext `Issue` has SLA tracking (`service_level_agreement.py`). However, DEC-010 explicitly prohibits mapping Customer Service to A2S without BRD authority. Service Request in A2S is maintenance-oriented. | OQ-001, OQ-011; DEC-010 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse Issue SLA engine, but isolate ticket-to-maintenance dispatch boundary. |
| **5. Technician Assignment** | Skills-based routing, geo-dispatch, technician availability, mobile notification (BRD §6.3, §7.14; FR-MFS-003, FR-MFS-004) | `Maintenance Visit` (`maintenance/doctype/maintenance_visit/`) `assigned_to` field | Missing / Absent | ERPNext has basic user assignment in Maintenance Visit. **Completely missing:** skills-based matching, GPS tracking, territory scheduling, route planning, and mobile field dispatch. | OQ-001, OQ-011, OQ-013 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (absence) | Field technician scheduling and mobile dispatch must be KIYA-owned. |
| **6. Spare Parts** | Truck stock, BOM-to-asset spare parts, reservation, field consumption (BRD §6.3, §7.8, §7.14; FR-INV-001, FR-MFS-004) | `Maintenance Visit Purpose` item table (maintenance) or `Stock Entry` (Doc 21 §WF-16) | Weak / Analogous Match | ERPNext Maintenance Visit lists items/spares inspected or replaced, but does NOT natively execute truck-stock replenishment, mobile field consumption SLEs, or return of defective parts. | OQ-001, OQ-007, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Field spare parts management requires dedicated KIYA integration between Field Service and Stock Entry. |
| **7. Work Order** | Field service work execution, safety checklist, customer sign-off (BRD §6.3, §7.14; FR-MFS-004) | **Naming Collision:** ERPNext `Work Order` belongs strictly to *Manufacturing* (Doc 21 §WF-09). Service work uses `Maintenance Visit` or `Asset Repair` (Doc 21 §WF-16). | Missing / Structural Collision | **Critical architecture hazard:** KIYA A2S requires a Field Service Work Order. ERPNext uses "Work Order" exclusively for discrete factory manufacturing. Reusing ERPNext manufacturing Work Order for field service would corrupt manufacturing logic. | OQ-001, OQ-002, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (collision) | KIYA must establish a distinct `Field Service Work Order` entity separate from manufacturing Work Order. |
| **8. Maintenance** | Preventive schedules, corrective maintenance, breakdown repair, calibration (BRD §6.3, §7.14; FR-MFS-002, FR-MFS-005) | `Maintenance Schedule` (customer) / `Asset Maintenance Log` (internal) (Doc 21 §WF-16) | Partial Match | ERPNext has separate maintenance schedules for customer equipment and internal assets. Supports basic recurring calendar intervals. | OQ-001, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Maintenance schedule structures can be adapted; unify internal vs external maintenance logic. |
| **9. Service Invoice** | Billing labor hours, travel, parts consumed, warranty deduction (BRD §6.3, §7.14, §7.17; FR-MFS-006, FR-ACC-002) | `Sales Invoice` created from `Maintenance Visit` or `Timesheet` (Doc 21 §WF-03, WF-18) | Partial Match | ERPNext can bill customer via Sales Invoice, but lacks automated billing rules combining warranty-covered labor, billable parts, and travel expenses into a single consolidated service invoice. | OQ-001, OQ-002, OQ-011 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Reuse Sales Invoice backend; billing calculator must be KIYA-owned. |
| **10. Payment** | Service payment collection, online field payments, receipts (BRD §6.3, §7.17; FR-ACC-004) | `Payment Entry` (`accounts/doctype/payment_entry/`) (Doc 21 §WF-04) | Exact Match | Reuses standard Payment Entry against the service invoice. | OQ-001, OQ-002 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Direct reuse of Payment Entry. |
| **11. Asset History** | Comprehensive timeline of breakdown, maintenance, parts, costs, MTBF/MTTR (BRD §6.3, §7.13; FR-AST-004, FR-AST-005) | Asset Dashboard (internal) / Serial No log (customer) | Weak / Analogous Match | ERPNext stores discrete maintenance visit logs and repairs, but lacks unified equipment health dashboards, predictive maintenance analytics, and automated MTBF/MTTR calculations. | OQ-001, OQ-011, OQ-014 | `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE` | Asset telemetry, timeline, and reliability metrics must be KIYA-owned. |

---

## 4. Supporting Workflows Alignment

### 4.1 Project-to-Invoice (`Project → Task → Timesheet → Sales Invoice`)
- **KIYA BRD:** Projects, milestones, task tracking, timesheets, project billing, revenue recognition (BRD §7.16; FR-PROJ-001–006).
- **ERPNext Reference (Doc 21 §WF-18):** `Project → Task → Timesheet → Sales Invoice`. Timesheet tracks billable hours and employee; `make_sales_invoice` creates SI child rows; project cost center tracks financials.
- **Match Level:** **Exact Match**.
- **Classification:** `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE`.
- **Reuse Assessment:** Candidate for direct reuse; extend with KIYA milestone billing and resource utilization analytics.

### 4.2 Quality Non-Conformance & CAPA (`Inspection Rejection → NCR → CAPA`)
- **KIYA BRD:** Real-time quality logging, non-conformance records (NCR), corrective/preventive actions (CAPA), vendor quality tracking (BRD §7.12; FR-QLTY-005, FR-QLTY-006).
- **ERPNext Reference (Doc 21 §WF-10, WF-11):** `Quality Inspection` lives under Stock; `Non Conformance`, `Quality Action`, and `Quality Goal` live under `quality_management`.
- **Match Level:** **Weak / Analogous Match**.
- **Critical Difference:** In ERPNext, Quality Inspection rejection does NOT automatically generate a Non Conformance record (no automated link in core header). Non Conformance is primarily a free-text ISO document.
- **Classification:** `BRD-REQUIRED` (KIYA) / `ERPNext-SPECIFIC` (decoupled architecture).
- **Reuse Assessment:** Reuse DocType structures; KIYA must build the automated state machine linking inspection failure to quarantine and CAPA workflow.

### 4.3 Subcontracting Manufacturing Flow
- **KIYA BRD:** Outward subcontracting of operations, component issue, finished goods receipt (BRD §7.10; FR-MFG-004).
- **ERPNext Reference (Doc 21 §Structural Inventory §Subcontracting):** `Subcontracting Order → Subcontracting Receipt`, with `subcontracting_controller.py` handling raw material transfer and FG valuation.
- **Match Level:** **Exact Match**.
- **Classification:** `BRD-DERIVED` (KIYA) / `ERPNext-REFERENCE`.
- **Reuse Assessment:** Strong candidate for direct reuse for external processing workflows.

### 4.4 Transaction Cancellation & Reverse Accounting
- **KIYA BRD:** Platform-wide auditability, error correction, immutable ledger entries, cancellation controls (BRD §7.1, §7.28, §10; FR-PADM-1.4.1, FR-ASC-001).
- **ERPNext Reference (Doc 21 §WF-21):** Document cancellation (`docstatus=2`) posts reverse GL (`make_reverse_gl_entries`) and reverse SLE. Returns handled via separate `is_return` documents.
- **Match Level:** **Exact Match**.
- **Classification:** `BRD-REQUIRED` (KIYA) / `ERPNext-REFERENCE`.
- **Reuse Assessment:** Outstanding accounting and stock cancellation design pattern; candidate for direct adoption across all transactional ledgers.

---

## 5. Synthesis of Critical Gaps & Open Questions

The workflow alignment matrix reveals eight architectural discrepancies that must NOT be smoothed over by assumptions:

1. **Enquiry Document Omission:** ERPNext has no Enquiry DocType. KIYA C2C mandates Lead → Opportunity → Enquiry → Quotation. *Status: TBD (OQ-001, OQ-002).*
2. **RFP Sourcing Gap:** ERPNext buying has RFQ but no RFP DocType for complex multi-attribute bidding. *Status: TBD (OQ-001).*
3. **WMS Physical Topology Mismatch:** ERPNext `Warehouse` is an accounting node and `Bin` is an item-quantity cache. KIYA requires true aisle/rack/bin physical location management. *Status: TBD (OQ-001, OQ-007).*
4. **Asset vs Customer Equipment Duality:** ERPNext `Asset` is strictly company-owned depreciable property. KIYA A2S covers customer assets/machines under service. *Status: TBD (OQ-011).*
5. **Work Order Naming Collision:** In ERPNext, "Work Order" is manufacturing only. KIYA A2S requires a Field Service Work Order. *Status: TBD (OQ-002, OQ-011).*
6. **Statutory Tax Localization Absence:** The ERPNext reference tree explicitly stripped India GST/e-invoice/e-way bill (`remove_india_localisation.py`). *Status: TBD (OQ-005).*
7. **Quality Inspection & NCR Decoupling:** ERPNext Quality Inspection and Non Conformance belong to different modules and lack an automatic transition pipeline. *Status: TBD (OQ-009).*
8. **Direct Billing Sequence Divergence:** ERPNext allows direct `Sales Order → Sales Invoice` bypassing delivery. KIYA core C2C requires physical dispatch before commercial invoicing. *Status: TBD (OQ-002).*

---

## 6. Document Metadata & Traceability

- **Created:** 14 September 2026
- **Baseline Document Reference:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md`
- **Output Artifacts:** Feeds directly into `docs/00-requirements/23-erpnext-kiya-domain-mapping.md`, `24-erpnext-kiya-gap-analysis.md`, and `25-erpnext-reuse-vs-build-boundary.md`.
