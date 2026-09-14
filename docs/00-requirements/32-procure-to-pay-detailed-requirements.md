# KIYA 360 — Procure-to-Pay (P2P) Detailed Requirements Expansion (Batch 2)

## 1. Document Control, Authority & Scope

- **Document ID:** `32-procure-to-pay-detailed-requirements`
- **Phase:** Phase 0B-2 — Detailed Requirements Expansion (Batch 2: Procure-to-Pay)
- **Status:** In Review / Detailed Functional Requirements Baseline (Final Classification Cleanup Completed)
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026: Section 6.1, Section 6.2, Section 7.6, 7.7, 7.8, 7.9, 7.12, 7.17, 7.18, 7.22, Section 8, Section 10)
- **Approved Clarification Decisions:**
  - `CD-001` (`DEC-012`): Hybrid Scope-Expansion Approach — Fully detail the complete BRD P2P core flow; use proven ERP-standard behavior as a traceable reference baseline for non-specified standard mechanics; zero automatic ERPNext coupling; explicit KIYA differentiators and documented exceptions (`docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md`).
  - `CD-002` (`DEC-013`): Operational Business Status Model — Use Business Status representing operational progression; reject ERPNext's dual `docstatus` technical model; progress statuses organically (`docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md`).
- **Dependencies Governed:** `DEP-003` (MRP to Procurement), `DEP-004` (Manufacturing to Quality), `DEP-005` (Order to Billing / Accounting), `DEP-006` (Procurement to Supplier Management), `DEP-007` (Procurement to Inventory/Warehouse), `DEP-008` (Procurement to Finance & Tax).
- **Reference Evidence Baseline:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` through `27-erpnext-analysis-review.md`.

---

### 1.1 Classification Discipline & Working Principles

In strict compliance with repository governance (`AGENTS.md`, `docs/00-requirements/12-requirement-status-legend.md`, and `CD-001`), this detailed expansion enforces five discrete levels of requirements authority:

1. **`BRD-REQUIRED`:** Core capabilities, functional entities, and flow stages explicitly mandated by BRD v2.0 (e.g., Supplier, Supplier Sourcing, RFQ/RFP, Supplier Quotation, Purchase Order, Goods Receipt, Quality Gate, Inventory Putaway, Supplier Invoice / 3-Way Match, Global Tax Engine, Payment, and Supplier Performance).
2. **`BRD-DERIVED`:** Behaviors and rules that are necessary logical consequences of an explicit BRD mandate (e.g., matching invoice quantities against goods receipt records, reversing provisional purchase accruals upon billing, decrementing open order balances on receipt), where the exact implementation mechanism is not explicitly dictated by the BRD.
3. **`ERP-REFERENCE`:** Proven enterprise/ERP standard patterns (reverse-engineered from ERPNext in Docs 21–27) adopted as a baseline to accelerate functional definition. These are reference baselines and **must never silently become binding KIYA requirements** without formal ratification.
4. **`PROPOSED`:** Reasonable candidate business rules, field validations, configuration thresholds, or high-value differentiators (such as multi-envelope RFP evaluations or automated Quality Inspection rejection to NCR generation) designed to complete the functional specification, pending formal stakeholder confirmation.
5. **`TBD`:** Functional ambiguities, statutory mechanics, or policy choices requiring formal stakeholder clarification (e.g., open questions `OQ-003` through `OQ-015`) before they can be treated as confirmed requirements.

**Operational Business Status Discipline (`CD-002`):**
In accordance with `CD-002` (`DEC-013`), KIYA 360 uses operational **Business Status** as its primary lifecycle model, discarding ERPNext's technical `docstatus` (Draft/Submitted/Cancelled) paradigm. The status values listed under each stage below represent **Candidate Operational Lifecycles (`PROPOSED`)** subject to final tenant workflow configuration; they are not rigid, frozen database enumerations.

**Unified Data Model Discipline (`DEC-007`):**
Master entities (`Supplier Master`, `Item Master`, `Warehouse Master`, `Company Master`, `Tax Template`, `Chart of Accounts`, `Currency Master`, `UOM Master`) are strictly unified across all 12 stages and must never be duplicated across module boundaries.

---

## 2. Procure-to-Pay Flow Overview & Architectural Spine

The Procure-to-Pay (P2P) business flow is the operational procurement and supply backbone of KIYA 360. As mandated by BRD §6.1, it spans 12 distinct stages across 8 functional modules, unifying Supplier Management, Sourcing, Purchasing, Receiving, Quality Control, Physical Warehousing, Accounts Payable, Tax Compliance, and Analytics:

```
+-------------+     +----------------------+     +---------------+     +--------------------+
| 1. Supplier | --> | 2. Supplier Sourcing | --> | 3. RFQ / RFP  | --> | 4. Supplier Quote  |
+-------------+     +----------------------+     +---------------+     +--------------------+
                                                                                  |
+---------------------+     +--------------------+     +--------------------------+
| 8. Inventory Putaway| <-- | 7. Quality Gate    | <-- | 6. Goods Receipt / Inward| <-- (5. Purchase Order)
+---------------------+     +--------------------+     +--------------------------+
          |
          v
+---------------------+     +--------------------+     +--------------------------+
| 9. Supplier Invoice | --> | 10. Tax (ITC & RCM)| --> | 11. Payment Disbursement |
|    (3-Way Match)    |     +--------------------+     +--------------------------+
+---------------------+                                             |
          |                                                         v
          +--------------------------------------------> +--------------------------+
                                                         | 12. Supplier Performance |
                                                         +--------------------------+
```

### 2.1 Master Data vs. Transaction Data in P2P
- **Unified Master Data (`DEC-007`):**
  - `Supplier Master` (`FR-PADM-1.4.2` / `FR-SUPM-001`): Unified single vendor entity across Purchasing, Accounts Payable, Quality Audits, and Scorecards.
  - `Item Master` (`FR-PADM-1.4.3` / `FR-INV-001`): Unified purchased item/service definition across procurement, inventory valuation, inspection templates, and billing.
  - `Warehouse Master` (`FR-WH-001`): Logical stores, receiving bays, inspection quarantine holding zones, and physical storage locations.
  - `Company & Branch Master` (`FR-PADM-1.1.1`, `FR-PADM-1.1.2`): Multi-entity operating units, billing addresses, and GSTIN registration contexts.
  - `Tax Template & Chart of Accounts` (`FR-PADM-1.4.5`, `FR-FIN-001`): Unified tax accounts, Input Tax Credit (ITC) ledgers, and Accounts Payable liability accounts.
- **Transaction Data Records:**
  `Supplier Registration`, `Sourcing Requirement`, `Request for Quotation (RFQ)`, `Request for Proposal (RFP)`, `Supplier Quotation`, `Purchase Order`, `Goods Receipt (Inward Delivery Note)`, `Quality Inspection`, `Warehouse Putaway Task`, `Supplier Invoice`, `Payment Entry`, `GL Entry`, `Stock Ledger Entry`, `Supplier Scorecard Record`.

---

## 3. Detailed Requirements per P2P Stage

---

### Stage 1: Supplier Master & Registry
- **Requirement ID:** `DR-P2P-001`
- **Phase 0A Baseline ID:** `FR-SUPM-001` (Supplier Master), `FR-SUPM-002` (Onboarding & Compliance)
- **Module:** Supplier Management | **Sub-Module:** Vendor Master & Lifecycle Management
- **BRD Source:** BRD §6.1, §6.2, §7.7; FR-SUPM-001, FR-SUPM-002
- **Stage Classification:** `BRD-REQUIRED` (Core Entity & Master Data Anchor)
- **1. Purpose & Objective:** Maintain a single, authoritative, multi-entity master record for every external vendor, contractor, and service provider, capturing commercial, statutory, banking, and compliance attributes.
- **2. Actors & Roles:** Procurement Officer, Vendor Onboarding Specialist, Accounts Payable Manager, Compliance Officer.
- **3. Preconditions:** Company Master active; Country, Currency, and Tax classification tables configured.
- **4. Inputs:** Legal vendor name, trade name, tax registration number (GSTIN / PAN / VAT / Tax ID), corporate address, contact persons (name, phone, email), bank account details (IFSC, SWIFT, IBAN), standard payment terms, default currency, supplier classification category.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages complete supplier profile and contact directory (`FR-SUPM-001`).
  - `[BRD-REQUIRED / Unified Data Model DEC-007]` Provides a single unified supplier record utilized across Purchasing, Accounts Payable, Quality, and Scorecards without data duplication.
  - `[BRD-REQUIRED]` Captures statutory tax identification numbers and verifies GSTIN format (`FR-SUPM-002`, `FR-TAX-003`).
  - `[PROPOSED / Reference Baseline]` Maintains multiple remittance bank accounts, designating a primary active account for electronic AP disbursements.
  - `[PROPOSED / Reference Baseline]` Associates default commercial parameters (payment terms, incoterms, price lists).
- **6. Business Rules:**
  - `[BRD-REQUIRED / DEC-007]` Single Master Rule: A vendor record exists once globally; branch/multi-entity associations link to the unified master.
  - `[PROPOSED / Reference Baseline]` Duplicate Detection Rule: System warns if tax ID matches an existing supplier master record.
  - `[PROPOSED Policy / TBD]` Status-Based Sourcing Restrictions: Restricting procurement actions against vendors marked `On Hold` or `Blocked` is governed by configurable vendor management policy (`TBD`).
- **7. Validations:**
  - `[BRD-REQUIRED / FR-TAX-003]` Statutory format validation on tax identification strings (e.g. 15-digit alphanumeric GSTIN structure for Indian entities).
  - `[PROPOSED / Standard Validation]` Bank account number and routing code format verification before enabling electronic disbursements.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Lifecycle (`PROPOSED`):* `Prospect / Draft` → `Under Compliance Review` → `Approved / Active` → `Suspended / On Hold` (or `Deactivated / Blacklisted`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Supplier` (`buying/doctype/supplier/`), child tables `Supplier Address`, `Supplier Contact`, and link to `Party Account`.
  - *Adoption Assessment:* Core supplier entity fields, payment terms linkage, and bank account mapping adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Core Requirement:* Deep unification across P2P transactions and supplier portal synchronization (`FR-SUPM-004`).
