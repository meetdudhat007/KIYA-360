# 📊 ERPNext — Accounting Module: Complete Sidebar Guide (ALL Sections)
> All 24 sidebar items covered. Every field scraped live via REST API. No screenshots.

---

## 🧭 MODULE OVERVIEW

The Accounting sidebar is divided into 5 sections:
1. **Receivables** — Money coming IN (customers)
2. **Payables** — Money going OUT (suppliers)
3. **Payments** — Recording actual cash/bank movement
4. **Reports** — Financial statements and ledgers
5. **Settings** — System-wide accounting configuration

---

# 🏠 HOME / INVOICING DASHBOARD
**URL:** `/desk/invoicing`

The home page is a **quick-action dashboard** showing:

| Card / Button | What it does |
|---|---|
| **Create Sales Invoice** | Shortcut to open a blank Sales Invoice form |
| **Create Purchase Invoice** | Shortcut to open a blank Purchase Invoice form |
| **Create Payment Entry** | Shortcut to record a payment |
| **Create Journal Entry** | Shortcut to open a Journal Entry form |
| **Unpaid Sales Invoices** | Count + link to list of all overdue/unpaid sales invoices |
| **Unpaid Purchase Invoices** | Count + link to all bills you haven't paid yet |
| **Open Journal Entries** | Draft journal entries awaiting submission |
| **Bank & Cash** | Current balance summary of all bank/cash accounts |

---

# 📊 DASHBOARD — ACCOUNTS
**URL:** `/desk/dashboard-view/Accounts`

A visual analytics dashboard with live charts.

| Widget | What it shows |
|---|---|
| **Accounts Receivable (AR)** | Bar/line chart of outstanding customer balances over time |
| **Accounts Payable (AP)** | Outstanding supplier balances |
| **Monthly Sales** | Revenue trend month by month |
| **Monthly Purchases** | Purchase spend month by month |
| **Bank Balances** | Current balance of each bank account |
| **Filter buttons** | Switch between This Week / This Month / This Quarter / This Year |
| **Company selector** | Switch between companies (multi-company setup) |

---

# 🌿 CHART OF ACCOUNTS
**URL:** `/desk/account`

A **tree view** of every financial ledger in the system.

| Button | What it does |
|---|---|
| **Add Child** | Create a sub-account under the selected parent |
| **Edit** | Modify the selected account name, type, or parent |
| **Delete** | Remove account (only if no transactions posted) |
| **View Ledger** | Open General Ledger filtered to this one account |
| **Expand All / Collapse All** | Toggle the entire tree open or closed |
| **Company dropdown** | Switch between companies to see their chart |
| **Show balances** | Toggle real-time balance display next to each account |

**Account form fields:**

| Field | Layman | Technical |
|---|---|---|
| **Account Name** | Name of the ledger | e.g., "HDFC Bank", "CGST Payable" |
| **Account Number** | Optional numeric code | e.g., 1001, 2101 for structured coding |
| **Is Group** ✅ | Is this a folder (parent) or leaf (posting) account? | Group = cannot post transactions; Leaf = postable |
| **Parent Account** | Which account is above this one in the tree | e.g., "Bank Accounts" is parent of "HDFC Bank" |
| **Account Type** | Bank / Cash / Receivable / Payable / Tax / Depreciation / etc. | Drives system behavior (e.g., Receivable type = party-wise ledger) |
| **Root Type** | Asset / Liability / Equity / Income / Expense | Determines which financial statement this appears in |
| **Currency** | If this account is in a foreign currency | For foreign currency bank accounts |
| **Freeze Account** ✅ | Block any new transactions to this account | Used for old/inactive accounts |
| **Disabled** ✅ | Hide from all dropdowns without deleting | For accounts no longer in use |
| **Tax Rate** | Only for Tax accounts — the rate (e.g., 18%) | Used in automatic tax calculation |

---

# 👤 CUSTOMER
**URL:** `/desk/customer`

**Layman:** A master record for everyone who buys from you. One customer record, all their invoices linked to it.

**Technical:** The party master for AR side. All Sales Invoices, Payments, and Receivable reports are filtered by Customer.

### Customer Form Fields

| Field | Layman | Technical |
|---|---|---|
| **Customer Name** ⭐ | Full name of the customer | Required. Used on all documents. |
| **Customer Type** ⭐ | Company or Individual | Affects address format and tax treatment |
| **Alias** | Short nickname | Alternative search name |
| **Gender** | Male/Female/Other | For individual customers |
| **Customer Group** | Category (Retail, Wholesale, VIP, etc.) | Used for grouping in reports and pricing rules |
| **Territory** | Sales region | Drives territory-wise sales reports |
| **Billing Currency** | Currency for all their invoices | All invoices auto-set to this currency |
| **Company Bank Account** | Your bank for receiving payments from this customer | Pre-filled on Payment Entries |
| **Price List** | Which rate card applies | Automatically pulled into sales orders |
| **Payment Terms Template** | When payment is due | Auto-applied to all invoices (e.g., Net 30) |
| **Loyalty Program** | Rewards scheme | Customer earns points with every purchase |
| **Loyalty Program Tier** | Current tier (Bronze/Silver/Gold) | Auto-updated based on accumulated points |
| **Customer Primary Address** | Main billing address | Appears on invoices |
| **Customer Primary Contact** | Main contact person | Appears on invoices; used for email |
| **Mobile No / Email** | (Read-only) | Auto-filled from linked Contact record |
| **Default Accounts table** | Which AR account to use per company | Overrides company default for this customer |
| **Credit Limits table** | Max outstanding allowed | ERPNext blocks orders when exceeded |
| **Is Internal Customer** ✅ | Is this actually another company you own? | Enables inter-company sales |
| **Tax ID** | GST/PAN/VAT number | Printed on invoices for compliance |
| **Tax Category** | Which tax template auto-applies | e.g., "Intrastate" auto-applies CGST+SGST |
| **Tax Withholding Category** | TDS rate for this customer | TDS deducted at this rate on every payment |
| **Is Frozen** ✅ | Block all new transactions | For disputed accounts or inactive customers |
| **Disabled** ✅ | Hide from all dropdowns | Soft delete — historical data preserved |
| **Account Manager** | Internal salesperson responsible | For CRM and follow-up |
| **Sales Team table** | Multiple salespeople with commission % | Split commission credit |
| **Portal Users table** | Which users can see this customer's portal | Customer self-service portal access |
| **Lead / Opportunity / Prospect** | Where this customer came from in CRM | For full sales funnel tracking |
| **Customer Details** | Internal notes | Not visible to customer; for internal use |
| **Supplier Numbers table** | How this customer identifies YOUR company | Their PO/vendor codes for reconciliation |

**Top buttons on Customer form:**

| Button | What it does |
|---|---|
| **Save** | Save master data |
| **Fetch from GSTIN** *(India)* | Auto-fill name, address from GST portal using Tax ID |
| **View Ledger** | Open General Ledger filtered to this customer |
| **Accounting Ledger** | See all invoices and payments for this customer |
| **Dashboard tab** | See count of all linked orders, invoices, payments |

---

# 🧾 SALES INVOICE
**URL:** `/desk/sales-invoice`

*(Fully documented in previous section — see Part 1 of accounting guide)*

**Additional items not previously covered:**

| Button / Feature | What it does |
|---|---|
| **Make** dropdown (after submit) | Create linked documents: Payment Entry, Delivery Note, Credit Note, Maintenance Schedule, Project |
| **Credit Note** (from Make menu) | Creates a return/refund invoice against this one |
| **Payment** (from Make menu) | Opens a Payment Entry pre-filled to clear this invoice |
| **Subscription** (from Make menu) | Link this invoice to a recurring subscription |
| **Connection links panel** | Shows all related documents: linked Payment Entries, Delivery Notes, Return Invoices |

