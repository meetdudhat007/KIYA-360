# 🏢 ERPNext Organization Module — Live Button-by-Button Guide
> ✅ Based on **live screenshots** from your actual ERPNext instance at `http://localhost:8080`

---

## 1️⃣ COMPANY

### 📋 Company List Page

![Company List Page](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_list_page_1790796894917.png)

**Buttons on the list page:**

| Button | What it does |
|---|---|
| **➕ Add Company** | Opens a blank Company form to register a new company |
| **🔍 Search bar** | Type company name to instantly find it |
| **⚙️ Filter** | Filter list by any field (e.g., country, currency) |
| **↕️ Sort** | Sort companies alphabetically or by date |
| **☰ List / Tree** | Switch between flat list and tree (for group companies) |
| **⬇️ Export** | Download the company list as Excel/CSV |
| **📥 Import** | Bulk-upload companies from a spreadsheet |
| **⋮ Actions** | Bulk edit, bulk delete selected rows |

---

### 🗂️ Tab 1 — DETAILS

![Company Details Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_details_tab_1790796912684.png)

| Field / Button | What it does |
|---|---|
| **Company Name** | Legal name of your business. Appears on every document (invoice, PO, salary slip). Cannot be easily changed after transactions. |
| **Abbreviation** | Short code like "KD". Auto-appended to all account names (e.g., "Cash - KD"). **Set once, never change.** |
| **Default Currency** | The main currency of all financial reports (e.g., INR). |
| **Country** | Determines tax laws, address format, and chart of accounts template. |
| **Is Group** ✅ | Makes this a parent/holding company. No transactions can be posted directly to a group company — it just contains child companies. |
| **Domain** | Your business type (Manufacturing, Retail, Healthcare). Customizes which ERPNext modules are shown on the dashboard. |
| **Tax ID** | GST number, PAN, CIN, or VAT registration. Printed on all outgoing invoices for legal compliance. |
| **Date of Incorporation** | When the company was legally registered. |
| **Phone / Fax / Email / Website** | Company contact info. Appears on letterheads and printed documents. |
| **Default Address** | The registered office address of the company. |
| **Company Logo** | Upload your logo. Shown on the sidebar, printed documents, and email headers. |
| **➕ Create Address** | Quick button to add a new company address without leaving this page. |

---

### 🗂️ Tab 2 — ACCOUNTS

![Company Accounts Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_accounts_tab_1790796924078.png)

**Section: Chart of Accounts**

| Field / Button | What it does |
|---|---|
| **Create Chart of Accounts Based On** | Choose "Standard Template" (pre-built for your country) or "Existing Company" (copy from another company). |
| **Chart of Accounts Template** | Select the country template. "India - Chart of Accounts" auto-creates all GST accounts (IGST, CGST, SGST), Debtors, Creditors, etc. |
| **🔗 View Chart of Accounts** | Jumps directly to your account tree. Click to see all your financial ledgers. |

**Section: Default Accounts** *(These are auto-used in every transaction)*

| Field | What it does |
|---|---|
| **Default Bank Account** | Your primary bank (e.g., HDFC Bank). Used when recording bank payments. |
| **Default Cash Account** | Petty cash account. Used in cash payment entries. |
| **Default Receivable Account** | "Debtors" account — tracks money customers OWE you. Created on every Sales Invoice. |
| **Default Payable Account** | "Creditors" account — tracks money you OWE suppliers. Created on every Purchase Bill. |
| **Default Income Account** | Where sales revenue is booked by default. Appears on P&L report. |
| **Default Cost Center** | The main cost center for all expenses. Usually "Main - CompanyCode". |
| **Write Off Account** | Used when a customer debt is written off as uncollectable (bad debt). |
| **Cost of Goods Sold Account** | Records the purchase cost of items you've sold. Used in P&L for Gross Profit calculation. |

**Section: Exchange Gain/Loss**

| Field | What it does |
|---|---|
| **Exchange Gain/Loss Account** | For foreign currency transactions — automatically books currency fluctuation gains or losses when payment rate differs from invoice rate. |
| **Unrealized Exchange Gain/Loss Account** | For OPEN (unpaid) foreign invoices — books paper gain/loss until actual payment is received. |

**Section: Round Off**

| Field | What it does |
|---|---|
| **Round Off Account** | When invoice total has ₹0.01 fractions, this account absorbs the rounding difference automatically. |
| **Round Off Cost Center** | Cost center for the rounding entries. |

**Section: Deferred Accounting**

