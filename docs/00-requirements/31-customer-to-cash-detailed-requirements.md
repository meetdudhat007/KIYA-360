# KIYA 360 — Customer-to-Cash (C2C) Detailed Requirements Expansion (Batch 1)

## 1. Document Control, Authority & Scope

- **Document ID:** `31-customer-to-cash-detailed-requirements`
- **Phase:** Phase 0B-2 — Detailed Requirements Expansion (Batch 1: Customer-to-Cash)
- **Status:** In Review / Detailed Functional Requirements Baseline (Corrected Pass)
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026: Section 6.1, Section 7.2, 7.3, 7.8, 7.9, 7.10, 7.11, 7.12, 7.17, 7.18, 7.22, Section 8, Section 10)
- **Approved Clarification Decisions:**
  - `CD-001` (`DEC-012`): Hybrid Scope-Expansion Approach — Fully detail the complete BRD C2C flow; use proven ERP-standard behavior as traceable reference baseline for non-specified standard mechanics; zero automatic ERPNext coupling; explicit KIYA differentiators and documented exceptions (`docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md`).
  - `CD-002` (`DEC-013`): Operational Business Status Model — Use Business Status representing operational progression; reject ERPNext's dual `docstatus` technical model; progress statuses organically (`docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md`).
- **Dependencies Governed:** `DEP-001`, `DEP-002`, `DEP-003`, `DEP-004`, `DEP-005`, `DEP-009`, `DEP-010`, `DEP-011`.
- **Reference Evidence Baseline:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` through `27-erpnext-analysis-review.md`.

---

### 1.1 Classification Correction Notes & Working Discipline

In strict compliance with repository governance (`AGENTS.md`, `docs/00-requirements/12-requirement-status-legend.md`, and `CD-001`), this corrected expansion strictly distinguishes between five levels of requirements authority:

1. **`BRD-REQUIRED`:** Core capabilities, functional entities, and flow stages explicitly mandated by BRD v2.0 (e.g., Lead, Opportunity, Enquiry, Quotation, Sales Order, Inventory, MRP, Manufacturing, Quality, Warehouse, Dispatch, Invoice, Global Tax Engine, Payment, Double-Entry Accounting, BI Profitability, and Customer 360).
2. **`BRD-DERIVED`:** Behaviors and rules that are necessary logical consequences of an explicit BRD mandate (e.g., matching billed quantities to delivered quantities, sequential dispatch-before-invoicing in core C2C, inventory ledger reductions on dispatch), where the exact implementation mechanism is not explicitly dictated by the BRD.
3. **`ERP-REFERENCE`:** Proven enterprise/ERP standard patterns (reverse-engineered from ERPNext in Docs 21–27) adopted as a baseline to accelerate functional definition. These are reference baselines and **must never silently become binding KIYA requirements** without formal ratification.
4. **`PROPOSED`:** Reasonable candidate business rules, field validations, configuration thresholds, or high-value differentiators (such as automated Quality Inspection rejection to NCR generation) designed to complete the functional specification, pending formal stakeholder confirmation.
5. **`TBD`:** Functional ambiguities, statutory mechanics, or policy choices requiring formal stakeholder clarification (e.g., open questions `OQ-003` through `OQ-015`) before they can be treated as confirmed requirements.

**Operational Business Status Discipline (`CD-002`):**
In accordance with `CD-002` (`DEC-013`), KIYA 360 uses operational **Business Status** as its primary lifecycle model, discarding ERPNext's technical `docstatus` (Draft/Submitted/Cancelled) paradigm. The status values listed under each stage below represent **Candidate Operational Lifecycles (`PROPOSED`)** subject to final tenant workflow configuration; they are not rigid, frozen database enumerations.

**Unified Data Model Discipline (`DEC-007`):**
Master entities (`Customer Master`, `Item Master`, `Warehouse Master`, `Company Master`, `Tax Template`) are strictly unified across all 18 stages and must never be duplicated across module boundaries.

---

## 2. Customer-to-Cash Flow Overview & Architectural Spine

The Customer-to-Cash (C2C) business flow is the commercial backbone of KIYA 360. As mandated by BRD §6.1, it spans 18 distinct stages across 10 functional modules, unifying CRM, Sales, Operations, Shop Floor, Warehouse, Accounting, and Analytics:

```
+---------+     +---------------+     +-----------+     +-------------+     +---------------+
| 1. Lead | --> | 2.Opportunity | --> | 3.Enquiry | --> | 4.Quotation | --> | 5.Sales Order |
+---------+     +---------------+     +-----------+     +-------------+     +---------------+
                                                                                    |
+-------------------+     +-------------+     +------------------------+            |
| 8. MRP / Planning | <-- | 7.Inventory | <-- | 6. Availability Check  | <----------+
+-------------------+     +-------------+     +------------------------+
         |
         v
+---------------+     +--------------------+     +---------------+     +---------------+
| 9. Production | --> | 10. Quality Check  | --> | 11. Warehouse | --> | 12. Dispatch  |
+---------------+     +--------------------+     +---------------+     +---------------+
                                                                               |
+---------------------+     +--------------------+     +-------------+         |
| 16. Accounting (GL) | <-- | 15. Payment Collect| <-- | 14. Tax Eng | <-------+ (13. Invoice)
+---------------------+     +--------------------+     +-------------+
         |
         v