---

# 📋 CREDIT NOTE
**URL:** `/desk/sales-invoice/view/list?is_return=1`

**Layman:** A **refund document** — you're reversing a sale. "Customer returned goods, we give money back."

**Technical:** A Sales Invoice with `is_return = 1`. Creates reverse GL entries: Credit Debtors, Debit Sales Revenue + Tax accounts. Reduces customer's outstanding balance.

| Key difference from Sales Invoice | Detail |
|---|---|
| **Is Return (Credit Note)** ✅ | Pre-checked. This is what makes it a Credit Note. |
| **Return Against** | Which original Sales Invoice is being reversed |
| **Quantities** | Negative (e.g., -10 Kg instead of +10 Kg) |
| **Amounts** | Negative — reduces revenue and tax liability |
| **Update Billed Amount** | Optionally reduces the billed qty on original Delivery Note |

**How to create:** Open the original Sales Invoice → Click **Make → Return / Credit Note**. ERPNext pre-fills all fields automatically.

---

# 📈 ACCOUNTS RECEIVABLE REPORT
**URL:** `/desk/query-report/Accounts%20Receivable`

**Layman:** "Who owes me money and how long have they owed it?"

**Technical:** Shows all outstanding Sales Invoice amounts by customer, aged into buckets (0–30, 31–60, 61–90, 90+ days).

| Filter | What it does |
|---|---|
| **Company** | Filter to one company |
| **Report Date** | As-of date (what was outstanding ON this date) |
| **Customer** | Filter to one specific customer |
| **Customer Group** | Filter to a category of customers |
| **Payment Terms Template** | Filter by payment terms |
| **Territory** | Filter by sales region |
| **Based On** | Due Date or Posting Date (how ageing buckets are calculated) |
| **Ageing Range** | Customize bucket sizes (default: 30/60/90 days) |
| **Show Future Payments** | Include payments not yet cleared |
| **Group by Customer** | Collapse multiple invoices per customer into one row |
| **Show Delivery Notes** | Include DN details per invoice |
| **Include PO No** | Add customer PO number column |

**Columns in the report:**

| Column | What it shows |
|---|---|
| Customer | Customer name |
| Invoice No | Sales Invoice number |
| Posting Date | Invoice date |
| Due Date | Payment due date |
| Invoiced Amount | Original invoice total |
| Paid Amount | How much has been received |
| Outstanding | Still unpaid (Invoiced - Paid) |
| 0-30 / 31-60 / 61-90 / 90+ | Ageing buckets |
| Currency | Invoice currency |

**Top buttons on the report:**

| Button | What it does |
|---|---|
| **Refresh** | Re-run report with current filters |
| **Export** | Download as Excel / CSV / PDF |
| **Chart** | Toggle a bar chart view of the ageing |
| **Print** | Print the report |
| **Email** | Email the report to someone |
| **Set as User Default** | Save current filters as your personal default |

---

# 🏭 SUPPLIER
**URL:** `/desk/supplier`

**Layman:** Master record for everyone you BUY from.

**Technical:** The party master for AP side. All Purchase Invoices, Payments, and Payable reports are linked to Suppliers.

| Field | Layman | Technical |
|---|---|---|
| **Supplier Name** ⭐ | Full legal name | Required |
| **Supplier Type** ⭐ | Company or Individual | Affects tax treatment |
| **Supplier Group** | Category (Raw Material, Service, Freight, etc.) | For grouping and spend analysis |
| **Country** | Where supplier is located | For GST type (interstate = IGST) |
| **Billing Currency** | Their invoice currency | Auto-set on Purchase Orders |
| **Payment Terms** | When you must pay them | Auto-applied to Purchase Invoices |
| **Per-Company Accounts table** | Which AP account to use per company | Overrides company default |
| **Tax ID** | Their GST/PAN | Required for GST Input Credit claim |
| **Tax Withholding Category** | TDS rate to deduct when paying | TDS deducted at source on each payment |
| **Is Transporter** ✅ | Is this supplier a logistics/freight company? | Makes them selectable on Delivery Notes |
| **Block Supplier** ✅ | Stop all transactions with this supplier | For disputed suppliers |
| **Hold Type** | All / Invoices / Payments | What type of transactions are blocked |
| **Release Date** | When the block expires | Leave blank for indefinite block |
| **Is Frozen** ✅ | Block new accounting entries | Only senior role can unfreeze |
| **Disabled** ✅ | Hide from dropdowns | Soft delete |
| **Allow Purchase Invoice without PO** ✅ | Skip the Purchase Order step | For services and urgent purchases |
| **Allow Purchase Invoice without PR** ✅ | Skip the Purchase Receipt step | For service-type suppliers |
| **Customer Numbers table** | Your customer codes in supplier's system | For statement reconciliation |

**Top buttons on Supplier form:**

| Button | What it does |
|---|---|
| **View Ledger** | Open General Ledger for this supplier |
| **Accounting Ledger** | All invoices and payments for this supplier |
| **Fetch from GSTIN** | Auto-fill from GST portal (India) |
| **Make** → **Payment Entry** | Create a payment to this supplier |

---

# 📋 PURCHASE INVOICE
**URL:** `/desk/purchase-invoice`

*(Fully documented in Part 2 of accounting guide)*

**Make dropdown after submit:**

| Option | What it creates |
|---|---|
| **Payment** | Payment Entry to pay this bill |
| **Debit Note** | Return/correction note to supplier |
| **Purchase Order** | (rare) Retrospectively link a PO |
| **Journal Entry** | Manual accounting entry related to this bill |

---

# 📋 DEBIT NOTE
**URL:** `/desk/purchase-invoice/view/list?is_return=1`

**Layman:** You returned goods to supplier or supplier overcharged you — you're "debiting" them (reducing what you owe).

**Technical:** A Purchase Invoice with `is_return = 1`. Reverses the original purchase: Debit Creditors (reduces payable), Credit Stock/Expense + Input Tax Credit accounts.

| Key field | Detail |
|---|---|
| **Is Return (Debit Note)** ✅ | Pre-checked |
| **Return Against** | Original Purchase Invoice |
| **Quantities** | Negative |
| **Impact** | Reduces outstanding payable to supplier |

---

# 📊 ACCOUNTS PAYABLE REPORT
**URL:** `/desk/query-report/Accounts%20Payable`

**Layman:** "How much do I owe suppliers and how overdue am I?"

**Technical:** Mirror of AR report but for Purchase Invoices. Shows outstanding payable amounts aged by due date.

| Filter | What it does |
|---|---|
| **Company** | Filter by company |
| **Report Date** | As-of date |
| **Supplier** | Single supplier filter |
| **Supplier Group** | Category filter |
| **Ageing Range** | Customize 30/60/90 day buckets |
| **Based On** | Due Date or Posting Date |
| **Group by Supplier** | One row per supplier |
| **Show Remarks** | Include narration column |

---

# 💰 PAYMENT ENTRY
*(Fully documented — see Part 3 of accounting guide)*

---

# 📝 JOURNAL ENTRY
*(Fully documented — see Part 4 of accounting guide)*

---

# 📨 PAYMENT REQUEST
*(Fully documented — see Part 5 of accounting guide)*

---

# 📦 PAYMENT ORDER
**URL:** `/desk/payment-order`

**Layman:** A **batch payment instruction** — instead of paying suppliers one by one, bundle multiple payments into one instruction sent to the bank.

