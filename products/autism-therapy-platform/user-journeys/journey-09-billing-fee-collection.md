# User Journey: Billing & Fee Collection

**Previously:** J5 | ✅ **IN SCOPE — MVP**
**Trigger:** End of billing cycle (monthly) — Rahul needs to generate invoices for all active families and collect payment
**Primary actor:** Rahul (Center Director — billing owner)
**Supporting actors:** Meena (parent — the payer); System (auto-generates invoices from attendance records); Priya (attendance source — her marks feed invoice generation)
**Entry condition:** At least one child has confirmed session attendance for the billing period AND a fee structure has been configured for that child (INV-001). DPDPA parental consent must be confirmed for each child before any financial record is generated.
**End state:** All active children have invoices generated for the month; payment links sent via WhatsApp; payments confirmed and receipts issued; overdue families flagged for follow-up
**Journey source documents:**
- cluster-3-billing-payments.md — Stories INV-001 through INV-005, UPI-001 through UPI-005
- cluster-4-scheduling-communication.md — Stories WA-003, WA-005, REMIND-003
- cluster-2-patient-records-intake.md — Story INT-003 (DPDPA consent gate context)
- cluster-1-clinical-documentation.md — Story EMR-001, EMR-002 (child record and consent dependencies)

---

## Discovery Context

**MVP Scope:** ✅ IN SCOPE — MVP

**Pain points & friction:**
- No automated payment reminder — Rahul must manually track who has paid and who hasn't 🔵 Inferred from absence of structured billing tool
- Session count for billing depends on paper attendance records that may be inconsistent 🔶 [HYPOTHESIS]
- Fee conversations are relationship-sensitive — delayed or avoided, leading to receivables piling up 🔶 [HYPOTHESIS]
- No financial dashboard: Rahul cannot see at a glance monthly revenue, outstanding fees, or collection rate 🔵 Inferred from "no single system" product context
- Evidence base for structured reminders reducing no-shows: 39% no-show (no reminder) vs. 3% (live call) ✅ Psychiatric Services study — directly applicable to appointment reminders; fee payment reminder ROI is 🔵 inferred analogy

**Emotional states:**
- Rahul: Asking families for money is uncomfortable — especially when he knows the family is financially stretched. Likely delays these conversations. 🔶 [HYPOTHESIS] (pattern documented in small Indian private health practices analogously)
- Meena: Financial stress is documented. Fee reminder may trigger anxiety or disengagement. ✅ Tandfonline 2025: "financial pressures" as driver of "invisible exits"