+---------------------+     +----------------------+
| 17. Profitability   | --> | 18. Customer History |
+---------------------+     +----------------------+
```

### 2.1 Master Data vs. Transaction Data in C2C
- **Unified Master Data (`DEC-007`):**
  - `Customer Master` (`FR-PADM-1.4.1` / `FR-CRM-003` / `FR-CRM-004`): Unified single customer record across CRM, Sales, and Receivables.
  - `Item Master` (`FR-PADM-1.4.3` / `FR-INV-001`): Unified product definition across pricing, inventory, BOM manufacturing, and invoicing.
  - `Warehouse Master` (`FR-WH-001`): Logical and physical inventory storage entities.
  - `Company & Branch Master` (`FR-PADM-1.1.1`, `FR-PADM-1.1.2`): Multi-entity organizational context and GSTIN registration boundaries.
  - `Tax Template & Chart of Accounts` (`FR-PADM-1.4.5`, `FR-FIN-001`): Unified tax classifications and double-entry accounting nodes.
- **Transaction Data Records:**
  `Lead`, `Opportunity`, `Enquiry`, `Quotation`, `Sales Order`, `Stock Reservation Entry`, `Production Plan`, `Work Order`, `Job Card`, `Quality Inspection`, `Delivery Note (Dispatch)`, `Sales Invoice`, `Payment Entry`, `GL Entry`, `Stock Ledger Entry`.

---

## 3. Detailed Requirements per C2C Stage

---

### Stage 1: Lead Management
- **Requirement ID:** `DR-C2C-001`
- **Phase 0A Baseline ID:** `FR-CRM-001` (Leads), `FR-CRM-004` (Contacts)
- **Module:** CRM | **Sub-Module:** Lead Acquisition & Qualification
- **BRD Source:** BRD §6.1, §7.2; FR-CRM-001, FR-CRM-004
- **Stage Classification:** `BRD-REQUIRED` (Core Entity & Pipeline Stage)
- **1. Purpose & Objective:** Capture prospective buyers across intake channels, qualify interest, and convert qualified prospects into Opportunities and Customers.
- **2. Actors & Roles:** Marketing Representative, Sales Development Representative (SDR), Lead Qualifier.
- **3. Preconditions:** Company and Branch master context active; territory and lead source tables configured (`BRD-DERIVED`).
- **4. Inputs:** Prospect name, organization name, contact details (email, phone, address), lead source, estimated requirement, assigned territory.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` System captures lead records manually or via bulk import / integration endpoints (`FR-CRM-001`).
  - `[BRD-DERIVED]` Generates unique sequential ID per numbering rules (`SF-013`).
  - `[PROPOSED]` Evaluates configurable qualification criteria.
  - `[BRD-DERIVED]` Upon qualification, triggers conversion to generate an `Opportunity` and create or link a unified `Customer Master` record.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline]` Mandatory Contact Rule: At least one primary contact channel (email or phone) is required prior to triggering lead conversion. (Note: BRD does not mandate phone verification; verification mechanics are marked `TBD`).
  - `[PROPOSED / Reference Baseline]` Duplicate Detection Rule: System alerts user if email or phone matches an existing active Lead or Customer Master.
- **7. Validations:**
  - `[PROPOSED / Standard Validation]` Standard format checks on email and phone strings.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Lifecycle (`PROPOSED`):* `New` → `Contacted` → `Qualified` → `Converted` (or `Disqualified` / `Lost`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext uses `Lead` doctype (`crm/doctype/lead/`) with `lead/mapper.py:make_customer` and `make_opportunity`.
  - *Adoption Assessment:* Core lead capture and conversion mechanics adopted as proven ERP reference baseline (`ERP-REFERENCE`).
  - *KIYA Planned Enhancements:* Omnichannel ingestion queues (`FR-CRM-001`) and AI predictive scoring (`FR-AIAU-001`) are classified as `PROPOSED / Future Capability` and not treated as rigid baseline prerequisites for Phase 0B.
- **10. Cross-Module Handoffs:** Handoff to Sales Pipeline upon qualification (`DEP-001`).
- **11. Audit & Security:** Modifications logged to audit trail (`FR-PADM-1.8.2`, `SF-008`).
- **12. Acceptance Criteria:**
  - Given a valid prospect input, when submitted, a Lead record with candidate status `New` must be created with an audit timestamp.
  - When qualification is confirmed, conversion must generate a linked Opportunity and link/create a unified Customer Master.

---

### Stage 2: Opportunity Tracking
- **Requirement ID:** `DR-C2C-002`
- **Phase 0A Baseline ID:** `FR-CRM-002` (Opportunities), `FR-CRM-006` (Pipeline Management)
- **Module:** CRM | **Sub-Module:** Deal Pipeline & Probability Tracking
- **BRD Source:** BRD §6.1, §7.2; FR-CRM-002, FR-CRM-006
- **Stage Classification:** `BRD-REQUIRED` (Core Entity & Pipeline Stage)
- **1. Purpose & Objective:** Track qualified business opportunities, expected deal value, pipeline milestones, close dates, and win probability.
- **2. Actors & Roles:** Account Executive, Sales Manager.
- **3. Preconditions:** Converted Lead or direct Opportunity created against an existing Customer Master.
- **4. Inputs:** Customer Master reference, Opportunity title, expected closing date, estimated deal value, currency, sales stage, probability percentage, item/service interest list.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Maintains deal progression through defined pipeline milestones (`FR-CRM-006`).
  - `[BRD-DERIVED]` Aggregates pipeline values for sales forecasting.
  - `[BRD-REQUIRED]` Links upstream to Lead (if applicable) and downstream to commercial quotes or technical enquiries.
- **6. Business Rules:**
  - `[ERP-REFERENCE / Standard Validation]` Expected close date must be on or after creation date.
  - `[PROPOSED / Configurable Mechanics]` Win probability percentage may default based on tenant-configured pipeline stages, with manual override capability.
- **7. Validations:** Deal value must be positive; currency must match an active Currency Master (`FR-PADM-1.4.6`).
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Lifecycle (`PROPOSED`):* `Open` → `In Negotiation` → `Proposal Sent` → `Won` (or `Lost`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Opportunity` (`crm/doctype/opportunity/`) with child table `Opportunity Item`.
  - *Adoption Assessment:* Deal tracking and child item structure adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Planned Enhancements:* Executive forecasting (`FR-BI-001`, `FR-EPM-002`) leverages opportunity pipeline data (`BRD-DERIVED`).
- **10. Cross-Module Handoffs:** Generates downstream `Enquiry` or `Quotation` (`DEP-001`).
- **11. Acceptance Criteria:**
  - Given an active Opportunity, when updated to `Won`, system enables creation of downstream quotation or enquiry documents.
  - When marked `Lost`, system prompts for a loss reason code for CRM analysis (`PROPOSED`).

---

### Stage 3: Customer Enquiry (Explicit BRD Flow Stage & KIYA Structural Differentiator)
- **Requirement ID:** `DR-C2C-003`
- **Phase 0A Baseline ID:** `FR-SALES-001` (Enquiries)
- **Module:** Sales | **Sub-Module:** Technical & Commercial Enquiry Intake
- **BRD Source:** BRD §6.1, §7.3; FR-SALES-001; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Explicit BRD Flow Stage & Dedicated Entity)
- **1. Purpose & Objective:** Formally capture customer technical specifications, custom requirements, bills of quantities (BOQ), and requests for quotation between initial opportunity and formal pricing commitment.
- **2. Actors & Roles:** Sales Engineer, Technical Estimator, Commercial Sales Officer.
- **3. Preconditions:** Linked Customer Master and active Opportunity exist (or direct enquiry logged against Customer).
- **4. Inputs:** Customer reference, Opportunity reference (optional), enquiry receipt date, requested response deadline, technical specifications, item list / sketches / BOQ attachments, customer target price (optional), delivery location.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` System provides an independent, dedicated `Enquiry` transactional entity (`FR-SALES-001`).
  - `[BRD-DERIVED]` Serves as the operational bridge between deal origination (Opportunity) and price commitment (Quotation).
  - `[PROPOSED / Business Workflow]` Facilitates technical feasibility review and cost estimation routing to engineering teams before commercial pricing is locked.
  - `[PROPOSED / Configurable SLA]` Tracks response turnaround times against requested customer deadlines.
- **6. Business Rules:**
  - `[BRD-DERIVED]` Quotations generated from an Enquiry must maintain referential traceability to the source Enquiry.
  - `[PROPOSED / TBD Policy]` Technical feasibility sign-off before quotation issuance is a candidate policy for engineered/custom items, subject to tenant workflow configuration (`TBD`).
- **7. Validations:** Mandatory customer reference; response deadline must be future-dated relative to receipt.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Lifecycle (`PROPOSED`):* `Received` → `Under Review` → `Feasibility Confirmed` → `Quoted` (or `Declined / Regret`).
- **9. Traceable Reference Baseline & KIYA Differentiator:**
  - *Reference Finding (Doc 21 §WF-01, Doc 22 §3.1, Doc 24 §03):* **ERPNext has NO dedicated Enquiry DocType.** ERPNext collapses this requirement into a text field `enq_no` on Quotation or handles it vaguely within Opportunity.
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* KIYA strictly enforces `Lead → Opportunity → Enquiry → Quotation` as mandated by BRD §6.1. The Enquiry entity is an explicit, mandatory structural requirement.
- **10. Cross-Module Handoffs:** Feeds technical estimation into Manufacturing BOM Estimator and commercial items into Quotation (`DEP-001`).
- **11. Acceptance Criteria:**
  - System must provide an independent `Enquiry` transaction entity.
  - Creating a Quotation from an Enquiry must pull customer, items, and technical notes without manual re-entry.

---

### Stage 4: Sales Quotation
- **Requirement ID:** `DR-C2C-004`
- **Phase 0A Baseline ID:** `FR-SALES-002` (Quotations), `FR-SALES-004` (Pricing & Discounts)
- **Module:** Sales | **Sub-Module:** Commercial Quoting & Pricing Engine
- **BRD Source:** BRD §6.1, §7.3; FR-SALES-002, FR-SALES-004
- **Stage Classification:** `BRD-REQUIRED` (Core Entity & Pipeline Stage)
- **1. Purpose & Objective:** Generate formal commercial price quotations specifying item pricing, volume tiers, tax calculations, payment terms, and delivery schedules.
- **2. Actors & Roles:** Sales Executive, Pricing Manager, Commercial Director.
- **3. Preconditions:** Customer Master active, Item Master active, Enquiry or Opportunity reference established.
- **4. Inputs:** Customer reference, Enquiry/Opportunity reference, currency, price list, line items (item code, description, quantity, UOM, unit rate, discount percentage), tax template, payment terms, quotation validity expiry date (`valid_till`).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Generates commercial quotations detailing line items, prices, discounts, and taxes (`FR-SALES-002`).
  - `[BRD-DERIVED]` Computes net item amounts, line discounts, global discounts, and statutory taxes via the tax calculation engine.
  - `[ERP-REFERENCE / PROPOSED]` Enforces validity dates; warns or blocks order booking if expired unless overridden by authorized role.
  - `[PROPOSED / Reference Baseline]` Manages quotation revisions/versions while retaining historical records.
- **6. Business Rules:**
  - `[PROPOSED / Subject to OQ-003 Approval Policies]` Discount thresholds exceeding standard pricing policy trigger approval workflow (`DEP-010`, `OQ-003`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Line item pricing defaults from approved Price Lists (`FR-SALES-004`).
- **7. Validations:** Validity date must be greater than or equal to quote date; line quantities must be positive.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Lifecycle (`PROPOSED`):* `Draft` → `Pending Approval` → `Issued / Sent` → `Accepted` → `Ordered` (or `Expired` / `Declined`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Quotation` (`selling/doctype/quotation/`) with `taxes_and_totals.py` calculation engine.
  - *Adoption Assessment:* Item pricing calculation, tax application, and validity tracking adopted from ERP reference baseline (`ERP-REFERENCE`).
  - *KIYA Differentiator:* Mandatory upstream linkage to dedicated `Enquiry` entity (`BRD-REQUIRED`).
