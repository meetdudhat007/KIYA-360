# 🏢 ERPNext Organization Module — Every Button Explained

> This is a complete button-by-button walkthrough of the **Organization module** in your live ERPNext instance (`kelvin360 (Demo)`).

---

## 📌 PART 1 — THE LIST VIEW (When you open any section)

Every list page in ERPNext (Company list, Department list, etc.) has a standard toolbar. Here's what each button does:

### 🔝 Top Toolbar Buttons

| Button / Icon | Name | What it does |
|---|---|---|
| **➕ New** | New / Add Button | Creates a brand new record. Click to open a blank form. |
| **🔍 Search bar** | Filter / Search | Type anything to instantly search records in the list. |
| **⚙️ Filter** | Advanced Filter | Opens a filter panel where you can filter by any field (e.g., show only companies in India). |
| **↕️ Sort** | Sort Options | Sort the list A–Z, Z–A, newest first, oldest first. |
| **☰ List / Tree / Report** | View Switcher | Switch between **List view** (rows), **Tree view** (parent-child hierarchy), and **Report view** (spreadsheet style). |
| **✏️ Edit** (bulk) | Bulk Edit | Select multiple rows using checkboxes and edit them all at once. |
| **🗑️ Delete** (bulk) | Bulk Delete | Select multiple rows and delete them all at once. |
| **⬇️ Export** | Export to Excel/CSV | Downloads all the listed records into a spreadsheet. |
| **📥 Import** | Import | Upload records from a CSV/Excel file to bulk-create entries. |
| **🔔 Refresh** | Refresh | Reloads the list to show latest data. |
| **⭐ Saved Filters** | Saved Filters | Save your current filter settings so you can reuse them later. |

---

## 📌 PART 2 — THE COMPANY FORM (Most Important)

When you open a Company record (e.g., `kelvin360 (Demo)`), you see a form with **6 tabs** and a standard toolbar at the top.

### 🔝 Form Toolbar Buttons (Top Row)

| Button | What it does |
|---|---|
| **💾 Save** | Saves all changes you made to the company record. Always click this after making any change. |
| **✏️ Edit** | If the form is in read-only mode, this button switches it to edit mode so you can make changes. |
| **🗑️ Delete** | Permanently deletes this company record. ⚠️ DANGER — only use if no transactions exist. |
| **📋 Duplicate** | Creates a copy of this company with all settings. Useful when setting up a new company with similar structure. |
| **⋮ Menu (3-dot)** | Opens a dropdown with extra options: Rename, Print, Email, Copy Link, etc. |
| **🖨️ Print** | Opens the print preview of the company document (useful for official records). |
| **📧 Email** | Send this record by email to someone. |
| **🔗 Copy Link** | Copies the direct URL link to this record. |
| **⬅️ Back arrow** | Goes back to the Company list page. |
| **◀ ▶ Navigation arrows** | Moves to the previous or next company record in the list. |
| **👁️ Activity** | Shows the full history of who changed what and when in this record (audit trail). |
| **💬 Comment** | Adds a comment/note to this record that your team members can see. |
| **📎 Attach** | Attaches a file (PDF, image, document) to this company record. |

---

## 🗂️ TAB 1 — DETAILS

*This is the basic identity of your company.*

### Section: Company Info
| Field | What it does |
|---|---|
| **Company Name** | The legal registered name of your business. This appears on all documents (invoices, POs, salary slips). |
| **Abbreviation** | A short code (e.g., "KD" for Kelvin Demo). Used as a suffix on all account names (e.g., "Cash - KD"). Once set, **cannot be changed**. |
| **Default Currency** | The base currency of the company (e.g., INR, USD). All financial reports will use this currency. |
| **Country** | Where your company is located. This determines the default chart of accounts template, address format, and tax rules. |
| **Is Group** | ✅ Checkbox — If enabled, this company acts as a parent/holding company in a multi-company setup. |