**Current workarounds:**
- WhatsApp status used to post payment deadline reminders — indirect, non-confrontational 🔶 [HYPOTHESIS]
- Some centers require advance payment to avoid collection awkwardness 🔶 [HYPOTHESIS]
- Excel with conditional formatting used to track outstanding balances 🔶 [HYPOTHESIS]

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | System | Billing cycle end date reached (configurable: last day of month, or rolling 30 days). Invoice generation job triggers automatically. | Background — no user interaction | Cron job reads attendance records for all active children. Reads fee structure per child (INV-001). Only confirmed attendance (status = Present) is included. |
| 2 | System | For each active child with confirmed attendance and a configured fee structure, a draft invoice is created. | Invoice Draft created in DB | Per-session fee: one line item per attended session (date, session type, therapist, fee). Monthly flat: single line item. Package: deducted from prepaid balance. |
| 3 | System | Invoice generation job completes. Rahul receives in-app notification: "X draft invoices are ready for review." | Billing Dashboard — badge count on Billing tab | If job fails, Rahul receives an error alert and can manually trigger re-generation. No partial invoice states committed. |
| 4 | Rahul | Opens Billing section. Reviews the outstanding dashboard summary: total outstanding, number of families with balances, number of families with balances >30 days overdue. | Billing Dashboard — Outstanding tab (UPI-004) | Reads: all invoices with status = Draft or Sent + unpaid. Sorted by days overdue descending. Summary row totals calculated server-side. |
| 5 | Rahul | Taps into "Draft Invoices" view. Sees list of all draft invoices for the current billing cycle. | Draft Invoices List Screen | Reads: invoice records with status = Draft. Shows child name, parent name, amount, billing period, fee mode. |
| 6 | Rahul | Opens a specific draft invoice. Reviews line items. Optionally adjusts: adds discount, removes a disputed session, adds a miscellaneous charge. | Invoice Detail Screen (INV-002) | Writes: any adjustment is stored as a modification record. Total recalculates in real-time on device. Ambiguous sessions (cancelled vs. attended) highlighted in amber with review prompt. |
| 7 | Rahul | Confirms invoice is correct. Taps "Send". | Invoice Detail Screen | Writes: invoice status changes Draft → Sent. Invoice due date set (default 7 days from send). Triggers WhatsApp/SMS delivery of invoice to parent (Step 8). |
| 8 | System | Invoice PDF generated. Parent notified via WhatsApp (if opted in and WABA connected) or via pre-filled WhatsApp share intent. Message uses approved "Fee Due" template. | Background / WhatsApp intent | ⚠️ DPDPA — invoice PDF contains child name and financial data; transmitted via WhatsApp Business API only (not personal WhatsApp); parent must be opted in (WA-003). Delivery status logged. |
| 9 | Meena | Receives WhatsApp message from center's business number. Sees fee amount and payment link. Taps payment link. | Parent's WhatsApp — message thread | Deep link: `upi://pay?pa=...` format OR short URL. Opens GPay/PhonePe/Paytm/BHIM/BHIM UPI depending on parent's installed app. |
| 10 | Meena | Completes UPI payment via her preferred app. | Parent's UPI app — external | No platform interaction during actual payment. UPI payment gateway receives transaction. |
| 11 | System | UPI payment gateway sends confirmation callback to platform. Platform receives webhook/callback and auto-reconciles payment against the child's fee record within 60 seconds. | Background — payment reconciliation (UPI-002) | Writes: invoice status → Paid; outstanding balance reduced; payment record created with UPI reference ID, amount, timestamp. Idempotency: duplicate callbacks suppressed by transaction reference ID check. |
| 12 | System | Receipt auto-generated (PDF). Queued for WhatsApp delivery to parent. | Background — receipt generation (INV-004) | Writes: receipt record with unique receipt number, center name, child name, payment amount, method, date. PDF generated server-side within 60 seconds of payment confirmation. |
| 13 | Meena | Receives WhatsApp receipt from center: "Receipt for ₹[amount] — [Child Name]'s therapy payment received. Receipt #[number]." | Parent's WhatsApp | Delivery status logged. If WhatsApp delivery fails, receipt stored in platform; Rahul alerted to resend manually. |
| 14 | Rahul | Sees push notification: "Payment received: ₹[amount] from [Parent Name] for [Child Name]". Dashboard outstanding balance updates. | Billing Dashboard — real-time update | Client polls or receives push notification via app. Outstanding balance recalculated. Invoice removed from outstanding list. |
| 15 | Rahul | Reviews remaining outstanding invoices. For families who have not paid after due date, automated overdue reminders fire on configured schedule (default: 7 days after due date, then 14 days). | Background — overdue reminder job (INV-005) | Writes: reminder log entry per send. Uses approved WhatsApp template or DLT-registered SMS sender. Soft tone by default. Per-family disable toggle respected. |
| 16 | Rahul | Reviews outstanding dashboard for families still unpaid. For high-risk families (e.g., 30+ days overdue), manually initiates a new UPI payment request or takes direct action. | Outstanding Balance Dashboard (UPI-004) | Rahul taps "Send Reminder" on any row → triggers WhatsApp payment link send (WA-005) or generates new UPI link (UPI-001). |
| 17 | Rahul | For families who pay in cash or bank transfer, manually records the payment. | Record Payment form (INV-003) | Writes: payment record with amount, method (Cash/Bank Transfer/Cheque), date, recorder identity. Outstanding balance updated locally immediately; syncs when connection restored. Triggers receipt generation (INV-004). |
| 18 | System | Monthly billing cycle complete. All invoices in Paid, Partially Paid, or Overdue state. Rahul's dashboard shows a clean view of collection status. | Billing Dashboard — end state | No auto-close of billing cycle; Rahul reviews at his discretion. Overdue reminders continue on schedule for unpaid invoices. |