| Field | What it does |
|---|---|
| **Default Deferred Revenue Account** | For advance payments received — e.g., annual subscription billed upfront but recognized monthly. |
| **Default Deferred Expense Account** | For prepaid expenses — e.g., annual insurance paid upfront but spread over 12 months. |

**Section: Advance Payments**

| Field | What it does |
|---|---|
| **Book Advance Payments in Separate Party Account** ✅ | Keeps advance receipts from customers in a separate ledger instead of adjusting against invoices immediately. Gives cleaner audit trail. |
| **Reconciliation Takes Effect On** | When advance-payment matching is applied — at reconciliation date or at invoice date. |

---

### 🗂️ Tab 3 — ACCOUNTS CLOSING

![Company Accounts Closing Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_accounts_closing_tab_1790796935402.png)

> Use this tab to **lock your books** after year-end. Nobody can accidentally post transactions to a closed year.

| Field | What it does |
|---|---|
| **Accounts Frozen Till Date** | 📅 Set a cutoff date. No accounting entry can be posted BEFORE this date. Example: "31-03-2025" freezes FY 2024-25 permanently. |
| **Role Allowed to Set Frozen Accounts** | Only users with this role (e.g., "Accounts Manager") can change the freeze date. |
| **Role Allowed to Edit Frozen Entries** | Even after freezing, senior roles can still post correction entries to frozen periods. |

---

### 🗂️ Tab 4 — BUYING AND SELLING

![Company Buying Selling Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_buying_selling_tab_1790796946193.png)

| Field | What it does |
|---|---|
| **Default Buying Terms** | Standard purchase terms automatically added to all Purchase Orders (e.g., "Delivery within 7 days, payment net 30"). |
| **Default Selling Terms** | Standard sales terms automatically added to all Quotations and Sales Orders. |
| **Monthly Sales Target (₹)** | Set a revenue goal. Shown on the Sales dashboard for performance tracking. |
| **Total Monthly Sales (₹)** | (Auto-calculated) Actual sales for the current month. Compared against target above. |
| **Credit Limit** | Maximum outstanding balance allowed for customers. ERPNext warns or blocks new orders if this is exceeded. |
| **Default Warehouse** | The warehouse that items are taken from or sent to by default in sales transactions. |
| **Purchase Expense Account** | Default account for goods purchases (inventory). |
| **Service Purchase Account** | Default account for service-type purchases (consulting, repairs, utilities). |

---

### 🗂️ Tab 5 — STOCK AND MANUFACTURING

![Company Stock Manufacturing Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_stock_manufacturing_tab_1790796958773.png)

**Section: Stock Settings**

| Field | What it does |
|---|---|
| **Enable Perpetual Inventory** ✅ | **THE MOST IMPORTANT TOGGLE.** When ON: every stock movement instantly creates accounting entries (stock in/out = debit/credit). When OFF: stock is only updated periodically. Always turn ON for manufacturing/trading. |
| **Enable Item-wise Inventory Account** ✅ | Each product gets its OWN inventory account in the chart of accounts. Useful for tracking high-value items (e.g., gold, machinery) separately. |
| **Default Inventory Account** | Master account where total stock value is shown on your Balance Sheet as a current asset. |
| **Default Stock Valuation Method** | **FIFO** = oldest stock is costed first. **Moving Average** = average cost of all available stock. Choose based on your business type. |
| **Stock Adjustment Account** | Where stock write-offs, damaged goods, or manual adjustments are booked. |
| **Stock Received But Not Billed Account** | Liability account for goods received but supplier invoice not yet received. Cleared when you create the Purchase Invoice. |
| **Expenses Included in Valuation Account** | Account for additional costs added to stock value (e.g., freight, import duty). |

**Section: Manufacturing Settings**

| Field | What it does |
|---|---|
| **Default Operating Cost Account** | For factory overhead costs like electricity, machine wear. Posted during production orders. |
| **Default WIP (Work In Progress) Warehouse** | Where raw materials and semi-finished goods are held DURING production. |
| **Default Finished Goods Warehouse** | Where completed products go after manufacturing. |
| **Default Scrap Warehouse** | Where waste material from production is stored. Scrap can be valued and re-used or sold. |

---

### 🗂️ Tab 6 — DASHBOARD

![Company Dashboard Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\company_dashboard_tab_1790796973815.png)

> This tab shows **live counts** of all documents linked to this company. Every number is a **clickable link** that opens the filtered list.

| Section | What it shows |
|---|---|
| **Pre Sales** | Number of active Quotations |
| **Orders** | Sales Orders, Delivery Notes, Sales Invoices |
| **Buying** | Purchase Orders, Purchase Receipts, Purchase Invoices |
| **HR** | Employees, Salary Slips |
| **Projects** | Active Projects |
| **Support** | Open Customer Issues |