**Technical:** Aggregates multiple Payment Requests or Purchase Invoices into a single bank payment file (e.g., NEFT bulk file).

| Field | What it does |
|---|---|
| **Company** ⭐ | Which company is making the payments |
| **Posting Date** ⭐ | Date of the payment batch |
| **Payment Order Type** | Outward (paying suppliers) or Inward (collecting from customers) |
| **Company Bank Account** | The bank account to debit for all payments |
| **References table** | List of Payment Requests or invoices included in this batch |
| **Total Amount** | Sum of all payments in the batch |

**Buttons:**

| Button | What it does |
|---|---|
| **Get From** | Fetch pending Payment Requests or Purchase Invoices to add to this batch |
| **Submit** | Finalizes the batch; creates Payment Entries for each row |
| **Download Bank File** | Exports a file in bank-specific format (e.g., HDFC NEFT format) for bulk upload to banking portal |

---

# 🔄 PAYMENT RECONCILIATION
**URL:** `/desk/payment-reconciliation`

**Layman:** Sometimes a payment is received but not automatically matched to an invoice. This tool **manually links** payments to their invoices.

**Technical:** Matches Payment Entries / Journal Entries against open Sales or Purchase Invoices to clear outstanding amounts.

| Field | What it does |
|---|---|
| **Company** ⭐ | Which company to reconcile |
| **Party Type** ⭐ | Customer or Supplier |
| **Party** ⭐ | The specific customer or supplier |
| **Receivable / Payable Account** ⭐ | The AR or AP ledger account |
| **Default Advance Account** | If advance payments in a separate account, specify here |
| **From/To Invoice Date** | Filter invoices by date range |
| **From/To Payment Date** | Filter payments by date range |
| **Minimum / Maximum Invoice Amount** | Amount range filter for invoices |
| **Minimum / Maximum Payment Amount** | Amount range filter for payments |
| **Invoice Limit / Payment Limit** | Max number of records to fetch (0 = all) |
| **Bank / Cash Account** | Filter Journal Entry payments by account |
| **Cost Center / Project** | Additional filters |
| **Filter on Invoice** | Search for a specific invoice number |
| **Filter on Payment** | Search for a specific payment reference |
| **Invoices table** | Fetched open invoices |
| **Payments table** | Fetched unallocated payments |
| **Allocation table** | Where you link payment rows to invoice rows |

**Buttons:**

| Button | What it does |
|---|---|
| **Get Unreconciled Entries** | Fetches all open invoices and unallocated payments for this party |
| **Reconcile** | Posts the allocation — clears outstanding on selected invoices |
| **Allocate** | Auto-matches payments to invoices (oldest first) |
| **Clear Filters** | Resets all filter fields |

---

# ↩️ UNRECONCILE PAYMENT
**URL:** `/desk/unreconcile-payment`

**Layman:** You reconciled (matched) a payment to the wrong invoice — this tool **undoes that match**.

**Technical:** Removes the GL links between a Payment Entry and the invoices it was reconciled against. The payment goes back to "unallocated" status and the invoice goes back to "outstanding".

| Field | What it does |
|---|---|
| **Company** ⭐ | Company |
| **Payment / Journal Entry** | The payment document to unreconcile |
| **Allocations table** | Shows all invoices this payment is currently matched to |
| **Select rows** | Choose which allocations to remove |

**Button:**

| Button | What it does |
|---|---|
| **Unreconcile** | Removes the selected matches; restores outstanding amounts |

---

# ⚙️ PROCESS PAYMENT RECONCILIATION
**URL:** `/desk/process-payment-reconciliation`

**Layman:** Auto-reconciliation in **bulk** — instead of matching one party at a time, run it for ALL customers or suppliers at once in the background.

**Technical:** A background job that runs the reconciliation algorithm across multiple parties simultaneously.

| Field | What it does |
|---|---|
| **Company** ⭐ | Which company to process |
| **Party Type** ⭐ | Customer or Supplier |
| **Party** | Leave blank for all, or pick one |
| **Receivable / Payable Account** | The AR/AP account to reconcile |
| **From / To Date** | Date range filter |

**Buttons:**

| Button | What it does |
|---|---|
| **Submit** | Starts the background reconciliation job |
| **View Logs** | Check progress and results of the background job |

---

# 🔁 REPOST ACCOUNTING LEDGER
**URL:** `/desk/repost-accounting-ledger`

**Layman:** If you changed settings (like default accounts or tax rules) after transactions were already posted, this tool **recalculates** the GL entries for selected documents.

**Technical:** Re-runs the accounting posting logic for specified vouchers — updates GL Entry records without cancelling/re-submitting the source documents.

| Field | What it does |
|---|---|
| **Vouchers table** | Add the documents (Sales Invoice, Purchase Invoice, Payment Entry, etc.) to repost |
| **DocType column** | Which document type |
| **Voucher No column** | Specific document number |
| **Posting Date** | Date of the voucher |

**Button:**

| Button | What it does |
|---|---|
| **Submit** | Starts the repost job. GL entries are updated in the background. |

> [!WARNING]
> Use this only when instructed by your accountant. Incorrect use can create accounting discrepancies.

---

# 🔁 REPOST PAYMENT LEDGER
**URL:** `/desk/repost-payment-ledger`

**Layman:** Similar to above but specifically for the **Payment Ledger** — fixes outstanding amount calculations on invoices without changing GL entries.

**Technical:** Rebuilds Payment Ledger Entry records for selected vouchers. Fixes cases where outstanding amounts show incorrect values due to background job failures.

| Field | What it does |
|---|---|
| **Vouchers table** | Payment Entries or invoices to repost |
| **Submit** button | Triggers background repost job |

---

# 📒 GENERAL LEDGER REPORT
**URL:** `/desk/query-report/General%20Ledger`

**Layman:** The **complete raw diary of every accounting entry** ever made — every debit and every credit, in date order.

**Technical:** Queries GL Entry table — the lowest level of accounting data. Every posted transaction creates rows here.

**Filters:**

| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company's ledger |
| **From Date / To Date** ⭐ | Date range |
| **Account** | Filter to one specific account |
| **Voucher No** | Search for a specific document |
| **Party Type / Party** | Filter by customer or supplier |
| **Project** | Filter by project |
| **Cost Center** | Filter by department/branch |
| **Finance Book** | For parallel accounting books |
| **Group by** | Group entries by Voucher, Account, or Party |
| **Show Opening Entries** | Include period-opening balances |
| **Include Default Book Entries** | Include base finance book entries |
| **Dimension filters** | Any custom accounting dimensions |

**Columns:**

| Column | What it shows |
|---|---|
| Date | Posting date |
| Voucher Type | Sales Invoice / Payment Entry / Journal Entry / etc. |
| Voucher No | Document number (clickable link) |
| Account | Which ledger was affected |
| Party | Customer/Supplier if applicable |
| Debit | Amount debited |
| Credit | Amount credited |
| Balance | Running balance of the account |
| Remarks | Narration/description |

---

# ⚖️ TRIAL BALANCE REPORT
**URL:** `/desk/query-report/Trial%20Balance`

**Layman:** A **summary of all account balances** at a point in time. Debits must equal Credits — if not, something is wrong.

**Technical:** Aggregates GL Entry totals per account for a period. Verifies mathematical accuracy of the double-entry system.

**Filters:**

| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Fiscal Year** ⭐ | Which financial year |
| **From Date / To Date** | Sub-period within the year |
| **Show Zero Balance Accounts** | Include accounts with no activity |
| **Show Opening / Closing Debit/Credit** | Include period opening and closing columns |