---

## Decision Points

### Decision 1: Does a child have a fee structure configured?
**At step:** 1–2 (invoice generation)
**Question:** Has Rahul configured INV-001 fee structure for this child?
- **Path A — Fee structure exists:** Invoice is generated. → Continue at Step 2
- **Path B — No fee structure:** No invoice generated for this child. Child appears in "No fee structure set" list on Billing Dashboard. Rahul is prompted: "No fee structure set for [Child Name]. Add a fee structure in Billing Settings first." → Rahul configures fee structure (INV-001), then re-triggers invoice generation.
- **Path C (Edge case) — Fee structure is ₹0/session:** Invoice generated for ₹0. System displays warning to Rahul. Reminder suppressed (EC-01 of INV-005).

### Decision 2: Does the child have confirmed attendance for the billing period?
**At step:** 1–2 (invoice generation)
**Question:** Are there any sessions with status = Present in this billing period?
- **Path A — Attendance exists:** Invoice generated with session line items. → Continue at Step 2
- **Path B — No attendance:** No invoice generated. Child appears in "No sessions this period" list. Rahul is informed but no action is forced.
- **Path C (Edge case) — Attendance ambiguous:** Some sessions marked Cancelled vs. Attended in dispute. Draft invoice highlights these sessions in amber. → Continue at Step 6 (Rahul must review before sending).

### Decision 3: Is the parent opted in to WhatsApp?
**At step:** 7–8 (invoice delivery)
**Question:** Does parent have WhatsApp opt-in status = Opted in AND WABA connected?
- **Path A — Opted in, WABA active:** WhatsApp message sent using approved "Fee Due" template. → Continue at Step 9
- **Path B — Not opted in or WABA not connected:** WhatsApp button greyed out. Rahul sends invoice via pre-filled WhatsApp share intent (UPI-001 fallback) or manual share. Platform does not auto-send in this case.
- **Path C — Opted out between invoice send and reminder:** Subsequent automated reminders suppressed for this parent (WA-003 AC-04).

### Decision 4: Does Meena pay via UPI payment link?
**At step:** 9–11 (payment collection)
**Question:** Does Meena complete payment through the UPI link?
- **Path A — UPI payment completed:** Auto-reconciliation fires. → Continue at Step 11
- **Path B — UPI payment failed (insufficient funds, cancelled, expired link):** Payment request status → Failed. Rahul sees "Failed" on billing record with timestamp. Can regenerate a new payment link from the same screen. Overdue reminder cycle continues.
- **Path C — Meena pays cash at center:** Rahul records manually (INV-003). → Jump to Step 17
- **Path D — UPI callback delayed >2 hours:** System re-queries payment status at 5 minutes and 30 minutes. If unconfirmed after 2 hours, status → "Status Unknown". Rahul alerted to verify manually.
- **Path E (Edge case) — Partial payment:** System records amount paid, calculates remaining balance, flags as "Partially Paid" for Rahul's review. New payment request can be generated for remainder.

