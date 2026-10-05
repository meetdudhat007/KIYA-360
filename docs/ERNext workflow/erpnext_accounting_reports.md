# 📊 ERPNext Accounting — All Reports Guide
> Every report from the Accounting sidebar documented: filters, columns, buttons, and use cases.

---

## 🗂️ REPORT SECTIONS OVERVIEW

| Section | Reports |
|---|---|
| **Financial Reports** | Balance Sheet, P&L, Cash Flow, Trial Balance, Consolidated, Custom, Financial Report Template |
| **Ledgers** | General Ledger, Customer Ledger Summary, Supplier Ledger Summary |
| **Registers** | AR, AP, AR Summary, AP Summary, Sales Register, Purchase Register, Item-wise Sales, Item-wise Purchase |
| **Profitability** | Gross Profit, Profitability Analysis, Sales Invoice Trends, Purchase Invoice Trends |
| **Other Reports** | Trial Balance for Party, Payment Period, Sales Partners Commission, Customer Credit Balance, Sales Payment Summary, Address & Contacts, UAE VAT 201 |

---

# 📊 FINANCIAL REPORTS

---

## 1. 📋 Balance Sheet
**URL:** `/query-report/Balance%20Sheet`

**Layman:** A **company health snapshot** — what does the company OWN (Assets) and what does it OWE (Liabilities)? The difference is Owner's Equity.
Formula: `Assets = Liabilities + Equity`

**Technical:** Pulls from GL Entry, aggregated by account root type (Asset/Liability/Equity) as of a specific date.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company to report on |
| **Date** ⭐ | Balance sheet AS OF this date (e.g., 31-Mar-2025) |
| **Finance Book** | Which parallel book (IFRS / Tax / etc.) |
| **Cost Center** | Restrict to a specific department |
| **Presentation Currency** | Display amounts in a different currency |
| **Period** | Monthly / Quarterly / Half-Yearly / Yearly column breakdown |
| **Accumulated Values** | Show running cumulative vs period-only values |
| **With Period Closing Entry** | Include Period Closing Voucher effects |
| **Show Zero Balance Accounts** | Include accounts with ₹0 balance |
| **Show Opening Balance** | Add an opening column |

### Columns
`Account | Opening Balance | Current Period | Closing Balance`

### Structure
```
ASSETS
  ├── Current Assets
  │   ├── Bank Accounts         → Your cash at bank
  │   ├── Accounts Receivable   → Customers owe you
  │   └── Stock In Hand         → Inventory value
  └── Fixed Assets
      └── Machinery, Buildings

LIABILITIES
  ├── Current Liabilities
  │   ├── Accounts Payable      → You owe suppliers
  │   └── GST Payable
  └── Long-term Liabilities

EQUITY
  ├── Share Capital
  └── Retained Earnings
```

### Buttons
| Button | What it does |
|---|---|
| **Refresh** | Re-run with current filters |
| **Export** | Download as Excel / CSV / PDF |
| **Chart** | Toggle bar chart view |
| **Print** | Printer-friendly format |
| **Email** | Send report by email |
| **Set User Default** | Save these filter settings as your personal default |
| **Click on any account** | Drills down to General Ledger filtered to that account |

---

## 2. 📈 Profit and Loss Statement
**URL:** `/query-report/Profit%20and%20Loss%20Statement`

**Layman:** "Did we make money or lose money?" Shows all income and all expenses for a period. `Profit = Income − Expenses`

**Technical:** Aggregates GL Entry by Income and Expense account root types for a date range.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | The period (e.g., 01-Apr-2024 to 31-Mar-2025) |
| **Finance Book** | Parallel accounting book |
| **Cost Center** | Department-specific P&L |
| **Period** | Monthly / Quarterly columns |
| **Accumulated Values** | Running total vs period-only |
| **Show Zero Balance** | Include accounts with no activity |
| **Include Default Book Entries** | Include base finance book |
| **Presentation Currency** | Display in alternate currency |

### Structure
```
INCOME
  ├── Sales Revenue              → Revenue from goods/services
  ├── Service Income
  └── Other Income

EXPENSES
  ├── Cost of Goods Sold (COGS)  → Direct production costs
  ├── Salaries                   → Staff costs
  ├── Rent & Utilities
  └── Depreciation

NET PROFIT / (LOSS) = Income − Expenses
```