### Section: Company Setup
| Field | What it does |
|---|---|
| **Tax ID** | Your GST number, PAN, or VAT registration number. Printed on invoices for legal compliance. |
| **Domain** | Select business domain (e.g., Manufacturing, Retail, Healthcare). Customizes the ERPNext interface to show relevant modules. |
| **Date of Incorporation** | When the company was legally registered. Used for company records. |
| **Phone No** | Company main phone. Appears on letterheads and printed documents. |
| **Email** | Company main email. Used as "From" address on outgoing emails. |
| **Website** | Company website URL. Shown on printed documents. |
| **Fax** | Company fax number (legacy field). |
| **Registration Details** | Free text field to record company registration numbers, CIN, etc. |

### Section: Address & Contact
| Field | What it does |
|---|---|
| **Default Address** | Select the registered address of the company. This is printed on all outgoing documents. |
| **Company Logo** | Upload your company logo. Appears on letterheads, reports, and the ERPNext sidebar. |

### Button inside this section:
| Button | What it does |
|---|---|
| **➕ Create Address** | Quick link to create a new company address without leaving this form. |

---

## 🗂️ TAB 2 — ACCOUNTS

*This is the financial backbone — the most important tab.*

### Section: Chart of Accounts
| Field/Button | What it does |
|---|---|
| **Create Chart of Accounts Based On** | Dropdown: Choose whether to use a **Standard Template** (country-specific pre-built accounts) or a **Existing Company** (copy another company's accounts). |
| **Chart of Accounts Template** | Select which country template to use (e.g., "India - Chart of Accounts"). Auto-creates all accounts like CGST, SGST, IGST, Debtors, Creditors, etc. |
| **🔗 View Chart of Accounts** | Button that jumps directly to the full Chart of Accounts tree page for this company. |

### Section: Default Accounts
> These are the accounts ERPNext will use automatically for common transactions. Every time an invoice is created, ERPNext uses these defaults so you don't have to manually select accounts every time.

| Field | What it does |
|---|---|
| **Default Bank Account** | The main bank account (e.g., HDFC Bank) used for payments. |
| **Default Cash Account** | The petty cash account used for cash transactions. |
| **Default Receivable Account** | The "Debtors" account — where money owed TO your company is tracked. |
| **Default Payable Account** | The "Creditors" account — where money your company OWES is tracked. |
| **Write Off Account** | Account used when a bad debt (uncollectable money) is written off. |
| **Cost of Goods Sold** | Account where the cost of items you've sold is recorded (for P&L). |
| **Default Income Account** | Where all sales revenue goes by default. |
| **Default Cost Center** | The default cost center for all expenses. Usually the main/head office. |

### Section: Exchange Gain/Loss
| Field | What it does |
|---|---|
| **Exchange Gain/Loss Account** | When you deal in foreign currencies, the value fluctuates. This account records those gains or losses automatically. |
| **Unrealized Exchange Gain/Loss Account** | For foreign invoices that are OPEN (not yet paid) — unrealized means the exchange rate may still change. |

### Section: Round Off
| Field | What it does |
|---|---|
| **Round Off Account** | When invoice totals have fractions (e.g., ₹999.999), rounding differences are posted here. |
| **Round Off Cost Center** | Cost center for the rounding adjustment entries. |
| **Round Off for Opening** | Round-off account specifically used when entering opening balances. |

### Section: Deferred Accounting
| Field | What it does |
|---|---|
| **Default Deferred Revenue Account** | For services billed in advance (e.g., annual subscription paid upfront). Revenue is recognized month by month. |
| **Default Deferred Expense Account** | For expenses paid in advance (e.g., annual insurance premium). Expense is spread over the coverage period. |

### Section: Advance Payments
| Field | What it does |
|---|---|
| **Book Advance Payments in Separate Party Account** | ✅ Checkbox — If ON, advance payments from customers are tracked in a separate ledger (not directly adjusted against invoices). Gives cleaner accounting. |
| **Reconciliation Takes Effect On** | Dropdown: Choose when advance-payment reconciliation is effective — "Reconciliation Date" or "First Unadjusted Invoice Date". |

---

## 🗂️ TAB 3 — ACCOUNTS CLOSING

*For locking your books at year end.*

| Field/Button | What it does |
|---|---|
| **Accounts Frozen Till Date** | 📅 Date field — Set a date before which no one can post any accounting entries. Used after year-end closing to protect finalized books. Example: Set to 31-March-2025 to freeze FY2024-25. |
| **Role Allowed to Set Frozen Accounts** | Dropdown — Only users with this role can change the freeze date. Protects against accidental changes. |
| **Role Allowed to Edit Frozen Entries** | Dropdown — Even after books are frozen, certain senior roles (e.g., Accounts Manager) can still make corrections. |

### Activity Section (Bottom of every form)
| Element | What it does |
|---|---|
| **💬 Add a comment** | Type a comment/note. Visible to all users with access to this record. Useful for leaving notes like "Updated bank account on 1 Oct 2025". |
| **📧 New Email** | Send an email directly from within this record. The email is logged in the activity thread. |
| **Activity Timeline** | Shows full history: who created the record, who edited it, what was changed, and when. This is the **audit trail**. |

---

## 🗂️ TAB 4 — BUYING AND SELLING

*Links your company settings to purchase and sales operations.*

### Section: Buying & Selling Settings
| Field | What it does |
|---|---|
| **Default Buying Terms** | Pre-written terms & conditions automatically added to all Purchase Orders (e.g., "Payment due within 30 days"). |
| **Default Selling Terms** | Pre-written terms & conditions automatically added to all Sales Orders and Invoices. |
| **Monthly Sales Target (₹)** | Set a monthly revenue goal for your company. Used in the Sales analytics dashboard. |
| **Total Monthly Sales (₹)** | (Read-only) Auto-calculated field showing actual sales for the current month. Compared against the target above. |
| **Credit Limit** | Maximum credit you'll extend to customers by default. ERPNext will warn or block orders if a customer exceeds this. |

### Section: Purchase Expense Accounts
| Field | What it does |
|---|---|
| **Purchase Expense Account** | Default account where purchase costs are booked (for goods). |
| **Service Expense Account** | Default account for service purchases (e.g., consulting, repairs). |

### Section: Stock Expense Accounts
| Field | What it does |
|---|---|
| **Expenses Added to Stock** | Account for additional costs added to stock value (e.g., freight, customs duty on import). |
| **Expenses Added to Stock Contra** | The contra/offsetting account for the above entry. Used in double-entry accounting. |

---

## 🗂️ TAB 5 — STOCK AND MANUFACTURING

*Controls how inventory and production costs are tracked.*

### Section: Stock Settings
| Field | What it does |
|---|---|
| **Enable Perpetual Inventory** | ✅ Checkbox — When ON, every stock movement (receipt, delivery, transfer) instantly creates accounting entries. When OFF, stock is only reconciled periodically. **Recommended: ON for accurate real-time accounting.** |
| **Enable Item-wise Inventory Account** | ✅ Checkbox — Allows each product/item to have its OWN inventory account instead of one shared account. Useful for tracking high-value items separately. |
| **Default Inventory Account** | Account where the value of all stock in hand is recorded (e.g., "Stock In Hand - KD"). Appears on the Balance Sheet as a current asset. |
| **Default Stock Valuation Method** | How the cost of sold goods is calculated: **FIFO** (First In, First Out — oldest stock priced first) or **Moving Average** (average cost of all stock). |
| **Stock Adjustment Account** | Account for stock write-offs, damaged goods, or manual stock adjustments. |
| **Stock Received But Not Billed** | Account for goods received from a supplier but whose invoice hasn't arrived yet. Creates a liability until the bill is received. |

### Section: Manufacturing
| Field | What it does |
|---|---|
| **Default Operating Cost Account** | Account for manufacturing overhead costs like electricity, machine maintenance. |
| **Default Work In Progress Warehouse** | Where partially-manufactured goods are stored during production. |
| **Default Finished Goods Warehouse** | Where completed manufactured products are stored. |
| **Default Scrap Warehouse** | Where waste/scrap material from production goes. Scrap can be re-used or sold. |

---

## 🗂️ TAB 6 — DASHBOARD

*A quick overview of all connected documents.*

| Section | What it shows |
|---|---|
| **Pre Sales** | Number of Quotations linked to this company. Click to see the list. |
| **Orders** | Count of Sales Orders, Delivery Notes, Sales Invoices. |
| **Support** | Number of open customer Issues/tickets. |
| **Projects** | Number of active Projects. |

> [!TIP]
> These are **clickable counters** — click any number to jump directly to the filtered list of those records for this company.

---

## 📌 PART 3 — FISCAL YEAR PAGE

**URL:** `/app/fiscal-year`

| Button / Field | What it does |
|---|---|
| **➕ New Fiscal Year** | Creates a new accounting year (e.g., 2026-2027: April 1, 2026 to March 31, 2027). |
| **Year Name** | A name like "2026-2027". Used in all financial reports as the period selector. |
| **Year Start Date** | When the financial year begins (e.g., 01-04-2026 for India). |
| **Year End Date** | When the financial year ends (e.g., 31-03-2027 for India). |
| **Is Short Year** | ✅ Checkbox — For companies that started mid-year and have a short first year (e.g., July to March only). |
| **Companies table** | Link this fiscal year to specific companies (needed in multi-company setups). |
| **⚙️ Set as Default** | Button in the fiscal year form — marks this year as the active year. All new transactions will default to this year. |

---

## 📌 PART 4 — CHART OF ACCOUNTS

**URL:** `/app/account`

This opens as a **Tree View** (expandable hierarchy).

| Button | What it does |
|---|---|
| **➕ Add Child** | Adds a new sub-account under a selected parent account. Example: Add "HDFC Bank" under "Bank Accounts". |
| **✏️ Edit** | Opens the selected account for editing (change name, type, parent). |
| **🗑️ Delete** | Removes the account (only allowed if no transactions posted against it). |
| **📊 View Ledger** | Opens the General Ledger for this account — shows every debit/credit entry ever posted. |
| **🔽 Expand All / Collapse All** | Expands or collapses the entire account tree. |
| **Company filter** | Dropdown at top — switch between companies if you have multiple. Shows that company's chart. |
| **Is Group** (in account form) | ✅ Checkbox — Group accounts are "folders" that contain other accounts. Non-group accounts are "leaf nodes" where actual transactions are posted. |
| **Freeze Account** | ✅ Checkbox — Prevents any new transactions from being posted to this specific account. |
| **Disabled** | ✅ Checkbox — Hides this account from all dropdowns without deleting it. |

---

## 📌 PART 5 — COST CENTER

**URL:** `/app/cost-center`

Also a **Tree View**.

| Button | What it does |
|---|---|
| **➕ Add Child** | Creates a new cost center under a parent. Example: Add "Weaving Unit" under "Production". |
| **📊 Budget Variance Report** | Button on the cost center form — shows actual spending vs. the budget you set for this cost center. |
| **Budgets Table** | Inside the cost center form — add a row to set budget for each account per fiscal year. |
| **Is Group** | Same as Chart of Accounts — marks this as a folder vs. an actual trackable center. |
| **Disabled** | Hides this cost center from future transactions. |

---

## 📌 PART 6 — BRANCH

**URL:** `/app/branch`

Simple master page.

| Button | What it does |
|---|---|
| **➕ New Branch** | Create a new branch (e.g., "Mumbai Office", "Surat Factory"). |
| **Branch** field | The name of the branch. This name is used when assigning employees or filtering reports by location. |

---

## 📌 PART 7 — DEPARTMENT

**URL:** `/app/department`

Tree view (departments can have sub-departments).

| Button / Field | What it does |
|---|---|
| **➕ Add Child** | Creates a sub-department (e.g., "Dyeing" under "Production"). |
| **Department Name** | The name of the team/unit (HR, Accounts, Production, etc.). |
| **Is Group** | Marks it as a parent/folder department. |
| **Company** | Link to a specific company (for multi-company setups where departments differ per company). |
| **Leave Block List** | Attach a leave restriction list — blocks employees in this department from taking leaves during specific busy periods (e.g., busy season). |
| **Payroll Cost Center** | Which cost center should bear the salary cost of employees in this department. |

---

## 📌 PART 8 — DESIGNATION

**URL:** `/app/designation`

Simplest master in the module.

| Button / Field | What it does |
|---|---|
| **➕ New Designation** | Create a new job title (e.g., "Senior Accountant", "Machine Operator", "Factory Manager"). |
| **Designation Name** | The job title. Used in employee profiles, offer letters, and org charts. |
| **Skills Table** | (Optional) List skills associated with this designation. Used in HR competency tracking. |

---

## 📌 PART 9 — LETTER HEAD

**URL:** `/app/letter-head`

| Button / Field | What it does |
|---|---|
| **➕ New Letter Head** | Create a new letterhead design. |
| **Letter Head Name** | A label for this design (e.g., "Main Letterhead", "Legal Letterhead"). |
| **Is Default** | ✅ Checkbox — This letterhead will be auto-applied on all new documents. |
| **Source: Image / HTML** | Radio button — Choose between uploading an image as the header, OR writing HTML code for a fully custom design. |
| **Header** | The top section (company logo, name, address). |
| **Footer** | The bottom section (contact info, bank details, website). |
| **👁️ Preview** | Button — Shows a live preview of how your documents will look when printed. |
| **📐 Content Editor** | Rich text editor — drag and resize your logo, add text boxes, colors, etc. without coding. |

---

## 📌 PART 10 — SALES TAXES AND CHARGES TEMPLATE

**URL:** `/app/sales-taxes-and-charges-template`

| Button / Field | What it does |
|---|---|
| **➕ New Template** | Create a new tax template (e.g., "GST 18% - Interstate", "GST 5% - Textile"). |
| **Template Title** | Name this template (appears in the dropdown when creating invoices). |
| **Is Default** | ✅ Checkbox — Auto-applied to all new Sales Orders and Invoices. |
| **Company** | Which company this template belongs to. |
| **Tax Table (rows)** | Add rows for each tax component: |
| ↳ **Type** | How the tax is calculated: % of Net Total, Fixed Amount, % of Previous Row Total, etc. |
| ↳ **Account Head** | Which tax account this posts to (e.g., "Output GST - IGST", "CGST Payable"). |
| ↳ **Rate %** | The tax percentage (e.g., 18 for 18% GST). |
| ↳ **Amount** | (Calculated automatically based on the invoice amount and rate). |
| ↳ **Include in Print Rate** | ✅ Checkbox — Show tax-inclusive price on the printed invoice (e.g., MRP-inclusive). |
| **➕ Add Row** | Add another tax component (e.g., CGST + SGST as two separate rows for intrastate). |
| **🗑️ Delete Row** | Remove a tax row from the template. |

---

## 🔄 Universal Buttons on EVERY Form

These appear on every single form in ERPNext regardless of which module you're in:

| Button | What it does |
|---|---|
| **💾 Save** | Save changes. |
| **❌ Discard** | Cancel changes made since last save. |
| **⋮ Menu** | Print, Email, Duplicate, Rename, Copy Link, Reload, Share. |
| **📎 Attach** | Upload files (PDF, images, Excel) to link to this record. |
| **💬 Comment** | Leave a note for your team. |
| **📧 Email** | Send this record as an email. |
| **👁️ Activity** | See the full audit log of changes to this record. |
| **🔔 Follow** | Subscribe to get notified when this record changes. |
| **🔗 Links section** | Shows all other documents linked to this record (e.g., on Company → shows Quotations, Invoices, etc.). |

---

> [!IMPORTANT]
> The **Company form's Accounts tab** is the most critical — the default accounts you set here are used as fallbacks across the ENTIRE system. If they are wrong, your financial reports will be wrong.

> [!TIP]
> Always set **"Enable Perpetual Inventory" = ON** in the Stock & Manufacturing tab if you are a manufacturing or trading company. This gives you real-time stock valuation in your Balance Sheet.