### Decision 5: Does invoice become overdue?
**At step:** 15 (overdue reminder)
**Question:** Is invoice still unpaid after due date passes?
- **Path A — Invoice paid before due date:** Reminder job checks status before sending; finds invoice = Paid. No reminder sent. → Journey ends at Step 14.
- **Path B — Invoice unpaid at 7 days past due:** Soft reminder sent via WhatsApp/SMS. → Continue at Step 15
- **Path C — Invoice unpaid at 14 days past due:** Standard reminder sent. Rahul receives in-app alert. → Continue at Step 16
- **Path D — Per-family reminder disabled:** Reminders suppressed silently. Logged in delivery log as "Suppressed — reminders disabled for this family." Rahul must follow up manually.

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Billing Dashboard — Outstanding tab | Rahul's single view of all families with outstanding balances | Tap family row → billing profile / tap "Send Reminder" | Rahul | UPI-004 |
| Draft Invoices List | Review all draft invoices before sending | Tap invoice to open detail | Rahul | INV-002 |
| Invoice Detail Screen | Review, adjust, and send an individual invoice | Tap "Send" to finalize and deliver invoice | Rahul | INV-002 |
| UPI Payment Request Screen | Generate and share a UPI payment link for a specific family | Tap "Generate Link" | Rahul | UPI-001 |
| Record Payment form | Manually log cash or bank transfer payment | Tap "Save" to record payment | Rahul | INV-003 |
| Payment History tab (per child) | Full chronological log of all payments for a child | Review / filter by date, method, status | Rahul | UPI-003 |
| Settings > Billing | Configure center UPI VPA, fee structure defaults, billing cycle dates, overdue thresholds | Tap "Save" to confirm settings | Rahul | UPI-005, INV-001 |
| Settings > Reminders | Edit reminder templates (fee due, fee overdue), enable/disable automation globally | Tap "Save template" | Rahul | REMIND-003, REMIND-004 |
| Settings > WhatsApp | Connect WABA account, manage approved templates, view connection status | Tap "Connect" | Rahul | WA-001, WA-002 |
| Reminder Delivery Log | Audit trail of all reminders sent across the center | Tap "Retry" on failed messages | Rahul | REMIND-005 |
| Meena's WhatsApp — invoice message | Parent receives fee due message with payment link | Tap payment link → UPI app | Meena | WA-005 |
| Meena's WhatsApp — receipt | Parent receives payment receipt | Read / save | Meena | INV-004 |

---

## Designer Handoff

### Screen: Billing Dashboard — Outstanding tab

**Purpose:** Give Rahul a single-view snapshot of all families with outstanding balances — total receivables, count of overdue accounts, and a quick path to send a reminder or payment link.
**Primary action:** Tap a family row to open their billing profile, or tap "Send Reminder" shortcut directly from the row.
**Entry point(s):** Bottom nav or sidebar tap on "Billing" tab → Outstanding sub-tab (default view when there are outstanding invoices).
**Exit point(s):** Tap row → Invoice Detail Screen; tap "Send Reminder" → WhatsApp payment link send flow (UPI-001 / WA-005).

**Key components:**
- Summary row (top, pinned): Total outstanding across all families (₹X), number of families with outstanding balances (N), number with balances >30 days overdue (N). Non-tappable summary banner.
- Family list rows: Child name, parent name, outstanding amount, invoice due date, days overdue (calculated), "Send Reminder" shortcut button (right-aligned, ≥44px).
- Overdue status labels: "On time" / "X days overdue" as text labels alongside color indicators (amber for 1–29 days; red for 30+ days). Color never used alone.
- Sort control: Default = Days Overdue descending. Sort chip visible at top of list.

**States:**
- **Empty state:** "All families are up to date. No outstanding balances." — positive confirmation, no empty list visual. Show a "View payment history" link.
- **Loading state:** Skeleton cards (3 rows) while data fetches. Show "Last updated [time]" timestamp.
- **Error state:** "Could not load outstanding balances. Pull down to refresh." Retry tap available.
- **Offline state:** Shows last-synced data with a banner: "Offline — showing data from [date/time]. Payment actions unavailable." Payment link send and record payment actions disabled.

**Constraints:**
- Must be operable one-handed on a mid-range Android (5.5–6.5 inch screen).
- Touch targets for "Send Reminder" button: minimum 44×44px, right-edge placement for thumb reach.
- Do not show more than 4 columns of data in the list row — overflow to second line rather than horizontal scroll.

---

### Screen: Invoice Detail Screen