**Columns:** Account Name | Opening Debit | Opening Credit | Debit | Credit | Closing Debit | Closing Credit

---

# 📊 FINANCIAL REPORTS
**URL:** `/desk/financial-reports`

A hub page linking to the 3 main financial statements:

### 1. Balance Sheet

**Layman:** A **snapshot** of what your company OWNS (Assets) and OWES (Liabilities + Equity) at a specific date.

**Technical:** Structured as Assets = Liabilities + Equity. Pulls from Chart of Accounts root types.

| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Date** ⭐ | Balance sheet as of this date |
| **Finance Book** | Which book (for parallel accounting) |
| **Cost Center** | Filter by department |
| **Period** | Monthly / Quarterly / Yearly columns |
| **Accumulated Values** | Show cumulative vs periodic values |

### 2. Profit and Loss Statement (P&L)

**Layman:** Did you make money or lose money? Income − Expenses = Profit/Loss.

**Technical:** Compares Income accounts vs Expense accounts for a period.

| Filter | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **From Date / To Date** ⭐ | The period |
| **Finance Book** | Parallel book |
| **Period** | Monthly / Quarterly breakdown |
| **Show Accumulated Values** | Running total vs period-only |

### 3. Cash Flow Statement

**Layman:** Where did the cash actually come from and where did it go? (Different from P&L which includes non-cash items like depreciation)

**Technical:** Classifies cash movements into Operating, Investing, and Financing activities.

---

# ⚙️ ACCOUNTS SETTINGS
**URL:** `/desk/accounts-settings`

**The master configuration panel for all accounting behavior.**

| Setting | Layman | Technical |
|---|---|---|
| **Automatically process deferred accounting** ✅ | Auto-book deferred revenue/expense each month | Background job runs monthly to recognize deferred entries |
| **Book deferred entries via Journal Entry** ✅ | Use JV instead of direct GL | Creates auditable JVs for each deferred entry |
| **Submit Journal entries automatically** ✅ | Auto-submit JVs created by system | Deferred, depreciation JVs submitted without manual action |
| **Determine Address Tax Category from** | Billing Address or Shipping Address | Which address determines IGST vs CGST+SGST |
| **Add taxes from Item Tax Template** ✅ | Auto-apply item-level tax rates | Fetches tax rates from Item master |
| **Add taxes from Taxes and Charges Template** ✅ | Auto-apply template on selection | If no taxes set and template selected, auto-fills |
| **Book tax loss on early payment discount** ✅ | Split discount into income loss and tax adjustment | For early payment discount scenarios |
| **Round tax amount row-wise** ✅ | Round each tax row separately | vs rounding the total tax only |
| **Show inclusive tax in print** ✅ | Print tax-inclusive prices | For B2C / MRP-based selling |
| **Show taxes as table in print** ✅ | Show detailed tax breakdown on printed docs | |
| **Show Payment Schedule in print** ✅ | Print installment schedule on invoice | |
| **Maintain same rate in internal transactions** ✅ | Enforce same price for inter-company sales | Prevents price manipulation between group companies |
| **Allow Stale Exchange Rates** ✅ | Use old rates if fresh rate unavailable | When OFF: blocks transaction if rate is older than Stale Days |
| **Stale Days** | How old a rate can be before it's considered stale | e.g., 7 days |
| **Auto reconcile Payments** ✅ | Run background auto-matching of payments to invoices | Uses rule-based matching algorithm |
| **Auto Reconciliation job trigger** | How often (minutes) to run the auto-reconcile job | Between 1 and 59 minutes |
| **Reconciliation queue size** | How many documents per job run | Between 5 and 100 |
| **Over Billing Allowance (%)** | How much % above order value can be invoiced | e.g., 10% = can bill 110% of ordered amount |
| **Role allowed to bypass credit limit** | Which role can override credit limit warnings | e.g., "Sales Manager" |
| **Role Allowed to over bill** | Which role can invoice above the allowance % | |
| **Prevent Sales Invoice when Customer is Overdue** ✅ | Block new invoices for overdue customers | Enforces collection before new sales |
| **Role Allowed to Bypass Over Billing** | Role that can still bill overdue customers | |
| **Book Asset Depreciation automatically** ✅ | Auto-create depreciation JVs on schedule | Background job per depreciation schedule |
| **Role to Notify on Depreciation Failure** | Who gets notified if depreciation job fails | |
| **Ignore Account closing balance** ✅ | Use raw GL entries instead of period-closing snapshots | Enable if Period Closing Vouchers are incomplete/missing |
| **General Ledger remarks length** | Truncate long remarks in GL | e.g., set to 200 characters |
| **Default Ageing Range** | Default bucket sizes for AR/AP reports | e.g., "30, 60, 90, 120" |
| **Show balances in Chart of Accounts** ✅ | Display live balances in account tree | |
| **Enable Automatic Party Matching** ✅ | Auto-match party in Bank Transactions | Uses description matching |
| **Enable Fuzzy Matching** ✅ | Approximate name matching for bank reconciliation | Handles typos/abbreviations |
| **Match transfers within N days** | Window for matching inter-account transfers | For internal fund transfers |
| **Create payment requests in Draft status** ✅ | Don't auto-submit payment request emails | Manual review before sending |
| **Allowed DocTypes table** | Which document types can be reposted via Repost Ledger | Security control |

---

---

# 📈 SHARE MANAGEMENT

## 👤 Shareholder
**Layman:** A person or company that **owns shares** in your company.

| Field | What it does |
|---|---|
| **Title** ⭐ | Full name of the shareholder |
| **Folio No** | Unique share certificate number assigned to this shareholder |
| **Company** ⭐ | Which company's shares they hold |
| **Share Balance table** | Auto-updated list of share types and quantities held |

## 🔄 Share Transfer
**Layman:** Record the **buying, selling, or gifting of shares** — from one person to another or as a new issue.

| Field | What it does |
|---|---|
| **Transfer Type** ⭐ | Purchase (new shares issued) / Transfer (between shareholders) / Return (shares returned to company) |
| **Date** ⭐ | Date of the share transaction |
| **From Shareholder** | Who is transferring shares FROM |
| **From Folio No** | Folio number of the seller/transferor |
| **To Shareholder** | Who is receiving the shares |
| **To Folio No** | Folio number of the buyer/recipient |
| **Equity/Liability Account** ⭐ | The equity account (e.g., "Share Capital") that records the value |
| **Asset Account** | The bank/asset account where share payment is received |
| **Share Type** ⭐ | Type of share (Equity, Preference, etc.) |
| **From No / To No** ⭐ | Share certificate number range being transferred |
| **No of Shares** ⭐ | Total count of shares in this transaction |
| **Rate** ⭐ | Price per share |
| **Amount** | Auto-calculated (Shares × Rate) |
| **Remarks** | Notes about the transaction |

**Buttons:**
| Button | What it does |
|---|---|
| **Submit** | Finalizes the transfer; updates Share Balance of both shareholders |
| **Cancel** | Reverses the transfer |

## 📊 Share Ledger Report
**Layman:** Full history of every share transaction — who bought, sold, or received shares and when.
Shows: Date | Transfer Type | From/To Shareholder | No. of Shares | Rate | Amount | Balance

## 📊 Share Balance Report
**Layman:** A snapshot — who currently holds how many shares of each type.
Shows: Shareholder | Share Type | No. of Shares | Rate | Amount | Folio No

---

# 🔁 SUBSCRIPTION MANAGEMENT

## 📋 Subscription Plan
**Layman:** A **pricing template** for recurring services — like a monthly SaaS plan or annual maintenance contract.