- **10. Cross-Module Handoffs:** Provides vendor identity and default terms to RFQ/RFP (Stage 3), Purchase Orders (Stage 5), Invoicing (Stage 9), and Payments (Stage 11) (`DEP-006`, `DEP-008`).
- **11. Audit & Security:** All profile edits, bank account changes, and status transitions logged to immutable audit trail (`FR-PADM-1.8.2`, `SF-008`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Notification sent to AP team when supplier bank account details are modified.
  - `[PROPOSED / Subject to OQ-003]` Supplier approval workflow required before transitioning from `Under Review` to `Approved`.
- **13. Documents & Attachments:** Supports attachment of tax registration certificates, bank verifications, compliance certifications, and non-disclosure agreements (`FR-DMS-001`).
- **14. Cancellation & Deactivation:**
  - `[PROPOSED / Reference Baseline]` Deactivating a supplier restricts new PO generation while permitting settlement of open invoices per configured policy.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Subject to Tax Policy]` Missing statutory tax identification flags compliance exceptions prior to vendor approval.
- **16. Reporting & KPI Implications:** Feeds supplier count by category, geographic distribution, and compliance reporting (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Given valid vendor input with unique tax ID, when submitted, an active Supplier Master record is created.
  - System provides status controls to prevent selection of inactive or blocked suppliers on new commercial purchase orders per configured supplier status policies.

---

### Stage 2: Supplier Sourcing & Qualification
- **Requirement ID:** `DR-P2P-002`
- **Phase 0A Baseline ID:** `FR-SUPM-002` (Onboarding & Compliance), `FR-PROC-001` (Purchase Requisitions)
- **Module:** Procurement / Supplier Management | **Sub-Module:** Strategic Sourcing & Discovery
- **BRD Source:** BRD §6.1, §6.2, §7.6, §7.7; FR-SUPM-002, FR-PROC-001; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Explicit Flow Stage in BRD §6.1)
- **1. Purpose & Objective:** Identify prospective supply sources, evaluate vendor manufacturing/service capability, qualify vendors against technical and financial standards, and pool candidates for tendering.
- **2. Actors & Roles:** Strategic Sourcing Specialist, Category Manager, Procurement Director.
- **3. Preconditions:** Item Master active; supplier categories defined; internal purchase demand established or strategic sourcing campaign initiated.
- **4. Inputs:** Sourcing requirement, target item/commodity categories, estimated annual spend, technical capability criteria, quality certification requirements, geographical constraints.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages supplier discovery and qualification pipelines (`FR-SUPM-002`).
  - `[BRD-DERIVED]` Groups suppliers into approved vendor lists (AVL) per product category or commodity code.
  - `[PROPOSED / Business Workflow]` Evaluates supplier capability questionnaires, financial solvency indicators, and compliance documents before inviting vendors to bid.
  - `[BRD-DERIVED]` Links MRP shortage demands or approved internal Purchase Requisitions (`FR-PROC-001`) to eligible qualified vendor groups.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline Policy]` Regulated or engineered components may only be sourced from pre-qualified suppliers on the Approved Vendor List.
  - `[PROPOSED Policy / TBD]` Re-qualification intervals: Supplier qualifications expire periodically (e.g. annually) requiring compliance document refresh (`TBD`).
- **7. Validations:** Sourcing candidate must be mapped to at least one valid Item Master category or commodity group.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Sourcing Project Status (`PROPOSED`):* `Initiated` → `Supplier Discovery` → `Evaluation / Auditing` → `Qualified` (or `Rejected / Ineligible`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Finding (Doc 21 §WF-05, Doc 24 §06):* **ERPNext has NO dedicated Sourcing or Qualification DocType.** ERPNext collapses sourcing directly into creating an RFQ against existing supplier records.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA explicitly mandates `Supplier Sourcing` as a distinct upstream operational stage preceding tendering, managing capability vetting and qualification.
- **10. Cross-Module Handoffs:** Qualified vendor pool feeds directly into RFQ / RFP generation (Stage 3) (`DEP-006`).
- **11. Audit & Security:** Qualification scoring, evaluator notes, and audit sign-offs preserved in audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-003]` Formal qualification sign-off by Quality Assurance for safety-critical component categories.
- **13. Documents & Attachments:** Quality audit reports, facility inspection checklists, financial statements, and certifications.
- **14. Cancellation & Archive:** Sourcing projects may be cancelled prior to tendering without affecting master data.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Failed supplier audits route to qualification review and notify the sourcing team.
- **16. Reporting & KPI Implications:** Sourcing cycle time, qualification pass rate, and vendor diversity metrics (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System enables logging sourcing criteria and shortlisting qualified vendors against specific item categories.
  - System supports filtering and shortlisting qualified vendors from the approved pool for category solicitations per configured sourcing rules.

---

### Stage 3: Request for Quotation & Request for Proposal (RFQ / RFP)
- **Requirement ID:** `DR-P2P-003`
- **Phase 0A Baseline ID:** `FR-PROC-002` (RFQ & RFP Management)
- **Module:** Procurement | **Sub-Module:** Tendering & Sourcing Solicitations
- **BRD Source:** BRD §6.1, §6.2, §7.6; FR-PROC-002; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Explicit BRD Flow Stage & Dual Sourcing Mechanism)
- **1. Purpose & Objective:** Solicit competitive commercial price quotes (via RFQ) for standard goods or detailed technical/commercial proposals (via RFP) for complex engineering, capital assets, or services.
- **2. Actors & Roles:** Procurement Officer, Sourcing Manager, Technical Evaluator.
- **3. Preconditions:** Sourcing pool qualified (Stage 2) or active suppliers exist; Purchase Requisitions approved or item specifications defined.
- **4. Inputs:** Requisition reference (optional), target supplier list, requested items/services, quantities, technical drawings/BOQ, delivery deadlines, bid submission deadline (`bid_closing_date`), terms and conditions.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Supports dual tendering mechanisms: standard Request for Quotation (RFQ) and complex Request for Proposal (RFP) (`FR-PROC-002`).
  - `[BRD-DERIVED]` Ingests line items and quantities from upstream Purchase Requisitions (`FR-PROC-001`) or MRP demands (`FR-MRP-002`).
  - `[ERP-REFERENCE]` Dispatches solicitation packages to selected qualified suppliers via email or supplier portal.
  - `[PROPOSED / KIYA Differentiator]` For RFPs: Supports multi-envelope submissions (technical proposal separate from commercial bid) to enable blinded technical evaluations.
  - `[PROPOSED / Configurable Mechanics]` Enforces submission deadlines, locking portal submissions past bid closing date unless deadline is extended.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline]` An RFQ/RFP may be sent to a designated minimum number of suppliers (e.g. minimum 3) based on company procurement policy (`TBD`).
  - `[PROPOSED Policy / TBD]` For RFPs: Commercial price bids remain sealed until technical qualification threshold is cleared per configured tender rules (`TBD`).