- **10. Cross-Module Handoffs:** Source document for Sales Order generation (`DEP-001`).
- **11. Acceptance Criteria:**
  - Converting an accepted Quotation must generate a Sales Order copying line items, pricing, and tax structures accurately.
  - System enforces validity date controls during conversion to Sales Order.

---

### Stage 5: Sales Order Commitment
- **Requirement ID:** `DR-C2C-005`
- **Phase 0A Baseline ID:** `FR-SALES-003` (Sales Orders)
- **Module:** Sales | **Sub-Module:** Order Booking & Customer Commitment
- **BRD Source:** BRD §6.1, §7.3; FR-SALES-003; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Entity & Pipeline Stage)
- **1. Purpose & Objective:** Record confirmed customer orders, lock commercial terms, establish delivery schedules, and initiate supply chain fulfillment.
- **2. Actors & Roles:** Sales Administrator, Order Desk Manager, Credit Controller.
- **3. Preconditions:** Customer Master active; Quotation accepted or direct commercial order validated; Customer PO reference provided.
- **4. Inputs:** Customer reference, Customer PO number and date, linked Quotation ID (if applicable), ordered items, quantities, agreed rates, delivery dates per line, billing address, shipping address, tax GSTIN context, payment terms.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Books confirmed customer sales orders with locked commercial pricing and terms (`FR-SALES-003`).
  - `[BRD-DERIVED]` Triggers downstream inventory availability checks and demand allocation.
  - `[BRD-DERIVED]` Tracks fulfillment and billing progress indicators (`delivered_qty`, `billed_amt`).