---

## 2️⃣ LETTER HEAD

### 📋 Letter Head List

![Letter Head List](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\letter_head_list_page_1790797001543.png)

### 📝 Letter Head Form

![Letter Head Form](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\letter_head_detail_page_1790797023520.png)

| Field / Button | What it does |
|---|---|
| **Letter Head Name** | A label for this design (e.g., "Main Letterhead", "Legal Documents Header"). |
| **Is Default** ✅ | Automatically applies this letterhead to all new documents (invoices, POs, salary slips). Only one can be default. |
| **Source: Image** (radio) | Upload an image file (PNG/JPG) as your letterhead. Simple option — just upload your logo. |
| **Source: HTML** (radio) | Write custom HTML code for full control over the design (colors, fonts, layout, address placement). |
| **Header section** | What appears at the TOP of all printed documents — company logo, name, address, contact info. |
| **Footer section** | What appears at the BOTTOM — bank details, GST number, website, social media. |
| **👁️ Preview** | Shows a live preview of how your letterhead will look on a printed document. **Always check this before saving.** |
| **Content Editor toolbar** | Bold, Italic, Insert Image, Insert Table, Font Size, Color, Alignment — standard rich text editor tools. |
| **+ Add Image** | Inserts your company logo inside the header. |

---

## 3️⃣ DEPARTMENT

### 📋 Department List

![Department List](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\department_list_page_1790797055305.png)

### 📝 Department Form

![Department Form](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\department_detail_page_1790797090796.png)

| Field / Button | What it does |
|---|---|
| **Department Name** | Name of the team (e.g., "Accounts", "Production", "Quality Control"). |
| **Is Group** ✅ | Makes this a parent department. Child departments can be nested under it (e.g., "Manufacturing > Weaving > Dyeing"). |
| **Parent Department** | Select which department this one belongs to (for tree structure). |
| **Company** | Which company this department belongs to. Required in multi-company setups. |
| **Leave Block List** | Link a leave restriction list. Blocks employees in this department from taking leave during critical periods (e.g., busy season, audit month). |
| **Payroll Cost Center** | Which cost center bears the salary cost of ALL employees in this department. Salary postings automatically go to this cost center. |

---

## 4️⃣ BRANCH

### 📋 Branch List

![Branch List](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\branch_list_page_1790797142091.png)

### 📝 Branch Form

![Branch Form](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\branch_new_form_page_1790797180842.png)

> Branch is the simplest master in the Organization module. It's just a **location tag**.

| Field | What it does |
|---|---|
| **Branch** | The name/location (e.g., "Mumbai HQ", "Surat Factory", "Delhi Sales Office"). |

**Where Branch is used:**
- Assigned to `Employee` records → "This employee works at Surat Factory"
- Filter HR reports by branch (branch-wise salary, leave reports)
- Can be mapped to Cost Centers for location-wise P&L reports

---

## 5️⃣ USER

### 📋 User List

![User List](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\user_list_page_1790797218592.png)

A User is anyone who can **log in** to your ERPNext system.

### 🗂️ User Tab 1 — DETAILS

![User Details Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\user_details_tab_1790797243152.png)

| Field / Button | What it does |
|---|---|
| **Email** | The login username (must be a valid email). Used for login and all system communications. |
| **First Name / Last Name** | User's display name — shown in documents, comments, and the top bar. |
| **Full Name** | Auto-filled from first + last name. |
| **Username** | Optional shorter login alias (e.g., @john instead of john@company.com). |
| **Language** | The UI language for THIS user (e.g., English, Hindi, Arabic). Other users are unaffected. |
| **Time Zone** | User's local time zone. All timestamps shown to this user are adjusted to their zone. |
| **Gender** | Optional — used in HR records. |
| **Phone / Mobile No.** | Contact numbers. Also used for 2FA (two-factor authentication via SMS). |
| **Enabled** ✅ | If unchecked, the user is deactivated and cannot log in. Data is preserved. |
| **Allow Login With** | Choose login method: Email + Password, Mobile No., or Username. |
| **🔑 Set Password** | Button to manually set a new password for this user. |
| **📧 Send Welcome Email** | Sends the user an invitation email with a link to set their own password. |
| **Logout From All Devices** | Forces this user to log out from all browser sessions immediately (useful if account is compromised). |

---

### 🗂️ User Tab 2 — ROLES

![Roles Permissions Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\roles_permissions_tab_1790797257635.png)

> Roles control **what a user can see and do** in ERPNext. This is the access control center for this specific user.