- **7. Validations:** Submission deadline must be future-dated; target supplier list must contain at least one active supplier.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Solicitation Status (`PROPOSED`):* `Draft` → `Published / Sent` → `Bidding Open` → `Bidding Closed` → `Evaluated` (or `Cancelled`).
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext `Request for Quotation` (`buying/doctype/request_for_quotation/`) sends emails to suppliers and provides vendor web forms.
  - *Critical Architectural Gap (Doc 21 §WF-05, Doc 22 §3.2, Doc 24 §06):* **ERPNext has NO RFP DocType.** ERPNext only supports simple item/quantity price requests (RFQ) and lacks multi-envelope tendering, statement-of-work bidding, and RFP evaluation structures.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA explicitly mandates both RFQ and RFP. Standard price requests leverage RFQ mechanics (`ERP-REFERENCE`), while complex tendering incorporates dedicated RFP multi-envelope evaluation workflows (`PROPOSED / KIYA Differentiator`).
- **10. Cross-Module Handoffs:** Generates downstream Supplier Quotations (Stage 4) upon bid receipt (`DEP-006`).
- **11. Audit & Security:** All solicitation distributions, deadline extensions, and vendor communications logged (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Bid reminder notifications to vendors prior to closing deadline.
  - `[PROPOSED / Subject to OQ-003]` Sourcing solicitation approval required for high-value tenders.
- **13. Documents & Attachments:** Technical specifications, CAD sketches, statements of work (SOW), and non-disclosure agreements.
- **14. Cancellation & Amendment:** Solicitation can be amended with notification to all bidders prior to deadline.
- **15. Exceptions & Failure Paths:** If zero bids are received by deadline, system alerts sourcing officer to re-solicit or extend deadline.
- **16. Reporting & KPI Implications:** RFQ response rates, bid turnaround times, and competitive bidding coverage ratios (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System generates RFQ/RFP records linked to item specifications and dispatches to multiple designated vendors.
  - System enforces submission deadline controls, transitioning the solicitation status according to configured bidding rules.

---

### Stage 4: Supplier Quotation & Bid Evaluation
- **Requirement ID:** `DR-P2P-004`
- **Phase 0A Baseline ID:** `FR-PROC-003` (Supplier Quotations & Evaluation)
- **Module:** Procurement | **Sub-Module:** Bid Capture & Comparative Evaluation
- **BRD Source:** BRD §6.1, §6.2, §7.6; FR-PROC-003; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Flow Stage)
- **1. Purpose & Objective:** Capture vendor commercial proposals, evaluate multi-vendor bids side-by-side across price, lead time, and technical capability, and recommend winning bids for purchase commitment.
- **2. Actors & Roles:** Procurement Officer, Technical Evaluator, Sourcing Committee Member.
- **3. Preconditions:** Published RFQ/RFP (Stage 3) active; supplier responses received (or direct unsolicited quote logged).
- **4. Inputs:** Linked RFQ/RFP reference, supplier reference, item rates, currency, quantity price breaks, taxes, lead times, payment terms, quote validity date (`valid_till`), technical scores.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Captures detailed supplier quotes manually or via vendor portal integration (`FR-PROC-003`, `FR-SUPM-004`).
  - `[ERP-REFERENCE]` Generates side-by-side comparative bid matrices normalizing currencies and payment terms.
  - `[PROPOSED / Configurable Analytics]` Calculates total cost of ownership (TCO), factoring freight, taxes, and payment discounts.
  - `[PROPOSED / Reference Baseline]` Flags lowest bid (L1) and highlights variances against historical purchase rates.
  - `[BRD-DERIVED]` Triggers award recommendation, enabling creation of downstream Purchase Order.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline]` Expired quotes cannot be converted to Purchase Orders unless validity date is explicitly extended.
  - `[PROPOSED Policy / TBD]` Multi-criteria weighted scoring: For RFPs, winning bid selection combines technical evaluation score and commercial price score based on configured weighting policies (`TBD`).
- **7. Validations:** Quoted quantities must be positive; rates must be non-negative; currency must be active in Currency Master (`FR-PADM-1.4.6`).
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Bid Status (`PROPOSED`):* `Draft / Received` → `Under Evaluation` → `Shortlisted` → `Awarded` (or `Rejected` / `Expired`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Supplier Quotation` (`buying/doctype/supplier_quotation/`) and `supplier_quotation_comparison` report.
  - *Adoption Assessment:* Quote capture, line structure, and basic comparison matrix adopted as proven reference baseline (`ERP-REFERENCE`).
  - *KIYA Planned Enhancements:* Multi-attribute weighted scoring and TCO modeling are classified as `PROPOSED / KIYA Enhancements`.
- **10. Cross-Module Handoffs:** Awarded quote converts directly to Purchase Order (Stage 5) (`DEP-006`).
- **11. Audit & Security:** Bid comparisons, evaluation scores, and selection justifications preserved immutably (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-003]` Sourcing committee award approval required for orders exceeding authorized procurement thresholds.
  - `[PROPOSED / Subject to OQ-004]` Regret notifications dispatched to unsuccessful bidders upon PO release.
- **13. Documents & Attachments:** Vendor quotation PDFs, technical compliance sheets, and warranty certificates.
- **14. Cancellation & Rejection:** Unsuccessful quotes are marked `Rejected` with recorded justification.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Subject to Budget Policy]` If bids exceed planned budget limits, the system supports price negotiation or tender cancellation workflows.
- **16. Reporting & KPI Implications:** Price variance against standard cost, procurement savings realized, and vendor participation metrics (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Submitting supplier quotations against an RFQ renders a normalized side-by-side comparison matrix.
  - Selecting an awarded quote enables generation of a draft Purchase Order copying line items and rates.

---

### Stage 5: Purchase Order Commitment & Scheduling
- **Requirement ID:** `DR-P2P-005`
- **Phase 0A Baseline ID:** `FR-PROC-004` (Purchase Orders & Commitments)
- **Module:** Procurement | **Sub-Module:** Purchase Order Booking & Contract Commitment
- **BRD Source:** BRD §6.1, §6.2, §7.6; FR-PROC-004; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Transaction & Contractual Commitment)
- **1. Purpose & Objective:** Issue formal purchase orders recording the approved commercial commitment to suppliers, lock commercial pricing and delivery schedules, commit company budget, and govern fulfillment tracking.
- **2. Actors & Roles:** Procurement Officer, Purchasing Manager, Commercial Director, Finance Controller.
- **3. Preconditions:** Supplier Master active; Item Master active; approved Supplier Quotation, approved Purchase Requisition, or direct procurement authorization.
- **4. Inputs:** Supplier reference, Supplier Quotation reference, order date, delivery schedule per item, ship-to warehouse location, bill-to company context, line items (codes, descriptions, quantities, UOM, agreed rates, discounts), tax template, payment terms, incoterms.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Generates formal Purchase Orders locking items, rates, terms, and delivery milestones (`FR-PROC-004`).
  - `[BRD-DERIVED]` Links upstream to Supplier Quotation, Purchase Requisition, or MRP demand record.
  - `[ERP-REFERENCE]` Tracks fulfillment and billing completion indicators in real time (`per_received`, `per_billed`).
  - `[PROPOSED / Reference Baseline]` Enforces committed budget reservation checks against departmental cost centers.
- **6. Business Rules:**
  - `[PROPOSED / Subject to OQ-003 Approval Policies]` Purchase orders exceeding standard delegation of authority thresholds trigger multi-tier approval workflows (`OQ-003`).
  - `[BRD-REQUIRED / Unified Data Model DEC-007]` Vendor details and item codes must strictly reference unified master records.
  - `[PROPOSED Policy / TBD]` Re-negotiation of unit rates post-approval requires formal PO amendment versioning (`TBD`).
