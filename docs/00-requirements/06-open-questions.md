# KIYA 360 — Open Questions

These consequential gaps are recorded without supplying answers. All BRD Status values are TBD.

## OQ-001 — What detailed requirements beyond the listed sub-module names apply to modules 02–28?

### Question

What detailed requirements beyond the listed sub-module names apply to modules 02–28?

### Related Module

All modules except Platform & Administration

### Related Requirement

BRD §7.2–§7.28

### Why It Matters

The BRD states detailed design must expand these modules; later scope and acceptance depend on it.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-002 — What data fields, validation rules, and status values apply to each master and transaction?

### Question

What data fields, validation rules, and status values apply to each master and transaction?

### Related Module

All modules

### Related Requirement

Various

### Why It Matters

The BRD generally lists capabilities rather than record-level details.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-003 — What approval conditions, matrices, thresholds, escalation timing, and delegation rules apply to each process?

### Question

What approval conditions, matrices, thresholds, escalation timing, and delegation rules apply to each process?

### Related Module

Workflow & Approvals; Platform & Administration

### Related Requirement

FR-WFA-002 to FR-WFA-004; FR-PADM-1.2.4

### Why It Matters

Shared approvals are required, but operating rules are not defined.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-004 — Which events trigger each email, WhatsApp, SMS, push, and in-app notification, and what templates are required?

### Question

Which events trigger each email, WhatsApp, SMS, push, and in-app notification, and what templates are required?

### Related Module

Platform & Administration; Workflow & Approvals; Mobile Application

### Related Requirement

FR-PADM-1.7.1 to FR-PADM-1.7.6; FR-WFA-005; FR-MOB-006

### Why It Matters

The channels are listed but trigger/content rules are unspecified.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-005 — What tax-country rule sets are initially in scope besides India and one additional reference country, and what statutory filing behavior is required?

### Question

What tax-country rule sets are initially in scope besides India and one additional reference country, and what statutory filing behavior is required?

### Related Module

Tax & Statutory Compliance

### Related Requirement

FR-TAX-001 to FR-TAX-007

### Why It Matters

Country coverage and statutory details affect requirements validation.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-006 — What payroll and statutory calculations are required for India and the one reference country?

### Question

What payroll and statutory calculations are required for India and the one reference country?

### Related Module

HR & Payroll; Tax & Statutory Compliance

### Related Requirement

FR-HR-004

### Why It Matters

The BRD limits geographic scope but does not define calculations.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-007 — What rules define inventory reservation, valuation application, shortages, and availability-check outcomes?

### Question

What rules define inventory reservation, valuation application, shortages, and availability-check outcomes?

### Related Module

Sales; Inventory; Warehouse

### Related Requirement

FR-SALES-003 to FR-SALES-005; FR-INV-002 to FR-INV-006

### Why It Matters

These rules govern Customer-to-Cash execution but are not specified.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-008 — What rules govern demand/planning, capacity, work-order release, and exceptions?

### Question

What rules govern demand/planning, capacity, work-order release, and exceptions?

### Related Module

MRP & Planning; Manufacturing

### Related Requirement

FR-MRP-001 to FR-MRP-006; FR-MFG-003 to FR-MFG-005

### Why It Matters

Flow stages are named but planning decisions and exceptions are not.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-009 — What inspection criteria, acceptance/rejection rules, and NCR/CAPA lifecycle apply?

### Question

What inspection criteria, acceptance/rejection rules, and NCR/CAPA lifecycle apply?

### Related Module

Quality

### Related Requirement

FR-QLTY-001 to FR-QLTY-006

### Why It Matters

Quality checkpoints are required but their controls are unspecified.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-010 — What supplier-evaluation and performance-scorecard measures and calculations apply?

### Question

What supplier-evaluation and performance-scorecard measures and calculations apply?

### Related Module

Supplier Management

### Related Requirement

FR-SUPM-003; FR-SUPM-005

### Why It Matters

Procurement activity feeds the scorecard, but measures are undefined.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-011 — What asset installation, warranty, dispatch, spare-parts, and service-billing rules apply?

### Question

What asset installation, warranty, dispatch, spare-parts, and service-billing rules apply?

### Related Module

Asset Management; Maintenance & Field Service

### Related Requirement

FR-AST-001 to FR-AST-006; FR-MFS-001 to FR-MFS-007

### Why It Matters

Asset-to-Service operating policies are incomplete.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-012 — Which third-party systems, API/webhook events, data-sync rules, and error-handling expectations are required?

### Question

Which third-party systems, API/webhook events, data-sync rules, and error-handling expectations are required?

### Related Module

Integration & API

### Related Requirement

FR-INTG-001 to FR-INTG-007

### Why It Matters

No counterparties or interaction behavior are named.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-013 — What offline data, conflict resolution, synchronization behavior, and supported mobile tasks apply to each app?

### Question

What offline data, conflict resolution, synchronization behavior, and supported mobile tasks apply to each app?

### Related Module

Mobile Application

### Related Requirement

FR-MOB-001 to FR-MOB-007

### Why It Matters

Offline sync is required but detailed mobile behavior is not.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-014 — What data-access boundaries, human-review rules, outcome criteria, and governance apply to AI and automation?

### Question

What data-access boundaries, human-review rules, outcome criteria, and governance apply to AI and automation?

### Related Module

AI & Automation; Business Intelligence

### Related Requirement

FR-AIAU-001 to FR-AIAU-007; FR-BI-006

### Why It Matters

The BRD names capabilities without decision boundaries or acceptance measures.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.

## OQ-015 — What measurable availability, performance, scalability, security-monitoring, support, and real-time latency targets define the NFRs?

### Question

What measurable availability, performance, scalability, security-monitoring, support, and real-time latency targets define the NFRs?

### Related Module

All modules / Audit, Security & Compliance

### Related Requirement

BRD §10; FR-ASC-001 to FR-ASC-005

### Why It Matters

The BRD sets qualitative NFRs but not measurable targets.

### BRD Status

TBD

### Required Decision From

Not specified in the BRD.