### Key Insight
> Click any line to drill down into the General Ledger for that account.

---

## 3. 💧 Cash Flow Statement
**URL:** `/query-report/Cash%20Flow`

**Layman:** Where did the **actual cash** come from and where did it go? (P&L includes non-cash like depreciation; Cash Flow only counts real cash movement.)

**Technical:** Classifies GL entries into 3 activity types using account mapping in Cash Flow Mapping masters.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Period |
| **Finance Book** | Parallel book |
| **Period** | Monthly / Quarterly |
| **Accumulated Values** | Cumulative vs period |
| **Presentation Currency** | Alternate display currency |

### Structure
```
Cash Flow from OPERATING Activities
  + Net Profit
  + Depreciation (add back non-cash)
  ± Changes in Working Capital (AR, AP, Stock)

Cash Flow from INVESTING Activities
  − Purchase of Fixed Assets
  + Sale of Assets

Cash Flow from FINANCING Activities
  + Loans Received
  − Loan Repayments
  + Share Capital Raised
  − Dividends Paid

NET CHANGE IN CASH = Operating + Investing + Financing
```

---

## 4. ⚖️ Trial Balance
**URL:** `/query-report/Trial%20Balance`

**Layman:** A **summary of ALL accounts** with their balances — Total Debits must equal Total Credits. If not, there's a data entry error.

**Technical:** Aggregates GL Entry by account for a period. Verifies mathematical integrity of the double-entry ledger.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Fiscal Year** ⭐ | Which financial year |
| **From Date / To Date** | Sub-period |
| **Finance Book** | Parallel book |
| **Show Zero Balance** | Include dormant accounts |
| **Show Opening / Closing** | Add opening and closing debit/credit columns |

### Columns
`Account | Opening Debit | Opening Credit | Debit | Credit | Closing Debit | Closing Credit`

### Key Use
Run at month-end and year-end to verify books are balanced before generating financial statements.

---

## 5. 🌐 Consolidated Financial Statement
**URL:** `/query-report/Consolidated%20Financial%20Statement`

**Layman:** If you own multiple companies (a group), see **all their financials combined** into one report — as if they were one single business.

**Technical:** Merges GL Entry data across multiple companies in the same group, eliminating inter-company transactions.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | The parent/holding company |
| **Fiscal Year** ⭐ | Which year |
| **Report** ⭐ | Balance Sheet / Profit and Loss / Cash Flow |
| **Period** | Monthly / Quarterly breakdown |
| **Include Inter-company Transactions** | Whether to include or eliminate internal transfers |
| **Accumulated Values** | Cumulative vs period |

### Use Case
Group companies (e.g., Kiya Fabrics + Kiya Exports + Kiya Retail) → see consolidated balance sheet.

---

## 6. 🛠️ Custom Financial Statement
**URL:** `/query-report/Custom%20Financial%20Statement`

**Layman:** Build your **own financial report layout** — pick which accounts go in which sections and in what order.

**Technical:** Uses Financial Report Template master to define custom row structure, then pulls GL data.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Period |
| **Finance Book** | Parallel book |
| **Report Template** | Which Custom Template to use |
| **Period** | Monthly / Quarterly columns |

---

## 7. 📐 Financial Report Template
**URL:** `/desk/financial-report-template`

**Layman:** Design your own report structure — define rows, groupings, and which accounts appear in which section.

| Field | What it does |
|---|---|
| **Template Name** ⭐ | Name of the custom template |
| **Report Type** ⭐ | Balance Sheet / Profit and Loss / Cash Flow |
| **Module** | Which app/module this template belongs to (for export) |
| **Disabled** ✅ | Hide from selection |
| **Report Line Items table** | Each row defines: Account / Group Label / Formula / Indentation Level |

---

# 📒 LEDGER REPORTS

---

## 8. 📖 General Ledger
**URL:** `/query-report/General%20Ledger`

**Layman:** The **raw diary** of every single accounting entry — every debit and credit ever posted, in date order.

**Technical:** Direct query on GL Entry table. Most granular accounting report.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Date range |
| **Account** | Filter to one account |
| **Voucher No** | Find a specific document |
| **Party Type / Party** | Filter by customer/supplier |
| **Cost Center** | Filter by department |
| **Project** | Filter by project |
| **Finance Book** | Parallel book |
| **Group by** | Voucher / Account / Party |
| **Show Opening Entries** | Include period-opening GL rows |
| **Show Cancelled Entries** | Include reversed/cancelled documents |
| **Include Default Book Entries** | Include base book entries |
| **Accounting Dimensions** | Any custom dimensions added |