**Purpose:** Let Rahul review the auto-generated draft invoice line by line, make any adjustments, and send to the parent.
**Primary action:** Tap "Send" to finalize the invoice and trigger parent notification.
**Entry point(s):** Tap invoice from Draft Invoices List or from Outstanding tab.
**Exit point(s):** Tap "Send" → invoice status = Sent, returns to Draft Invoices List (now with one fewer draft); tap "Back" → Draft Invoices List.

**Key components:**
- Invoice header: Child name, parent name, billing period (e.g., "April 2026"), invoice number (auto-generated), due date (7 days from send, adjustable).
- Line items list: Each row shows date, session type, therapist name (for per-session billing), amount. Swipe-left on a row to delete it. Tap to edit amount.
- Adjustment controls: "Add discount" button (opens amount + reason fields). "Add line item" button (opens description + amount fields).
- Total row (pinned to bottom of list): Recalculates in real-time as line items are added/removed/adjusted.
- Ambiguous session flag: Amber highlight on sessions where attendance status is disputed. Prompt reads: "Review attendance for [date] before finalising."
- "Send" button: Primary CTA, bottom of screen. Green, full-width. Disabled until all amber flags are resolved or explicitly overridden.

**States:**
- **Empty state:** Should not occur for a draft invoice (invoice is only created if attendance exists). If reached: "No sessions found for this billing period."
- **Loading state:** Skeleton line items list while invoice data loads.
- **Error state:** If send fails: "Could not send invoice. Check your connection and try again." Invoice remains in Draft status — no partial send.
- **Offline state:** Invoice detail readable from cache. "Send" button disabled with label "Sending requires internet connection."

**Constraints:**
- Total must always be visible — sticky footer or pinned bottom row. User should not have to scroll to see the total.
- Destructive action (delete line item) must require swipe, not an accidental tap.
- "Send" should not be tappable while any amber-flagged sessions remain unresolved without an explicit "I've reviewed this" confirmation.

---

### Screen: UPI Payment Request Screen

**Purpose:** Generate a shareable UPI payment link for a specific family's outstanding balance and send it via WhatsApp in one tap.
**Primary action:** Tap "Generate Link" → then "Send via WhatsApp."
**Entry point(s):** Tap "Request Payment" from Invoice Detail Screen or Outstanding tab "Send Reminder" shortcut.
**Exit point(s):** Tap "Send via WhatsApp" → WhatsApp intent opens, pre-filled with parent number and message. User returns to billing screen after sharing.

**Key components:**
- Pre-filled amount field: Shows outstanding balance. Editable for partial payment.
- Payment link status: Shows "Pending" with expiry countdown (default 48 hours) if link already exists for this invoice.
- "Generate Link" button: Creates new UPI deep link + short URL.
- "Send via WhatsApp" button: Opens WhatsApp intent with pre-filled message: "Dear [Parent Name], please find the payment link for [Child Name]'s therapy fees for [Month]: [link]. Total: ₹[amount]. — [Center Name]"
- "Copy link" option: Copies short URL to clipboard for alternate channel sharing.

**States:**
- **Empty state:** If outstanding balance is ₹0: "Request Payment" button disabled. Tooltip: "No outstanding balance for this family."
- **Loading state:** "Generating link..." spinner on button for up to 3 seconds.
- **Error state:** "Could not generate payment link. Please try again." If UPI VPA not configured: "Complete UPI setup in Settings before generating links."
- **Offline state:** "Payment links require an internet connection." Action blocked.

**Constraints:**
- UPI VPA must be verified before link generation (UPI-005). Gate this with a clear prompt to Settings if not configured.
- WhatsApp fallback via system share sheet if WhatsApp not installed.
- Do not auto-send the WhatsApp message — the intent opens and Rahul taps Send in WhatsApp. This preserves his ability to review the message before it goes.

---

### Screen: Record Payment form

**Purpose:** Allow Rahul to manually log a cash or bank transfer payment against an outstanding invoice without generating a UPI link.
**Primary action:** Tap "Save" to record the payment and update the outstanding balance.
**Entry point(s):** Tap "Record Payment" from Invoice Detail Screen or Payment History tab.
**Exit point(s):** Tap "Save" → outstanding balance updated; receipt generated; returns to Invoice Detail or Payment History.