| Feature | What it does |
|---|---|
| **Role Table** | List of all roles assigned to this user. Add rows to grant access. |
| **➕ Add Row** | Add a new role (e.g., "Accounts User", "Purchase Manager", "Stock User"). |
| **🗑️ Remove Row** | Remove a role to revoke that level of access. |
| **System User** ✅ | If ON, this is a regular internal user. If OFF, it's an "external" user (like a customer portal user) with very limited access. |
| **Role: System Manager** | Full admin access to everything. Only give this to trusted admins. |
| **Role: Accounts Manager** | Can approve and post all accounting entries. |
| **Role: HR Manager** | Full access to employee, payroll, and leave management. |
| **Role: Purchase Manager** | Can create, approve, and amend all purchase documents. |
| **Role: Sales Manager** | Can manage all sales documents and override discounts. |

---

### 🗂️ User Tab 3 — MORE INFO

![More Info Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\more_info_tab_1790797276631.png)

| Field | What it does |
|---|---|
| **Employee** | Link this user to their Employee record. When linked, salary slips, leave requests, etc. are auto-connected. |
| **Department** | The department this user belongs to. |
| **Designation** | Their job title. |
| **Location** | Physical work location. |
| **Banner Image** | A profile banner image for the user's profile page. |
| **Bio** | A short personal bio visible on the user profile. |
| **User Type** | System User (internal staff) or Website User (customer/vendor portal). |
| **Simultaneous Sessions** | How many browsers/devices this user can be logged into at the same time. |
| **Home Page** | The ERPNext page this user sees first after login (default: desk). |

---

### 🗂️ User Tab 4 — SETTINGS

![Settings Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\settings_tab_1790797296181.png)

| Field | What it does |
|---|---|
| **Email Signature** | The signature automatically added to all emails sent by this user from ERPNext. |
| **Allowed in Mentions** ✅ | If ON, other users can tag this person in comments using @name. |
| **Thread Notify** ✅ | User receives email/notification when someone replies to a thread they're involved in. |
| **Send Notifications for Email Threads** ✅ | Get notified when emails received by the company are responded to. |
| **Track Shown Documents** ✅ | ERPNext tracks which documents this user has already seen (marks them as "read"). |
| **Two Factor Authentication** | Enable 2FA for this user — login requires a one-time password (OTP) via app or SMS. |
| **Bypass 2FA Restrictions for OTP** | ✅ If the user has issues with 2FA, temporarily bypass it (admin use only). |
| **Default Print Format** | The print layout this user sees by default when printing any document. |
| **Background Image** | The wallpaper/background on this user's ERPNext desk. |

---

### 🗂️ User Tab 5 — SESSIONS / CONNECTIONS

![Sessions Tab](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\sessions_tab_1790797326094.png)

| Section | What it does |
|---|---|
| **Active Sessions** | Shows all currently active browser sessions for this user (device, IP, last seen). |
| **Third Party Apps** | OAuth apps connected to this user's account (e.g., mobile app, API integrations). |
| **API Access Tokens** | API keys generated for this user for external integrations. Can be revoked here. |

---

## 6️⃣ ROLE PERMISSIONS MANAGER

![Permission Manager Page](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\permission_manager_page_1790798158902.png)

> This is the **central security control panel** of ERPNext. Here you define what each role can Read, Write, Create, Delete, Submit, Cancel, and Amend for every document type.

| Button / Element | What it does |
|---|---|
| **Document Type dropdown** | Select which document (e.g., "Sales Invoice", "Employee") whose permissions you want to manage. |
| **Role dropdown** | Filter to see permissions for a specific role only. |
| **By Role** tab | See all documents a specific role can access. |
| **By Document Type** tab | See all roles that can access a specific document. |
| **➕ Add a New Rule** | Create a custom permission rule for a document+role combination. |
| **Read** ✅ | This role can view/see documents of this type. |
| **Write** ✅ | This role can edit existing documents. |
| **Create** ✅ | This role can create new documents. |
| **Delete** ✅ | This role can delete documents (use carefully!). |
| **Submit** ✅ | This role can submit (finalize/freeze) documents like invoices. |
| **Cancel** ✅ | This role can cancel submitted documents. |
| **Amend** ✅ | This role can amend (correct) a cancelled document by making a new version. |
| **Print** ✅ | This role can print the document. |
| **Email** ✅ | This role can send the document by email. |
| **Export** ✅ | This role can export document data to Excel/CSV. |
| **Import** ✅ | This role can import data into this document type. |
| **Share** ✅ | This role can share documents with other users. |
| **Set User Permissions** ✅ | This role can create user-level restrictions (e.g., this user can only see documents for Company X). |
| **If Owner** | Applies permission ONLY if the current user created/owns the document. |
| **Restrict by Link** | Limit visibility to only documents matching a specific linked field value. |
| **🗑️ Delete Rule** | Remove this permission rule. |
| **🔄 Reset to Defaults** | Wipe all custom permissions for this document and restore ERPNext's factory defaults. |