### Columns
`Date | Voucher Type | Voucher No | Account | Party | Debit | Credit | Balance | Remarks`

### Key Use
- Investigate any specific transaction
- Verify that a document posted correctly
- Audit trail for any account

---

## 9. 👤 Customer Ledger Summary
**URL:** `/query-report/Customer%20Ledger%20Summary`

**Layman:** For each customer — what was their **opening balance, total invoices raised, payments received, and closing balance** for a period?

**Technical:** Aggregates GL Entry per customer from the Receivable account.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Period |
| **Customer** | Single customer filter |
| **Customer Group** | Category filter |
| **Territory** | Region filter |
| **Presentation Currency** | Alternate currency display |
| **Include Ageing Column** | Add days overdue column |

### Columns
`Customer | Opening Balance | Invoiced | Paid | Return | Closing Balance`

### Key Use
> Monthly customer statement — print and send to each customer for account reconciliation.

---

## 10. 🏭 Supplier Ledger Summary
**URL:** `/query-report/Supplier%20Ledger%20Summary`

**Layman:** Same as Customer Ledger but for **suppliers** — what you owed, what you paid, closing balance.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Period |
| **Supplier** | Single supplier |
| **Supplier Group** | Category |

### Columns
`Supplier | Opening Balance | Invoiced | Paid | Return | Closing Balance`

---

# 📋 REGISTERS

---

## 11. 📈 Accounts Receivable
*(Already documented in main accounting guide — see full filter/column list there)*

**Quick summary:** All open/outstanding Sales Invoices with ageing buckets (0-30, 31-60, 61-90, 90+ days).

---

## 12. 📉 Accounts Payable
*(Already documented — mirror of AR but for Purchase Invoices)*

---

## 13. 📈 AR Summary (Accounts Receivable Summary)
**URL:** `/query-report/Accounts%20Receivable%20Summary`

**Layman:** Like Accounts Receivable but **collapsed to one row per customer** — not one row per invoice.

**Technical:** Groups and sums all open invoices per customer. Good for a quick overview of top debtors.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Report Date** ⭐ | As-of date |
| **Customer** | Single customer |
| **Customer Group / Territory** | Category filter |
| **Ageing Range** | Customize bucket sizes |

### Columns
`Customer | Total Invoiced | Total Paid | Total Outstanding | 0-30 | 31-60 | 61-90 | 90+`

### Key Difference from AR
- **AR Report:** One row per invoice (detailed)
- **AR Summary:** One row per customer (aggregated)

---

## 14. 📉 AP Summary (Accounts Payable Summary)
Same as AR Summary but for suppliers. One row per supplier showing total outstanding payable.

---

## 15. 🛒 Sales Register
**URL:** `/query-report/Sales%20Register`

**Layman:** A **list of all Sales Invoices** in a period with key details — customer, amount, taxes, payment status.

**Technical:** Queries Sales Invoice table with tax breakdown columns.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Invoice posting date range |
| **Customer** | Single customer filter |
| **Customer Group** | Category |
| **Territory** | Region |
| **Item Group** | Filter by item category |
| **Mode of Payment** | Cash/Bank/UPI filter |
| **Warehouse** | Filter by source warehouse |
| **Owner** | Filter by who created the invoice |
| **Cost Center** | Department filter |
| **Is Return** ✅ | Show only Credit Notes |

### Columns
`Invoice No | Date | Customer | Item | Qty | Rate | Net Amount | Tax Amount | Grand Total | Outstanding | Status`

### Key Use
- Monthly sales register for GST filing (GSTR-1)
- Sales performance by territory/customer

---

## 16. 🏭 Purchase Register
**URL:** `/query-report/Purchase%20Register`

**Layman:** A **list of all Purchase Invoices** — every bill received from suppliers in a period.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Date range |
| **Supplier** | Single supplier |
| **Supplier Group** | Category |
| **Item Group** | Item category |
| **Mode of Payment** | Payment method |
| **Is Return** ✅ | Show only Debit Notes |

### Columns
`Bill No | Date | Supplier | Net Amount | Tax Amount | Grand Total | Outstanding | Status`