**Key components:**
- Amount field: Pre-filled with outstanding balance. Editable (for partial payments).
- Payment method dropdown: Cash / Bank Transfer / Cheque.
- Date field: Defaults to today. Editable (for backdated entries).
- Notes field (optional): Free text, max 200 characters. For recording bank reference numbers, cheque numbers, etc.
- "Save" button: Primary CTA. Enabled once amount > ₹0 is entered.

**States:**
- **Empty state:** Not applicable — form always opens pre-filled with outstanding balance.
- **Loading state:** "Saving..." on button. Optimistic update: balance updates on-screen immediately even before server confirmation.
- **Error state:** "Could not save payment record. Try again." Amount field restored; no data lost.
- **Offline state:** Form submittable offline. Record queued locally. Balance updated on device immediately. Banner: "Saved offline — will sync when connected."

**Constraints:**
- Offline write is a hard requirement (Rahul may be recording a cash payment with no connectivity).
- Overpayment warning: If amount > outstanding balance, show: "This amount exceeds the outstanding balance of ₹[X]. Record ₹[X] as a credit?" — allow confirm or adjust.

---

### Screen: Settings > Billing (fee structure per child)

**Purpose:** Let Rahul configure the billing rule for each enrolled child — per session, monthly flat, or session package. Set once; updated when terms change.
**Primary action:** Select fee mode and enter amount. Tap "Save."
**Entry point(s):** Navigate from child's profile → Billing Settings tab.
**Exit point(s):** Tap "Save" → fee structure stored with effective date; returns to child's billing profile.

**Key components:**
- Fee mode selector: Three options displayed as large radio chips — "Per Session", "Monthly Flat", "Session Package". Each chip shows a brief explanation.
- Amount input: Appears after mode is selected. ₹ prefix, numeric keyboard. Shows "₹0" warning if entered.
- Effective date: Defaults to today. Editable.
- Fee history accordion (below form): Shows all past fee structures with effective dates — read-only.

**States:**
- **Empty state:** If no fee structure configured: "No fee structure set. Add one to enable invoice generation." Orange prompt banner. Shown on child's billing profile tab.
- **Loading state:** Spinner on "Save" button while saving.
- **Error state:** "Could not save fee structure. Try again." No partial state committed.
- **Offline state:** Fee structure configuration requires network. Form is read-only offline with banner: "Offline — fee structure changes require internet connection."