| Field | What it does |
|---|---|
| **Plan Name** ⭐ | Name of the plan (e.g., "Basic Monthly", "Enterprise Annual") |
| **Currency** ⭐ | Currency for this plan's pricing |
| **Item** ⭐ | The ERPNext Item that gets added to invoices for this plan |
| **Subscription Price Based On** ⭐ | Fixed Rate (set price) or Based on Price List (dynamic) |
| **Cost** | Fixed price per billing cycle |
| **Price List** | If price list-based, which list to use |
| **Billing Interval** ⭐ | Day / Week / Month / Year |
| **Billing Interval Count** ⭐ | How many intervals per cycle (e.g., 3 Months = quarterly) |
| **Payment Gateway** | For online payment — which gateway handles this plan |
| **Cost Center** | Which cost center to use for revenue from this plan |

## 🔄 Subscription
**Layman:** An active subscription for a specific customer — ERPNext **automatically creates invoices** on the billing schedule.

| Field | What it does |
|---|---|
| **Party Type / Party** ⭐ | Customer or Supplier being billed/paying |
| **Company** | Which company is running this subscription |
| **Status** | Active / Cancelled / Past Due / Trialling |
| **Subscription Start Date** | When billing begins |
| **Subscription End Date** | When it expires (blank = ongoing) |
| **Cancellation Date** | When it was cancelled |
| **Trial Period Start / End** | Free trial window before billing starts |
| **Follow Calendar Months** ✅ | Align billing to calendar month starts (e.g., always bill on 1st) |
| **Generate New Invoices Past Due Date** ✅ | Keep generating even if customer hasn't paid previous invoice |
| **Submit Generated Invoices** ✅ | Auto-submit invoices (no manual intervention needed) |
| **Current Invoice Start / End** | Date range of the current billing period |
| **Days Until Due** | How many days after invoice creation until payment is due |
| **Generate Invoice At** ⭐ | Beginning or End of the billing period |
| **Cancel At End Of Period** ✅ | Subscription auto-cancels when current period ends |
| **Plans table** ⭐ | Which Subscription Plans are active for this subscription |
| **Sales Taxes Template** | Tax template applied to auto-generated invoices |
| **Additional Discount %** | Recurring discount on each invoice |
| **Cost Center** | Revenue cost center |

**Buttons:**
| Button | What it does |
|---|---|
| **Cancel Subscription** | Immediately stops future invoice generation |
| **Restart Subscription** | Re-activates a cancelled subscription |
| **Fetch Subscription Updates** | Syncs with payment gateway for latest status |

## ⚙️ Subscription Settings
| Setting | What it does |
|---|---|
| **Cancel After Grace Period** ✅ | Auto-cancel if customer doesn't pay within grace period days |
| **Grace Period** | Number of days to wait for payment before cancelling |
| **Prorate per month** ✅ | If subscription starts mid-month, charge only partial amount |
| **Follow Calendar Months** ✅ | Default for all new subscriptions |

---

# 📂 OPENING AND CLOSING

## 🛠️ Opening Invoice Creation Tool
**Layman:** When you're **migrating to ERPNext** from another system, use this to bring in all unpaid invoices from the old system as opening balances.

| Field | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Invoice Type** ⭐ | Sales (customers owe you) or Purchase (you owe suppliers) |
| **Create Missing Party** ✅ | If customer/supplier doesn't exist yet, auto-create them |
| **Cost Center** | Default cost center for opening entries |
| **Project** | Default project linkage |
| **Invoices table** ⭐ | Add rows: Party Name, Outstanding Amount, Posting Date, Due Date, Item Name |

**Buttons:**
| Button | What it does |
|---|---|
| **Make Invoices** | Creates all the invoices in one click. Each row becomes one Sales/Purchase Invoice |

## 📥 Chart of Accounts Importer
**Layman:** If you have your account structure in an Excel file, **import it all at once** instead of creating accounts one by one.

| Field | What it does |
|---|---|
| **Company** | Which company's Chart of Accounts to populate |
| **Download Template** *(button)* | Downloads a pre-formatted Excel template showing the exact column structure needed |
| **Attach custom Chart of Accounts file** | Upload your completed Excel file |

**Buttons:**
| Button | What it does |
|---|---|
| **Download Template** | Get the Excel template with correct column headers |
| **Import** | Process the uploaded file and create all accounts |

## 📅 Period Closing Voucher
**Layman:** At year-end, "close the books" — transfer the year's profit/loss into the Retained Earnings account to start fresh next year.

**Technical:** Posts GL entries to zero out all Income and Expense accounts into a Closing Account (Retained Earnings / Profit & Loss). Required before generating next year's opening balances.

Key fields:
| Field | What it does |
|---|---|
| **Transaction Date** ⭐ | The closing date (last day of fiscal year, e.g., 31-Mar-2025) |
| **Fiscal Year** ⭐ | Which year is being closed |
| **Company** ⭐ | Which company |
| **Closing Account** ⭐ | The Retained Earnings / P&L account where net profit/loss is transferred |
| **Cost Center** | Cost center for the closing entries |
| **Remarks** | Notes about this closing |

---

# 🏦 BANKING

## 🏛️ Bank
**Layman:** A master record for each bank you deal with (HDFC, SBI, ICICI, etc.)

| Field | What it does |
|---|---|
| **Bank Name** ⭐ | Full name of the bank |
| **Bank Account No** | Your account number (optional at bank level) |
| **IBAN** | International bank account number |
| **SWIFT Number** | Bank's international identifier code |
| **Branch Code** | Specific branch identifier (IFSC in India) |
| **Address / Website** | Bank contact details |

## 🏦 Bank Account
**Layman:** A specific bank account belonging to your company or a party (customer/supplier).