### Key Use
- Monthly purchase register for GST Input Credit (GSTR-2)
- Vendor spend analysis

---

## 17. 📦 Item-wise Sales Register
**URL:** `/query-report/Item-wise%20Sales%20Register`

**Layman:** **Which products** were sold, to whom, at what price, in what quantity — one row per invoice line item.

**Technical:** Joins Sales Invoice with Sales Invoice Item child table.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Date range |
| **Item** | Single product filter |
| **Item Group** | Category |
| **Customer** | Single customer |
| **Customer Group** | Category |
| **Territory** | Region |
| **Warehouse** | Source stock location |

### Columns
`Date | Invoice No | Customer | Item Code | Item Name | Qty | UOM | Rate | Amount | Tax | Grand Total`

### Key Use
- Product-wise sales analysis
- Item-level GST register (HSN-wise for GSTR-1)
- Identify best-selling products

---

## 18. 📦 Item-wise Purchase Register
**URL:** `/query-report/Item-wise%20Purchase%20Register`

**Layman:** Which **raw materials / services** were purchased, from whom, at what rate.

### Filters
Same as Item-wise Sales Register but for Purchase Invoices (Supplier, Supplier Group instead of Customer).

### Columns
`Date | Bill No | Supplier | Item Code | Item Name | Qty | UOM | Rate | Amount | Tax | Grand Total`

### Key Use
- Raw material cost tracking
- HSN/SAC-wise purchase register for GST

---

# 💹 PROFITABILITY REPORTS

---

## 19. 💰 Gross Profit
**URL:** `/query-report/Gross%20Profit`

**Layman:** For each item sold — how much did you **make vs how much it cost** to make/buy it?
`Gross Profit = Selling Price − Cost of Goods`

**Technical:** Compares Sales Invoice amount with stock valuation rate (buying cost) per item.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Date range |
| **Sales Invoice** | Single invoice filter |
| **Item Code** | Single product |
| **Item Group** | Product category |
| **Customer** | Single customer |
| **Customer Group** | Category |
| **Territory** | Region |
| **Warehouse** | Stock location |
| **Group by** | Invoice / Item / Customer / Territory / Item Group / Customer Group |

### Columns
`Invoice No | Item | Qty | Selling Rate | Buying Rate | Selling Amount | Buying Amount | Gross Profit | Gross Profit %`

### Key Insights
- Negative gross profit = selling below cost (loss on each unit)
- Low GP% = high COGS, review supplier pricing or efficiency
- Group by Item to find most/least profitable products

---

## 20. 📊 Profitability Analysis
**URL:** `/query-report/Profitability%20Analysis`

**Layman:** P&L breakdown **sliced by a dimension** — e.g., "Show me profit/loss separately for each Sales Person, or each Territory, or each Project."

**Technical:** Aggregates GL entries across Income and Expense accounts, grouped by an accounting dimension.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Period |
| **Based on** ⭐ | **Cost Center / Project / Sales Person / Territory** — the dimension to slice by |
| **Finance Book** | Parallel book |
| **Period** | Monthly / Quarterly columns |
| **Show Zero Balance** | Include inactive dimensions |

### Columns
`Dimension | Income | Expense | Net Profit/Loss | Profit %`

### Key Use
- "Which territory is most profitable?"
- "Which project is over budget?"
- "Which sales person generates highest margin?"

---

## 21. 📈 Sales Invoice Trends
**URL:** `/query-report/Sales%20Invoice%20Trends`

**Layman:** A **monthly/quarterly trend chart** of your sales — are you growing month over month?

**Technical:** Groups Sales Invoice amounts by period (month/quarter/year).

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Based On** ⭐ | **Item / Customer / Territory / Sales Person** — what to group rows by |
| **Fiscal Year** ⭐ | Which year |
| **Period** ⭐ | Monthly / Quarterly / Half-Yearly / Yearly columns |
| **From Date / To Date** | Date range |
| **Item Group** | Product category |
| **Customer Group** | Customer category |
| **Territory** | Region |

### Columns
`[Group] | Jan | Feb | Mar | Apr | ... | Total`

### Key Use
- Spot seasonality patterns
- Compare month-over-month growth
- Identify declining customers or items

---

## 22. 📉 Purchase Invoice Trends
**URL:** `/query-report/Purchase%20Invoice%20Trends`

