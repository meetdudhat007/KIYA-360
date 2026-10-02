# 💸 ERPNext — Payments (Accounting) Deep Dive
> Every field, every button, every graph — scraped live and explained in layman + technical terms.

---

# 📊 SECTION 1 — ACCOUNTS DASHBOARD GRAPHS

**URL:** `/desk/dashboard-view/Accounts`

The Accounts Dashboard is the **first thing you see** in accounting. It shows your financial health at a glance without opening any report. Think of it like the **instrument panel in a car** — it tells you speed, fuel, and warnings all in one view.

---

## 🔢 NUMBER CARDS (Top row — 4 big numbers)

These are the **headline figures** — big colored boxes showing total amounts.

### 💳 Card 1: Total Outgoing Bills
| What it shows | The **total sales invoice value** (how much you've billed to customers) |
|---|---|
| **Layman** | "We have raised ₹50 Lakh worth of bills to customers" |
| **Source** | Sales Invoice → `base_net_total` field |
| **Filter** | Only submitted (finalized) invoices |
| **Formula** | `SUM(Sales Invoice.base_net_total) WHERE docstatus = 1` |
| **Updates** | Real-time — refreshes every time you open the dashboard |

### 💳 Card 2: Total Incoming Bills
| What it shows | The **total purchase invoice value** (bills received from suppliers) |
|---|---|
| **Layman** | "Our suppliers have billed us ₹30 Lakh total" |
| **Source** | Purchase Invoice → `base_net_total` field |
| **Filter** | Only submitted purchase invoices |
| **Formula** | `SUM(Purchase Invoice.base_net_total) WHERE docstatus = 1` |

### 💳 Card 3: Total Incoming Payment
| What it shows | **Total cash/bank received** from customers |
|---|---|
| **Layman** | "Customers have actually paid us ₹40 Lakh (cash in bank)" |
| **Source** | Payment Entry → `base_received_amount` field |
| **Filter** | Submitted Payment Entries WHERE `payment_type = "Receive"` |
| **Formula** | `SUM(Payment Entry.base_received_amount) WHERE payment_type='Receive' AND docstatus=1` |
| **Key Insight** | This ≠ Total Outgoing Bills. The difference = Outstanding Receivable |

### 💳 Card 4: Total Outgoing Payment
| What it shows | **Total cash/bank paid out** to suppliers |
|---|---|
| **Layman** | "We have actually paid suppliers ₹25 Lakh so far" |
| **Source** | Payment Entry → `base_paid_amount` field |
| **Filter** | Submitted Payment Entries WHERE `payment_type = "Pay"` |
| **Formula** | `SUM(Payment Entry.base_paid_amount) WHERE payment_type='Pay' AND docstatus=1` |

> **How to read the 4 cards together:**
> - If Card 1 (Sales Billed) >> Card 3 (Received) → you have a lot of **unpaid customer dues**
> - If Card 2 (Purchase Billed) >> Card 4 (Paid out) → you owe suppliers money but haven't paid yet

---

## 📈 CHART 1: Outgoing Bills (Sales Invoice)
*(Green Bar Chart — top left)*

| Property | Value |
|---|---|
| **Chart Type** | Bar Chart |
| **Color** | Green `#7b933d` |
| **X-axis (Horizontal)** | Months (Jan, Feb, Mar...) |
| **Y-axis (Vertical)** | Total Sales Invoice amount in ₹ |
| **Time Period** | Last 12 months |
| **Data Source** | Sales Invoice → `base_net_total` |
| **Grouped by** | `posting_date` → Monthly buckets |
| **Filter** | Only submitted invoices (`docstatus = 1`) |

**Layman Explanation:**
> Imagine a bar chart where each bar = one month. The taller the bar, the more sales you invoiced that month. A growing bar height month-over-month = good! A sudden dip = fewer sales or invoices delayed.

**How it's generated:**
1. ERPNext fetches all submitted Sales Invoices from the past 12 months
2. Groups them by `posting_date` into monthly buckets
3. Sums the `base_net_total` (amount in company currency) per month
4. Draws one bar per month, height = that month's sum

**What to look for:**
- 📈 Rising bars = revenue growing
- 📉 Falling bars = sales declining — investigate
- 🔴 Sudden spike = large one-time sale or delayed bulk invoicing
- Seasonal pattern = normal for businesses with peak seasons

---

## 📉 CHART 2: Incoming Bills (Purchase Invoice)
*(Red/Brown Bar Chart — top right)*

| Property | Value |
|---|---|
| **Chart Type** | Bar Chart |
| **Color** | Red `#a83333` |
| **X-axis** | Months |
| **Y-axis** | Total Purchase Invoice amount in ₹ |
| **Time Period** | Last 12 months |
| **Data Source** | Purchase Invoice → `base_net_total` |
| **Filter** | Submitted invoices only |

**Layman Explanation:**
> Each bar = how much you were billed by suppliers that month. Compare this to the green Sales chart — if the red bars are close to the green bars, your margins are thin (you're spending almost as much as you earn).

**How it's generated:**
Same logic as Sales chart but queries Purchase Invoice table instead.

**What to look for:**
- Red bars consistently lower than green bars = healthy gross margin
- Red bars exceeding green bars in any month = you spent more than you earned → loss
- Sudden red spike = bulk purchase or unexpected large bill

---

## 🍩 CHART 3: Accounts Receivable Ageing
*(Donut Chart — middle left)*

| Property | Value |
|---|---|
| **Chart Type** | Donut (pie) Chart |
| **Data Source** | Accounts Receivable Report (live calculation) |
| **Ageing Buckets** | 0–30 days / 31–60 days / 61–90 days / 91–120 days / 120+ days |
| **Based On** | Due Date |

**Layman Explanation:**
> The donut is divided into colored slices. Each slice = a group of unpaid customer invoices based on how old they are.
>
> - 🟢 Small slice on the left = new invoices (not yet due) — normal
> - 🟡 Growing slices in 30–60 range = some customers are slow to pay
> - 🔴 Large slice on the right (60+, 90+) = serious problem — old unpaid dues!

**Slices of the donut:**
| Slice | What it means |
|---|---|
| **0–30 days** | Fresh invoices — within payment terms, no concern |
| **31–60 days** | Slightly overdue — send a reminder |
| **61–90 days** | Significantly overdue — follow up urgently |
| **91–120 days** | Very overdue — consider credit hold |
| **120+ days** | Potentially bad debt — may need write-off |

**How it's generated:**
1. Runs the Accounts Receivable report in the background
2. For each unpaid invoice, calculates: `Today's Date − Invoice Due Date = Age in days`
3. Puts each invoice's outstanding amount into the correct age bucket
4. Adds all amounts per bucket
5. Draws each bucket as a slice of the donut, proportional to its amount

**What to look for:**
- Donut dominated by 0–30 slice = excellent collections
- Donut shifting right (60–90+ growing) = collections getting worse
- Click any slice → drill down to see exactly which customers/invoices are in that bucket

---

## 🍩 CHART 4: Accounts Payable Ageing
*(Donut Chart — middle right)*

| Property | Value |
|---|---|
| **Chart Type** | Donut Chart |
| **Data Source** | Accounts Payable Report |
| **Buckets** | 0–30 / 31–60 / 61–90 / 91–120 / 120+ days |
| **Based On** | Due Date |

**Layman Explanation:**
> Mirror of AR Ageing but for your own unpaid supplier bills.
>
> - 🟢 All in 0–30 = you're paying suppliers on time
> - 🔴 Large 60–90+ slices = you're delaying payments to suppliers — relationship risk and potential penalties

**What to look for:**
- Match this against your bank balance — if you have cash but large 60+ AP slices, you're sitting on supplier money unnecessarily
- Suppliers in 120+ may stop supplying or charge late payment interest

---

## 📊 CHART 5: Budget Variance
*(Full-width Bar Chart — bottom)*

| Property | Value |
|---|---|
| **Chart Type** | Bar Chart (grouped) |
| **Data Source** | Budget Variance Report |
| **Period** | Monthly |
| **Budget Against** | Cost Center |
| **Shows** | Budgeted vs Actual spending side by side |

**Layman Explanation:**
> Two bars per month — one bar = what you PLANNED to spend, another bar = what you ACTUALLY spent.
>
> - Bars equal height = spending exactly as planned
> - Actual bar taller than Budget bar = you overspent ⚠️
> - Actual bar shorter = you underspent (good for cost savings, but could mean delayed purchases)

**How it's generated:**
1. Fetches all Budget records for the current fiscal year
2. Fetches actual GL expenses for each cost center per month
3. Compares: Budget Amount vs Actual GL Amount
4. Shows side-by-side bars per month per cost center

**What to look for:**
- Red/overflowing bars = departments exceeding budget → management action needed
- Consistent underspend in Q1 + overspend in Q3/Q4 = poor budget distribution

---

## 📈 CHART 6: Bank Balance
*(Full-width Line Chart — very bottom)*

| Property | Value |
|---|---|
| **Chart Type** | Line Chart |
| **Data Source** | Custom — queries Bank Account GL balances |
| **Time Period** | Last 12 months |
| **Interval** | Monthly |

**Layman Explanation:**
> A line that goes up and down showing your **total cash in all bank accounts** over the past 12 months.
>
> - Line going up = cash accumulating (good)
> - Line going down = cash being spent faster than received (bad — watch for cash flow crisis)
> - Sharp drops = large payments went out (loans, bulk purchases, salaries)
> - Sharp rises = large receipts (customer collections, loans received)

**How it's generated:**
1. Looks at all accounts with type = "Bank"
2. Reads the running GL balance at end of each month
3. Sums all bank account balances together
4. Plots one point per month and connects them into a line

**What to look for:**
- Is the line staying above zero at all times? (negative = overdraft)
- Is there enough cash for next month's expected payables?
- Seasonal patterns match your business cycle?

---

# 💳 SECTION 2 — PAYMENT ENTRY (Deep Dive)
**URL:** `/desk/payment-entry`

**Layman:** This is where you **record that money actually moved** — cash received from a customer, or cash paid to a supplier. Every real bank/cash transaction must have a Payment Entry.

**Technical:** Creates GL entries debiting/crediting Bank/Cash accounts and clearing outstanding invoices from the Receivable/Payable ledger.

---

## 📋 ALL FIELDS — SECTION BY SECTION

### 🔷 Section 1: Type of Payment

| Field | Layman | Technical |
|---|---|---|
| **Series** ⭐ | Auto-number format (e.g., ACC-PAY-2025-0001) | Naming series for document numbering |
| **Payment Type** ⭐ | **Receive** (from customer) / **Pay** (to supplier) / **Internal Transfer** (bank to bank) | Determines GL direction: Receive = Dr Bank, Cr AR; Pay = Dr AP, Cr Bank |
| **Posting Date** ⭐ | The actual date the payment happened | GL entries are posted on this date |
| **Company** ⭐ | Which company is receiving/making the payment | Determines default accounts |
| **Mode of Payment** | How money moved — Cash / Cheque / NEFT / UPI / Credit Card | Sets default accounts; used in Sales Payment Summary report |

---

### 🔷 Section 2: Payment From / To (Party)

| Field | Layman | Technical |
|---|---|---|
| **Party Type** | Customer / Supplier / Employee / Shareholder | Which master type is involved |
| **Party** | The specific customer or supplier name | Links to Customer/Supplier master |
| **Party Name** | Auto-filled full name | Read-only from party master |
| **Book Advance in Separate Party Account** ✅ | Put this payment in a special "Advance Received" account instead of the main AR account | Used when payment received before invoice exists |
| **Consider for Tax Withholding (TDS)** ✅ | Should TDS be deducted from this payment? | Triggers TDS calculation on the payment amount |
| **Tax Withholding Category** | Which TDS section applies | e.g., 194C, 194Q — determines TDS rate |
| **Company Bank Account** | Your bank account (HDFC, SBI, etc.) | The company's bank where money goes in/out |
| **Party Bank Account** | Customer's or supplier's bank details | For NEFT/RTGS payments to supplier |
| **Contact** | Person at the party to be emailed | For automated payment advice emails |
| **Email** | Contact's email address | Auto-filled from Contact record |

---

### 🔷 Section 3: Accounts (GL Accounts)

| Field | Layman | Technical |
|---|---|---|
| **Account Paid From** ⭐ | Where money leaves (bank account or AR ledger) | For Receive: AR account. For Pay: Bank account |
| **Account Currency (From)** ⭐ | Currency of the source account | e.g., INR, USD |
| **Account Paid To** ⭐ | Where money arrives | For Receive: Bank account. For Pay: AP account |
| **Account Currency (To)** ⭐ | Currency of the destination account | Used for cross-currency payments |

**How accounts work by Payment Type:**
```
RECEIVE (Customer pays you):
  Paid From = Accounts Receivable (AR)   [customer owes you]
  Paid To   = Bank Account               [money arrives in bank]
  GL: DR Bank / CR Accounts Receivable

PAY (You pay supplier):
  Paid From = Bank Account               [money leaves bank]
  Paid To   = Accounts Payable (AP)      [reduces what you owe]
  GL: DR Accounts Payable / CR Bank

INTERNAL TRANSFER (Bank to Bank):
  Paid From = Bank Account A             [e.g., HDFC]
  Paid To   = Bank Account B             [e.g., SBI]
  GL: DR Bank B / CR Bank A
```

---

### 🔷 Section 4: Amount

| Field | Layman | Technical |
|---|---|---|
| **Paid Amount** ⭐ | How much the customer paid / you paid | In the payment's currency |
| **Source Exchange Rate** ⭐ | Rate to convert "From" currency to company currency | Only relevant for foreign currency payments |
| **Paid Amount (Company Currency)** ⭐ | Same amount converted to your base currency (INR) | `Paid Amount × Source Exchange Rate` |
| **Received Amount** ⭐ | Amount received in "To" account | May differ from Paid Amount if cross-currency |
| **Target Exchange Rate** ⭐ | Rate to convert "To" currency to company currency | For cross-currency payments |
| **Received Amount (Company Currency)** ⭐ | Converted received amount | `Received Amount × Target Exchange Rate` |

> **Simple example:** Customer pays $1,000. Rate = 83. Paid Amount = $1000. Received in INR bank = ₹83,000.

---

### 🔷 Section 5: Reference (Invoice Matching) — THE MOST IMPORTANT SECTION

| Field / Button | Layman | Technical |
|---|---|---|
| **🔘 Get Outstanding Invoices** | "Show me all unpaid invoices for this customer/supplier so I can match this payment to them" | Fetches all open Sales/Purchase Invoices with outstanding amount > 0 for the selected party |
| **🔘 Get Outstanding Orders** | Fetch advance-payment-linked orders | For payments against Sales/Purchase Orders (advance payments) |
| **Payment References table** | The list of invoices this payment is being applied to | Each row = one invoice being cleared |

**Payment References Table — each row contains:**

| Column | Layman | Technical |
|---|---|---|
| **Reference Type** | Is this against an Invoice, Order, or Journal Entry? | Sales Invoice / Purchase Invoice / Journal Entry / Sales Order / Purchase Order |
| **Reference Name** | The specific document number (e.g., ACC-SINV-2025-0042) | Document ID |
| **Due Date** | When was payment due for this invoice | From invoice |
| **Invoice Amount** | Total invoice value | Grand Total of the invoice |
| **Outstanding Amount** | How much is still unpaid on this invoice | Grand Total − Already Paid |
| **Allocated Amount** | How much of THIS payment goes to this invoice | You enter this — can be partial |

**Example:**
```
Customer Ravi pays ₹50,000. He has 3 open invoices:
  Invoice #1 = ₹20,000 outstanding → Allocate ₹20,000 → CLOSED ✅
  Invoice #2 = ₹30,000 outstanding → Allocate ₹30,000 → CLOSED ✅
  Invoice #3 = ₹15,000 outstanding → Not allocated (no money left)
Total Allocated = ₹50,000 ✅
```

---

### 🔷 Section 6: Writeoff

| Field | Layman | Technical |
|---|---|---|
| **Total Allocated Amount** | Sum of all amounts you've allocated to invoices | Auto-calculated from References table |
| **Total Allocated (Company Currency)** | Same in base currency | For multi-currency |
| **Unallocated Amount** | Money received but NOT matched to any invoice | `Paid Amount − Total Allocated` |
| **Difference Amount** | Rounding or exchange rate difference | `Paid Amount (base) − Received Amount (base)` |
| **🔘 Write Off Difference Amount** | Book the tiny rounding difference as a write-off expense | Posts a small GL entry to a Write-off expense account |

> **Layman:** If customer pays ₹49,998 but invoice is ₹50,000 — the ₹2 difference can be written off instead of leaving the invoice partially open.

---

### 🔷 Section 7: Taxes and Charges

| Field | Layman | Technical |
|---|---|---|
| **Purchase Taxes Template** | Apply purchase tax rules to this advance payment | For advance payments that carry TDS or GST |
| **Sales Taxes Template** | Apply sales tax rules | For advance receipts |
| **Advance Taxes and Charges table** | The actual tax rows | Each row: Tax type, Account, Rate, Amount |
| **Total Taxes (Company Currency)** | Sum of all taxes in base currency | Auto-calculated |
| **Total Taxes** | Sum in payment currency | Auto-calculated |

---

### 🔷 Section 8: Deductions or Loss

| Field | Layman | Technical |
|---|---|---|
| **Payment Deductions or Loss table** | If customer paid less than invoice (e.g., took a discount), record the write-off here | Each row: Account + Cost Center + Amount to debit/credit |

**Use case:** Customer was given 2% early payment discount. Invoice = ₹1,00,000. Customer paid ₹98,000. Deduction = ₹2,000 → booked to "Discount Allowed" expense account.

---

### 🔷 Section 9: Tax Withholding (TDS)

| Field | Layman | Technical |
|---|---|---|
| **Tax Withholding Group** | Which TDS group applies | Filters rates within withholding category |
| **Ignore TDS Threshold** ✅ | Apply TDS even if payment is below the threshold limit | Override the cumulative limit check |
| **Edit Tax Withholding Entries** ✅ | Manually modify TDS amounts | For special cases |
| **Tax Withholding Entries table** | The actual TDS rows — Amount, Account, Rate | Auto-calculated based on category rates |

---

### 🔷 Section 10: Transaction ID (Bank Reference)

| Field | Layman | Technical |
|---|---|---|
| **Cheque/Reference No** | The bank transaction reference (UTR, NEFT ref, Cheque no.) | Used in Bank Reconciliation matching |
| **Cheque/Reference Date** | Date on the cheque or bank transaction | |
| **Clearance Date** | Date the cheque actually cleared | Set during Bank Clearance process |
| **Project** | Link this payment to a project | For project-wise accounting |
| **Cost Center** | Which department this payment belongs to | For departmental accounting |

---

### 🔷 Section 11: More Information

| Field | Layman | Technical |
|---|---|---|
| **Status** | Draft / Submitted / Cancelled / Reconciled | Auto-managed by system |
| **Custom Remarks** ✅ | Write your own narration | Overrides auto-generated remarks |
| **Remarks** | Description of the payment | Appears in General Ledger as narration |
| **In Words (Company Currency)** | Amount spelled out (e.g., "Fifty Thousand Rupees Only") | For cheque printing |
| **Is Opening** | Is this an opening balance entry? | For migration; won't affect P&L |
| **Letter Head** | Company letterhead for print | For formal payment receipts |
| **Print Heading** | Title on the printed document | e.g., "Receipt Voucher" |
| **Bank / Bank Account No** | Read-only — auto-filled from Party Bank Account | Shown for reference |
| **Payment Order** | If created via Payment Order batch | Link to parent Payment Order |
| **In Words** | Amount spelled in payment currency | For foreign currency payments |
| **Auto Repeat** | Link to recurring payment schedule | For monthly rent/EMI payments |

---

## 🔘 ALL BUTTONS ON PAYMENT ENTRY FORM

| Button | When it appears | What it does |
|---|---|---|
| **Save** | Always | Saves as Draft (no GL impact yet) |
| **Submit** | After Save | Finalizes — posts GL entries. Cannot be edited after this. |
| **Cancel** | After Submit | Reverses all GL entries. Creates an amendment. |
| **Amend** | After Cancel | Creates a new editable copy to fix the cancelled one |
| **Get Outstanding Invoices** | Payment From/To section | Fetches all open invoices for this party to allocate |
| **Get Outstanding Orders** | Payment From/To section | Fetches open orders for advance payment |
| **Write Off Difference Amount** | Writeoff section | Books the rounding difference to write-off account |
| **Print** | Top toolbar | Print payment receipt/voucher |
| **Email** | Top toolbar | Email payment advice to the party |
| **Duplicate** | Top toolbar (⋮ menu) | Create a copy of this payment |
| **View Ledger** | After Submit | Open General Ledger filtered to this payment |
| **Repost** | ⋮ menu | Redo the GL posting (if accounts changed) |

---

# 📝 SECTION 3 — JOURNAL ENTRY (Deep Dive)
**URL:** `/desk/journal-entry`

**Layman:** A **manual accounting entry** for anything that doesn't fit a standard form. Example: recording monthly depreciation, adjusting a wrong entry, booking a bank charge, recording a loan.

**Technical:** Directly creates GL Entry records with user-defined debit/credit rows. Every debit MUST equal every credit (double-entry rule).

---

## 📋 ALL FIELDS — SECTION BY SECTION

### 🔷 Header Section

| Field | Layman | Technical |
|---|---|---|
| **Company** ⭐ | Which company | Determines accounts and fiscal year |
| **Entry Type** ⭐ | What kind of journal entry? | Controls GL behavior and available fields |
| **Series** ⭐ | Auto document number | Naming series |
| **Posting Date** ⭐ | The accounting date | GL entries posted here |
| **Multi Currency** ✅ | Does this entry have foreign currency rows? | Enables exchange rate fields in accounts table |
| **Consider for Tax Withholding** ✅ | Should TDS apply? | For payment-related JVs |
| **Tax Withholding Category** | Which TDS section | TDS rate lookup |
| **Is System Generated** ✅ | Was this created by ERPNext automatically? | For depreciation, deferred entries — read-only |
| **Amended From** | If this is a corrected version of a cancelled JV | Linked to original |
| **From Template** | Was it created from a Journal Entry Template? | Auto-fill from saved template |

**Entry Type options and what they mean:**

| Entry Type | Layman Use Case | Technical |
|---|---|---|
| **Journal Entry** | General purpose adjustments | Standard double-entry |
| **Bank Entry** | Bank charges, bank interest received | Links to bank account |
| **Cash Entry** | Petty cash transactions | Links to cash account |
| **Credit Note** | Customer refund via journal | AR credit |
| **Debit Note** | Supplier deduction via journal | AP debit |
| **Contra Entry** | Cash withdrawn from bank or deposited | Bank ↔ Cash movement |
| **Excise Entry** | Excise/duty tax entries | Tax accounts |
| **Write Off Entry** | Writing off bad debts or losses | Expense posting |
| **Opening Entry** | Starting balances when going live | `is_opening = Yes`, no P&L impact |
| **Depreciation Entry** | Monthly asset depreciation | Auto-created by Asset module |
| **Exchange Gain or Loss** | Currency fluctuation booking | From Exchange Rate Revaluation |
| **Deferred Revenue** | Recognizing advance payments as income | For subscription/prepaid income |
| **Deferred Expense** | Recognizing prepaid expenses monthly | For insurance, rent paid in advance |
| **Inter Company Journal Entry** | Transaction between group companies | Inter-company eliminations |
| **Reversal Of** | Reversal of a previous JV | Creates equal opposite entry |

---

### 🔷 Periodic Accounting Section

| Field | Layman | Technical |
|---|---|---|
| **For All Stock Asset Accounts** ✅ | Apply to all stock-linked asset accounts | For periodic stock valuation adjustments |
| **Stock Asset Account** | Specific stock account | Inventory valuation account |
| **Periodic Entry Difference Account** | Account for posting the stock difference | Usually "Stock Adjustment" |
| **🔘 Get Balance** | Fetch current balance of selected stock account | Calculates how much to adjust |

---

### 🔷 Accounting Entries Table ⭐ (THE CORE OF JOURNAL ENTRY)

Every Journal Entry row (line item) has these columns:

| Column | Layman | Technical |
|---|---|---|
| **Account** ⭐ | Which GL ledger to affect | Must be a posting (non-group) account |
| **Party Type** | Customer / Supplier / Employee | For AR/AP accounts — required to identify the party |
| **Party** | Specific party name | Links to Customer/Supplier master |
| **Debit (In Account Currency)** | Amount to debit in that account's currency | Increases Assets/Expenses; Decreases Liabilities/Income |
| **Credit (In Account Currency)** | Amount to credit | Decreases Assets/Expenses; Increases Liabilities/Income |
| **Debit (In Company Currency)** | Converted to base currency | For foreign currency rows |
| **Credit (In Company Currency)** | Converted to base currency | For foreign currency rows |
| **Exchange Rate** | Rate for foreign currency conversion | e.g., 83 for USD→INR |
| **Cost Center** | Which department | For expense/income categorization |
| **Project** | Which project | Project-wise accounting |
| **Is Advance** ✅ | Is this an advance payment row? | Links to outstanding invoices differently |
| **Reference Type / Name** | Linked document (invoice being cleared) | Sales Invoice / Purchase Invoice / Payment Request |
| **Remarks** | Row-level narration | Appears in GL for this specific line |
| **User Remark** | Additional custom note | For internal use |

**Golden Rule:** Sum of all Debit rows MUST = Sum of all Credit rows. If Debit ≠ Credit, ERPNext won't submit.

---

### 🔷 Totals Section

| Field | Layman | Technical |
|---|---|---|
| **Total Debit** | Sum of all debit rows | Auto-calculated |
| **Total Credit** | Sum of all credit rows | Auto-calculated |
| **Difference (Dr - Cr)** | Must be ZERO to submit | If non-zero, entry is unbalanced |
| **🔘 Make Difference Entry** | Auto-add a balancing row | Creates a row in a "Temporary Opening" account to balance |

---

### 🔷 Reference Section

| Field | Layman | Technical |
|---|---|---|
| **Reference Number** | Cheque number or bank reference | For bank reconciliation |
| **Reference Date** | Date of cheque/bank transaction | |
| **Clearance Date** | Date cheque cleared | Set during Bank Clearance |
| **Bill No** | Supplier's bill number | For AP-type JVs |
| **Bill Date** | Supplier's bill date | |
| **Due Date** | Payment due date | |
| **Inter Company JE Reference** | Linked JV in the other group company | For inter-company consolidation |
| **Reversal Of** | Which JV this reversal is correcting | Links to original JV |
| **Payment Order** | If linked to a Payment Order batch | Batch payment reference |

---

### 🔷 Write Off Section

| Field | Layman | Technical |
|---|---|---|
| **Write Off Based On** | Invoices or Advances | Source for write-off calculation |
| **🔘 Get Outstanding Invoices** | Fetch overdue invoices for write-off | Pulls open invoices for the party |
| **Write Off Amount** | The amount to write off as bad debt | Posted to write-off expense account |

---

### 🔷 Additional Info Section

| Field | Layman | Technical |
|---|---|---|
| **Is Opening** | Opening balance entry? | No P&L impact; sets beginning balances |
| **Finance Book** | Which parallel accounting book | IFRS / Tax / Management |
| **Mode of Payment** | Cash / Cheque / NEFT | For bank reconciliation |
| **Pay To / Received From** | Name on the cheque | For cheque printing |
| **Custom Remark** ✅ | Write own narration | Overrides auto-narration |
| **Remark** | The GL narration | Appears in General Ledger |

---

## 🔘 BUTTONS ON JOURNAL ENTRY FORM

| Button | What it does |
|---|---|
| **Save** | Save as Draft — no GL impact |
| **Submit** | Post GL entries — locked after this |
| **Cancel** | Reverse all GL entries |
| **Get Balance** (Make Difference Entry) | Auto-create balancing row |
| **Get Outstanding Invoices** | For write-off JVs — fetch unpaid invoices |
| **From Template** (field) | Select a saved JE Template to pre-fill all rows |
| **Print** | Print the voucher |
| **Reverse Journal Entry** | Create an exact opposite JV to undo this one |

---

# 📨 SECTION 4 — PAYMENT REQUEST (Deep Dive)
**URL:** `/desk/payment-request`

**Layman:** You send the customer a **payment link** — they click it and pay online. ERPNext tracks whether they've paid.

**Technical:** Creates a payment gateway request that generates a URL. When customer pays via the gateway, a Payment Entry is auto-created.

---

## 📋 ALL FIELDS

### 🔷 Header

| Field | Layman | Technical |
|---|---|---|
| **Payment Request Type** ⭐ | **Inward** (you requesting money from customer) / **Outward** (requesting payment to supplier) | Determines GL direction |
| **Transaction Date** | Date of the request | |
| **Series** ⭐ | Document number | |
| **Company** | Which company | |
| **Mode of Payment** | Online / Bank Transfer / UPI | |

### 🔷 Party Details

| Field | Layman | Technical |
|---|---|---|
| **Party Type** | Customer / Supplier | |
| **Party** | Specific customer/supplier | |
| **Party Name** | Auto-filled | |
| **Reference Doctype** | What document is this request for? | Sales Invoice / Purchase Invoice / Sales Order |
| **Reference Name** | The specific document | e.g., ACC-SINV-2025-0042 |

### 🔷 Payment Reference Table
Lists all invoices or installments included in this payment request. Each row: Reference Type + Reference Name + Amount.

### 🔷 Transaction Details

| Field | Layman | Technical |
|---|---|---|
| **Amount** ⭐ | How much you're requesting | In transaction currency |
| **Transaction Currency** | Currency for the request | e.g., INR, USD |
| **Is a Subscription** ✅ | Is this for a recurring subscription? | Links to Subscription module |
| **Outstanding Amount** | How much is still unpaid | In party account currency |
| **Party Account Currency** | Customer's account currency | |

### 🔷 Bank Account Details

| Field | Layman | Technical |
|---|---|---|
| **Bank Account** | Your bank to receive payment into | |
| **Bank** | Bank name (auto-filled) | |
| **Bank Account No** | Account number (auto-filled) | |
| **IBAN / Branch Code / SWIFT** | Bank routing details for international payments | Read-only, auto-filled |

### 🔷 Recipient Message and Payment Details

| Field | Layman | Technical |
|---|---|---|
| **Print Format** | Which template to use for the payment request email | |
| **To (Email)** | Customer's email address | Payment link sent here |
| **Subject** | Email subject line | |
| **Payment Gateway Account** | Which online payment gateway (Razorpay, Stripe, PayPal) | The gateway that processes the payment |
| **Message** | Email body text | Supports HTML; includes the payment link |

### 🔷 Payment Gateway Details

| Field | Layman | Technical |
|---|---|---|
| **Payment Gateway** | e.g., Razorpay, Stripe | Read-only, set by gateway account |
| **Payment Account** | Ledger for recording gateway receipts | |
| **Payment Channel** | Email / SMS / WhatsApp | How the link is delivered |
| **Payment URL** | The actual payment link | Customer clicks this to pay |
| **Phone Number** | For SMS channel | |

---

## 🔘 BUTTONS ON PAYMENT REQUEST FORM

| Button | What it does |
|---|---|
| **Save** | Save as Draft |
| **Submit** | Sends the payment link to the customer's email/SMS |
| **Cancel** | Cancels the request — link becomes inactive |
| **Resend Payment Email** | Resend the payment link if customer didn't receive/use it |
| **Create Payment Entry** | Manually mark payment as done (without online gateway) |

---

# 📦 SECTION 5 — PAYMENT ORDER
*(For batch payments to multiple suppliers at once)*

**Layman:** Instead of paying 50 suppliers one by one, bundle all into ONE instruction to your bank. Your bank processes all 50 payments together.

### All Fields

| Field | Layman | Technical |
|---|---|---|
| **Company** ⭐ | Which company is paying | |
| **Posting Date** ⭐ | Payment batch date | |
| **Payment Order Type** | Outward (paying suppliers) / Inward (collecting from customers) | |
| **Company Bank Account** ⭐ | Your bank account to debit | |
| **References table** | Each row = one payment to be made | |
| ↳ **Payment Request / Invoice** | Source document for this payment row | |
| ↳ **Party Type / Party** | Who is being paid | |
| ↳ **Amount** | How much | |
| ↳ **Bank Account** | Supplier's bank details | |
| **Total Amount** | Grand total of all payments | Auto-calculated |

### Buttons

| Button | What it does |
|---|---|
| **Get From** | Fetch all pending Payment Requests or invoices | Adds rows automatically |
| **Submit** | Finalizes batch; triggers individual Payment Entries for each row |
| **Download Bank File** | Exports a bank-format file (HDFC/ICICI bulk payment format) |
| **Cancel** | Cancels the batch; reverses Payment Entries |

---

# 🔄 SECTION 6 — PAYMENT RECONCILIATION
*(Deep Dive — matching payments to invoices manually)*

**Layman:** Sometimes ERPNext can't automatically figure out which payment belongs to which invoice (e.g., customer made a bulk NEFT with no reference). You manually **drag and match** them here.

### Workflow (Step-by-Step)

```
Step 1: Select Company + Party Type + Party + AR/AP Account
Step 2: Click "Get Unreconciled Entries"
        ↓ Shows unmatched invoices in "Invoices" table
        ↓ Shows unallocated payments in "Payments" table
Step 3: Select rows from both tables
Step 4: Click "Allocate" → System auto-matches by amount/date
   OR  Manually type amounts in "Allocation" table
Step 5: Click "Reconcile"
        ↓ Posts reconciliation
        ↓ Invoice outstanding = 0
        ↓ Payment unallocated amount = 0
```

### Buttons Explained

| Button | What it does |
|---|---|
| **Get Unreconciled Entries** | Queries all open invoices and unmatched payments for the selected party |
| **Allocate** | Auto-algorithm matches payments to invoices (oldest-first, amount-matching) |
| **Reconcile** | Applies your allocation — clears invoice outstanding amounts |
| **Clear Filters** | Resets all date/amount filter fields |

---

# ↩️ SECTION 7 — UNRECONCILE PAYMENT
**Layman:** Oops — you matched the wrong payment to the wrong invoice. This tool **breaks the match** and sends both back to unmatched status.

### Workflow
1. Select Company + Payment Entry (the one wrongly matched)
2. System shows all invoices it's currently matched to
3. Select which allocation to break
4. Click **Unreconcile**
5. Invoice goes back to "outstanding", payment goes back to "unallocated"

---

# ⚙️ SECTION 8 — PROCESS PAYMENT RECONCILIATION
**Layman:** Run Payment Reconciliation for **all parties at once** in the background — instead of doing one customer at a time.

| Field | What it does |
|---|---|
| **Company** ⭐ | Which company |
| **Party Type** ⭐ | Customer or Supplier |
| **Party** | Leave blank = ALL parties |
| **Receivable/Payable Account** | Which AR/AP ledger |

| Button | What it does |
|---|---|
| **Submit** | Starts background job to auto-reconcile all matched payments |
| **View Logs** | Check progress, see which parties were reconciled, any errors |

---

# 🔁 SECTION 9 — REPOST ACCOUNTING LEDGER & REPOST PAYMENT LEDGER

**Repost Accounting Ledger:**
**Layman:** If you changed company settings (like default accounts) AFTER transactions were posted, the old GL entries are wrong. This tool **recalculates and fixes** the GL entries without cancelling/re-submitting documents.

**Repost Payment Ledger:**
**Layman:** If invoice outstanding amounts are showing wrong values (a known system glitch), this tool **rebuilds** the payment ledger to fix the numbers.

> [!WARNING]
> Both repost tools should ONLY be used when your accountant confirms something is wrong. Incorrect use can create accounting discrepancies that are hard to reverse.

| Field | What it does |
|---|---|
| **Vouchers table** | List the specific documents to repost |
| ↳ DocType | e.g., Sales Invoice, Payment Entry |
| ↳ Voucher No | The document number |
| ↳ Posting Date | Date of the document |

---

## 🗺️ PAYMENTS FLOW DIAGRAM

```
CUSTOMER PAYMENT FLOW:
─────────────────────
Sales Invoice (submitted) → Outstanding: ₹1,00,000
        ↓
Customer pays via:
  Option A: Online → Payment Request → Payment Gateway → Auto Payment Entry
  Option B: Bank Transfer → Manual Payment Entry
        ↓
Payment Entry (Receive)
  Paid From: Accounts Receivable
  Paid To:   Bank Account
  References: [Sales Invoice link]
        ↓
Invoice Outstanding: ₹0 ✅
Bank Account Balance: +₹1,00,000 ✅

SUPPLIER PAYMENT FLOW:
──────────────────────
Purchase Invoice (submitted) → Outstanding: ₹50,000
        ↓
You pay via:
  Option A: Single → Payment Entry (Pay)
  Option B: Batch → Payment Order → Individual Payment Entries
        ↓
Payment Entry (Pay)
  Paid From: Bank Account
  Paid To:   Accounts Payable
  References: [Purchase Invoice link]
        ↓
Invoice Outstanding: ₹0 ✅
Bank Account Balance: -₹50,000 ✅

IF PAYMENT NOT AUTO-MATCHED:
────────────────────────────
Payment Entry exists (unallocated)
        ↓
Payment Reconciliation Tool
  → Get Unreconciled Entries
  → Match Payment → Invoice
  → Reconcile
        ↓
Cleared ✅
```

---

> [!TIP]
> Always use **Get Outstanding Invoices** button in Payment Entry before manually typing amounts. It auto-fills all unpaid invoices — saving time and preventing errors.

> [!IMPORTANT]
> The **Payment Type** field (Receive/Pay/Internal Transfer) is the most critical field in Payment Entry. Getting it wrong creates reversed GL entries that are hard to spot.

> [!NOTE]
> The **Bank Balance line chart** on the Accounts Dashboard is the single best indicator of your company's cash health. Watch it daily — a consistent downward trend means you're burning cash faster than you're collecting it.