**Constraints:**
- This is an admin screen — not accessible to Priya. RBAC enforced.
- Fee history section is read-only. Past structures cannot be edited, only viewed.

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 1 | Invoice record (Draft status) per child per billing period | Attendance records (status=Present), fee structure per child | `POST /invoices/generate-batch` — cron-triggered | Server-side only; no client offline behavior | ⚠️ DPDPA — invoice contains child name + health-adjacent billing data; consent must be Active before invoice is written |
| 2 | Invoice line items per session | Session records, fee mode | Part of batch invoice generation job | Server-side | DPDPA consent check per child record |
| 3 | Notification record | Invoice count | `POST /notifications/push` | Push notification delivered when client connects | None |
| 4 | None (read-only) | Invoice records (Draft, Sent, unpaid), payment records | `GET /billing/outstanding` | Cached response served; staleness banner shown | RBAC: admin role only |
| 5 | None (read-only) | Draft invoices for current billing cycle | `GET /invoices?status=draft&cycle=[period]` | Cached list | RBAC: admin role only |
| 6 | Invoice line item modifications | Invoice record, session records | `PATCH /invoices/{id}/line-items` | Offline: queue edit locally; sync on restore | DPDPA: financial data update logged in audit trail |
| 7 | Invoice status: Draft → Sent; due date set | Invoice record | `POST /invoices/{id}/send` | Requires connectivity | DPDPA: transmission of financial data to parent; consent check |
| 8 | WhatsApp delivery log entry | Parent opt-in status, approved template, WABA connection | WhatsApp Business API — `POST /messages` (Meta) | Cannot send offline | ⚠️ DPDPA + WhatsApp opt-in required before send |
| 9–10 | (External — UPI app) | (External) | UPI deep link / short URL redirect | External to platform | None (platform not involved in transaction) |
| 11 | Payment record (amount, UPI reference ID, timestamp); invoice status → Paid; outstanding balance reduced | UPI callback payload | `POST /webhooks/upi-callback` (inbound from UPI gateway) | Server-side only; client reflects on next sync | DPDPA: payment data stored encrypted; admin access only |
| 12 | Receipt PDF (server-side generated); receipt record with unique number | Payment record, child name, center details | `POST /receipts/generate` — event-triggered by payment confirmation | Server-side | DPDPA: receipt contains child name; encrypted storage |
| 13 | WhatsApp delivery log entry for receipt | Receipt PDF, parent WhatsApp number, opt-in status | WhatsApp Business API — `POST /messages` (Meta) | Cannot send offline | DPDPA + WhatsApp opt-in |
| 14 | None | Payment record (real-time) | Push notification or WebSocket update to Rahul's client | Client reflects on reconnect | None |
| 15 | Reminder log entry; WhatsApp message sent | Invoices past due date, reminder schedule config, per-family disable flag | `POST /reminders/fee-overdue-job` — cron-triggered; WhatsApp API or SMS | Server-side; SMS/WhatsApp send cannot be offline | ⚠️ DPDPA: fee amount + child name in message; TRAI DLT sender ID required for SMS |
| 17 | Manual payment record; invoice status update; triggers receipt | Nothing read externally | `POST /payments/manual` | Writes locally when offline; syncs on restore; optimistic UI balance update | DPDPA: financial record; admin access only |

**Key state transitions:**
- Invoice transitions from `Draft` → `Sent` at Step 7
- Invoice transitions from `Sent` → `Paid` or `Partially Paid` at Step 11 (UPI callback) or Step 17 (manual)
- Invoice transitions from `Sent` → `Overdue` when current date > due_date (calculated field, not a DB write event)
- Payment request transitions from `Pending` → `Paid` / `Failed` / `Status Unknown` at Step 11

**Background jobs / async events triggered by this journey:**
- `invoice-generation-job`: Triggered at billing cycle end date. Generates all draft invoices. Runs once per cycle per center.
- `upi-callback-handler`: Triggered by UPI gateway webhook on payment completion. Idempotent by transaction reference ID.
- `receipt-generation-job`: Triggered by payment confirmation event. Generates PDF and queues WhatsApp send.
- `overdue-reminder-job`: Daily cron. Checks all invoices past due date by configured thresholds. Dispatches WhatsApp/SMS reminders.