**Layman:** Monthly trend of **how much you're spending** — is purchase cost rising or falling?

Same structure as Sales Invoice Trends but for Purchase Invoices.

### Filters
Same as Sales Trends — based on Item / Supplier / Item Group / Supplier Group.

### Columns
`[Group] | Jan | Feb | Mar | ... | Total`

---

# 🔍 OTHER REPORTS

---

## 23. ⚖️ Trial Balance for Party
**URL:** `/query-report/Trial%20Balance%20for%20Party`

**Layman:** Like Trial Balance but **filtered to a specific customer or supplier** — see opening balance, all debits/credits, and closing balance for that party only.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Fiscal Year** ⭐ | Which year |
| **From Date / To Date** | Sub-period |
| **Party Type** ⭐ | Customer / Supplier / Employee |
| **Party** | Specific party name |
| **Account** | The AR/AP account |

### Columns
`Party | Opening Debit | Opening Credit | Debit | Credit | Closing Debit | Closing Credit`

### Key Use
- "Show me exactly what happened in Tata Motors' account this year"
- Party-level reconciliation

---

## 24. ⏰ Payment Period Based On Invoice Date
**URL:** `/query-report/Payment%20Period%20Based%20On%20Invoice%20Date`

**Layman:** **How long** did customers take to actually pay their invoices? Measures payment delay.

**Technical:** Calculates the number of days between Invoice Date and Payment Date for each paid invoice.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Invoice date range |
| **Voucher Type** | Sales Invoice / Purchase Invoice |
| **Party Type** | Customer / Supplier |
| **Party** | Specific customer/supplier |

### Columns
`Invoice No | Party | Invoice Date | Payment Date | Days to Pay | Amount`

### Key Use
- Identify slow-paying customers
- Benchmark payment terms effectiveness
- Calculate DSO (Days Sales Outstanding)

---

## 25. 🤝 Sales Partners Commission
**URL:** `/query-report/Sales%20Partners%20Commission`

**Layman:** How much **commission is owed** to each sales agent/distributor based on invoices they brought in.

**Technical:** Query Report — joins Sales Invoice with Sales Partner and commission_rate field.

### Filters
| Filter | What it does |
|---|---|
| **Company** | Which company |
| **From Date / To Date** | Invoice date range |
| **Sales Partner** | Specific partner |
| **Allocated Amount** | Minimum commission threshold |

### Columns
`Sales Invoice | Date | Customer | Sales Partner | Net Amount | Commission Rate | Commission Amount`

### Key Use
- Monthly commission payout calculation
- Partner performance tracking

---

## 26. 💳 Customer Credit Balance
**URL:** `/query-report/Customer%20Credit%20Balance`

**Layman:** Which customers have a **credit (advance payment) balance** sitting with you — i.e., they've paid more than they owe?

**Technical:** Finds customers where payment entries exceed invoiced amounts — resulting in a credit balance in their AR ledger.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Customer** | Specific customer |
| **Customer Group** | Category |

### Columns
`Customer | Opening Balance | Invoiced | Paid | Credit Balance`

### Key Use
- Identify advance payments to adjust against future invoices
- Avoid accidentally treating credit balances as revenue

---

## 27. 💰 Sales Payment Summary
**URL:** `/query-report/Sales%20Payment%20Summary`

**Layman:** Breakdown of **how customers paid** — Cash vs. Bank vs. UPI vs. Credit Card for a period.

**Technical:** Groups Payment Entry amounts by Mode of Payment for Sales transactions.

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | Payment date range |
| **Mode of Payment** | Filter to one payment method |
| **Owner** | Filter by cashier/user |
| **Customer** | Single customer |

### Columns
`Mode of Payment | Total Transactions | Total Amount`

### Key Use
- Daily cash/card settlement reconciliation
- POS end-of-day cash count verification
- Payment method preference analysis

---

## 28. 📍 Address And Contacts
**URL:** `/query-report/Address%20And%20Contacts`

**Layman:** A **directory** of all contact information — all addresses and contacts linked to customers, suppliers, or any party.

### Filters
| Filter | What it does |
|---|---|
| **Show Contact Of** ⭐ | Customer / Supplier / Lead / Company / etc. |
| **Name** | Filter by party name |

### Columns
`Party | Contact Person | Phone | Mobile | Email | Address Line 1 | City | State | Country | PIN`

### Key Use
- Export mailing list for communications
- Verify contact details are complete
- Print address labels