| Field | What it does |
|---|---|
| **Account Name** ⭐ | Friendly name (e.g., "HDFC Current A/c - Operations") |
| **Company Account** | Link to the Chart of Accounts account (e.g., "HDFC Bank - KD") |
| **Bank** ⭐ | Which bank this account is at |
| **Account Type** | Current / Savings / Loan / Credit Card |
| **Account Subtype** | Further classification |
| **Is Default Account** ✅ | Use this account by default in Payment Entries |
| **Is Company Account** ✅ | Belongs to your company (vs a supplier/customer's bank account) |
| **Is Credit Card** ✅ | Mark if this is a credit card account |
| **Party Type / Party** | If this is a customer's or supplier's bank account |
| **IBAN** | International account number |
| **Branch Code** | IFSC code (India) |
| **Bank Account No** | The actual account number |
| **Statement Password** | Password for auto-importing bank statements (if encrypted PDF) |
| **Last Integration Date** | When bank data was last synced via Plaid/bank integration |

## 🧹 Bank Clearance
**Layman:** Mark which cheques or payments have **actually cleared** the bank (vs just recorded in ERPNext).

| Field | What it does |
|---|---|
| **Account** ⭐ | Which bank/cash account to clear entries for |
| **From Date / To Date** ⭐ | Date range |
| **Bank Account** | Filter by specific bank account |
| **Include Reconciled Entries** ✅ | Show already-reconciled entries too |
| **Include POS Transactions** ✅ | Include Point-of-Sale payments |
| **Payment Entries table** | Fetched entries awaiting clearance |

**Buttons:**
| Button | What it does |
|---|---|
| **Get Payment Entries** | Fetches all uncleared entries in the date range |
| **Update Clearance Date** | Sets the clearance date on selected rows — marks them as cleared |

## 🔄 Bank Reconciliation Tool
**Layman:** Compare your ERPNext records against your actual bank statement — find missing entries or discrepancies.

**Technical:** Interactive tool that loads bank statement transactions and matches them against Payment Entries / Journal Entries in ERPNext.

Key features:
| Feature | What it does |
|---|---|
| **Bank Account selector** | Pick which bank account to reconcile |
| **Date range** | Statement period |
| **Upload Bank Statement** | Import CSV/XLSX from your bank |
| **Auto Match** | Automatically matches bank rows to ERPNext transactions by amount+date |
| **Manual Match** | Drag/select to manually link a bank row to an ERPNext entry |
| **Create Journal Entry** | For bank rows with no matching ERPNext entry (bank charges, interest, etc.) |
| **Unmatched rows** | Highlighted in red — need attention |
| **Closing Balance** | Checks if bank statement balance matches ERPNext |

## 📊 Bank Reconciliation Statement Report
**Layman:** The official printable statement showing reconciliation status — which entries matched, which are pending.

Filters: Company | Account | Date | Show Cleared Entries

## 🔌 Plaid Settings
**Layman:** Connect ERPNext to your bank through **Plaid** (a banking integration service) for automatic bank statement import.

| Field | What it does |
|---|---|
| **Enabled** ✅ | Turn on Plaid integration |
| **Synchronize all accounts every hour** ✅ | Auto-sync bank transactions hourly |
| **Plaid Client ID** | Your Plaid API client ID |
| **Plaid Secret** | Your Plaid API secret key |
| **Plaid Environment** | Sandbox (testing) / Development / Production |
| **Enable European Access** ✅ | Enables Open Banking API for European banks |

---

# 💱 MULTI CURRENCY

## 🌐 Currency
**Layman:** Define all currencies your business deals in.

| Field | What it does |
|---|---|
| **Currency Name** ⭐ | e.g., "Indian Rupee", "US Dollar", "Euro" |
| **Currency Symbol** | ₹, $, €, £ |
| **Fraction** | Subdivision name (e.g., "Paise" for INR) |
| **Fraction Units** | How many fractions in 1 unit (100 paise = 1 rupee) |
| **Symbol on Right** ✅ | Show symbol after amount (e.g., "100 €") |
| **Smallest Currency Fraction Value** | Minimum denomination (e.g., 0.01 for most currencies) |
| **Number Format** | How amounts are formatted (e.g., #,##,###.## for Indian format) |
| **Enabled** ✅ | Active currency |

## 💱 Currency Exchange
**Layman:** Record today's exchange rate — "1 USD = ₹83.50 today."

| Field | What it does |
|---|---|
| **From Currency** ⭐ | Source currency (e.g., USD) |
| **To Currency** ⭐ | Target currency (e.g., INR) |
| **Exchange Rate** ⭐ | How many "To" units per 1 "From" unit |
| **Date** ⭐ | The date this rate is valid for |
| **For Buying** ✅ | Use this rate for purchase transactions |
| **For Selling** ✅ | Use this rate for sales transactions |

> ERPNext fetches fresh rates automatically from configured exchange rate providers. Manual rates here override auto-fetched rates.

## 📊 Exchange Rate Revaluation
**Layman:** At month/year end, **recalculate the value** of all foreign currency balances using current exchange rates and book the gain or loss.

| Field | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Posting Date** ⭐ | Revaluation date (usually month-end) |
| **Rounding Loss Allowance** | Small rounding differences below this threshold are ignored |
| **Get Entries** *(button)* | Fetches all foreign currency accounts with open balances |
| **Accounts table** ⭐ | List of accounts with old rate, new rate, and gain/loss |
| **Gain/Loss from Revaluation** | Net unrealized gain or loss |
| **Gain/Loss already booked** | Previously recognized amounts |
| **Total Gain/Loss** | Net final amount |

**Buttons:**
| Button | What it does |
|---|---|
| **Get Entries** | Scans all foreign currency accounts for open balances |
| **Submit** | Creates Journal Entry booking the gain/loss |

---

# 💰 COST CENTER AND BUDGETING

## 🌿 Chart of Cost Centers
*(Same as Organization module — see organization guide)*
Tree view of all cost centers. Add Child, Edit, Delete, view budget variance.

## 📋 Budget
**Layman:** Set a **spending limit** for a department/project for the year. ERPNext warns or blocks when you exceed it.

| Field | What it does |
|---|---|
| **Series** ⭐ | Naming series |
| **Budget Against** ⭐ | Cost Center or Project (which entity has this budget) |
| **Company** ⭐ | Which company |
| **Cost Center / Project** | The specific entity being budgeted |
| **Account** ⭐ | Which expense account this budget applies to |
| **From / To Fiscal Year** ⭐ | Budget period |
| **Distribution Frequency** ⭐ | Monthly / Quarterly / Half-Yearly / Yearly |
| **Budget Amount** ⭐ | Total annual budget |
| **Distribute Equally** ✅ | Split equally across months |
| **Budget Distribution table** | Manual month-by-month allocation |
| **Applicable on Material Request** ✅ | Check budget when purchase requisition is raised |
| **Action if Annual Budget Exceeded on MR** | Ignore / Warn / Stop |
| **Applicable on Purchase Order** ✅ | Check budget at PO stage |
| **Action if Annual Budget Exceeded on PO** | Ignore / Warn / Stop |
| **Applicable on booking actual expenses** ✅ | Check budget when Purchase Invoice is posted |
| **Action if Annual Budget Exceeded on Actual** | Ignore / Warn / Stop |
| **Applicable on Cumulative Expense** ✅ | Check budget against PO + MR + Actual combined |

## 📐 Accounting Dimension
**Layman:** Add **custom tracking fields** to every accounting entry — like tracking by Project, Branch, Product Line, Region — beyond just Cost Center.

| Field | What it does |
|---|---|
| **Reference Document Type** ⭐ | Which DocType is the dimension (e.g., "Project", "Branch", "Territory") |
| **Dimension Name** | Label shown on accounting forms (e.g., "Project", "Region") |
| **Dimension Defaults table** | Set default dimension values per company |

Once created, this dimension appears as a filter field on every Sales Invoice, Purchase Invoice, Journal Entry, and GL report.

## 🔀 Cost Center Allocation
**Layman:** Automatically **split** one cost center's expenses across multiple cost centers by a fixed percentage.

**Example:** Marketing department costs are split 60% to North Region and 40% to South Region.

| Field | What it does |
|---|---|
| **Main Cost Center** ⭐ | The primary cost center whose costs will be split |
| **Company** ⭐ | Which company |
| **Valid From** ⭐ | When this allocation rule takes effect |
| **Allocation Percentages table** ⭐ | Each row: Target Cost Center + Percentage (must total 100%) |

## 📊 Budget Variance Report
**Layman:** Side-by-side comparison of **budgeted vs actual spending** — are you over or under budget?

Filters: Company | Fiscal Year | Period (Monthly/Quarterly) | Budget Against (Cost Center/Project) | Show Cumulative

Columns: Account | Budget | Actual | Variance | % Used

## 📅 Monthly Distribution
**Layman:** Define **how a yearly budget is spread** across months — not always equally (e.g., more spending in festive season).

| Field | What it does |
|---|---|
| **Distribution Name** ⭐ | Label (e.g., "Seasonal Pattern 2025") |
| **Fiscal Year** | Which year |
| **Monthly Percentages table** | 12 rows (Jan–Dec), each with a % (must total 100%) |

---

# 🧾 TAX MASTERS

## 📋 Sales Taxes and Charges Template
**Layman:** Pre-built tax rules for selling — "always apply 18% GST on this type of sale."

| Field | What it does |
|---|---|
| **Template Title** ⭐ | Name (e.g., "GST 18% - Interstate", "GST 5% - Textile") |
| **Company** | Which company |
| **Is Default** ✅ | Auto-apply to all new Sales Invoices |
| **Tax Table rows** | Each row = one tax component |
| ↳ **Type** | % of Net Total / Fixed / % of Previous Row / % of Net+Prev / % of Item |
| ↳ **Account Head** | Tax ledger (e.g., IGST Payable, CGST Payable) |
| ↳ **Rate %** | e.g., 18, 9, 5 |
| ↳ **Amount** | Auto-calculated |
| ↳ **Include in Print Rate** ✅ | Show tax-inclusive price on printout |
| ↳ **Is this Tax included in Basic Rate** ✅ | For inclusive-tax items |
| **➕ Add Row** | Add another tax component |

## 📋 Purchase Taxes and Charges Template
Same structure as Sales Tax template but for Purchase Orders and Bills.
Used to claim GST Input Credit (CGST Input, SGST Input, IGST Input accounts).

## 🏷️ Item Tax Template
**Layman:** Override tax rates for **specific products** — e.g., some fabrics have 5% GST while others have 12%.

| Field | What it does |
|---|---|
| **Title** ⭐ | Template name (e.g., "Cotton Fabric - 5% GST") |
| **Company** ⭐ | Which company |
| **Disabled** ✅ | Deactivate without deleting |
| **Tax Rates table** ⭐ | Each row: Tax Type + Rate % |

When this template is set on an Item, it overrides the standard Sales/Purchase Tax Template rate for that specific item.

## 🏷️ Tax Category
**Layman:** A label that determines **which tax template applies** — e.g., "Interstate" triggers IGST template, "Intrastate" triggers CGST+SGST template.

| Field | What it does |
|---|---|
| **Title** ⭐ | Category name (e.g., "Intrastate", "Interstate", "Export") |
| **Disabled** ✅ | Deactivate |

Tax Category is set on Customer/Supplier. ERPNext uses it to auto-select the correct tax template on invoices.

## 📏 Tax Rule
**Layman:** Advanced **auto-selection rules** — "If customer is in Maharashtra AND item is Textile → apply 5% SGST template."

| Field | What it does |
|---|---|
| **Tax Type** | Sales or Purchase |
| **Sales Tax Template** | Which template to apply for sales |
| **Purchase Tax Template** | Which template to apply for purchases |
| **Customer / Supplier** | Apply only for this specific party |
| **Item** | Apply only for this specific item |
| **Billing City/State/Country** | Geographic condition |
| **Shipping City/State/Country** | Shipping address condition |
| **Tax Category** | Apply when this category is selected |
| **Customer Group / Supplier Group** | Apply for entire group |
| **Item Group** | Apply for entire item category |
| **From Date / To Date** | Date-limited rule |
| **Priority** | If multiple rules match, higher priority wins |
| **Use for Shopping Cart** ✅ | Apply in the e-commerce checkout |

## 🏛️ Tax Withholding Category (TDS/TCS)
**Layman:** Defines the **TDS (Tax Deducted at Source)** rules — what percentage of a payment must be withheld and deposited with the government.

| Field | What it does |
|---|---|
| **Category Name** | e.g., "194C - Contractors", "194Q - Purchase of Goods" |
| **Deduct Tax On Basis** ⭐ | Payment / Invoice / Whichever is Earlier |
| **Round Off Tax Amount** ✅ | Round TDS to nearest integer |
| **Only Deduct Tax On Excess Amount** ✅ | Apply TDS only on amount exceeding threshold |
| **Disable Cumulative Threshold** ✅ | Apply per-transaction rate only |
| **Disable Transaction Threshold** ✅ | Apply cumulative threshold only |
| **Rates table** ⭐ | Each row: From Date, To Date, Tax Rate %, Threshold (cumulative), Single Transaction Threshold |
| **Accounts table** ⭐ | Per-company TDS liability account |

## 📄 Lower Deduction Certificate
**Layman:** Some suppliers have a government certificate allowing **reduced TDS rates**. Record the certificate here so ERPNext applies the correct lower rate.

| Field | What it does |
|---|---|
| **Tax Withholding Category** ⭐ | Which TDS section this applies to |
| **Fiscal Year** ⭐ | Valid for which year |
| **Company** ⭐ | Which company |
| **Certificate No** ⭐ | Government-issued certificate number |
| **Supplier** ⭐ | Which supplier has this certificate |
| **PAN No** ⭐ | Supplier's PAN |
| **Valid From / Valid Up To** ⭐ | Certificate validity period |
| **Rate of TDS As Per Certificate** ⭐ | Reduced TDS rate (e.g., 1% instead of 2%) |
| **Certificate Limit** ⭐ | Maximum payment amount covered by this certificate |

---

# 📝 PAYMENT MASTERS (Additional)

## 📋 Journal Entry Template
**Layman:** Save a **frequently used journal entry** as a template so you can recreate it in one click next time (e.g., monthly rent, depreciation, salary accrual).

| Field | What it does |
|---|---|
| **Template Title** ⭐ | Name of the template (e.g., "Monthly Office Rent") |
| **Journal Entry Type** ⭐ | The type to pre-select (Bank / Cash / Journal / etc.) |
| **Series** ⭐ | Naming series for journals created from this template |
| **Company** ⭐ | Which company |
| **Is Opening** | Mark as opening balance entry |
| **Multi Currency** ✅ | Template involves foreign currencies |
| **Accounting Entries table** | Pre-filled debit/credit rows with accounts and amounts |

**Usage:** In Journal Entry form → "From Template" field → select this template → all rows auto-fill.

## 📄 Terms and Conditions
**Layman:** Standard legal text that appears at the bottom of your sales and purchase documents.

| Field | What it does |
|---|---|
| **Title** ⭐ | Name (e.g., "Standard Sales Terms", "Export Terms") |
| **Disabled** ✅ | Hide from selection dropdowns |
| **Copy Attachments to Transaction** ✅ | Any files attached here are also attached to the transaction |
| **Selling** ✅ | Available on Sales Invoices/Orders |
| **Buying** ✅ | Available on Purchase Orders/Bills |
| **Terms and Conditions** | The actual legal text (rich text editor) |

---

# 🏛️ ACCOUNTING MASTERS (Additional)

## 📖 Finance Book
**Layman:** Maintain **two sets of books** simultaneously — e.g., one for local tax compliance (Companies Act) and one for IFRS/US GAAP reporting.

| Field | What it does |
|---|---|
| **Finance Book Name** | Label (e.g., "IFRS Books", "Tax Books", "Management Accounts") |

All GL entries can be tagged to a Finance Book. Reports can filter by Finance Book to show either set of books.

## 📅 Accounting Period
**Layman:** Lock down specific **document types** for a time period — e.g., "Sales Invoices cannot be created for January 2025 anymore (it's been closed)."

**Technical:** More granular than Fiscal Year freeze — you can selectively lock only certain DocTypes.

| Field | What it does |
|---|---|
| **Period Name** ⭐ | e.g., "Q1 2025 Closed" |
| **Start Date / End Date** ⭐ | The period to lock |
| **Company** ⭐ | Which company |
| **Disabled** ✅ | Temporarily disable this period lock |
| **Exempted Role** | Role allowed to bypass this period restriction |
| **Closed Documents table** ⭐ | List of DocTypes blocked in this period (e.g., Sales Invoice, Purchase Invoice, Journal Entry) |

## ⏱️ Payment Term
**Layman:** Define a single installment rule — "50% due in 30 days, 50% due in 60 days." Multiple terms combine into a Payment Terms Template.

| Field | What it does |
|---|---|
| **Payment Term Name** | e.g., "30 Days Net", "50% Advance" |
| **Invoice Portion (%)** | What % of the invoice this term covers |
| **Mode of Payment** | How this portion should be paid |
| **Due Date Based On** | Net Days / End of Month / End of next month / Day(s) after invoice date |
| **Credit Days** | Number of days until due |
| **Credit Months** | Number of months until due |
| **Discount Type** | Percentage / Amount |
| **Discount** | Early payment discount offered |
| **Discount Validity Based On** | Days after invoice or due date |
| **Discount Validity** | How many days the discount is valid |
| **Description** | Explanation of this term |

**Payment Terms Template** = a collection of multiple Payment Terms (e.g., "30% on delivery + 70% in 30 days" = 2 Payment Term rows).

---

## 🗺️ COMPLETE SIDEBAR MAP (ALL SECTIONS)

```
Accounting Module
│
├── 🏠 Home (Invoicing Dashboard)
├── 📊 Dashboard (Accounts Charts)
├── 🌿 Chart of Accounts
│
├── RECEIVABLES
│   ├── 👤 Customer
│   ├── 🧾 Sales Invoice
│   ├── 📋 Credit Note
│   └── 📈 Accounts Receivable Report
│
├── PAYABLES
│   ├── 🏭 Supplier
│   ├── 🧾 Purchase Invoice
│   ├── 📋 Debit Note
│   └── 📊 Accounts Payable Report
│
├── PAYMENTS
│   ├── 💰 Payment Entry
│   ├── 📝 Journal Entry
│   ├── 📨 Payment Request
│   ├── 📦 Payment Order
│   ├── 🔄 Payment Reconciliation
│   ├── ↩️ Unreconcile Payment
│   ├── ⚙️ Process Payment Reconciliation
│   ├── 🔁 Repost Accounting Ledger
│   └── 🔁 Repost Payment Ledger
│
├── REPORTS
│   ├── 📒 General Ledger
│   ├── ⚖️ Trial Balance
│   └── 📊 Financial Reports (Balance Sheet / P&L / Cash Flow)
│
├── 📈 SHARE MANAGEMENT
│   ├── 👤 Shareholder
│   ├── 🔄 Share Transfer
│   ├── 📊 Share Ledger (Report)
│   └── 📊 Share Balance (Report)
│
├── 🔁 SUBSCRIPTION MANAGEMENT
│   ├── 📋 Subscription Plan
│   ├── 🔄 Subscription
│   └── ⚙️ Subscription Settings
│
├── 📂 OPENING AND CLOSING
│   ├── 🛠️ Opening Invoice Creation Tool
│   ├── 📥 Chart of Accounts Importer
│   └── 📅 Period Closing Voucher
│
├── 🏦 BANKING
│   ├── 🏛️ Bank
│   ├── 🏦 Bank Account
│   ├── 🧹 Bank Clearance
│   ├── 🔄 Bank Reconciliation Tool
│   ├── 📊 Bank Reconciliation Statement (Report)
│   └── 🔌 Plaid Settings
│
├── 💱 MULTI CURRENCY
│   ├── 🌐 Currency
│   ├── 💱 Currency Exchange
│   └── 📊 Exchange Rate Revaluation
│
├── 💰 COST CENTER AND BUDGETING
│   ├── 🌿 Chart of Cost Centers
│   ├── 📋 Budget
│   ├── 📐 Accounting Dimension
│   ├── 🔀 Cost Center Allocation
│   ├── 📊 Budget Variance Report
│   └── 📅 Monthly Distribution
│
├── 🧾 TAX MASTERS
│   ├── 📋 Sales Taxes and Charges Template
│   ├── 📋 Purchase Taxes and Charges Template
│   ├── 🏷️ Item Tax Template
│   ├── 🏷️ Tax Category
│   ├── 📏 Tax Rule
│   ├── 🏛️ Tax Withholding Category
│   └── 📄 Lower Deduction Certificate
│
├── 📝 PAYMENT EXTRAS
│   ├── 📋 Journal Entry Template
│   ├── 📄 Terms and Conditions
│   └── 💳 Mode of Payment
│
└── 🏛️ ACCOUNTING MASTERS
    ├── 🏢 Company
    ├── 🌿 Chart of Accounts
    ├── ⚙️ Accounts Settings
    ├── 📅 Fiscal Year
    ├── 📐 Accounting Dimension
    ├── 📖 Finance Book
    ├── 📅 Accounting Period
    └── ⏱️ Payment Term
```

---

> [!IMPORTANT]
> **Tax Masters** (Tax Rule + Tax Withholding Category) are critical for GST compliance in India. Set these up correctly before processing any invoices.

> [!TIP]
> Use **Subscription Management** for any recurring billing — annual maintenance, SaaS, AMC contracts. ERPNext will auto-generate and submit invoices on schedule without manual effort.

> [!WARNING]
> **Period Closing Voucher** should be run only ONCE per fiscal year, after all entries are verified. Running it incorrectly can lock your books for that year and require an admin to reverse.

> [!NOTE]
> **Finance Book** is for companies that maintain parallel accounting (e.g., one set for Indian Companies Act, another for IFRS). Most companies don't need this unless they have international reporting requirements.


```
Accounting Module
│
├── 🏠 Home (Invoicing Dashboard)
├── 📊 Dashboard (Accounts Charts)
├── 🌿 Chart of Accounts (Account Tree)
│
├── RECEIVABLES
│   ├── 👤 Customer (Party Master)
│   ├── 🧾 Sales Invoice (Bill to Customer)
│   ├── 📋 Credit Note (Customer Refund)
│   └── 📈 Accounts Receivable Report (Ageing)
│
├── PAYABLES
│   ├── 🏭 Supplier (Party Master)
│   ├── 🧾 Purchase Invoice (Bill from Supplier)
│   ├── 📋 Debit Note (Supplier Return)
│   └── 📊 Accounts Payable Report (Ageing)
│
├── PAYMENTS
│   ├── 💰 Payment Entry (Record Payment)
│   ├── 📝 Journal Entry (Manual Accounting)
│   ├── 📨 Payment Request (Online Payment Link)
│   ├── 📦 Payment Order (Batch Payments)
│   ├── 🔄 Payment Reconciliation (Match Payments to Invoices)
│   ├── ↩️ Unreconcile Payment (Undo a Match)
│   ├── ⚙️ Process Payment Reconciliation (Bulk Auto-Match)
│   ├── 🔁 Repost Accounting Ledger (Fix GL Entries)
│   └── 🔁 Repost Payment Ledger (Fix Outstanding Amounts)
│
├── REPORTS
│   ├── 📒 General Ledger (Every GL Entry)
│   ├── ⚖️ Trial Balance (All Account Balances)
│   └── 📊 Financial Reports
│       ├── Balance Sheet (Assets vs Liabilities)
│       ├── Profit & Loss (Income vs Expense)
│       └── Cash Flow Statement
│
└── ⚙️ Settings (Accounts Settings)
```

---

> [!IMPORTANT]
> **Payment Reconciliation** is one of the most-used tools in daily accounting. If a customer payment doesn't automatically clear an invoice, use this tool to manually match them.

> [!TIP]
> Set up **Accounts Settings → Auto Reconcile Payments = ON** and **Auto Reconciliation Trigger = 15 minutes** for a nearly hands-free payment matching system.

> [!WARNING]
> **Repost Accounting Ledger** and **Repost Payment Ledger** are advanced tools. Only use them when your accountant tells you an entry needs correction. Wrong use can corrupt financial reports.