- **7. Validations:** Required delivery date must be on or after order date; item warehouse must be a valid, active warehouse node.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Order Status (`PROPOSED`):* `Draft` → `Pending Approval` → `Approved / Ordered` → `Partially Received` → `Completed / Closed` (or `On Hold` / `Cancelled`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Purchase Order` (`buying/doctype/purchase_order/`) with child table `Purchase Order Item`.
  - *Adoption Assessment:* PO structure, child item mapping, and receiving/billing progress tracking adopted as reference baseline (`ERP-REFERENCE`).
  - *Approval Integration:* Multi-tier workflow authorization mapped to Frappe Workflow / KIYA Workflow engine (`DEP-010`).
- **10. Cross-Module Handoffs:** Authorizes Goods Receipt (Stage 6) and establishes expected liability for 3-Way Match (Stage 9) (`DEP-006`, `DEP-007`, `DEP-008`).
- **11. Audit & Security:** Versioning snapshots on amendment; all approval actions logged with timestamps and user roles (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-003]` Hierarchical approval workflow based on total PO monetary value.
  - `[PROPOSED / Subject to OQ-004]` PDF PO dispatch to supplier contact upon final approval.
- **13. Documents & Attachments:** Commercial terms, detailed technical annexures, and purchase agreement contracts (`FR-DMS-001`).
- **14. Cancellation & Amendment:** Orders can be cancelled if no downstream Goods Receipt has been submitted.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Subject to approval and budget policy]` Handling of budget overruns is governed by configured organizational approval and budget policies (unresolved details governed under `OQ-003`).
- **16. Reporting & KPI Implications:** Open procurement commitments, purchase order cycle time, and spend by supplier/category (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Approving a Purchase Order locks line pricing and makes quantities available for inward receiving at designated warehouses.
  - System enforces receiving and billing limits against the PO in accordance with configured tolerance settings.

---

### Stage 6: Goods Receipt & Inward Gate Entry
- **Requirement ID:** `DR-P2P-006`
- **Phase 0A Baseline ID:** `FR-PROC-005` (Goods Receipt / Inward), `FR-WH-001` (Warehouse Hierarchy)
- **Module:** Procurement / Warehouse | **Sub-Module:** Inbound Receiving & Physical Intake
- **BRD Source:** BRD §6.1, §6.2, §7.6, §7.9; FR-PROC-005, FR-WH-001; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Operational Flow Stage)
- **1. Purpose & Objective:** Record the physical arrival of purchased materials at the warehouse gate, verify received packages against the Purchase Order, stage goods in the receiving bay, and initiate quality inspection.
- **2. Actors & Roles:** Gate Security Guard, Receiving Clerk, Warehouse Inward Supervisor.
- **3. Preconditions:** Approved Purchase Order in active status (`Approved / Ordered`).
- **4. Inputs:** Purchase Order reference, supplier delivery challan / packing slip number and date, carrier name, vehicle number, received item codes, arrived quantities, rejected on arrival (damaged packaging), target receiving warehouse/bay.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Logs physical material inward arrival against open Purchase Orders (`FR-PROC-005`).
  - `[BRD-DERIVED]` Pulls line items, agreed quantities, and prices from source PO child rows (`po_detail`).
  - `[BRD-DERIVED]` Updates Purchase Order `received_qty` and fulfillment status.
  - `[ERP-REFERENCE / Accounting Practice]` Posts provisional accounting accrual GL entries (Debits Stock Received But Not Billed / GRNI Accrual, Credits Provisional Accounts Payable).
  - `[BRD-DERIVED]` Segregates items requiring quality inspection and holds them in an Inward Inspection / Quarantine Warehouse.
- **6. Business Rules:**
  - `[PROPOSED / Configurable Policy]` Over-Receipt Policy: Receiving quantities exceeding PO ordered balance is governed by a configurable over-receipt tolerance percentage (`TBD`).
  - `[BRD-DERIVED]` Direct stock release: Items flagged as requiring quality inspection cannot be received directly into sellable inventory without Stage 7 sign-off.
- **7. Validations:** Received quantity cannot exceed PO open balance plus allowed over-receipt tolerance; supplier challan reference required.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Receipt Status (`PROPOSED`):* `Draft / Gate Logged` → `Received in Bay` → `Pending Inspection` → `Accepted & Staged` (or `Rejected at Gate` / `Cancelled`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Purchase Receipt` (`stock/doctype/purchase_receipt/`), updating `po_detail` and executing provisional GL postings (`stock_controller.py`).
  - *Adoption Assessment:* Inward receiving data structure, child link mapping (`po_detail`), and provisional stock ledger accounting adopted as reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Routes goods to Inward Quality Gate (Stage 7) or directly to Putaway (Stage 8) if inspection is not required (`DEP-004`, `DEP-007`).
- **11. Audit & Security:** Gate timestamps, vehicle numbers, and physical count verifications logged to immutable audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Inward arrival triggers inspection notification to the Quality team.
- **13. Documents & Attachments:** Supplier delivery challan copy, bill of lading, and physical package inspection photos (`FR-DMS-001`).
- **14. Cancellation & Return:** Submitting a Goods Receipt cancellation generates reversing stock and provisional GL ledger entries.
- **15. Exceptions & Failure Paths:** Severe packaging damage upon arrival allows gate rejection with return-to-vendor documentation.
- **16. Reporting & KPI Implications:** Inward dock-to-stock turnaround time, supplier shipment timeliness, and receipt discrepancies (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Submitting a Goods Receipt updates the PO's received quantity and creates an inward stock holding entry in the receiving/inspection warehouse.
  - Receiving quantities exceeding ordered balances are validated against configured over-receipt tolerance parameters.

---

### Stage 7: Inward Quality Gate & Inspection
- **Requirement ID:** `DR-P2P-007`
- **Phase 0A Baseline ID:** `FR-QLTY-001` (Inspection Templates), `FR-QLTY-002` (Incoming QC), `FR-QLTY-006` (NCR/CAPA)
- **Module:** Quality | **Sub-Module:** Incoming Inspection Gating & Non-Conformance Disposition
- **BRD Source:** BRD §6.1, §6.2, §7.12; FR-QLTY-001, FR-QLTY-002, FR-QLTY-006; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Inward Quality Gate)
- **1. Purpose & Objective:** Inspect incoming materials against defined engineering specifications, physical tolerances, and chemical/dimensional standards, gating stock putaway and segregating non-compliant materials.
- **2. Actors & Roles:** Inward Quality Inspector, QA Lead, Material Review Board (MRB) Chair.
- **3. Preconditions:** Goods Receipt record submitted; material held in Inward Inspection bay.
- **4. Inputs:** Reference Goods Receipt ID, Purchase Order reference, Item Master, lot/batch number, inspection template, sample size, observed test parameter readings.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Performs quality inspections against pre-configured item inspection templates (`FR-QLTY-001`, `FR-QLTY-002`).
  - `[BRD-DERIVED]` Records quantitative measurements and qualitative pass/fail verdicts per test parameter.
  - `[BRD-DERIVED]` Determines final lot disposition: `Accepted`, `Rejected`, or `Accepted with Concession / Deviation`.
  - `[BRD-DERIVED]` Accepted quantities are released for physical warehouse putaway (Stage 8).
  - `[BRD-DERIVED]` Rejected quantities are transferred to Quarantine Warehouse awaiting Return to Vendor (RTV).
  - `[PROPOSED / Candidate Differentiator]` Automated NCR Pipeline: Proposes automated creation of a Non-Conformance Report (NCR) record when an inspection is marked `Rejected` (`FR-QLTY-006`).
- **6. Business Rules:**
  - `[BRD-DERIVED / BRD §6.1, §7.12]` **Quality Gating Rule:** Items classified as requiring inspection cannot be moved to sellable/production inventory or approved for 3-way match without an approved Quality Inspection.
  - `[PROPOSED / Candidate Differentiator - Subject to Stakeholder Confirmation]` **Automated Inspection-to-NCR Pipeline:** In strict compliance with anti-hallucination discipline, automatic NCR generation on QI rejection is classified as `PROPOSED / TBD`. (ERPNext lacks this mapper; BRD requires both Quality Inspection and NCR/CAPA, but does not mandate an automatic trigger).
- **7. Validations:** Sample test readings must be recorded for all designated inspection parameters; inspected quantity cannot exceed receipt quantity.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Inspection Status (`PROPOSED`):* `Pending Inspection` → `Under Testing` → `Accepted` / `Rejected` / `Accepted with Concession` (or `Quarantined`).
- **9. Traceable ERP Reference Behavior & KIYA Exception:**
  - *Reference Behavior:* ERPNext `Quality Inspection` (`stock/doctype/quality_inspection/`), linked via `reference_type: Purchase Receipt`. Rejections update `rejected_qty` and move items to `rejected_warehouse`.
  - *Adoption Assessment:* Inspection parameter table, reading comparison, and rejected warehouse segregation adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Differentiator / Correction:* In ERPNext, QI rejection does NOT automatically create an NCR. The automated QI-rejection-to-NCR state machine is a proposed KIYA enhancement (`PROPOSED (Candidate KIYA Differentiator)`).