- **6. Business Rules:**
  - `[BRD-DERIVED / Approved Flow Rule - CD-001, Doc 22 §3.1]` **Sequential C2C Fulfillment Rule:** Core physical goods fulfillment mandates physical dispatch via Delivery Note before commercial invoicing (rejecting ERPNext's direct invoice-before-delivery bypass for physical product fulfillment).
  - `[PROPOSED Policy / TBD - Subject to Credit Policy Configuration]` Customer credit limit checking and overdue invoice hold rules are candidate risk-management policies subject to tenant credit control configuration (`TBD`).
- **7. Validations:**
  - `[ERP-REFERENCE / PROPOSED Validation]` Customer PO date must be on or before Order date; warehouse location specified for deliverable items.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Operational Lifecycle (`PROPOSED`):* `Draft` → `Confirmed / Booked` → `In Fulfillment` → `Delivered` → `Closed` (or `On Hold` / `Cancelled`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Sales Order` (`selling/doctype/sales_order/`) with child table `Sales Order Item`.
  - *Adoption Assessment:* Core sales order structure, customer PO capture, and progress tracking percentages adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Core Flow Rule:* Rejection of ERPNext's direct `Sales Order → Sales Invoice` bypass for physical inventory fulfillment (`CD-001`).
- **10. Cross-Module Handoffs:** Triggers Stage 6 (Availability Check) and feeds Stage 8 (MRP / Planning) (`DEP-002`, `DEP-003`).
- **11. Acceptance Criteria:**
  - Booking a Sales Order locks line pricing and records traceable link fields to the source Quotation.
  - Cancellation of an active order verifies that no downstream delivery or production order is actively running.

---

### Stage 6: Availability Check (ATP & Allocation)
- **Requirement ID:** `DR-C2C-006`
- **Phase 0A Baseline ID:** `FR-SALES-003` (Sales Orders), `FR-INV-002` (Stock Quantity)
- **Module:** Sales / Inventory | **Sub-Module:** Available-to-Promise (ATP) & Stock Allocation
- **BRD Source:** BRD §6.1, §7.8; FR-SALES-003, FR-INV-002; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Evaluate real-time physical inventory availability across warehouses, calculate Available-to-Promise (ATP) balances, and initiate reservation holds.
- **2. Actors & Roles:** Order Fulfillment Coordinator, Inventory Controller.
- **3. Preconditions:** Confirmed Sales Order line items exist.
- **4. Inputs:** Item code, required delivery date, requested quantity, target ship-from warehouse.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Checks inventory availability across designated warehouses (`FR-INV-002`).
  - `[BRD-DERIVED]` Calculates net available stock: `Actual Physical Stock - Existing Reserved Stock = Available to Promise`.
  - `[BRD-DERIVED]` If stock is sufficient: Allocates stock to Sales Order line for picking.
  - `[BRD-DERIVED / PROPOSED]` If stock is insufficient (shortage): Flags shortage balance for production or procurement planning.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline Policy]` Inventory allocation policy may prioritize FIFO / earliest expiry for perishable or batch-managed goods.
  - `[TBD - Governed under Open Question OQ-007]` Shortage handling and backorder splitting behavior (partial delivery vs. complete order shipment) is an open policy question (`OQ-007`).
- **7. Validations:** Availability checks must query live ledger balances, not uncommitted cache data.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Line Allocation Statuses (`PROPOSED`):* `Fully Allocated` / `Partially Allocated` / `Backordered / Out of Stock`.
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext uses `Bin.projected_qty` and `Stock Reservation Entry` (SRE) (`stock/doctype/stock_reservation_entry/`).
  - *Adoption Assessment:* Explicit reservation voucher concept adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Planned Enhancements:* Multi-warehouse ATP lookahead across regional distribution branches (`BRD-DERIVED`).
- **10. Cross-Module Handoffs:** Sufficient stock routes to Stage 7 / Stage 11 (Warehouse Picking); shortages route to Stage 8 (MRP / Planning) (`DEP-002`, `DEP-003`).
- **11. Acceptance Criteria:**
  - When stock is confirmed, an allocation hold prevents other sales orders from claiming the same inventory.
  - Shortage quantities are transparently visible to supply chain planning.

---

### Stage 7: Inventory Reservation & Hold
- **Requirement ID:** `DR-C2C-007`
- **Phase 0A Baseline ID:** `FR-INV-002` (Stock Quantity), `FR-INV-003` (Batch/Serial)
- **Module:** Inventory | **Sub-Module:** Stock Reservation & Batch Pegging
- **BRD Source:** BRD §6.1, §7.8; FR-INV-002, FR-INV-003
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Place formal, traceable inventory holds against specific warehouse stock, batches, or serial numbers to guarantee fulfillment of booked orders.
- **2. Actors & Roles:** Inventory Controller, System Automation Service.
- **3. Preconditions:** Successful Availability Check allocation.
- **4. Inputs:** Sales Order reference, line item, warehouse, reserved quantity, batch number (if batch-managed), serial numbers (if serialized).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Tracks stock reservation against confirmed orders (`FR-INV-002`).
  - `[BRD-DERIVED]` Generates a reservation record pegging specific stock to the Sales Order.
  - `[BRD-DERIVED]` Increments reserved stock metrics, decrementing available-to-promise balances.
  - `[PROPOSED / TBD Configuration]` Auto-releases reservation if order is cancelled or if reservation expiry threshold lapses.
- **6. Business Rules:**
  - `[BRD-DERIVED / PROPOSED]` Batch and serial pegging is enforced for serialized or regulated items (`FR-INV-003`).
  - `[BRD-DERIVED]` Reserved stock cannot be consumed by unlinked manual stock issues or other sales orders.
- **7. Validations:** Reserved quantity cannot exceed unreserved physical stock on hand.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Voucher Status (`PROPOSED`):* `Reserved` → `Partially Delivered` → `Fully Delivered` (or `Released / Expired`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Stock Reservation Entry` (`stock_reservation_entry.py`) updates `Bin.reserved_qty`.
  - *Adoption Assessment:* Explicit reservation document mechanism adopted as reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Reserved stock unblocks Warehouse Picking & Packing (Stage 11) (`DEP-002`).
- **11. Acceptance Criteria:**
  - System prevents picking or dispatching reserved items for any order other than the tagged Sales Order.

---

### Stage 8: MRP & Material Planning Explosion
- **Requirement ID:** `DR-C2C-008`
- **Phase 0A Baseline ID:** `FR-MRP-001` (Demand Planning), `FR-MRP-002` (Material Requirements), `FR-MRP-004` (Production Planning)
- **Module:** MRP & Planning | **Sub-Module:** Demand Explosion & Supply Generation
- **BRD Source:** BRD §6.1, §7.11; FR-MRP-001, FR-MRP-002, FR-MRP-004; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Explode unfulfilled sales order demand through multi-level Bills of Materials (BOM), calculate gross and net component requirements, and generate production work orders or purchase requisitions.
- **2. Actors & Roles:** Production Planner, Materials Manager.
- **3. Preconditions:** Sales Order confirmed with shortage/unallocated quantities; active BOMs exist for manufactured products.
- **4. Inputs:** Sales Order shortage lines, required delivery dates, Bill of Materials (BOM), on-hand stock, open purchase orders, open work orders, safety stock thresholds.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Explodes demand through multi-level BOMs into component requirements (`FR-MRP-001`, `FR-MRP-002`).
  - `[BRD-DERIVED]` Nets gross requirements against available inventory and scheduled receipts.
  - `[BRD-REQUIRED]` Generates planned supply orders: Work Orders for manufactured items and Purchase Requisitions for raw materials (`FR-MRP-004`).
- **6. Business Rules:**
  - `[ERP-REFERENCE / PROPOSED]` Lead-time backward scheduling: Calculates planned production start dates using BOM operation and item lead times.
  - `[ERP-REFERENCE / PROPOSED]` Safety stock thresholds may trigger replenishment recommendations.
  - `[TBD / Unresolved - Governed under Open Question OQ-008]` Capacity-constrained scheduling (Finite vs. Infinite MRP capacity) remains an open clarification question (`OQ-008`).
- **7. Validations:** Manufactured items must have an active, approved default BOM (`FR-MFG-001`).
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Planning Status (`PROPOSED`):* `Draft Plan` → `Calculated` → `Orders Released` (or `Cancelled`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Production Plan` (`manufacturing/doctype/production_plan/`) queries sales orders and executes BOM explosion.
  - *Adoption Assessment:* Demand import, multi-level BOM explosion, and work order/purchase requisition generation adopted as reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Releases Work Orders to Manufacturing (Stage 9) and Purchase Requisitions to Procurement (`DEP-003`, `DEP-004`).
- **11. Acceptance Criteria:**
  - Running MRP for a finished good shortage generates work orders for assemblies and purchase requests for shortage raw materials.

---

### Stage 9: Shop Floor Production Execution
- **Requirement ID:** `DR-C2C-009`
- **Phase 0A Baseline ID:** `FR-MFG-001` (BOM), `FR-MFG-002` (Routing), `FR-MFG-003` (Work Orders), `FR-MFG-005` (Shop Floor)
- **Module:** Manufacturing | **Sub-Module:** Work Order Execution & Job Card Tracking
- **BRD Source:** BRD §6.1, §7.10; FR-MFG-001, FR-MFG-002, FR-MFG-003, FR-MFG-005
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Execute factory manufacturing orders, transfer raw materials to WIP, track shop-floor routing operations via Job Cards, and record finished goods production.
- **2. Actors & Roles:** Production Supervisor, Machine Operator, Shop Floor Workstation Lead.
- **3. Preconditions:** Work Order released from MRP or manually created; raw materials available in stores.
- **4. Inputs:** Work Order ID, target item, quantity to produce, BOM reference, routing sequence, assigned workstations.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Tracks work order execution from release through completion (`FR-MFG-003`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Stage 9A (Material Issue): Transfers raw materials from stores to WIP warehouse via stock transfer.
  - `[BRD-DERIVED / ERP-REFERENCE]` Stage 9B (Operation Tracking): Tracks operations, workstation times, and completed quantities via Job Cards (`FR-MFG-005`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Stage 9C (Production Receipt): Records finished goods production, consumes WIP inventory, and routes completed lots to Quality Check.
- **6. Business Rules:**
  - `[PROPOSED / Reference Baseline Policy]` Material consumption variance exceeding defined BOM tolerance triggers supervisor authorization.
  - `[PROPOSED / Reference Baseline]` Scrap and by-product quantities recorded against standard scrap percentages (`FR-MFG-007`).
- **7. Validations:**
  - `[PROPOSED / Configurable Parameter]` Produced quantity cannot exceed authorized work order quantity plus permitted over-production tolerance.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Work Order Status (`PROPOSED`):* `Not Started` → `In Process` → `Completed` (or `Stopped` / `Cancelled`).
  - *Candidate Job Card Status (`PROPOSED`):* `Open` → `In Progress` → `Completed`.
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Work Order`, `Job Card`, and `Stock Entry` (types: Material Transfer for Manufacture, Manufacture) (`manufacturing/`).
  - *Adoption Assessment:* 3-stage manufacturing transaction model (Transfer → Job Card → Manufacture Receipt) adopted as proven reference baseline (`ERP-REFERENCE`).
  - *KIYA Guardrail:* Clear functional separation between factory manufacturing Work Orders and Field Service Work Orders (`CD-001`, Doc 27 Correction 1).
- **10. Cross-Module Handoffs:** Routes completed production lots to Quality Check (Stage 10) before warehouse putaway (`DEP-004`).
- **11. Acceptance Criteria:**
  - Completing production posts inventory ledger deductions for raw materials and creates an uninspected finished goods receipt.

---

### Stage 10: In-Process & Final Quality Check
- **Requirement ID:** `DR-C2C-010`
- **Phase 0A Baseline ID:** `FR-QLTY-003` (In-Process Inspection), `FR-QLTY-004` (Final Inspection), `FR-QLTY-006` (NCR/CAPA)
- **Module:** Quality | **Sub-Module:** Inspection Gating & Non-Conformance Management
- **BRD Source:** BRD §6.1, §7.12; FR-QLTY-003, FR-QLTY-004, FR-QLTY-006; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Inspect manufactured or incoming goods against defined quality parameters, verify tolerances, and gate inventory putaway into sellable stock.
- **2. Actors & Roles:** Quality Inspector, Quality Assurance Manager.
- **3. Preconditions:** Finished goods produced from Work Order or operation completed.
- **4. Inputs:** Reference Work Order / Job Card ID, item code, inspection lot size, quality inspection template, observed test readings.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Performs quality inspections against defined parameter templates (`FR-QLTY-003`, `FR-QLTY-004`).
  - `[BRD-DERIVED]` Determines inspection verdict: `Accepted`, `Rejected`, or `Accepted with Concession`.
  - `[BRD-DERIVED]` If Accepted: Releases inspected goods to sellable finished goods warehouse.
  - `[PROPOSED / High-Value KIYA Enhancement]` If Rejected: Quarantines rejected lot and initiates Non-Conformance Report (NCR) workflow (`FR-QLTY-006`).
- **6. Business Rules:**
  - `[BRD-DERIVED / BRD §6.1, §7.12]` **Mandatory Quality Gating:** Finished goods cannot be received into sellable warehouse inventory without an approved Quality Inspection.
  - `[PROPOSED / Candidate Differentiator - Subject to Stakeholder Confirmation]` **Automated Inspection-to-NCR Pipeline:** An automated pipeline creating an NCR immediately upon Quality Inspection rejection is proposed as an enterprise differentiator. (Note: BRD mandates both Quality Inspection and NCR/CAPA capabilities, but does not explicitly mandate an automated trigger; ERPNext has no such mapper. This automation is therefore classified as `PROPOSED`, awaiting stakeholder sign-off).
- **7. Validations:** Sample size must conform to defined inspection lot criteria.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Inspection Status (`PROPOSED`):* `Pending Inspection` → `Accepted` / `Rejected` / `Quarantined`.
- **9. Traceable Reference Baseline & KIYA Differentiator:**
  - *Reference Behavior:* ERPNext `Quality Inspection` (`stock/doctype/quality_inspection/`).
  - *Adoption Assessment:* Parameter reading comparison and inspection document structure adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Differentiator Analysis:* ERPNext Quality Inspection rejection does NOT automatically create an NCR. The automated QI-rejection-to-NCR state machine is a proposed KIYA enhancement (`PROPOSED (Candidate KIYA Differentiator)`).
- **10. Cross-Module Handoffs:** Accepted goods route to Warehouse Putaway (Stage 11); rejected goods route to Quality Quarantine / MRB (`DEP-004`).
- **11. Acceptance Criteria:**
  - Rejected finished goods lots are blocked from transfer to sellable inventory.
  - Quality inspection records store parameter readings against defined acceptance criteria.

---

### Stage 11: Warehouse Putaway & Outbound Fulfillment
- **Requirement ID:** `DR-C2C-011`
- **Phase 0A Baseline ID:** `FR-WH-001` (Warehouse Setup), `FR-WH-002` (Bin Locations), `FR-WH-004` (Outbound), `FR-WH-005` (Pick/Pack)
- **Module:** Warehouse | **Sub-Module:** Physical Bin Management, Picking & Packing
- **BRD Source:** BRD §6.1, §7.9; FR-WH-001, FR-WH-002, FR-WH-004, FR-WH-005; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage; Physical WMS Differentiator)
- **1. Purpose & Objective:** Manage physical warehouse putaway into storage bins, generate picking waves against reserved sales orders, execute packing, and stage goods for dispatch.
- **2. Actors & Roles:** Warehouse Supervisor, Forklift Operator, Picker/Packer.
- **3. Preconditions:** Quality Inspection approved (for manufactured goods) or stock reserved; Sales Order ready for fulfillment.
- **4. Inputs:** Sales Order ID, item codes, quantities, target shipping warehouse, physical bin locations, packing specifications.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Manages physical warehouse layout and bin locations (`FR-WH-001`, `FR-WH-002`).
  - `[BRD-REQUIRED]` Manages picking and packing workflows (`FR-WH-004`, `FR-WH-005`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Generates Pick Lists directing warehouse personnel to designated storage bins.
  - `[ERP-REFERENCE / PROPOSED]` Generates Packing Slips recording package dimensions, gross weight, and container IDs.
- **6. Business Rules:**
  - `[BRD-REQUIRED / KIYA Differentiator]` **Physical WMS Location Rule:** System must track true physical storage topologies (aisles, racks, shelves, bins) (`FR-WH-002`), distinct from ERPNext's item-quantity cache.
  - `[PROPOSED / Reference Baseline]` Barcode / QR scan verification during picking is supported (`FR-WH-005`, `FR-MOB-004`).
- **7. Validations:** Packed quantity cannot exceed picked quantity; package weight must be positive.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Pick List Status (`PROPOSED`):* `Draft` → `Assigned` → `Picking` → `Picked` → `Packed / Staged`.
- **9. Traceable Reference Baseline & KIYA Differentiator:**
  - *Reference Behavior:* ERPNext `Pick List` and `Packing Slip` (`stock/`).
  - *Adoption Assessment:* Pick list generation and packing slip structure adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Core Differentiator (`BRD-REQUIRED`):* ERPNext `Bin` is an item-balance cache, not a physical bin location. KIYA mandates true physical coordinate location tracking (`FR-WH-002`, Doc 27 Correction 3).
- **10. Cross-Module Handoffs:** Packed shipments handoff to Dispatch Management (Stage 12) (`DEP-002`).
- **11. Acceptance Criteria:**
  - Pick lists display designated physical storage bin locations.
  - Completing packing transitions shipment to ready-for-dispatch status.

---

### Stage 12: Dispatch & Delivery Note
- **Requirement ID:** `DR-C2C-012`
- **Phase 0A Baseline ID:** `FR-SALES-005` (Delivery & Dispatch), `FR-INV-002` (Stock Quantity)
- **Module:** Sales / Logistics | **Sub-Module:** Commercial Dispatch & Stock Issuance
- **BRD Source:** BRD §6.1, §7.3, §7.15; FR-SALES-005; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Issue goods out of the warehouse, generate legal delivery notes / transport manifests, update inventory stock ledgers, and trigger shipment transit.
- **2. Actors & Roles:** Dispatch Officer, Logistics Coordinator, Gate Security.
- **3. Preconditions:** Packing completed; carrier/vehicle assigned; Sales Order in fulfillment status.
- **4. Inputs:** Sales Order reference, Packing Slip ID, carrier details, vehicle number, driver details, tracking number, ship-to address, delivery note date.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Issues delivery notes and transport manifests (`FR-SALES-005`).
  - `[BRD-REQUIRED / BRD-DERIVED]` Permanently decrements physical inventory in the stock ledger upon dispatch submission (`FR-INV-002`).
  - `[BRD-DERIVED]` Updates Sales Order `delivered_qty` and fulfillment progress metrics.
  - `[BRD-DERIVED]` Releases/consumes active `Stock Reservation Entry` (SRE) vouchers.
  - `[ERP-REFERENCE / Standard Practice]` Posts perpetual inventory GL entries (debits COGS, credits Stock In Hand).
- **6. Business Rules:**
  - `[BRD-DERIVED / Approved Flow Rule - CD-001, Doc 22 §3.1]` **Sequential C2C Flow Rule:** Physical dispatch via Delivery Note must occur before commercial sales invoicing in core physical fulfillment.
  - `[PROPOSED / Reference Baseline]` Over-delivery allowance is governed by configurable tolerance settings.
- **7. Validations:** Dispatched quantity cannot exceed un-delivered order balance.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Delivery Note Status (`PROPOSED`):* `Draft` → `Dispatched / In Transit` → `Delivered` (or `Return Initiated` / `Cancelled`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Delivery Note` (`stock/doctype/delivery_note/`), updating `so_detail` and executing `stock_controller.py:make_sl_entries()`.
  - *Adoption Assessment:* Delivery Note data structure, child link mapping (`so_detail`), and perpetual inventory posting adopted as reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Triggers commercial Invoicing (Stage 13) and logistics tracking (`DEP-002`, `DEP-005`).
- **11. Acceptance Criteria:**
  - Submitting a Delivery Note decrements physical stock balances in the stock ledger and updates the Sales Order delivered quantity.

---

### Stage 13: Commercial Sales Invoicing
- **Requirement ID:** `DR-C2C-013`
- **Phase 0A Baseline ID:** `FR-SALES-005` (Delivery & Dispatch), `FR-FIN-003` (Accounts Receivable)
- **Module:** Sales / Finance | **Sub-Module:** Commercial Billing & Receivable Invoicing
- **BRD Source:** BRD §6.1, §7.3, §7.17; FR-SALES-005, FR-FIN-003; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Generate commercial legal billing invoices based on dispatched goods, establishing accounts receivable obligations against the customer.
- **2. Actors & Roles:** Billing Specialist, Accounts Receivable Clerk, Finance Manager.
- **3. Preconditions:** Submitted Delivery Note exists with unbilled quantities.
- **4. Inputs:** Delivery Note reference, Sales Order reference, customer billing details, dispatched items and quantities, agreed rates, tax categorization context, payment terms.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Generates commercial sales invoices establishing accounts receivable (`FR-FIN-003`).
  - `[BRD-DERIVED]` Pulls dispatched quantities and prices from Delivery Note lines (`dn_detail`).
  - `[BRD-REQUIRED]` Calls Global Tax Engine (Stage 14) for statutory tax determination (`FR-TAX-001`).
  - `[BRD-DERIVED]` Updates `billed_amt` and `per_billed` on source Sales Order and Delivery Note.
- **6. Business Rules:**
  - `[BRD-DERIVED / Approved Flow Rule - CD-001, Doc 22 §3.1]` **Invoicing Sequence Rule:** Invoices for physical goods must reference a verified Delivery Note.
  - `[BRD-DERIVED]` Line pricing must reconcile to locked Sales Order terms unless an authorized commercial amendment is approved.
- **7. Validations:** Billed quantity cannot exceed delivered quantity; posting date must fall in an open fiscal period.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Invoice Status (`PROPOSED`):* `Draft` → `Posted / Unpaid` → `Partially Paid` → `Paid in Full` (or `Overdue` / `Cancelled`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Sales Invoice` (`accounts/doctype/sales_invoice/`) linked via `dn_detail`.
  - *Adoption Assessment:* Invoicing calculation, payment terms scheduling, and line mapping adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Core Flow Rule:* Rejection of ERPNext's direct `Sales Order → Sales Invoice` bypass for physical inventory fulfillment (`CD-001`).
- **10. Cross-Module Handoffs:** Handoff to Tax Engine (Stage 14) and General Ledger Accounting (Stage 16) (`DEP-005`).
- **11. Acceptance Criteria:**
  - Sales Invoice created from a Delivery Note populates shipped quantities and agreed pricing without manual re-entry.

---

### Stage 14: Global Tax Engine & Statutory Compliance
- **Requirement ID:** `DR-C2C-014`
- **Phase 0A Baseline ID:** `FR-TAX-001` (Global Tax Engine), `FR-TAX-003` (GST/VAT), `FR-TAX-005` (E-Invoicing/E-Way Bill)
- **Module:** Tax & Statutory Compliance | **Sub-Module:** Multi-National Tax Determination & India Compliance
- **BRD Source:** BRD §6.1, §7.18; FR-TAX-001, FR-TAX-003, FR-TAX-005; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Mandatory Regulatory Engine)
- **1. Purpose & Objective:** Determine statutory tax liabilities across national and regional jurisdictions, calculate GST/VAT/Sales Tax, and support statutory e-invoicing and e-way bill compliance.
- **2. Actors & Roles:** Tax Specialist, Finance Controller, System Automation Gateway.
- **3. Preconditions:** Sales Invoice lines populated with Item codes, HSN/SAC codes, and branch/shipping addresses.
- **4. Inputs:** Company GSTIN/Tax ID, Customer GSTIN/Tax ID, place of supply, shipping origin/destination, item HSN/SAC code, taxable line values.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Determines statutory tax classifications across jurisdictions (`FR-TAX-001`, `FR-TAX-003`):
    - Intra-state (India): CGST + SGST split.
    - Inter-state (India): IGST.
    - Export / SEZ: Zero-rated or with payment of IGST.
  - `[BRD-REQUIRED]` Applies item-specific tax rates and statutory exemptions (`FR-TAX-003`).
  - `[BRD-REQUIRED Capability / TBD Implementation Architecture]` Generates statutory e-invoicing (IRN) and e-Way Bill compliance data (`FR-TAX-005`). (Note: Statutory API gateway integration method is an open clarification question under `OQ-005`).
- **6. Business Rules:**
  - `[BRD-REQUIRED / FR-TAX-003]` HSN/SAC classification is mandatory on all commercial invoice lines.
  - `[PROPOSED Statutory Rule / TBD Implementation]` Applicable invoices generate statutory Invoice Reference Number (IRN) and QR codes per statutory turnover rules.
- **7. Validations:** Tax rate calculation must reconcile to statutory jurisdiction rounding rules.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Compliance Status (`PROPOSED`):* `Tax Computed` → `IRN Generated` → `E-Way Bill Active` (or `Sync Error / Pending Retry`).
- **9. Traceable Reference Baseline & KIYA Differentiator:**
  - *Reference Finding (Doc 21 §Regional, Doc 24 §18, Doc 27 Correction 2):* **India GST and statutory e-invoicing were removed from the ERPNext develop core repository** (`remove_india_localisation.py`).
  - *KIYA Core Requirement (`BRD-REQUIRED`):* Global Tax Engine and India GST/e-invoicing are **100% KIYA-owned or integrated capabilities**. The reference baseline provides only generic table tax structures (`taxes_and_totals.py`).
  - *Statutory Architecture (`TBD`):* Governed under Open Question `OQ-005` (Built-in GSP/ASP connector vs. third-party middleware).
- **10. Cross-Module Handoffs:** Provides tax liability distribution lines to General Ledger (Stage 16) (`DEP-005`).
- **11. Acceptance Criteria:**
  - Submitting an invoice for an Indian branch entity automatically determines CGST/SGST vs. IGST based on place of supply and summarizes HSN totals.

---

### Stage 15: Payment Collection & Cash Application
- **Requirement ID:** `DR-C2C-015`
- **Phase 0A Baseline ID:** `FR-FIN-003` (Accounts Receivable), `FR-FIN-004` (Cash & Bank)
- **Module:** Finance & Accounting | **Sub-Module:** AR Cash Application & Bank Settlement
- **BRD Source:** BRD §6.1, §7.17; FR-FIN-003, FR-FIN-004; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & Flow Stage)
- **1. Purpose & Objective:** Record customer payment receipts across banking and digital channels, reconcile receipts against open invoices, and allocate deductions or advances.
- **2. Actors & Roles:** Cashier, AR Collector, Treasury Specialist.
- **3. Preconditions:** Submitted Sales Invoice with outstanding balance > 0, or customer advance payment receipt.
- **4. Inputs:** Customer reference, payment date, payment mode (wire, check, digital gateway), deposit bank account, received amount, invoice allocation references, write-offs/bank charges.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Records customer payment transactions across channels (`FR-FIN-004`).
  - `[BRD-REQUIRED]` Reconciles received cash against open Sales Invoices (`FR-FIN-003`).
  - `[BRD-DERIVED]` Updates invoice outstanding balances and status (`Partially Paid`, `Paid in Full`).
  - `[BRD-DERIVED / ERP-REFERENCE]` Supports customer advances, permitting future allocation against subsequent invoices.
- **6. Business Rules:**
  - `[BRD-DERIVED]` Payment allocation cannot exceed invoice outstanding balance unless explicitly booked as an unallocated customer advance.
  - `[ERP-REFERENCE / PROPOSED]` Multi-currency receipts compute realized exchange gain/loss at settlement.
- **7. Validations:** Received amount must be positive; deposit bank account must be active.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Payment Status (`PROPOSED`):* `Draft` → `Cleared / Posted` (or `Bounced / Cancelled`).
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `Payment Entry` (`accounts/doctype/payment_entry/`) with `Payment Ledger Entry` (PLE) reconciliation.
  - *Adoption Assessment:* Core payment entry structure, deduction tables, and multi-currency reconciliation adopted as reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Clears Accounts Receivable balance in General Ledger (Stage 16) (`DEP-005`).
- **11. Acceptance Criteria:**
  - Submitting a payment matching an invoice's outstanding balance updates the invoice business status to `Paid in Full`.

---

### Stage 16: General Ledger Accounting Integration
- **Requirement ID:** `DR-C2C-016`
- **Phase 0A Baseline ID:** `FR-FIN-001` (General Ledger), `FR-FIN-006` (Cost Accounting)
- **Module:** Finance & Accounting | **Sub-Module:** Double-Entry Bookkeeping & Financial Posting
- **BRD Source:** BRD §6.1, §7.17; FR-FIN-001, FR-FIN-006; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Architectural & Financial Capability)
- **1. Purpose & Objective:** Automatically post double-entry financial transactions to the General Ledger for all C2C commercial milestones (Delivery COGS, Invoicing, Tax, and Payment).
- **2. Actors & Roles:** Financial Controller, General Ledger Accountant.
- **3. Preconditions:** Company Chart of Accounts active; fiscal period open; commercial transactions submitted.
- **4. Inputs:** Voucher references (Delivery Note, Sales Invoice, Payment Entry), debit/credit accounts, amounts, cost centers, project references.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Posts balanced double-entry accounting transactions to the General Ledger (`FR-FIN-001`):
    - *At Delivery:* Debit COGS Account / Credit Stock In Hand Inventory Account (`DEP-002`).
    - *At Invoicing:* Debit Customer Accounts Receivable / Credit Sales Revenue Account & Credit Tax Liability Accounts (`DEP-005`).
    - *At Payment:* Debit Bank Account / Credit Customer Accounts Receivable (`DEP-005`).
  - `[ERP-REFERENCE / Standard Practice]` Cancellation of any posted commercial document generates offsetting reversal GL entries (`Doc 21 §Shared Mechanics`).
- **6. Business Rules:**
  - `[BRD-REQUIRED / Core Accounting Principle]` Total Debits must strictly equal Total Credits for every transaction.
  - `[BRD-DERIVED]` Postings into locked or closed accounting periods are strictly blocked.
- **7. Validations:** Account must be a leaf node (not a group node); posting currency must match account currency.
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Entry Status (`PROPOSED`):* `Posted` (immutable) / `Reversed`.
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext `GL Entry` (`accounts/doctype/gl_entry/`) and `general_ledger.py`.
  - *Adoption Assessment:* Double-entry perpetual inventory posting and cancellation reversal mechanics adopted as proven reference baseline (`ERP-REFERENCE`).
- **10. Cross-Module Handoffs:** Feeds Trial Balance, Balance Sheet, and Profitability Analysis (Stage 17) (`DEP-005`, `DEP-009`).
- **11. Acceptance Criteria:**
  - Submitting a Sales Invoice creates balanced GL entries crediting revenue and tax accounts while debiting customer accounts receivable.

---

### Stage 17: Order & Customer Profitability Analytics
- **Requirement ID:** `DR-C2C-017`
- **Phase 0A Baseline ID:** `FR-BI-001` (Dashboards), `FR-BI-003` (KPI Management)
- **Module:** Business Intelligence | **Sub-Module:** Margin & Profitability Analysis
- **BRD Source:** BRD §6.1, §7.22; FR-BI-001, FR-BI-003; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core BI Capability)
- **1. Purpose & Objective:** Calculate gross profit, contribution margins, and cost variances for sales orders, customer accounts, and product lines.
- **2. Actors & Roles:** Commercial Director, CFO, Sales Operations Lead.
- **3. Preconditions:** Completed Sales Invoice with linked Delivery Note valuation costs.
- **4. Inputs:** Invoice net revenue, inventory valuation cost (from Stock Ledger), manufacturing actual cost (from Work Order), direct freight costs.
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Analyzes order and customer profitability across commercial dimensions (`FR-BI-001`, `FR-BI-003`).
  - `[BRD-DERIVED / PROPOSED Formula]` Computes Realized Gross Profit: `Net Invoice Value - Cost of Goods Sold (COGS) - Direct Freight`.
  - `[BRD-DERIVED / PROPOSED Formula]` Computes Margin Percentage: `(Gross Profit / Net Revenue) * 100`.
  - `[BRD-DERIVED]` Aggregates profitability metrics by customer, territory, item category, and sales representative.
- **6. Business Rules:**
  - `[ERP-REFERENCE / PROPOSED]` Profitability calculations source actual inventory valuation rates from the Stock Ledger.
- **7. Validations:** Revenue and cost inputs must be denominated in company base currency.
- **8. Business Status Lifecycle (`CD-002`):**
  - Continuous analytical metric; no document transactional lifecycle.
- **9. Traceable Reference Baseline & KIYA Differentiator:**
  - *Reference Behavior:* ERPNext standard Gross Profit report (`gross_profit.py`).
  - *Adoption Assessment:* Cost-of-goods matching formula adopted as reference concept (`ERP-REFERENCE`).
  - *KIYA Planned Enhancements:* Multi-dimensional EPM profitability modeling (`FR-EPM-002`) and AI margin anomaly alerts (`FR-AIAU-003`) are classified as `PROPOSED / Future Capability`.
- **10. Cross-Module Handoffs:** Feeds executive BI dashboards and Customer 360 profile (Stage 18) (`DEP-009`).
- **11. Acceptance Criteria:**
  - System displays gross profit and percentage margin on completed sales invoice records.

---

### Stage 18: Customer 360 Timeline & History
- **Requirement ID:** `DR-C2C-018`
- **Phase 0A Baseline ID:** `FR-CRM-008` (Customer 360 View)
- **Module:** CRM | **Sub-Module:** Unified Customer History & Relationship Timeline
- **BRD Source:** BRD §6.1, §7.2; FR-CRM-008; Business Flows §1
- **Stage Classification:** `BRD-REQUIRED` (Core Capability & CRM Anchor)
- **1. Purpose & Objective:** Aggregate commercial, operational, financial, and service interactions for a customer into a unified, chronological 360-degree timeline.
- **2. Actors & Roles:** Account Manager, Customer Success Officer, Executive Leadership.
- **3. Preconditions:** Customer Master active; transactional history recorded.
- **4. Inputs:** Customer Master ID, all linked transaction records (Leads, Opportunities, Enquiries, Quotes, Orders, Deliveries, Invoices, Payments, Outstanding balances).
- **5. Core Functional Behavior:**
  - `[BRD-REQUIRED]` Provides a unified 360-degree customer view aggregating interactions across touchpoints (`FR-CRM-008`).
  - `[BRD-REQUIRED / Unified Data Model DEC-007]` Aggregates chronological interaction history from the single Customer Master entity without data duplication.
  - `[PROPOSED / Analytical Metrics]` Computes lifetime value (LTV), total revenue, average order value, payment track record (average days to pay), and active pipeline.
  - `[BRD-DERIVED]` Provides drill-down navigation to underlying source transactions.
- **6. Business Rules:**
  - `[BRD-REQUIRED / DEC-007]` Timeline data must be dynamically aggregated from the single Unified Data Model, ensuring zero cross-module duplicate customer stores.
- **7. Validations:** Access control enforced per role and territory permissions (`FR-PADM-1.2.3`).
- **8. Business Status Lifecycle (`CD-002`):**
  - *Candidate Master Entity Status (`PROPOSED`):* `Active` / `Inactive` / `Credit Blocked`.
- **9. Traceable Reference Baseline (ERP Comparison):**
  - *Reference Behavior:* ERPNext Customer Dashboard and document activity timeline.
  - *Adoption Assessment:* Dashboard counts and transaction linking adopted as reference baseline (`ERP-REFERENCE`).
  - *KIYA Planned Enhancements:* Field service history integration and AI customer health metrics (`FR-AIAU-001`) classified as `PROPOSED / Future Capability`.
- **10. Cross-Module Handoffs:** Provides unified customer context for retention, sales campaigns, and credit reviews (`DEP-001`, `DEP-009`).
- **11. Acceptance Criteria:**
  - Viewing a Customer 360 profile displays historical transaction summaries, open invoice balances, and quote/order histories from a single unified customer record.

---

## 4. Traceability & Classification Summary Matrix

| Req ID | C2C Stage | Baseline ID | Module | Primary Stage Classification | Explicit KIYA Differentiators & Candidate Enhancements | Dependency | Current Status |
|---|---|---|---|---|---|---|---|
| **DR-C2C-001** | Stage 1: Lead | `FR-CRM-001` | CRM | `BRD-REQUIRED` | Omnichannel ingestion & AI scoring (`PROPOSED`) | `DEP-001` | Baseline Corrected |
| **DR-C2C-002** | Stage 2: Opportunity | `FR-CRM-002` | CRM | `BRD-REQUIRED` | Pipeline probability defaulting (`PROPOSED`) | `DEP-001` | Baseline Corrected |
| **DR-C2C-003** | Stage 3: Enquiry | `FR-SALES-001` | Sales | `BRD-REQUIRED` | **Dedicated Enquiry Entity** (`BRD-REQUIRED`); Feasibility review (`PROPOSED / TBD`) | `DEP-001` | Baseline Corrected |
| **DR-C2C-004** | Stage 4: Quotation | `FR-SALES-002` | Sales | `BRD-REQUIRED` | Multi-tier discount thresholds (`PROPOSED / OQ-003`) | `DEP-001` | Baseline Corrected |
| **DR-C2C-005** | Stage 5: Sales Order | `FR-SALES-003` | Sales | `BRD-REQUIRED` | **Dispatch-Before-Invoicing** (`BRD-DERIVED`); Credit hold rules (`PROPOSED / TBD`) | `DEP-002`, `DEP-003` | Baseline Corrected |
| **DR-C2C-006** | Stage 6: Availability Check | `FR-SALES-003` / `INV-002` | Sales/Inv | `BRD-REQUIRED` | Multi-warehouse ATP lookahead (`BRD-DERIVED`); Shortage policy (`TBD / OQ-007`) | `DEP-002` | Baseline Corrected |
| **DR-C2C-007** | Stage 7: Stock Reservation | `FR-INV-002` / `INV-003` | Inventory | `BRD-REQUIRED` | Hard stock pegging (`BRD-DERIVED`); Expiry thresholds (`PROPOSED / TBD`) | `DEP-002` | Baseline Corrected |
| **DR-C2C-008** | Stage 8: MRP Explosion | `FR-MRP-001` / `MRP-002` | MRP | `BRD-REQUIRED` | Multi-level BOM explosion (`BRD-DERIVED`); Finite capacity (`TBD / OQ-008`) | `DEP-003` | Baseline Corrected |
| **DR-C2C-009** | Stage 9: Shop Floor Mfg | `FR-MFG-003` / `MFG-005` | Mfg | `BRD-REQUIRED` | 3-stage execution (`ERP-REFERENCE`); Variance authorization (`PROPOSED`) | `DEP-004` | Baseline Corrected |
| **DR-C2C-010** | Stage 10: Quality Check | `FR-QLTY-003` / `QLTY-004` | Quality | `BRD-REQUIRED` | Mandatory Quality Gating (`BRD-DERIVED`); **Automated QI Rejection → NCR** (`PROPOSED / TBD`) | `DEP-004` | Baseline Corrected |
| **DR-C2C-011** | Stage 11: Warehouse WMS | `FR-WH-002` / `WH-005` | Warehouse | `BRD-REQUIRED` | **True Physical Coordinate WMS Topology** (`BRD-REQUIRED`) vs. ERPNext cache | `DEP-002` | Baseline Corrected |
| **DR-C2C-012** | Stage 12: Dispatch & DN | `FR-SALES-005` / `INV-002` | Logistics | `BRD-REQUIRED` | **Dispatch-Before-Invoicing** (`BRD-DERIVED`); Gate pass mechanics (`PROPOSED`) | `DEP-002` | Baseline Corrected |
| **DR-C2C-013** | Stage 13: Sales Invoicing | `FR-SALES-005` / `FIN-003` | Finance | `BRD-REQUIRED` | Rejection of ERPNext direct SO→SI bypass (`CD-001`); DN line link (`ERP-REFERENCE`) | `DEP-005` | Baseline Corrected |
| **DR-C2C-014** | Stage 14: Global Tax Engine | `FR-TAX-001` / `TAX-003` | Tax | `BRD-REQUIRED` | **Global Tax Engine & India GST/e-Inv** (`BRD-REQUIRED`); Gateway architecture (`TBD / OQ-005`) | `DEP-005` | Baseline Corrected |
| **DR-C2C-015** | Stage 15: Payment Collect | `FR-FIN-003` / `FIN-004` | Finance | `BRD-REQUIRED` | AR reconciliation (`BRD-DERIVED`); Advance allocation & FX gain/loss (`ERP-REFERENCE / PROPOSED`) | `DEP-005` | Baseline Corrected |
| **DR-C2C-016** | Stage 16: GL Accounting | `FR-FIN-001` / `FIN-006` | Finance | `BRD-REQUIRED` | Balanced double-entry integration (`BRD-REQUIRED`); Reversal postings (`ERP-REFERENCE`) | `DEP-005` | Baseline Corrected |
| **DR-C2C-017** | Stage 17: Profitability | `FR-BI-001` / `BI-003` | BI | `BRD-REQUIRED` | Real-time margin capability (`BRD-REQUIRED`); Detailed formulas & AI alerts (`PROPOSED`) | `DEP-009` | Baseline Corrected |
| **DR-C2C-018** | Stage 18: Customer 360 | `FR-CRM-008` | CRM | `BRD-REQUIRED` | **Unified Data Model adherence** (`BRD-REQUIRED / DEC-007`); LTV & health metrics (`PROPOSED`) | `DEP-001`, `DEP-009` | Baseline Corrected |

---

## 5. Explicit KIYA Gaps & Differentiators Summary

In strict compliance with `CD-001` and anti-hallucination discipline, the following 5 areas represent explicit KIYA differentiators where standard ERPNext behavior was rejected, found absent, or expanded beyond standard ERP conventions:

1. **Dedicated Customer Enquiry Entity (DR-C2C-003) — `BRD-REQUIRED`:**
   ERPNext lacks a dedicated Enquiry DocType (collapsing enquiry details into Opportunity or Quotation text fields). KIYA strictly mandates an independent Enquiry transaction entity capturing customer specifications, BOQs, and requests for quote between Opportunity and Quotation as required by BRD §6.1.
2. **Sequential Dispatch-Before-Invoicing Enforcement (DR-C2C-012, DR-C2C-013) — `BRD-DERIVED / Approved Flow Rule`:**
   ERPNext permits direct `Sales Order → Sales Invoice` billing skipping delivery notes (`skip_delivery_note`). In KIYA core C2C physical goods fulfillment, physical warehouse dispatch via Delivery Note must precede commercial invoicing (`CD-001`, Doc 22 §3.1).
3. **Physical WMS Location Topologies (DR-C2C-011) — `BRD-REQUIRED`:**
   ERPNext `Bin` is an internal item-quantity balance cache, not a physical storage location. KIYA mandates true physical warehouse coordinate topologies (aisle, rack, shelf, bin) and barcode verification (`FR-WH-002`, `FR-WH-005`).
4. **Automated Quality-to-NCR Pipeline (DR-C2C-010) — `PROPOSED (Candidate KIYA Differentiator) / TBD`:**
   In ERPNext, Quality Inspection rejection does not automatically create a Non-Conformance Report (NCR). While BRD §7.12 mandates both Quality Inspection and NCR/CAPA, it does not explicitly dictate an automated trigger. KIYA proposes an automated inspection-rejection to quarantine/NCR state machine as a high-value operational differentiator, pending formal stakeholder confirmation of trigger rules.
5. **India GST Statutory & E-Invoicing Engine (DR-C2C-014) — `BRD-REQUIRED (Engine) / TBD (Architecture)`:**
   India GST localization was excised from the ERPNext develop core repository (`remove_india_localisation.py`). KIYA mandates a native Global Tax Engine supporting GST/VAT determination, HSN categorization, and e-invoicing (`BRD-REQUIRED`). The specific statutory API gateway integration model (built-in GSP/ASP vs. third-party middleware) is governed under open clarification question `OQ-005` (`TBD`).

---

## 6. Document Metadata & Governance

- **Prepared By:** Antigravity Enterprise Requirements Architect
- **Creation Date:** 14 September 2026 | **Correction Pass:** 14 September 2026
- **Status:** Baseline Detailed Requirements Package (Corrected Quality-Control Pass Completed)
- **Traceability Chain:** `source/KIYA360_BRD.pdf v2.0` → `docs/00-requirements/01-master-requirements.md` → `docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md` → `docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md` → `docs/00-requirements/31-customer-to-cash-detailed-requirements.md`.
- **Immediate Next Action:** Update `docs/PROJECT-STATE.md`, `.kiya/AI-HANDOFF.md`, and `.kiya/AI-CHANGELOG.md`. Await stakeholder review of C2C correction pass before initiating Batch 2 (Procure-to-Pay).