**DPDPA compliance checkpoints:**
- Step 1: ⚠️ DPDPA — invoice generation reads child health-adjacent data; child consent record must be status = Active before any billing record is created
- Step 8: ⚠️ DPDPA — invoice PDF transmitted to parent via Meta's WhatsApp infrastructure; parent WhatsApp opt-in (WA-003) is the consent mechanism for this channel; platform must not transmit clinical data in WhatsApp message body
- Step 11: ⚠️ DPDPA — UPI reference ID and payment amount stored against child's record; financial data of a minor; access restricted to admin role; encrypted at rest
- Step 15: ⚠️ DPDPA — reminder message contains child name and fee amount; TRAI DLT-registered sender ID required for transactional SMS in India; message must not contain clinical information

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 3 — Scheduling & Attendance Management | Invoice auto-generation (INV-002) reads confirmed attendance records. Attendance is marked by Priya via SCHED-004. | If attendance is not marked digitally (still on paper), INV-002 has no input data. The core differentiator vs. PractiPal — attendance-driven invoicing — does not function. Rahul falls back to manual session counting. |
| Journey 2 — Intake & Enrollment | Fee structure configuration (INV-001) requires a child record to exist (EMR-001). DPDPA consent (EMR-002 / INT-003) must be confirmed before any billing record is created. | Invoice generation blocked for children without confirmed consent. Fee structure cannot be attached to a non-existent child record. |
| WhatsApp Business API setup (WA-001 to WA-003) | Invoice delivery via WhatsApp (WA-005) and automated overdue reminders (INV-005) depend on WABA connection and parent opt-in. | Without WABA, Rahul must manually forward invoices via WhatsApp share intent. Automated fee reminders fall back to SMS (if DLT SMS provider configured) or are not sent at all. |
| Journey 10 — Missed Session Detection & Dropout Prevention | Families at dropout risk (sustained absence) who are also receiving overdue reminders may be in financial distress. Coordinating billing follow-up with dropout intervention prevents compounding pressure. | Without dropout context, Rahul may send automated fee reminders to a family already in crisis — potentially accelerating disengagement. |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by competitive observation (PractiPal, TherapEZ, Jane App, SimplePractice) and document synthesis — not by validated user research. Before committing engineering capacity, a real product thinker should ask:

**What we assumed but haven't validated:**
- [ASSUMPTION] Rahul currently spends significant time manually calculating fees and sending payment reminders via WhatsApp. The actual time burden has not been measured in primary research. (H-12 in hypothesis register)
- [ASSUMPTION] Meena will click a UPI payment link in a WhatsApp message and complete payment digitally — rather than paying cash at the center or ignoring the link. Indian payment behavior at small private therapy centers is unconfirmed.
- [ASSUMPTION] Auto-generation of invoices from attendance records adds meaningful value — this assumes attendance is captured digitally and reliably. If attendance marking is inconsistent, invoice auto-generation produces inaccurate invoices that Rahul must manually correct every month, reducing net value.
- [ASSUMPTION] Automated overdue fee reminders will not damage the center-family relationship. Indian therapy center billing is relationship-sensitive (Tandfonline 2025: "financial pressures" as a driver of "invisible exits"). A tone-deaf automated reminder to a financially stressed family could accelerate dropout.
- [ASSUMPTION] Rahul is willing to set up WhatsApp Business API (requires Meta Business Manager verification, a dedicated business phone number, and ongoing Meta approval for templates). This is non-trivial for a small center director with limited technical capacity.

**What a researcher would ask before building this:**
- How does Rahul collect fees today? Has he tried any payment link tool (Practo, Razorpay payment pages) and abandoned it? What was the friction?
- What proportion of families pay cash vs. UPI? In which tier of market (metro vs. tier-2) does UPI payment behavior differ most?
- Would automated fee reminders help Rahul or create relationship damage? Ask him about a time he sent a fee reminder — what happened?

**What the Product Consultant would challenge:**
- The entire billing cluster has a critical dependency on the attendance records module (Journey 3). If attendance is not captured digitally, INV-002 — the core differentiator — cannot function. Gate the billing cluster on confirmed attendance data quality in production, not just in QA.
- Consider whether the MVP billing feature is just: (1) fee structure configuration + (2) manual invoice with PDF export + (3) UPI payment link via WhatsApp share intent. The auto-generation, automated reminders, and WABA integration can be Phase 2 once attendance data quality is proven.

**Risk level:**
- Invoice auto-generation (INV-002): Medium — depends on attendance module reliability
- UPI payment link (UPI-001–005): Low-Medium — table stakes in India; core behavior change risk is adoption not functionality
- Automated reminders (INV-005, REMIND-003): Medium — relationship sensitivity in Indian small-practice context is high; tone testing needed before launch
- WhatsApp Business API integration (WA-005): High — onboarding lift for center directors and Meta Business verification are significant barriers

Use the `/researcher` agent to validate H-12 (billing pain), H-09 (fee collection discomfort), and the UPI payment behavior assumption before sprint planning.
Use the `/product-consultant` agent to challenge the WABA scope and the billing-attendance dependency.