- **10. Cross-Module Handoffs:** Accepted goods route to Warehouse Putaway (Stage 8); rejected goods route to Quality MRB / Supplier Return (`DEP-004`, `DEP-007`).
- **11. Audit & Security:** Inspection readings, test tool serial numbers, inspector certifications, and timestamps logged immutably (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Alert dispatched to Procurement Officer upon material rejection.
  - `[PROPOSED / Subject to OQ-003]` Material Review Board (MRB) approval required for `Accepted with Concession` disposition.
- **13. Documents & Attachments:** Manufacturer test certificates (MTC), lab test reports, and defect photographs (`FR-DMS-001`).
- **14. Cancellation & Re-Inspection:** Re-inspection workflow permitted only upon authorized supervisor override.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Full lot rejection halts invoice matching for rejected quantities and initiates return-to-vendor processing.
- **16. Reporting & KPI Implications:** Inward acceptance rate, defect parts per million (PPM), and vendor quality rating feeds into Supplier Performance (Stage 12) (`FR-SUPM-003`).
- **17. Acceptance Criteria:**
  - For items requiring quality clearance, system gates warehouse putaway until Quality Inspection verdict is recorded as Accepted.
  - Rejected inspection quantities are directed to quarantine holding per defined quality disposition rules.

---

### Stage 8: Inventory Putaway & Storage Execution
- **Requirement ID:** `DR-P2P-008`
- **Phase 0A Baseline ID:** `FR-INV-002` (Stock Quantities & Valuation), `FR-WH-002` (Bin Locations), `FR-WH-003` (Inbound Putaway)
- **Module:** Inventory / Warehouse | **Sub-Module:** Physical Putaway & Stock Ledger Posting
- **BRD Source:** BRD §6.1, §6.2, §7.8, §7.9; FR-INV-002, FR-WH-002, FR-WH-003; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Operational Flow Stage; Physical WMS Differentiator)
- **1. Purpose & Objective:** Transfer accepted materials from receiving/inspection staging into designated physical storage locations (bins, racks), update real-time stock balances, activate serial/batch numbers, and calculate inventory valuation.
- **2. Actors & Roles:** Warehouse Supervisor, Forklift Operator, Material Handler.
- **3. Preconditions:** Quality Inspection approved (Stage 7); target warehouse and bin locations active.
- **4. Inputs:** Goods Receipt reference, Quality Inspection reference, item codes, accepted quantities, batch/lot numbers, manufacturer expiry dates, target physical storage bins (aisle, rack, shelf, bin).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages physical warehouse bin locations and storage layouts (`FR-WH-001`, `FR-WH-002`).
  - `[BRD-REQUIRED / BRD-DERIVED]` Generates inward `Stock Ledger Entry` (SLE) records, permanently increasing physical available inventory (`FR-INV-002`).
  - `[BRD-REQUIRED]` Activates batch records and individual serial numbers for traceable items (`FR-INV-003`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Updates inventory valuation rates using configured valuation methods (Moving Average / FIFO).
  - `[PROPOSED / Reference Baseline]` Generates Putaway Tasks directing warehouse operators to optimal physical bin coordinates based on storage constraints.
- **6. Business Rules:**
  - `[BRD-REQUIRED / KIYA Differentiator]` **Physical WMS Location Rule:** System must track physical storage coordinates (aisle, rack, shelf, bin) (`FR-WH-002`), distinct from ERPNext's item-quantity cache.
  - `[BRD-DERIVED / FR-INV-003]` Batch and serial numbers must be recorded for regulated, perishable, or high-value components prior to putaway completion.
- **7. Validations:** Putaway quantity must exactly equal Quality-accepted quantity; target bin must have available capacity.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Putaway Task Status (`PROPOSED`):* `Task Generated` → `Assigned` → `Moving` → `Completed / Binned` (or `Cancelled`).
- **9. Traceable ERP Reference Behavior & KIYA Differentiator:**
  - *Reference Behavior:* ERPNext uses `Stock Ledger Entry` (SLE) and `Serial and Batch Bundle` to update balances and moving average valuation.
  - *Critical Architectural Distinction (Doc 21 §WF-12, Doc 24 §09, Doc 27 Correction 3):* In ERPNext, `Bin` is merely an internal aggregate quantity cache (`stock/doctype/bin/`). It is **NOT** a physical storage location.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA mandates true physical storage coordinate management (`FR-WH-002`), barcode verification, and directed putaway workflows.
- **10. Cross-Module Handoffs:** Makes inventory immediately available for production consumption (Stage 9 in C2C) or sales reservation (`DEP-002`, `DEP-007`).
- **11. Audit & Security:** Operator putaway scan actions, timestamps, and bin movements logged to audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Putaway completion triggers notification to Production Planners for awaited shortage components.
- **13. Documents & Attachments:** Barcode/QR pallet labels and warehouse location maps (`FR-WH-005`, `FR-MOB-004`).
- **14. Cancellation & Transfer:** Incorrect putaway is resolved via internal stock transfer to the correct bin.
- **15. Exceptions & Failure Paths:** Full bin capacity triggers dynamic rerouting to overflow storage locations.
- **16. Reporting & KPI Implications:** Warehouse space utilization, putaway cycle time, and stock accuracy percentages (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Completing putaway updates physical stock balances at the specific bin level and updates total available inventory in the Stock Ledger.
  - Batch numbers and expiry dates are successfully tagged to the stored inventory.

---

### Stage 9: Supplier Invoice & 3-Way Matching
- **Requirement ID:** `DR-P2P-009`
- **Phase 0A Baseline ID:** `FR-PROC-006` (Invoice Verification & 3-Way Match), `FR-FIN-002` (Accounts Payable)
- **Module:** Procurement / Finance | **Sub-Module:** Accounts Payable Invoicing & 3-Way Matching
- **BRD Source:** BRD §6.1, §6.2, §7.6, §7.17; FR-PROC-006, FR-FIN-002; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Financial & Verification Stage)
- **1. Purpose & Objective:** Receive vendor commercial invoices, execute automated 3-way matching across Purchase Orders, Goods Receipts, and Invoices, record Accounts Payable liabilities, and reverse provisional receiving accruals.
- **2. Actors & Roles:** Accounts Payable Specialist, Finance Controller, Purchasing Officer.
- **3. Preconditions:** Verified Goods Receipt submitted (Stage 6) with Quality clearance (Stage 7); approved Purchase Order exists.
- **4. Inputs:** Vendor invoice number and date, PO reference, Goods Receipt reference, vendor billed quantities, unit rates, freight/ancillary charges, statutory tax amounts, payment terms, currency.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Generates Purchase Invoice records establishing accounts payable liabilities against the supplier (`FR-FIN-002`).
  - `[BRD-REQUIRED]` Executes automated **3-Way Matching** (`FR-PROC-006`):
    - *Quantity Check:* Billed Quantity (Invoice) vs. Received / Accepted Quantity (Goods Receipt).
    - *Price Check:* Billed Unit Rate (Invoice) vs. Agreed Contract Rate (Purchase Order).
    - *Tax Check:* Claimed Statutory Taxes vs. Calculated Statutory Tax Engine figures (Stage 10).
  - `[BRD-DERIVED]` Reverses provisional stock accruals booked during Goods Receipt (`Debit Stock Received But Not Billed`, `Credit Accounts Payable`).
  - `[BRD-DERIVED]` Updates `billed_amt` and `per_billed` on source Purchase Order.
  - `[PROPOSED / Reference Baseline Policy]` Discrepancy Handling: Invoices exhibiting quantity, price, or tax variances may be routed to an AP discrepancy review or placed on candidate payment hold based on configured tolerance policies (`TBD`).
- **6. Business Rules:**
  - `[BRD-REQUIRED / FR-PROC-006]` **3-Way Match Integrity Rule:** An invoice cannot be approved for payment without matching against both an approved Purchase Order and a verified Goods Receipt.
  - `[PROPOSED Policy / TBD]` Tolerance Limits: Price variance tolerance and quantity tolerance are configurable parameters (`TBD`). Invoices within tolerance match; variances beyond tolerance require authorization.
- **7. Validations:** Billed quantity cannot exceed received quantity; invoice date must fall in an open financial fiscal period.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Invoice Status (`PROPOSED`):* `Draft` → `Matched & Approved` → `Partially Paid` → `Paid in Full` (or `On Hold / Variance Pending` / `Cancelled`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Purchase Invoice` (`accounts/doctype/purchase_invoice/`), linked via `po_detail` and `pr_detail`. Validation in `purchase_invoice.py:validate_goods_received_and_billed()`.
  - *Adoption Assessment:* 3-way matching mechanics, link fields (`po_detail`, `pr_detail`), and provisional accrual reversal GL postings adopted as proven reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Handoffs to Tax Engine for ITC determination (Stage 10) and AP Payment Disbursement (Stage 11) (`DEP-005`, `DEP-008`).
- **11. Audit & Security:** All price variances, supervisor overrides, and 3-way match exceptions logged with audit trail (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-003]` Variance approval workflow required when invoice total exceeds PO total.
  - `[PROPOSED / Subject to OQ-004]` Notification sent to buyer when vendor invoice price differs from PO contract rate.
- **13. Documents & Attachments:** Scanned vendor tax invoice PDF, receipt inspection certificates, and debit note vouchers (`FR-DMS-001`).
- **14. Cancellation & Debit Notes:** Cancelling an invoice reverses AP liabilities and accruals; returning goods post-invoicing generates an AP Debit Note.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / TBD]` Unresolved 3-way match discrepancies are routed for commercial review or credit note reconciliation per configured AP policy (`TBD`).
- **16. Reporting & KPI Implications:** Accounts Payable aging, invoice processing cycle time, and 3-way match exception rates (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Submitting a Purchase Invoice matching PO rates and GR quantities successfully posts AP ledger entries and clears provisional receipt accruals.
  - When a 3-way match evaluation identifies discrepancies exceeding configured tolerances, the system flags the variance for discrepancy review per configured policy.

---

### Stage 10: Statutory Tax & Input Tax Credit (ITC) Determination
- **Requirement ID:** `DR-P2P-010`
- **Phase 0A Baseline ID:** `FR-TAX-001` (Global Tax Engine), `FR-TAX-003` (GST/VAT & ITC), `FR-TAX-005` (Inward Verification)
- **Module:** Tax & Statutory Compliance | **Sub-Module:** Input Tax Credit (ITC) & Withholding Tax
- **BRD Source:** BRD §6.1, §6.2, §7.18; FR-TAX-001, FR-TAX-003, FR-TAX-005; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Regulatory & Compliance Engine)
- **1. Purpose & Objective:** Determine statutory tax components on inward purchases, calculate eligible vs. ineligible Input Tax Credit (ITC), evaluate Reverse Charge Mechanism (RCM) liabilities, and calculate applicable tax withholding.
- **2. Actors & Roles:** Tax Manager, Accounts Payable Specialist, Financial Controller.
- **3. Preconditions:** Supplier Invoice (Stage 9) created with Item HSN/SAC codes, company GSTIN, and vendor GSTIN.
- **4. Inputs:** Place of supply, supplier GSTIN/tax registration status, item HSN/SAC code, invoice item taxable values, claimed tax rates, vendor classification.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Operates Global Tax Engine to determine statutory purchase taxes across jurisdictions (`FR-TAX-001`):
    - Intra-state (India): Inward CGST + SGST split.
    - Inter-state (India): Inward IGST.
    - Imports: Customs Duty + IGST under import documentation.
  - `[BRD-REQUIRED]` Evaluates Input Tax Credit (ITC) eligibility (`FR-TAX-003`):
    - Eligible ITC is segregated to statutory tax asset ledgers for offset against outward liabilities per statutory rules.
    - Ineligible or blocked credits are identified and routed to cost or expense accounts per configured compliance rules.
  - `[BRD-REQUIRED]` Supports Reverse Charge Mechanism (RCM) determination on applicable purchases per statutory rules (`FR-TAX-003`).
  - `[BRD-REQUIRED]` Calculates applicable Tax Deducted at Source (TDS/withholding) based on statutory rules and configured thresholds (`FR-TAX-003`).
  - `[BRD-REQUIRED Capability / TBD Implementation Architecture]` Inward tax reconciliation with statutory portals (`FR-TAX-005`). (Note: Gateway architecture is governed under `OQ-005`).
- **6. Business Rules:**
  - `[BRD-REQUIRED / FR-TAX-003]` HSN/SAC code is required on commercial purchase invoice line items.
  - `[PROPOSED / TBD Policy]` ITC eligibility is evaluated based on statutory compliance criteria and configured tax policy; handling of inactive registrations or non-creditable categories is governed by statutory rules (`TBD`).
- **7. Validations:** Tax rate calculation must reconcile to statutory rounding limits; TDS deduction must apply before net payable calculation.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Tax Compliance Status (`PROPOSED`):* `Tax Determined` → `ITC Categorized` → `Reconciliation Pending` (or `Reconciled` / `Discrepancy Flagged`).
- **9. Traceable ERP Reference Behavior & KIYA Exception:**
  - *Reference Finding (Doc 21 §Regional, Doc 24 §18, Doc 27 Correction 2):* **India GST localization, Input Tax Credit ledgers, and TDS withholding were removed from the ERPNext develop core repository** (`remove_india_localisation.py`).
  - *KIYA Core Requirement (`BRD-REQUIRED`):* Global Tax Engine, India GST ITC ledger segregation, RCM determination, and TDS withholding are **100% KIYA-owned or integrated capabilities**. The reference baseline provides only generic tax calculation tables (`purchase_taxes_and_totals.py`).
  - *Statutory Gateway Architecture (`TBD`):* Governed under Open Question `OQ-005` (Built-in GSP/ASP connector vs. third-party middleware).
- **10. Cross-Module Handoffs:** Provides tax liability/asset lines to General Ledger (Stage 11/Accounting) and feeds statutory tax filing returns (`DEP-005`, `DEP-008`).
- **11. Audit & Security:** Complete audit trail of ITC claims, blocked credit classifications, and statutory tax calculations (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Automated notification if inward invoice is mismatched during tax reconciliation.
- **13. Documents & Attachments:** Tax payment challans, statutory withholding certificates, and import customs entry documentation (`FR-DMS-001`).
- **14. Cancellation & Reversal:** Invoice cancellation reverses claimed ITC ledger entries.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / TBD]` Supplier tax-registration status is evaluated according to applicable statutory rules; resulting ITC/RCM treatment is governed by configured tax-compliance policy (`TBD`).
- **16. Reporting & KPI Implications:** ITC utilization reports, statutory tax reconciliation summaries, and withholding tax deduction registers (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Submitting a purchase invoice with valid statutory tax parameters calculates applicable inward taxes and categorizes eligible Input Tax Credit per configured tax engine rules.
  - Tax lines determined to be non-creditable per configured tax policy are appropriately routed to cost or expense accounts.

---

### Stage 11: Accounts Payable Settlement & Payment Disbursement
- **Requirement ID:** `DR-P2P-011`
- **Phase 0A Baseline ID:** `FR-FIN-002` (Accounts Payable), `FR-FIN-004` (Cash & Bank Management)
- **Module:** Finance & Accounting | **Sub-Module:** AP Disbursement & Bank Settlement
- **BRD Source:** BRD §6.1, §6.2, §7.17; FR-FIN-002, FR-FIN-004; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Financial Fulfillment Stage)
- **1. Purpose & Objective:** Settle approved accounts payable liabilities against supplier invoices, execute disbursements via banking/payment rails, allocate advance payments and debit notes, and update supplier balances.
- **2. Actors & Roles:** Accounts Payable Specialist, Treasury Manager, Chief Financial Officer (CFO).
- **3. Preconditions:** Approved Purchase Invoice (Stage 9) with outstanding balance > 0, or approved advance payment request.
- **4. Inputs:** Supplier reference, payment date, disbursement amount, payment mode (NEFT/RTGS, wire, check, corporate card), source bank account, invoice allocation schedule, early payment discounts, debit note allocations.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Records outgoing vendor payments across banking and digital payment channels (`FR-FIN-004`).
  - `[BRD-REQUIRED]` Allocates disbursements against specific approved Purchase Invoices, updating outstanding balances (`FR-FIN-002`).
  - `[BRD-DERIVED]` Updates Purchase Invoice status (`Partially Paid`, `Paid in Full`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Supports vendor advance payments, maintaining advance balance records for allocation against future invoices.
  - `[BRD-REQUIRED]` Posts double-entry General Ledger transactions:
    - *Debit:* Accounts Payable (Creditors) Account.
    - *Credit:* Company Bank / Cash Account.
    - *Credit:* Early Payment Discount / Purchase Rebate Account (if applicable).
  - `[ERP-REFERENCE / PROPOSED]` Realized foreign exchange gain/loss calculation for foreign currency disbursements at bank settlement date.
- **6. Business Rules:**
  - `[BRD-DERIVED]` Payment allocation cannot exceed total invoice outstanding amount unless explicitly classified as an unallocated vendor advance.
  - `[PROPOSED / Subject to OQ-003]` High-value disbursements require dual-authorization (maker-checker) approval before electronic banking transmission.
- **7. Validations:** Disbursement amount must be positive; source bank account must have active status and sufficient ledger balance.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Payment Status (`PROPOSED`):* `Draft` → `Pending Bank Authorization` → `Disbursed / Cleared` (or `Rejected / Bounced` / `Cancelled`).
- **9. Traceable ERP Reference Behavior:**
  - *Reference Behavior:* ERPNext `Payment Entry` (`accounts/doctype/payment_entry/`) with `Payment Ledger Entry` (PLE) and bank reconciliation tools.
  - *Adoption Assessment:* Payment Entry data model, child invoice allocation table, and double-entry clearing adopted as reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Clears Accounts Payable balance in General Ledger and feeds payment timeliness data into Supplier Performance (Stage 12) (`DEP-008`).
- **11. Audit & Security:** Dual-signature electronic authorization logs, bank reference numbers, and payment timestamps recorded (`FR-PADM-1.8.2`, `SF-008`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Payment Advice notification dispatched to vendor contact upon bank clearance.
  - `[PROPOSED / Subject to OQ-003]` Treasury limit authorization workflow required for disbursements exceeding configured thresholds.
- **13. Documents & Attachments:** Bank payment advice, bank clearance confirmations, and check counterfoils (`FR-DMS-001`).
- **14. Cancellation & Reversal:** Payment cancellation generates reversing GL entries and restores invoice outstanding balances.
- **15. Exceptions & Failure Paths:** Bank transmission failure reverts payment status to `Draft` and alerts the treasury team.
- **16. Reporting & KPI Implications:** Daily cash disbursement forecast, days payable outstanding (DPO), and early payment discount capture rate (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - Submitting a Payment Entry matching an invoice's total outstanding amount updates the invoice business status to `Paid in Full` and balances the AP ledger.

---

### Stage 12: Supplier Performance & Scorecard Analytics
- **Requirement ID:** `DR-P2P-012`
- **Phase 0A Baseline ID:** `FR-SUPM-003` (Supplier Evaluation), `FR-SUPM-005` (Supplier Risk & Performance)
- **Module:** Supplier Management / BI | **Sub-Module:** Vendor Scorecards & Performance Tracking
- **BRD Source:** BRD §6.1, §6.2, §7.7, §7.22; FR-SUPM-003, FR-SUPM-005, FR-BI-001; Business Flows §2
- **Stage Classification:** `BRD-REQUIRED` (Core Analytic & Governance Anchor)
- **1. Purpose & Objective:** Continuously aggregate transactional performance data across all P2P stages (delivery timeliness, quality acceptance, pricing stability, compliance), calculate objective supplier scorecard ratings, and guide future sourcing allocation.
- **2. Actors & Roles:** Procurement Director, Sourcing Manager, Supplier Quality Engineer.
- **3. Preconditions:** Completed P2P transactions (Purchase Orders, Goods Receipts, Quality Inspections, Invoices) recorded against the supplier.
- **4. Inputs:** PO promised delivery dates vs. actual receipt dates, received quantities vs. accepted quantities, quality rejection ppm, invoice price variances, supplier response turnaround times.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Computes objective supplier performance ratings across defined evaluation criteria (`FR-SUPM-003`, `FR-SUPM-005`).
  - `[BRD-DERIVED / PROPOSED Metrics]` Calculates core procurement performance dimensions:
    - *On-Time In-Full (OTIF) Delivery Rate:* Percentage of orders delivered on or before promised date in full quantity.
    - *Quality Acceptance Rate:* Percentage of inspected materials accepted without rejection or concession.
    - *Commercial Compliance:* Adherence to contracted PO rates and billing accuracy.
  - `[PROPOSED / Reference Baseline]` Generates periodic (monthly/quarterly) Supplier Scorecard records and updates the vendor rating on the Supplier Master.
  - `[BRD-DERIVED]` Feeds performance tiers into Stage 2 (Supplier Sourcing) and Stage 3 (RFP/RFQ) to prioritize top-performing vendors.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline Policy]` Vendors falling below minimum acceptable performance thresholds may be flagged for performance review or sourcing restrictions per configured evaluation policies.
  - `[TBD - Governed under Open Question OQ-010]` Specific scoring algorithms, metric weighting percentages, and automated tiering rules are open for stakeholder confirmation (`OQ-010`).
- **7. Validations:** Performance scores must be normalized on a consistent scale (e.g. 0 to 100); evaluation period must contain at least one closed transaction.
- **8. Candidate Business Status Lifecycle (`CD-002`):**
  - *Candidate Scorecard Period Status (`PROPOSED`):* `Period Open` → `Calculating` → `Published / Rated` → `Archived`.
- **9. Traceable ERP Reference Behavior & KIYA Gap:**
  - *Reference Behavior:* ERPNext `Supplier Scorecard` (`buying/doctype/supplier_scorecard/`) with daily scheduled calculation hooks (`cron_daily_records()`).
  - *Adoption Assessment:* Scorecard structural framework and periodic calculation scheduler adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Policy Distinction:* ERPNext scoring variables and formulas are generic; KIYA performance metrics and weights remain governed under open clarification question `OQ-010` (`TBD`).
- **10. Cross-Module Handoffs:** Feeds vendor rating back to Supplier Master (Stage 1) and Sourcing / Allocation rules (Stage 2 & Stage 3) (`DEP-006`, `DEP-009`).
- **11. Audit & Security:** Historical scorecards preserved immutably for vendor contract reviews and annual compliance audits (`FR-PADM-1.8.2`).
- **12. Notifications & Approvals:**
  - `[PROPOSED / Subject to OQ-004]` Performance scorecard summary dispatched to supplier via vendor portal (`FR-SUPM-004`).
- **13. Documents & Attachments:** Corrective Action Requests (CAPA), vendor audit reviews, and rating certificates (`FR-DMS-001`).
- **14. Cancellation & Recalculation:** Scorecards can be re-run if underlying transactional data was corrected during audit reconciliation.
- **15. Exceptions & Failure Paths:**
  - `[PROPOSED / Reference Baseline]` Persistently low evaluation scores trigger review warnings to the sourcing team.
- **16. Reporting & KPI Implications:** Strategic supplier spend vs. performance matrix, supply chain risk index, and vendor defect trend analytics (`FR-BI-001`).
- **17. Acceptance Criteria:**
  - System computes delivery timeliness and quality acceptance metrics for active suppliers over designated evaluation periods based on configured scoring rules.
  - Scorecard summaries are accessible directly on the Supplier Master record.

---

## 4. Traceability & Classification Summary Matrix

| Req ID | P2P Stage | Baseline ID | Module | Primary Stage Classification | Explicit KIYA Differentiators & Candidate Enhancements | Dependency | Current Status |
|---|---|---|---|---|---|---|---|
| **DR-P2P-001** | Stage 1: Supplier Master | `FR-SUPM-001` / `SUPM-002` | Supplier Mgmt | `BRD-REQUIRED` | **Unified Supplier Master** (`BRD-REQUIRED / DEC-007`); Status controls (`PROPOSED`) | `DEP-006`, `DEP-008` | Cleaned Baseline |
| **DR-P2P-002** | Stage 2: Sourcing & Qual | `FR-SUPM-002` / `PROC-001` | Procurement | `BRD-REQUIRED` | **Dedicated Sourcing & Qualification Stage** (`BRD-REQUIRED`); Qualification pooling (`PROPOSED`) | `DEP-006` | Cleaned Baseline |
| **DR-P2P-003** | Stage 3: RFQ / RFP Sourcing | `FR-PROC-002` | Procurement | `BRD-REQUIRED` | **Dual RFQ / RFP Capabilities** (`BRD-REQUIRED`); Multi-envelope technical-vs-commercial RFP evaluation (`PROPOSED / KIYA Differentiator`) | `DEP-006` | Cleaned Baseline |
| **DR-P2P-004** | Stage 4: Supplier Quote | `FR-PROC-003` | Procurement | `BRD-REQUIRED` | Side-by-side bid matrix (`ERP-REFERENCE`); Multi-attribute scoring (`PROPOSED / TBD`) | `DEP-006` | Cleaned Baseline |
| **DR-P2P-005** | Stage 5: Purchase Order | `FR-PROC-004` | Procurement | `BRD-REQUIRED` | Approved commercial commitment (`BRD-REQUIRED`); Approval tiers (`TBD / OQ-003`) | `DEP-006`, `DEP-007` | Cleaned Baseline |
| **DR-P2P-006** | Stage 6: Goods Receipt | `FR-PROC-005` / `WH-001` | Proc/Warehouse | `BRD-REQUIRED` | Gate entry & provisional GRNI accrual (`ERP-REFERENCE`); Over-receipt policy (`PROPOSED / TBD`) | `DEP-004`, `DEP-007` | Cleaned Baseline |
| **DR-P2P-007** | Stage 7: Quality Gate | `FR-QLTY-001` / `QLTY-002` | Quality | `BRD-REQUIRED` | Quality Gating Rule (`BRD-DERIVED`); **Automated QI Rejection → NCR** (`PROPOSED / TBD`) | `DEP-004`, `DEP-007` | Cleaned Baseline |
| **DR-P2P-008** | Stage 8: Inventory Putaway | `FR-INV-002` / `WH-002` | Inv/Warehouse | `BRD-REQUIRED` | **Physical Warehouse / Location / Bin Coordinate Tracking** (`BRD-REQUIRED`); Directed putaway & scan mechanics (`PROPOSED / Reference Baseline`) | `DEP-002`, `DEP-007` | Cleaned Baseline |
| **DR-P2P-009** | Stage 9: Supplier Invoice | `FR-PROC-006` / `FIN-002` | Proc/Finance | `BRD-REQUIRED` | **Automated 3-Way Matching** (`BRD-REQUIRED`); Discrepancy tolerances (`PROPOSED / TBD`) | `DEP-005`, `DEP-008` | Cleaned Baseline |
| **DR-P2P-010** | Stage 10: Statutory Tax / ITC | `FR-TAX-001` / `TAX-003` | Tax & Compliance | `BRD-REQUIRED` | **Global Tax Engine, India GST ITC & RCM** (`BRD-REQUIRED`); Gateway API (`TBD / OQ-005`) | `DEP-005`, `DEP-008` | Cleaned Baseline |
| **DR-P2P-011** | Stage 11: AP Payment | `FR-FIN-002` / `FIN-004` | Finance & Acct | `BRD-REQUIRED` | AP disbursement & GL settlement (`BRD-REQUIRED`); Multi-currency FX rules (`ERP-REFERENCE`) | `DEP-008` | Cleaned Baseline |
| **DR-P2P-012** | Stage 12: Supplier Perf | `FR-SUPM-003` / `SUPM-005` | Supplier/BI | `BRD-REQUIRED` | Automated scorecard tracking (`BRD-REQUIRED`); Specific metric weights (`TBD / OQ-010`) | `DEP-006`, `DEP-009` | Cleaned Baseline |

---

## 5. Explicit KIYA Gaps & Differentiators Summary

In strict compliance with `CD-001` and anti-hallucination discipline, the following 5 key areas represent explicit KIYA differentiators where standard ERPNext behavior was rejected, found absent, or expanded beyond standard ERP conventions:

1. **Dual RFQ / RFP Mechanism (`BRD-REQUIRED`) & Multi-Envelope RFP Evaluation (`PROPOSED / KIYA Differentiator`) (DR-P2P-002, DR-P2P-003):**
   In ERPNext, tendering is restricted to simple price requests via `Request for Quotation`. There is **no RFP DocType** and no concept of upstream supplier qualification pipelines or multi-envelope (technical vs. commercial) bid evaluation. KIYA explicitly mandates both standard RFQ capability and complex RFP capability as core procurement requirements (`FR-PROC-002`). Advanced mechanics such as multi-envelope technical-vs-commercial RFP bidding and sealed proposal evaluation are classified as `PROPOSED (Candidate KIYA Differentiator)` rather than confirmed BRD mandates.
2. **Physical Warehouse Location & Bin Coordinate Tracking (`BRD-REQUIRED`) vs. Directed Putaway Mechanics (`PROPOSED / ERP-REFERENCE`) (DR-P2P-008):**
   In ERPNext, `Bin` is merely an internal ledger balance cache (`stock/doctype/bin/`). It does not represent a physical warehouse location. KIYA mandates physical warehouse, location, and bin coordinate tracking (aisles, racks, shelves, bins) as an explicit core inventory capability (`FR-WH-002`, `FR-INV-002`). Operational mechanics such as directed putaway optimization, automated bin selection logic, and barcode/QR scanning verification tasks are classified as `PROPOSED / Reference Baseline Mechanics` consistent with Stage 8.
3. **Automated Quality Inspection Rejection to NCR Pipeline (DR-P2P-007) — `PROPOSED (Candidate KIYA Differentiator) / TBD`:**
   In ERPNext, rejecting an incoming Quality Inspection segregates stock into a rejected warehouse, but does NOT trigger a Non-Conformance Report (NCR) or CAPA workflow. KIYA proposes an automated inspection-rejection to quarantine/NCR state machine as a high-value operational differentiator, pending formal stakeholder confirmation of trigger rules (`TBD`).
4. **Automated 3-Way Matching with Tolerances (DR-P2P-009) — `BRD-REQUIRED (Matching) / PROPOSED (Tolerances)`:**
   While ERPNext provides basic billed-vs-received validation, KIYA establishes formal 3-way matching across PO prices, Goods Receipt quantities, and Supplier Invoice figures as an explicit financial gate (`FR-PROC-006`), with tolerance checking, discrepancy handling, and payment holds governed by configured policy (`PROPOSED / TBD`).
5. **Native Global Tax Engine & India GST Input Tax Credit (ITC) (DR-P2P-010) — `BRD-REQUIRED (Engine) / TBD (Architecture)`:**
   India GST localization and Input Tax Credit (ITC) tracking were excised from the ERPNext develop core repository (`remove_india_localisation.py`). KIYA mandates a dedicated Global Tax Engine supporting GST/VAT determination, Input Tax Credit evaluation, Reverse Charge Mechanism (RCM), and withholding capabilities (`BRD-REQUIRED`). The statutory API gateway architecture and detailed statutory treatment remain governed under open question `OQ-005` (`TBD`).

---

## 6. Cross-Module Interactions & Data Flow Architecture

The Procure-to-Pay flow exhibits extensive horizontal propagation across the enterprise platform:

1. **Demand Propagation (MRP to Procurement):**
   - Unfulfilled sales order shortages and production BOM material requirements explode in MRP (`Stage 8 in C2C`, `DR-C2C-008`), generating planned Purchase Requisitions that feed into Supplier Sourcing (`DR-P2P-002`) and RFQ/RFP (`DR-P2P-003`) (`DEP-003`).
2. **Contractual Fulfillment (Purchasing to Physical Warehouse):**
   - Approved Purchase Orders (`DR-P2P-005`) publish expected delivery milestones to Warehouse Receiving (`DR-P2P-006`), establishing receiving capacity requirements (`DEP-007`).
3. **Operational Gating (Receiving to Quality to Storage):**
   - Goods Receipt (`DR-P2P-006`) routes items requiring inspection to Inward Quality Gate (`DR-P2P-007`). Only accepted quantities generate Warehouse Putaway tasks (`DR-P2P-008`), while rejected lots route to Quality Quarantine (`DEP-004`).
4. **Financial Accruals & Liability Settlement (Warehouse to AP to GL):**
   - Goods Receipt (`DR-P2P-006`) posts provisional GRNI accruals to General Ledger (`DEP-005`).
   - Supplier Invoice (`DR-P2P-009`) executes 3-way matching, reverses provisional accruals, and establishes Accounts Payable liabilities.
   - Global Tax Engine (`DR-P2P-010`) determines Input Tax Credit (ITC) asset allocations and TDS deductions (`DEP-008`).
   - Payment Disbursement (`DR-P2P-011`) clears AP liabilities against corporate bank accounts.
5. **Continuous Governance Loop (Transactions to Supplier Scorecards to Sourcing):**
   - Transactional milestones (PO delivery dates, receipt dates, quality inspection acceptance rates, and invoice pricing stability) continuously stream into Supplier Performance (`DR-P2P-012`).
   - Calculated vendor scorecard ratings feed back to the Supplier Master (`DR-P2P-001`) and inform future sourcing allocations (`DR-P2P-002`, `DR-P2P-003`) (`DEP-006`, `DEP-009`).

---

## 7. Document Metadata & Governance

- **Prepared By:** Antigravity Enterprise Requirements Architect
- **Creation Date:** 14 September 2026 | **Correction Pass:** 14 September 2026 | **Classification Cleanup:** 14 September 2026
- **Status:** Baseline Detailed Requirements Package (Final Classification Cleanup Completed)
- **Traceability Chain:** `source/KIYA360_BRD.pdf v2.0` → `docs/00-requirements/01-master-requirements.md` → `docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md` → `docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md` → `docs/00-requirements/32-procure-to-pay-detailed-requirements.md`.
- **Immediate Next Action:** Update `docs/PROJECT-STATE.md`, `.kiya/AI-HANDOFF.md`, and `.kiya/AI-CHANGELOG.md`. Await stakeholder review of P2P before proceeding to Phase 0B-2 Batch 3 (Asset-to-Service Detailed Requirements Expansion).