---

## 29. 🇦🇪 UAE VAT 201
**URL:** `/query-report/UAE%20VAT%20201`

**Layman:** The official **UAE VAT return** report — required for businesses registered for VAT in the UAE. Formats data exactly as required by the Federal Tax Authority (FTA).

**Technical:** Aggregates Sales and Purchase invoice data into the VAT 201 return structure (Box 1 through Box 14).

### Filters
| Filter | What it does |
|---|---|
| **Company** ⭐ | Which UAE company |
| **From Date / To Date** ⭐ | VAT period (quarterly) |

### Boxes in the Report
| Box | What it covers |
|---|---|
| **Box 1** | Standard rated supplies (5% VAT) |
| **Box 2** | Zero-rated domestic supplies |
| **Box 3** | Exempt supplies |
| **Box 4** | Goods imported into UAE |
| **Box 5** | Total taxable supplies |
| **Box 6** | VAT collected on sales |
| **Box 7** | Recoverable VAT paid on purchases |
| **Box 8** | Net VAT due or refundable |

---

## 🗺️ COMPLETE REPORTS MAP

```
📊 FINANCIAL REPORTS
├── Balance Sheet         → Assets vs Liabilities snapshot
├── Profit and Loss       → Income vs Expenses for a period
├── Cash Flow             → Actual cash movement
├── Trial Balance         → All account balances (must balance)
├── Consolidated Report   → Group company combined financials
├── Custom Statement      → User-defined report layout
└── Financial Report Template → Design custom report rows

📒 LEDGERS
├── General Ledger        → Every GL entry (most granular)
├── Customer Ledger       → Per-customer opening/closing summary
└── Supplier Ledger       → Per-supplier opening/closing summary

📋 REGISTERS
├── Accounts Receivable   → Open invoices with ageing (per invoice)
├── Accounts Payable      → Open bills with ageing (per invoice)
├── AR Summary            → Ageing collapsed per customer
├── AP Summary            → Ageing collapsed per supplier
├── Sales Register        → All sales invoices list
├── Purchase Register     → All purchase invoices list
├── Item-wise Sales       → Sales per product/line item
└── Item-wise Purchase    → Purchases per product/line item

💹 PROFITABILITY
├── Gross Profit          → Selling price vs cost per item
├── Profitability Analysis → P&L sliced by dimension
├── Sales Invoice Trends  → Monthly sales growth chart
└── Purchase Invoice Trends → Monthly spend trend

🔍 OTHER REPORTS
├── Trial Balance for Party → Account statement per customer/supplier
├── Payment Period        → How long customers take to pay
├── Sales Partners Commission → Commission owed to agents
├── Customer Credit Balance → Customers with advance credits
├── Sales Payment Summary → Cash/Card/UPI breakdown
├── Address And Contacts  → Party contact directory
└── UAE VAT 201           → UAE VAT return filing
```

---

## 🔘 UNIVERSAL REPORT TOOLBAR BUTTONS
*(Available on every report page)*

| Button | What it does |
|---|---|
| **▶ Run / Refresh** | Execute the report with current filter values |
| **⬇️ Export** | Download as **Excel (.xlsx)** / **CSV** / **PDF** |
| **🖨️ Print** | Open printer-friendly version |
| **📧 Email** | Send report output as email attachment |
| **📊 Chart** | Toggle a visual chart (bar/line) of the data |
| **⭐ Set User Default** | Save current filters as YOUR default for this report |
| **☁️ Share** | Get a shareable URL with filters pre-applied |
| **⚙️ Edit Columns** | Show/hide/reorder columns in the report output |
| **📌 Add to Dashboard** | Add this report as a widget on your Accounts Dashboard |
| **🔗 Drill-down** | Click any value in most reports to jump to source documents |

---

> [!TIP]
> **Item-wise Sales Register** is the most important report for **GST GSTR-1 filing** in India — it gives you HSN/SAC-wise taxable value and tax amount breakdown per invoice.

> [!IMPORTANT]
> **Gross Profit report** requires **Perpetual Inventory** to be enabled and stock valuation rates to be accurate. If items have no buying cost, the report will show incorrect 100% margins.

> [!NOTE]
> **Consolidated Financial Statement** only works when your companies are set up as a **group** (parent-child relationship) in the Company master. Single-company setups won't see this option.