---

## 7️⃣ EMAIL ACCOUNT

### 📋 Email Account List

![Email Account List](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\email_account_list_1790798186988.png)

### 📝 Email Account Form

![Email Account Form](C:\Users\Hp\.gemini\antigravity-ide\brain\0c8d7c2c-02ab-4591-bd46-1d0c8cf8a5bd\email_account_form_1790798242469.png)

> Email Accounts connect ERPNext to your actual email inbox/outbox. ERPNext can **send** emails (outgoing) and **receive** emails (incoming) through this setup.

**Section: Basic Info**

| Field | What it does |
|---|---|
| **Email Account Name** | A label for this account (e.g., "Sales Email", "Support Inbox"). |
| **Email ID** | The actual email address (e.g., sales@yourcompany.com). |
| **Password** | The email password or App Password (for Gmail/Outlook 2FA accounts). |
| **Default Outgoing** ✅ | This email is used as the "From" address for all system-generated emails (invoices, notifications). Only one can be default outgoing. |
| **Default Incoming** ✅ | Incoming emails to this address are auto-imported into ERPNext's Communication module. |
| **Enable Incoming** ✅ | Turn on email fetching (ERPNext checks this inbox for new emails). |
| **Enable Outgoing** ✅ | Turn on email sending from ERPNext through this account. |

**Section: Incoming Mail (IMAP/POP3)**

| Field | What it does |
|---|---|
| **Service** | Dropdown — select Gmail, Outlook, Yahoo, or Custom. Auto-fills server settings. |
| **Email Server (IMAP)** | The IMAP server address (e.g., imap.gmail.com). |
| **Port** | Usually 993 for IMAP SSL. |
| **Use SSL** ✅ | Encrypts the email connection. Always ON for security. |
| **Frequency** | How often ERPNext checks for new emails (e.g., Every 30 minutes). |
| **Initial Sync Count** | How many old emails to import when first connecting (e.g., 100 most recent). |

**Section: Outgoing Mail (SMTP)**

| Field | What it does |
|---|---|
| **SMTP Server** | The outgoing mail server (e.g., smtp.gmail.com). |
| **SMTP Port** | Usually 587 (TLS) or 465 (SSL). |
| **Use TLS** ✅ | Encrypted outgoing connection. Always ON. |
| **Login ID** | Usually same as email ID. |

**Action Buttons**

| Button | What it does |
|---|---|
| **✅ Validate** | Tests the connection to your email server with the current settings. Tells you if login succeeds or fails before saving. |
| **📥 Get Mails Now** | Manually trigger an immediate email sync (instead of waiting for next scheduled check). |
| **💾 Save** | Saves all email account settings. |

**Section: Notification Settings**

| Field | What it does |
|---|---|
| **Append To** | Link incoming emails to a specific ERPNext document type. Example: emails to support@company.com are linked as "Issues". |
| **Create Contact** ✅ | Auto-create a Contact record in ERPNext for new email senders. |
| **Create Lead** ✅ | Auto-create a Lead (potential customer) when an unknown email sends to this inbox. |
| **Notify if Not Reply** | After X days of no reply, send the assigned user a reminder notification. |
| **Send Notification To** | Who gets notified when a new email arrives at this inbox. |

---

## 🔄 Universal Form Buttons (On Every Page)

| Button | What it does |
|---|---|
| **💾 Save** | Save all current changes |
| **❌ Discard** | Undo changes since last save |
| **⋮ Menu (3-dot)** | Print, Email, Duplicate, Rename, Copy Link, Reload |
| **📎 Attach** | Attach files to this record |
| **💬 Comment** | Leave a team note |
| **📧 New Email** | Send email directly from within this record |
| **👁️ Activity** | Full audit log — who changed what and when |
| **🔔 Follow** | Get notified whenever this record changes |

---

> [!IMPORTANT]
> **Role Permissions Manager** is the most powerful (and risky) page in this module. Giving too many permissions can expose sensitive financial data. Always follow the principle of **least privilege** — give users only what they need.

> [!TIP]
> For Email Account, always click the **Validate** button before saving. This confirms your email server credentials work correctly before ERPNext tries to send real emails.
