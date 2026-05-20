# Requirements: Journey 9 — Billing & Fee Collection

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 9 — Billing & Fee Collection
**MVP status:** IN SCOPE — MVP
**Primary actor:** Rahul (Center Director — billing owner)
**Supporting actors:** Meena (Parent / Primary Caregiver — the payer); Priya (Special Educator — attendance source); System (invoice generation, payment reconciliation, reminder dispatch)
**Date:** 2026-05-06
**Story ID prefix:** BILLING-
**Source documents:**
- `user-journeys/journey-09-billing-fee-collection.md`
- `user-journeys/journey-map.md` — Part 2, Journey 9

---

## Epic: BILLING — Billing & Fee Collection

**Goal:** Give Rahul a structured, end-to-end billing workflow that generates invoices automatically from confirmed attendance, delivers them to parents via WhatsApp, collects payment via UPI or manual entry, issues receipts, and surfaces outstanding balances in a single dashboard — replacing his current patchwork of Excel, manual WhatsApp messages, and memory.

**Copied from:** Jane App (automated billing from attendance), SimplePractice (invoice generation and payment link), Theralytics (payment tracking and overdue reminders), Razorpay (UPI payment link generation — India-native). No Indian competitor (TherapEZ, PractiPal) has attendance-driven invoice generation or automated payment reconciliation. This is a meaningful differentiator in the Indian market for this price tier.

**Target user(s):** Rahul (Center Director / Admin)

**Definition of Done:**
- Rahul can configure a fee structure for any enrolled child in under 60 seconds on minimum-spec Android or desktop Chrome
- Invoice generation runs automatically at billing cycle end; draft invoices for all active children with confirmed attendance appear in Rahul's dashboard within 5 minutes of the cron job trigger
- Rahul can review, adjust, and send any draft invoice to a parent in under 3 taps
- Parents opted in to WhatsApp receive the invoice as a PDF via WhatsApp Business API within 2 minutes of Rahul tapping Send
- A UPI payment deep link is generated per invoice and embedded in the WhatsApp message
- UPI payments are auto-reconciled within 60 seconds of gateway callback receipt
- Manual cash / bank transfer / cheque payments can be recorded fully offline and sync on restore
- PDF receipts are generated and delivered via WhatsApp within 60 seconds of payment confirmation
- Automated overdue reminders fire at day 7 and day 14 post-due-date, with per-family disable toggle
- Outstanding balance dashboard loads within 2 seconds on 4G and shows total outstanding, families with overdue balances, and families >30 days overdue
- All stories pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+) and desktop Chrome
- Offline behavior confirmed for all cash payment recording steps
- DPDPA consent check confirmed before any billing record is generated or transmitted

**Out of scope (this epic):**
- Credit card billing — not in scope; UPI, cash, bank transfer, and cheque only
- Insurance billing, reimbursement workflows, or GST invoice generation
- Multi-currency support — INR only
- Parent-facing self-service portal where Meena can view her own invoice history
- Bulk fee structure changes across all children at once
- Automated partial-payment installment plans
- Integration with external accounting software (Tally, Zoho Books) — Phase 2
- WhatsApp Business API setup and DLT registration — infrastructure prerequisite, not a story in this epic (see Pre-Build Decisions)
- In-app UPI payment collection (Meena pays inside the platform) — UPI link opens native payment app externally

**[ASSUMPTION — NOT VALIDATED]** This epic is built on the assumption that Rahul currently spends significant uncompensated time manually tracking fee collection via WhatsApp and Excel, and that this pain is severe enough to drive platform adoption for billing workflows (H-12). No primary research with Indian center directors has confirmed this. Validate before sprint planning.

---

## Story BILLING-001: Fee structure configuration per child

**As a** Rahul (Center Director)
**I want to** configure a billing rule for each enrolled child — choosing between per-session fee, monthly flat fee, or prepaid session package — and save it against their record
**So that** the invoice generation job has a defined fee basis for every child and I never receive a ₹0 or miscalculated invoice because a fee was not configured

**Inspired by:** Jane App billing settings per client; SimplePractice session rate configuration; Theralytics per-client billing mode

**Context:** Rahul performs this action once at enrollment and updates it when terms change (e.g., after a package is purchased or a fee revision). This is a prerequisite for BILLING-002 — if a fee structure does not exist for a child, no invoice can be generated. Action is performed on Android or desktop Chrome. Not accessible to Priya or Dr. Sunita — RBAC-gated to admin role.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director or Admin and opens a child's profile, when he taps or clicks the "Billing" tab, then a fee structure panel is shown with a prompt "No fee structure set. Add one to enable invoice generation." if no structure exists, or the current fee structure if one does
- [ ] AC-02: Given Rahul taps "Add / Edit Fee Structure", then a form opens with three mutually exclusive fee mode options displayed as large, labeled radio chips: "Per Session", "Monthly Flat", "Session Package"
- [ ] AC-03: Given Rahul selects "Per Session", then a required amount field appears with a ₹ prefix and numeric keyboard. Amount must be > ₹0 to enable Save
- [ ] AC-04: Given Rahul selects "Monthly Flat", then a required monthly amount field appears. Amount must be > ₹0 to enable Save
- [ ] AC-05: Given Rahul selects "Session Package", then two required fields appear: "Total sessions in package" (integer, ≥ 1) and "Package price (₹)" (numeric, > ₹0). The system derives cost-per-session for display purposes only; billing deducts one session from the package balance per attended session
- [ ] AC-06: Given any fee mode is selected and Save is tapped, then the fee structure is saved with: fee_mode, amount, effective_date (defaults to today, editable), and recorded_by (current user ID)
- [ ] AC-07: Given Save succeeds, then a fee history entry is appended below the form (read-only accordion): shows previous fee mode, amount, effective date, and set-by name. Past fee structures cannot be edited
- [ ] AC-08: Given Rahul enters ₹0 as the fee amount and taps Save, then a confirmation dialog appears: "You're setting a fee of ₹0 for [Child Name]. Invoices will be generated but will total ₹0. Continue?" — Save proceeds only on explicit confirm
- [ ] AC-09: Given a child's fee structure is set to "Session Package" and the package balance reaches 0 sessions remaining, then the system surfaces a "Package exhausted — no sessions remaining" banner on the child's billing tab and the child appears in a "Fee structure attention required" list on the Billing Dashboard. Invoice generation for that child is blocked until Rahul adds a new package or changes fee mode
- [ ] AC-10: Given Priya or Dr. Sunita navigates to a child's Billing tab, then the fee configuration controls are hidden and a read-only note reads "Billing settings are managed by the center admin." No RBAC error shown — just controlled UI suppression

**Edge Cases & Error States:**
- [ ] EC-01: If POST /children/{id}/fee-structure returns 5xx, the form shows "Couldn't save fee structure — tap to retry." No partial state committed. Previously saved fee structure remains unchanged
- [ ] EC-02: If Rahul attempts to set an effective date that predates an existing fee structure's effective date, show inline warning: "This date overlaps with an existing fee period. The new structure will replace it from [date]. Confirm?"
- [ ] EC-03: If the child record does not yet have confirmed DPDPA parental consent (status != Active), then the Billing tab shows a gate banner: "Parental consent must be confirmed before billing records can be created. Go to child profile to confirm consent." Fee structure form is read-only until gate is passed

**Non-Functional Requirements:**
- Performance: Fee structure save completes within 2 seconds on 4G; form renders within 1.5 seconds on minimum-spec Android
- Offline: Fee structure configuration requires network connectivity. Form is read-only offline with banner: "Offline — fee structure changes require an internet connection."
- Accessibility: Touch targets >= 44px; radio chips clearly labeled with fee mode name and a one-line description; ₹ prefix visible at all times in amount field
- Privacy: Fee structure data is financial data tied to a child record; access restricted to admin role (RBAC); DPDPA consent must be Active before any billing record is written

**Dependencies:**
- Blocked by: AUTH-001 (Rahul authenticated as Center Director / Admin), EMR-001 (child record exists), EMR-002 / INT-003 (DPDPA parental consent Active)
- Enables: BILLING-002 (invoice generation reads fee structure per child)

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android and desktop Chrome
- [ ] EC-01 (server error), EC-02 (date overlap), EC-03 (DPDPA gate) tested
- [ ] RBAC enforcement confirmed: Priya and Dr. Sunita cannot access fee configuration controls
- [ ] Fee history accordion renders correctly after multiple updates
- [ ] Package exhaustion state (AC-09) tested end-to-end
- [ ] Code reviewed and merged

---

## Story BILLING-002: Automated monthly invoice generation from attendance records

**As a** Rahul (Center Director)
**I want to** have the platform automatically generate draft invoices for all active children at the end of each billing cycle, reading confirmed attendance records and applying each child's configured fee structure
**So that** I don't manually count sessions or calculate fees, and I start each month's billing review from an accurate draft rather than a blank page

**Inspired by:** Jane App automated billing from appointment records; Theralytics session-based invoice generation; SimplePractice monthly billing run

**Context:** A server-side cron job triggers at the configured billing cycle end date (default: last day of calendar month; configurable per center). The job reads session records with status = Present for each active child, applies the child's fee structure, and creates a Draft invoice. Cancelled, No-show, and any other non-Present session statuses are excluded. The job is transactional — either all line items for a child's invoice are written or none are (no partial invoice states). Rahul receives an in-app push notification when drafts are ready.

**Acceptance Criteria:**
- [ ] AC-01: Given the billing cycle end date is reached, then the invoice generation cron job (`invoice-generation-job`) fires automatically within 5 minutes of the configured cycle end time
- [ ] AC-02: Given the job runs, then for each active child where: (a) DPDPA parental consent is Active AND (b) a fee structure is configured AND (c) at least one session with status = Present exists in the billing period — a Draft invoice record is created with: invoice_number (system-generated, unique per center per cycle), child_id, billing_period_start, billing_period_end, fee_mode, status = Draft, created_at
- [ ] AC-03: Given fee_mode = Per Session, then the invoice contains one line item per attended session with: session_date, session_type, therapist_name, session_fee. Total = sum of all session fees
- [ ] AC-04: Given fee_mode = Monthly Flat, then the invoice contains a single line item: "Monthly therapy fee — [Month Year]" with the configured flat amount. Total = flat amount regardless of session count
- [ ] AC-05: Given fee_mode = Session Package, then the invoice contains one line item per attended session (same as per-session). Total = sessions_attended × derived_cost_per_session. Package balance is decremented by sessions_attended. If sessions_attended would exceed remaining package balance, the invoice covers only the remaining sessions; Rahul is alerted via in-app notification: "[Child Name]'s package is exhausted mid-cycle — review billing"
- [ ] AC-06: Given a child has no configured fee structure, then no invoice is generated for that child. The child appears in a "No fee structure set" section on the Billing Dashboard with a prompt: "Add a fee structure for [Child Name] to generate their invoice."
- [ ] AC-07: Given a child has no sessions with status = Present in the billing period, then no invoice is generated. The child appears in a "No sessions this period" section on the Billing Dashboard. No action is required
- [ ] AC-08: Given a child's DPDPA parental consent is not Active, then no invoice is generated. The child appears in a "Consent required" section on the Billing Dashboard
- [ ] AC-09: Given the job completes successfully, then Rahul receives an in-app push notification: "X draft invoices are ready for review" with a deep link to the Draft Invoices List screen
- [ ] AC-10: Given the job encounters any error for a specific child, then that child's invoice is rolled back (no partial state committed), and the error is logged server-side. The child appears in an "Invoice generation failed" section on the Billing Dashboard. Rahul can manually re-trigger invoice generation for that child from the dashboard
- [ ] AC-11: Given the job runs, then it is idempotent for the same billing period — re-running the job for a period that already has Draft invoices does not create duplicate invoice records. Existing drafts are preserved unchanged; the re-run skips children with existing Draft invoices for that period
- [ ] AC-12: Given a session's attendance status is disputed (ambiguous — recorded as both Present and Cancelled for the same time slot due to a data conflict), then that session is excluded from the invoice and highlighted in amber on the Draft invoice for Rahul to resolve manually before sending

**Edge Cases & Error States:**
- [ ] EC-01: If the cron job fails to trigger (infrastructure failure), a dead-letter alert is sent to the platform ops team. Rahul sees a "Invoice generation did not run — tap to generate manually" prompt on the Billing Dashboard. Manual trigger via `POST /invoices/generate-batch` is available to Rahul at any time
- [ ] EC-02: If attendance records were retroactively modified after the cron job ran (e.g., Priya corrected a session status), then the existing Draft invoice reflects the state at job execution time. Rahul can manually add or remove line items in BILLING-003 to reconcile
- [ ] EC-03: If a center has more than 200 active children, the job processes children in batches of 50; total job completion target is under 10 minutes. Rahul's notification fires after the full batch completes

**Non-Functional Requirements:**
- Performance: Job must complete for a center with 50 active children within 5 minutes; for 200 children within 10 minutes
- Reliability: Job is idempotent (AC-11); no duplicate invoices; no partial invoice states committed (full transactional rollback per child on failure)
- Offline: Server-side job only; no client-side behavior. Rahul's push notification is delivered when client reconnects if offline at job completion
- Privacy: Invoice generation reads child name and session data — DPDPA parental consent must be Active (AC-08). Invoice records stored with encrypted child identifiers at rest. Access restricted to admin role

**Dependencies:**
- Blocked by: BILLING-001 (fee structure must exist per child), SCHED-004 / Journey 3 (session attendance records with status = Present must exist), INFRA-003 (cron job infrastructure), EMR-002 / INT-003 (DPDPA consent Active)
- Enables: BILLING-003 (Rahul reviews and sends Draft invoices)

**Definition of Done:**
- [ ] All AC pass QA with test center data covering all three fee modes
- [ ] Idempotency (AC-11) tested: run job twice for same period, confirm no duplicates
- [ ] Transactional rollback (AC-10) tested: simulate DB error mid-child, confirm no partial invoice
- [ ] All exclusion states tested: no fee structure (AC-06), no attendance (AC-07), DPDPA not Active (AC-08)
- [ ] Package balance decrement (AC-05) tested including mid-cycle exhaustion
- [ ] Push notification delivery confirmed on minimum-spec Android
- [ ] Code reviewed and merged

---

## Story BILLING-003: Invoice review and send

**As a** Rahul (Center Director)
**I want to** open any draft invoice, review its line items, make adjustments (add a discount, remove a disputed session, add a miscellaneous charge), and send it to the parent in one tap
**So that** I verify the invoice is accurate before it reaches the family, and the parent receives it immediately without me composing a separate WhatsApp message

**Inspired by:** Jane App invoice detail and send; SimplePractice invoice editing and delivery; Theralytics billing review flow

**Context:** Rahul accesses this from the Draft Invoices List or from the Billing Dashboard. He may be on Android or on desktop Chrome. The Send action transitions the invoice from Draft to Sent and triggers WhatsApp / SMS delivery (BILLING-007 for the delivery mechanics). No partial send state — if Send fails, invoice remains Draft.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Draft Invoices List, then he sees all invoices with status = Draft for the current billing cycle, each showing: child name, parent name, billing period, total amount, fee mode, and a "Review" CTA
- [ ] AC-02: Given Rahul taps a draft invoice, then the Invoice Detail Screen loads within 1.5 seconds on minimum-spec Android, showing: invoice number, child name, parent name, billing period, line items list, total (pinned to bottom of screen, always visible), and invoice due date (default 7 days from today, editable)
- [ ] AC-03: Given the invoice is open, then each line item row shows: date, session type, therapist name (per-session mode) or description (flat / package), and amount. Swipe-left on a line item reveals a "Remove" action
- [ ] AC-04: Given Rahul swipes left on a line item and taps "Remove", then a confirmation prompt appears: "Remove this session from the invoice? The session will remain in attendance records." On confirm, the line item is removed and the total recalculates immediately in real-time on device
- [ ] AC-05: Given Rahul taps "Add Discount", then a modal opens with two fields: discount amount (₹, required) and reason (free text, optional). On save, a discount line item is appended with a negative value. Total recalculates immediately
- [ ] AC-06: Given Rahul taps "Add Line Item", then a modal opens with two fields: description (text, required, max 100 chars) and amount (₹, required, > ₹0). On save, the line item is appended. Total recalculates immediately. This is the mechanism for adding miscellaneous charges (e.g., materials, assessment fee)
- [ ] AC-07: Given any line item is flagged as ambiguous (amber highlight — session with disputed attendance status per BILLING-002 AC-12), then the "Send" button is disabled and a banner reads: "Review the highlighted session(s) before sending. Remove them or confirm they are correct." Rahul can either remove the amber line item (AC-04) or tap "Confirm — include this session" to clear the flag. "Send" becomes enabled only when no amber flags remain
- [ ] AC-08: Given Rahul taps "Send" with no amber flags and a total > ₹0, then a confirmation dialog appears: "Send invoice of ₹[amount] to [Parent Name] for [Child Name]?" with "Send" and "Cancel" buttons
- [ ] AC-09: Given Rahul confirms Send, then: (a) invoice status transitions Draft → Sent, (b) invoice due date is written, (c) the send action is logged with sent_by and sent_at, and (d) WhatsApp / SMS delivery is triggered (see BILLING-004 and BILLING-007). Rahul is returned to the Draft Invoices List with a success toast: "Invoice sent to [Parent Name]"
- [ ] AC-10: Given invoice total = ₹0 (all sessions removed or ₹0 fee structure), then the Send button is replaced with a "Mark as Sent (₹0 invoice)" action that transitions status to Sent without triggering payment link generation
- [ ] AC-11: Given Rahul taps Send and the API call fails, then invoice status remains Draft, an error message appears: "Couldn't send invoice — check your connection and try again." No partial state is committed

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul navigates away from the Invoice Detail Screen after making adjustments but before sending, a confirmation dialog appears: "You have unsaved adjustments. Discard changes?" Adjustments are not auto-saved — only Send commits them
- [ ] EC-02: If a parent's WhatsApp opt-in status is not Active (not opted in), the Send flow completes (invoice transitions to Sent) but the automated WhatsApp delivery does not fire. Rahul sees: "Invoice sent — WhatsApp delivery unavailable. Share manually." A "Share manually" button opens a pre-filled WhatsApp share intent on his device with the invoice PDF attached, sending from his personal number. This is the DPDPA-compliant fallback
- [ ] EC-03: If the parent's mobile number is missing from their record, the Send button shows a warning: "No mobile number on record for this parent — add it in their profile before sending"

**Non-Functional Requirements:**
- Performance: Invoice detail loads <= 1.5s on minimum-spec Android; total recalculates in real-time (<200ms) as line items are added or removed
- Offline: Invoice Detail Screen is readable from cache offline. All write actions (remove line item, add discount, add line item, Send) require connectivity. Offline state shows banner: "Offline — changes and sending require an internet connection."
- Accessibility: Total amount is pinned and always visible without scrolling; touch targets >= 44px; swipe-to-remove has a minimum swipe distance to prevent accidental deletion; destructive actions (remove line item) require confirmation
- Privacy: Invoice detail contains child name and financial data; RBAC restricted to admin role; invoice PDF stored encrypted at rest

**Dependencies:**
- Blocked by: BILLING-002 (draft invoices must exist), BILLING-004 (UPI payment link generation triggered by Send), INFRA-004 (WABA / SMS delivery infrastructure)
- Enables: BILLING-004 (payment link generated on Send), BILLING-008 (overdue reminder clock starts at due date set during Send)

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android and desktop Chrome
- [ ] EC-01 (unsaved changes navigation), EC-02 (WhatsApp opt-out fallback), EC-03 (missing mobile) tested
- [ ] Amber flag gate (AC-07) tested: Send blocked until flags resolved
- [ ] Real-time total recalculation tested with add, remove, and discount operations
- [ ] Invoice status transition Draft → Sent confirmed in DB after Send
- [ ] Code reviewed and merged

---

## Story BILLING-004: UPI payment link generation and delivery

**As a** Rahul (Center Director)
**I want to** have a UPI payment deep link automatically generated for each invoice and embedded in the WhatsApp message sent to the parent
**So that** Meena can tap one link to pay directly via GPay, PhonePe, Paytm, or any UPI app without Rahul manually creating or sharing a payment link each time

**Inspired by:** Razorpay payment link for Indian SMBs; Jane App online payment integration; SimplePractice client-portal payment. UPI deep links (`upi://pay?`) are table stakes for any Indian billing tool targeting small businesses and parent payers.

**Context:** UPI payment link generation is triggered server-side when Rahul confirms Send on an invoice (BILLING-003 AC-09). The platform integrates with a third-party Indian UPI payment aggregator (Razorpay, PayU, or equivalent — see Pre-Build Decisions). The platform does not process payments directly. One active payment link is maintained per invoice at a time (idempotency). The link is embedded in the WhatsApp invoice message.

**Acceptance Criteria:**
- [ ] AC-01: Given an invoice transitions from Draft to Sent (BILLING-003), then the platform calls the UPI aggregator API to generate a payment request for the invoice total, and receives back: a UPI deep link in `upi://pay?pa=[VPA]&pn=[center_name]&am=[amount]&cu=INR&tn=[invoice_number]` format and a short URL redirect (for sharing in text)
- [ ] AC-02: Given the payment link is generated, then a payment_request record is written: invoice_id, upi_link, short_url, status = Pending, expiry (default: 48 hours from generation, configurable in Billing Settings), created_at
- [ ] AC-03: Given a payment_request record already exists for an invoice with status = Pending and expiry in the future, then calling the link generation API again returns the existing link — a new link is NOT created. This is the idempotency rule: one active payment link per invoice at a time
- [ ] AC-04: Given the existing payment link has expired (status = Expired or current time > expiry), then Rahul can generate a new link from the Invoice Detail Screen via "Regenerate Payment Link." The old link is voided at the UPI aggregator level and a new record is created
- [ ] AC-05: Given the payment link is generated, then it is embedded in the WhatsApp invoice message via WABA approved template (see BILLING-003 AC-09 and BILLING-007 for delivery mechanics). The message contains: parent name, child name, billing month, total amount in ₹, the short URL, and center name
- [ ] AC-06: Given the parent is NOT opted in to WhatsApp WABA, then the short URL is available to Rahul via "Copy link" on the Invoice Detail Screen and via the "Share manually" WhatsApp intent fallback (BILLING-003 EC-02)
- [ ] AC-07: Given Rahul views the Invoice Detail Screen for a Sent invoice, then a "Payment Link" section shows: link status (Pending / Paid / Expired / Failed), expiry countdown (if Pending), and "Regenerate" action (if Expired or Failed)
- [ ] AC-08: Given the UPI aggregator API call fails during invoice Send, then: (a) the invoice is still transitioned to Sent (the invoice send is not rolled back due to payment link failure), (b) the payment link section on Invoice Detail shows "Payment link generation failed — tap to retry", (c) the WhatsApp message is sent without a payment link, and (d) Rahul is shown an in-app alert: "Payment link could not be generated for [Child Name]'s invoice. Tap to retry."
- [ ] AC-09: Given the center's UPI VPA (Virtual Payment Address) is not configured in Billing Settings, then the "Send" button in BILLING-003 is disabled with tooltip: "Configure your UPI VPA in Billing Settings before sending invoices with payment links." Rahul is prompted to complete setup

**Edge Cases & Error States:**
- [ ] EC-01: If the invoice amount is ₹0, no payment link is generated. The invoice is sent without a payment link
- [ ] EC-02: If the UPI aggregator returns a payment_request_id that already exists in the platform's records (duplicate request), the existing record is returned and no new record is written
- [ ] EC-03: If Meena taps the payment link on a device with no UPI app installed, she lands on the short URL which shows a fallback page with UPI app download guidance — this page is rendered by the UPI aggregator, not the platform

**Non-Functional Requirements:**
- Performance: Payment link generation completes within 3 seconds of invoice Send confirmation; if longer, a "Generating payment link..." spinner is shown inline and the Send confirmation toast shows "Invoice sent — payment link generating"
- Security: UPI VPA and aggregator API credentials stored as encrypted environment variables; never exposed in client-side code or WhatsApp message body beyond the `pa=` parameter in the deep link
- Idempotency: One active payment link per invoice at a time (AC-03). Duplicate link creation must be blocked at both application and aggregator API level
- Privacy: Payment link URL contains invoice reference only — not child name or clinical data in URL parameters. DPDPA: payment data stored encrypted, admin access only

**Dependencies:**
- Blocked by: BILLING-003 (invoice Send triggers link generation), INFRA-005 (UPI aggregator account, API credentials, and center UPI VPA configured), BILLING-001 (center UPI VPA configured in Billing Settings)
- Enables: BILLING-005 (webhook reconciliation matches payment to this payment_request record), BILLING-008 (overdue reminders can regenerate or re-share the payment link)

**Definition of Done:**
- [ ] All AC pass QA using UPI aggregator sandbox environment
- [ ] Idempotency (AC-03) tested: call generate twice for same invoice, confirm single record
- [ ] Expired link regeneration (AC-04) tested
- [ ] UPI aggregator failure during Send (AC-08) tested: invoice transitions to Sent, alert shown, manual retry available
- [ ] UPI VPA not configured gate (AC-09) tested
- [ ] EC-01 (₹0 invoice) tested
- [ ] Code reviewed and merged

---

## Story BILLING-005: UPI payment webhook reconciliation

**As a** System
**I want to** receive the UPI gateway payment confirmation callback, automatically match it to the correct invoice, transition the invoice to Paid, and trigger receipt generation — all within 60 seconds of the gateway callback
**So that** Rahul's outstanding dashboard reflects accurate, real-time payment status without any manual reconciliation step

**Inspired by:** Razorpay webhook reconciliation (India-standard); Jane App online payment auto-reconciliation; SimplePractice payment sync

**Context:** The UPI aggregator sends an HTTP POST callback to the platform's webhook endpoint when a payment transaction completes (success, failure, or pending). The platform must process this callback idempotently — the same callback may be delivered multiple times by the aggregator (at-least-once delivery). Duplicate callbacks are suppressed by transaction reference ID. The reconciliation job also handles delayed payment status (re-query at 5 and 30 minutes if callback is not received).

**Acceptance Criteria:**
- [ ] AC-01: Given the UPI aggregator sends a success callback to `POST /webhooks/upi-callback`, then the platform: (a) validates the callback signature using the aggregator's shared secret, (b) extracts: transaction_reference_id, payment_request_id, amount, status, timestamp, (c) matches payment_request_id to an existing invoice payment_request record, and (d) writes a payment record: invoice_id, amount, method = UPI, upi_reference_id, paid_at, recorded_by = System
- [ ] AC-02: Given the payment record is written, then: (a) invoice status transitions Sent → Paid, (b) outstanding balance for the child is reduced by the paid amount, (c) if amount < invoice total, invoice status transitions to Partially Paid instead of Paid, and remaining_balance is calculated and stored
- [ ] AC-03: Given invoice status transitions to Paid or Partially Paid, then receipt generation is triggered within 60 seconds (see BILLING-007)
- [ ] AC-04: Given the callback contains a transaction_reference_id that already exists in the platform's payment records, then the callback is silently discarded (idempotency — duplicate suppression by transaction reference ID). No duplicate payment record is written. HTTP 200 is returned to the aggregator to prevent retry storm
- [ ] AC-05: Given the callback signature validation fails (tampered or malformed request), then the request is rejected with HTTP 400 and the event is logged to the security audit log. No payment record is written
- [ ] AC-06: Given a payment callback is not received within 5 minutes of the payment link being tapped (platform infers this from UPI app redirect event, if available), then the platform re-queries the payment status from the UPI aggregator at 5 minutes and again at 30 minutes
- [ ] AC-07: Given the payment status is still unconfirmed after 2 hours, then the payment_request status is set to "Status Unknown". Rahul receives an in-app alert: "Payment for [Child Name]'s invoice could not be confirmed automatically. Verify with your bank and record manually if received." Invoice status remains Sent (not assumed Paid)
- [ ] AC-08: Given the callback indicates a failed payment (insufficient funds, payment cancelled, timeout), then: (a) payment_request status → Failed, (b) invoice status remains Sent, (c) Rahul sees "Payment failed" on the Invoice Detail Screen with timestamp, and (d) Rahul can regenerate a new payment link (BILLING-004 AC-04)
- [ ] AC-09: Given Rahul views his Billing Dashboard after a successful UPI reconciliation, then the outstanding balance for the relevant child has decreased and a push notification is received: "Payment received: ₹[amount] from [Parent Name] for [Child Name]"

**Edge Cases & Error States:**
- [ ] EC-01: If the matched invoice is already in Paid status when the callback arrives (e.g., Rahul already recorded a manual payment), then the callback is logged as a duplicate payment event and Rahul is alerted: "A payment callback was received for [Child Name]'s invoice which is already marked Paid. Review the payment history." No second payment record is created
- [ ] EC-02: If the payment amount in the callback exceeds the invoice total (overpayment), the platform records the actual amount received and flags the invoice with an "Overpayment — ₹[X] received, ₹[Y] invoiced" note for Rahul's review
- [ ] EC-03: If the payment_request_id in the callback does not match any existing record, the event is logged to the ops error log and an alert is sent to the platform ops team. HTTP 200 is returned to prevent aggregator retry

**Non-Functional Requirements:**
- Performance: Webhook processing (signature validation + DB write + receipt trigger) must complete within 10 seconds of callback receipt. Receipt PDF generation target: within 60 seconds of payment confirmation
- Reliability: Webhook endpoint must be idempotent (AC-04). Callback processing must survive DB write failures with at-least-once delivery guarantee from the aggregator — use a processing queue with retry logic
- Security: Webhook signature validation is mandatory (AC-05); shared secret stored as encrypted environment variable; webhook endpoint accessible only via HTTPS; IP allowlist for UPI aggregator IPs where supported
- Privacy: UPI reference ID and payment amount stored encrypted against child record; DPDPA: financial data of a minor; access restricted to admin role

**Dependencies:**
- Blocked by: BILLING-004 (payment_request record must exist to match against), INFRA-005 (UPI aggregator webhook configuration — platform webhook URL registered with aggregator), INFRA-006 (webhook processing queue infrastructure)
- Enables: BILLING-007 (receipt generation triggered by payment confirmation), BILLING-009 (outstanding dashboard balance reduction)

**Definition of Done:**
- [ ] All AC pass QA using UPI aggregator sandbox webhook simulation
- [ ] Idempotency (AC-04) tested: send same callback twice, confirm single payment record
- [ ] Signature validation failure (AC-05) tested: confirm 400 and no payment record
- [ ] Delayed callback flow (AC-06 and AC-07) tested with mocked aggregator re-query
- [ ] Failed payment callback (AC-08) tested
- [ ] Partial payment (AC-02 Partially Paid state) tested
- [ ] Code reviewed and merged

---

## Story BILLING-006: Manual payment recording — cash, bank transfer, cheque

**As a** Rahul (Center Director)
**I want to** record a cash, bank transfer, or cheque payment against a specific invoice directly on my phone — even when I have no internet connection
**So that** offline payments are captured immediately in the system and the outstanding balance is accurate, without waiting for me to have connectivity

**Inspired by:** Jane App offline payment recording; SimplePractice manual payment entry; Theralytics payment logging. Cash payment at reception is the dominant payment mode for many Indian therapy centers — this story is not a fallback, it is a primary path.

**Context:** Rahul is at the reception or in his office when a parent pays cash or hands over a cheque. He opens the Record Payment form from the Invoice Detail Screen or from a quick-action on the Outstanding Dashboard. The write must succeed offline — it is written to device-local storage first and synced when connectivity is restored. The form triggers the same receipt generation flow as UPI payment (BILLING-007).

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul taps "Record Payment" from the Invoice Detail Screen or Outstanding Dashboard quick-action for any invoice with status = Sent or Partially Paid, then the Record Payment form opens within 1 second on minimum-spec Android, pre-filled with the outstanding balance as the amount
- [ ] AC-02: Given the Record Payment form is open, then the following fields are shown: Amount (₹, numeric, required, pre-filled with outstanding balance, editable), Payment method (required dropdown: Cash / Bank Transfer / Cheque), Payment date (required, defaults to today, editable — Rahul may backdate by up to 90 days), Reference / notes (optional free text, max 200 chars — for bank reference numbers, cheque numbers)
- [ ] AC-03: Given Rahul fills the form and taps "Save", then: (a) a payment record is written locally immediately with: invoice_id, amount, method, payment_date, notes, recorded_by, recorded_at, sync_status = Pending, (b) the invoice's displayed outstanding balance is updated optimistically on-device, (c) if connected: the record syncs to the server immediately and sync_status → Synced, (d) if offline: a banner shows "Saved offline — will sync when connected" and the record queues for background sync
- [ ] AC-04: Given Rahul is offline and saves a payment record, then when connectivity is restored, the queued payment record is synced to the server automatically in the background without requiring Rahul to take any action. On successful sync: (a) invoice status is updated server-side (Sent → Paid or Partially Paid), (b) receipt generation is triggered (BILLING-007), (c) the local record's sync_status → Synced
- [ ] AC-05: Given the saved amount equals the invoice total (or remaining balance for a partial payment), then invoice status transitions to Paid on sync. Given the saved amount is less than the remaining balance, then invoice status transitions to Partially Paid and remaining_balance is updated
- [ ] AC-06: Given the saved amount exceeds the outstanding balance, then before saving a warning dialog appears: "This amount (₹[X]) is more than the outstanding balance (₹[Y]). Record ₹[X] as a credit? Or adjust the amount?" — two actions: "Record with credit" or "Edit amount". If "Record with credit" is selected, the overpayment is stored as a credit note against the family's billing profile
- [ ] AC-07: Given Rahul taps "Save" with amount field empty or ₹0, then inline validation error appears on the amount field: "Enter a payment amount greater than ₹0." Form does not submit
- [ ] AC-08: Given Rahul opens the Record Payment form while offline, then a banner reads "Offline — payment will be saved locally and synced when connected." All form fields remain fully operable

**Edge Cases & Error States:**
- [ ] EC-01: If the server sync fails after connectivity is restored (5xx from `POST /payments/manual`), then the payment record remains in local queue with sync_status = Sync Failed. Rahul sees a "Sync failed" indicator on the invoice in his dashboard. A "Retry sync" action is available. The local balance update remains visible to Rahul on device
- [ ] EC-02: If a sync conflict is detected (e.g., Rahul recorded cash offline and a UPI payment also came in via webhook for the same invoice while offline), then on sync the platform detects a Paid invoice with a pending manual payment record. The conflict is surfaced to Rahul: "This invoice was already marked Paid via UPI. Review the duplicate payment." No duplicate payment record is created silently
- [ ] EC-03: If Rahul closes the app mid-form before saving, the partially entered form is discarded. No draft local save for the Record Payment form (unlike INQ-001 which uses draft-on-input). Rationale: payment forms should require explicit Save intent to prevent ghost records

**Non-Functional Requirements:**
- Performance: Form opens <= 1 second on minimum-spec Android; local write completes <= 500ms; optimistic balance update appears immediately on Save
- Offline: Full offline write capability is a hard requirement (AC-03). Record queued in device-local storage (SQLite or equivalent); persists across app close and reopen; syncs automatically on connectivity restore
- Accessibility: Touch targets >= 44px; amount field opens numeric keyboard automatically; payment method dropdown navigable without scroll on 360dp screen; date picker uses native Android date picker
- Privacy: Payment record is financial data tied to a child record; RBAC: admin role only; DPDPA: financial data of a minor; encrypted at rest after sync

**Dependencies:**
- Blocked by: BILLING-002 or BILLING-003 (invoice must exist and be in Sent or Partially Paid status), INFRA-007 (local-first offline storage / sync infrastructure)
- Enables: BILLING-007 (receipt generation triggered on payment sync), BILLING-009 (outstanding balance reduced after sync)

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] Full offline write flow tested: save offline, close app, reopen, restore connectivity, confirm sync and receipt generation
- [ ] EC-01 (sync failure) tested: payment stuck in local queue, retry available
- [ ] EC-02 (sync conflict with UPI payment) tested
- [ ] Overpayment warning (AC-06) tested
- [ ] Partial payment (AC-05 Partially Paid state) tested
- [ ] RBAC enforcement confirmed: Priya cannot access Record Payment form
- [ ] Code reviewed and merged

---

## Story BILLING-007: Automated payment receipt generation and WhatsApp delivery

**As a** System (on behalf of Rahul and Meena)
**I want to** automatically generate a PDF receipt within 60 seconds of any payment confirmation (UPI webhook or manual payment sync), deliver it to the parent via WhatsApp Business API, and store it on the platform regardless of WhatsApp delivery outcome
**So that** Meena receives proof of payment immediately without Rahul having to manually compose or forward a receipt, and Rahul has an auditable receipt record even if WhatsApp delivery fails

**Inspired by:** Razorpay automated receipt delivery; Jane App payment confirmation email; SimplePractice receipt generation. In India, digital receipt delivery via WhatsApp is now expected behavior for any payment in the informal private health sector.

**Context:** Receipt generation is triggered by two events: (1) successful UPI webhook reconciliation (BILLING-005 AC-03) and (2) successful manual payment sync to server (BILLING-006 AC-04). The trigger is the same in both cases — a confirmed payment record on the server. The receipt PDF is generated server-side, stored on the platform, and then queued for WhatsApp delivery. Delivery failure does not affect receipt storage.

**Acceptance Criteria:**
- [ ] AC-01: Given a payment record is confirmed on the server (via BILLING-005 or BILLING-006), then a receipt generation job triggers within 5 seconds and a receipt PDF is generated within 60 seconds containing: unique receipt number (format: RCT-[center_code]-[YYYYMM]-[sequential]), center name and address, child's first name only (not full name or diagnosis), parent name, payment amount (₹), payment method (UPI / Cash / Bank Transfer / Cheque), payment date, billing period covered, and invoice number reference
- [ ] AC-02: Given the receipt PDF is generated, then it is stored on the platform's encrypted file storage (server-side) regardless of WhatsApp delivery outcome. The receipt record is permanently associated with the invoice
- [ ] AC-03: Given the parent's WhatsApp opt-in status is Active and WABA is connected, then the receipt PDF is delivered via WABA using an approved "Payment Receipt" template within 60 seconds of receipt generation. The message reads: "Receipt #[number] — ₹[amount] received for [Child First Name]'s therapy session for [Month Year]. Thank you. — [Center Name]" with the PDF attached
- [ ] AC-04: Given the WhatsApp delivery attempt completes, then the delivery status (Sent / Delivered / Read / Failed) is logged against the receipt record. Rahul can see the delivery status badge on the Invoice Detail Screen and Payment History tab
- [ ] AC-05: Given WhatsApp delivery fails (WABA error, rate limit, or parent number unreachable), then: (a) the receipt PDF remains stored on the platform (AC-02 is unaffected), (b) Rahul sees a "Receipt delivery failed" alert on the Invoice Detail Screen, (c) a "Resend receipt" action is available to Rahul to retry WhatsApp delivery or use the manual share intent fallback
- [ ] AC-06: Given the parent is NOT opted in to WhatsApp WABA, then: (a) receipt is still generated and stored (AC-02), (b) automated WhatsApp delivery is not attempted, (c) Rahul sees "Receipt ready — share with parent" on the Invoice Detail Screen, (d) a "Share receipt" button opens a pre-filled WhatsApp share intent on Rahul's device with the receipt PDF, sending from his personal number. This is the DPDPA-compliant manual fallback
- [ ] AC-07: Given the receipt is generated, then Rahul receives an in-app push notification: "Receipt sent to [Parent Name] for ₹[amount] — [Child Name]" (if WABA delivery attempted) or "Receipt ready for [Child Name] — share with parent" (if manual fallback applies)
- [ ] AC-08: Given Rahul views the Invoice Detail Screen for any Paid invoice, then a "Receipts" section shows: receipt number, generated date, amount, delivery status badge (Sent via WhatsApp / Manually shared / Delivery failed), and a "View receipt" action that opens the stored PDF

**Edge Cases & Error States:**
- [ ] EC-01: If receipt generation fails (PDF generation job error), the failure is logged to the ops error queue and Rahul is alerted: "Receipt could not be generated for [Child Name]'s payment. Contact support." The payment record is not rolled back — payment is recorded regardless of receipt generation outcome
- [ ] EC-02: If the same payment triggers receipt generation twice (e.g., a duplicate webhook and a manual entry for the same invoice within the same session), the receipt generation job checks: if a receipt already exists for this invoice_id and payment_date, it returns the existing receipt and does not generate a second one (idempotency)
- [ ] EC-03: The receipt PDF must not contain the child's diagnosis, disability status, therapy targets, or any clinical information — financial data only. This is both a DPDPA constraint and a business rule (receipts are general tax/payment documents, not clinical records)

**Non-Functional Requirements:**
- Performance: Receipt generation within 60 seconds of payment confirmation (AC-01); WhatsApp delivery queued immediately after PDF is ready
- Reliability: Receipt generation is idempotent per invoice (EC-02); receipt storage is independent of WhatsApp delivery outcome (AC-02)
- Privacy: Receipt PDF contains child first name and financial data only — no clinical data (EC-03). PDF stored encrypted at rest. WABA delivery is the only compliant automated channel for sharing PDFs containing child PII. Personal WhatsApp sharing (manual fallback) is permitted as Rahul controls his own device. DPDPA: financial record of a minor; audit log of all access and delivery events maintained
- Offline: Receipt generation and WhatsApp delivery are server-side only. Rahul's in-app notification arrives when client reconnects

**Dependencies:**
- Blocked by: BILLING-005 (UPI payment confirmation triggers this) or BILLING-006 (manual payment confirmation triggers this), INFRA-004 (WABA connection for automated delivery), INFRA-008 (PDF generation service)
- Enables: BILLING-009 (invoice moves to Paid on dashboard; receipt delivery status visible)

**Definition of Done:**
- [ ] All AC pass QA including receipt PDF content review (EC-03: no clinical data)
- [ ] Receipt stored on server confirmed independent of WhatsApp delivery (AC-02) — simulate delivery failure, confirm receipt retrievable
- [ ] WABA opt-out fallback (AC-06) tested end-to-end
- [ ] Delivery status badges tested: Sent / Delivered / Failed states
- [ ] Idempotency (EC-02) tested: trigger twice for same invoice, confirm single receipt
- [ ] Receipt "View" action tested — PDF opens correctly on minimum-spec Android
- [ ] Code reviewed and merged

---

## Story BILLING-008: Overdue invoice reminders

**As a** Rahul (Center Director)
**I want to** have the system automatically send a soft payment reminder to parents whose invoices are 7 days overdue and again at 14 days overdue, with a per-family toggle to disable reminders and the ability for me to manually trigger a reminder from the outstanding dashboard at any time
**So that** overdue collection happens systematically without me having to remember which families to chase, and I can still exercise judgment to suppress reminders for families in sensitive situations

**Inspired by:** Jane App overdue reminder automation; SimplePractice payment reminders; Theralytics overdue alerting. Relationship-sensitivity is a documented constraint in Indian small-practice billing — reminder tone must be soft and non-confrontational by default.

**Context:** A daily cron job (`overdue-reminder-job`) runs at a configurable time (default: 9:00am IST) and checks all invoices where: status = Sent (not Paid), current_date > due_date. For each qualifying invoice it checks: days overdue threshold, per-family reminder disable flag, and last reminder sent timestamp (to avoid double-sending). Messages are sent via WABA approved template (preferred) or DLT-registered SMS (fallback). Rahul can also manually trigger a reminder from BILLING-009 at any time.

**Acceptance Criteria:**
- [ ] AC-01: Given an invoice with status = Sent and current_date = due_date + 7 days, then the overdue reminder job sends a reminder message to the parent via WABA (if opted in) or DLT SMS (if opted in to SMS). The message uses the approved "Fee Reminder Day 7" template. A reminder log entry is written: invoice_id, reminder_type = Day7, channel, sent_at, delivery_status
- [ ] AC-02: Given an invoice with status = Sent and current_date = due_date + 14 days AND a Day 7 reminder was already sent, then a second reminder message is sent using the "Fee Reminder Day 14" template. Rahul receives an in-app alert: "[Parent Name]'s invoice for [Child Name] is 14 days overdue."
- [ ] AC-03: Given the reminder job checks an invoice before sending, then it confirms invoice status = Sent (not Paid or Partially Paid). If the invoice was paid between the last job run and now, no reminder is sent. A status check immediately before dispatch is mandatory
- [ ] AC-04: Given a family has the per-family reminder disable toggle set to true (managed from BILLING-009 or the family's billing profile), then no automated reminders are sent for any of that family's invoices. The job logs each suppressed reminder as: invoice_id, status = Suppressed — reminders disabled for this family. The suppression is silent to the parent (no message is sent)
- [ ] AC-05: Given Rahul taps "Send Reminder" on any invoice row on the Outstanding Balance Dashboard (BILLING-009), then a manual reminder is dispatched immediately regardless of the automated reminder schedule. The same WABA / SMS template is used. A reminder log entry is written with reminder_type = Manual. Manual trigger is not blocked by per-family disable toggle — Rahul is the override
- [ ] AC-06: Given Rahul navigates to Settings > Reminders, then he can: (a) edit the "Fee Reminder Day 7" message template text within the approved WABA template variable slots (e.g., edit the greeting and closing line; cannot modify fixed template fields required by Meta/DLT), (b) edit the "Fee Reminder Day 14" template text within the same constraints, (c) enable or disable automated reminders globally for the center (does not affect manual send in AC-05)
- [ ] AC-07: Given the default "Fee Reminder Day 7" template, then the message text must: use a soft, non-confrontational opening (default: "Dear [Parent Name], we hope [Child First Name] is doing well."), state the outstanding amount clearly, include the payment link (short URL from BILLING-004), and end with a warm closing (default: "Thank you for your continued support. — [Center Name]"). The template text must be reviewed and DLT/WABA-registered before activation
- [ ] AC-08: Given neither WABA nor DLT SMS is configured for the center, then the overdue reminder job cannot send automated messages. The job runs but all reminder entries are logged as: status = Cannot send — no messaging channel configured. Rahul sees a center-level warning on the Billing Dashboard: "Automated reminders are not active. Configure WhatsApp or SMS in Settings to enable."

**Edge Cases & Error States:**
- [ ] EC-01: If the payment link associated with the invoice has expired by the time the Day 7 or Day 14 reminder fires, then a new payment link is generated (BILLING-004 AC-04) before the reminder is sent. The new link is included in the reminder message
- [ ] EC-02: If the reminder job fires but WABA delivery fails and SMS fallback also fails, the reminder log entry shows status = Delivery Failed. Rahul sees a "Reminder delivery failed" flag on the invoice row in BILLING-009. Manual retry is available (AC-05)
- [ ] EC-03: If an invoice is in Partially Paid status, overdue reminders still fire for the remaining balance. The reminder message states the remaining amount (not the original invoice total): "Outstanding balance: ₹[remaining_balance]"
- [ ] EC-04: If a family's per-family reminder disable toggle is off but the parent has revoked WhatsApp opt-in since the invoice was sent, then the WABA send is not attempted; reminder falls back to SMS if configured; if no fallback, reminder is logged as Suppressed — opt-out

**Non-Functional Requirements:**
- Performance: Overdue reminder job must process all invoices for a center (up to 200) within 5 minutes of trigger time
- Reliability: Job is idempotent for a given invoice and threshold — re-running the job does not send duplicate reminders for the same day-overdue threshold. Duplicate suppression by invoice_id + reminder_type
- Regulatory: WABA templates must be approved by Meta before activation. SMS templates must be DLT-registered with a valid sender ID before activation. Template text review required (see Pre-Build Decisions). TRAI DLT compliance is mandatory for transactional SMS in India
- Privacy: Reminder message contains child first name and outstanding amount — no clinical data. DPDPA: reminder is a financial communication; parent WhatsApp opt-in is the consent mechanism for WABA channel

**Dependencies:**
- Blocked by: BILLING-003 (invoices must be in Sent status with a due date), BILLING-004 (payment link for embedding in reminder), INFRA-003 (cron job infrastructure), INFRA-004 (WABA connection), INFRA-009 (DLT SMS provider)
- Enables: BILLING-009 (outstanding dashboard shows reminder delivery status per invoice row)

**Definition of Done:**
- [ ] All AC pass QA using test invoices with mocked overdue dates
- [ ] Day 7 and Day 14 reminder triggers tested independently
- [ ] Per-family disable toggle (AC-04) tested: confirm no message sent, suppression logged
- [ ] Manual send from dashboard (AC-05) tested: fires immediately, logs correctly
- [ ] Pre-send status check (AC-03) tested: pay invoice between job runs, confirm no reminder sent
- [ ] EC-01 (expired payment link regeneration before send) tested
- [ ] EC-03 (Partially Paid remainder amount) tested
- [ ] DLT sender ID and WABA template approval confirmed before production activation (see Pre-Build Decisions)
- [ ] Code reviewed and merged

---

## Story BILLING-009: Outstanding balance dashboard

**As a** Rahul (Center Director)
**I want to** see a single dashboard view of all families with outstanding invoice balances — total receivables at the top, a sortable list of families by days overdue, and quick actions to send a reminder or record a payment from each row — accessible on both Android and desktop Chrome
**So that** I can see my entire billing exposure at a glance and take action on overdue accounts without opening each invoice individually

**Inspired by:** SimplePractice outstanding balances view; Jane App billing overview; Theralytics payment dashboard. No Indian competitor has this feature — this is a direct gap vs. the Excel-conditional-formatting workaround currently used.

**Context:** This is Rahul's primary billing home screen. It is the default view when he opens the Billing section if any outstanding balances exist. It is read-write — quick actions from this screen trigger BILLING-008 (send reminder) and BILLING-006 (record payment). Data is server-computed; client caches the last response and shows staleness banner when offline.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Billing section, then the Outstanding Balance Dashboard loads as the default sub-tab within 2 seconds on 4G on both minimum-spec Android and desktop Chrome
- [ ] AC-02: Given the dashboard loads, then a pinned non-tappable summary banner at the top shows: (a) total outstanding across all families (₹X), (b) number of families with any outstanding balance (N families), (c) number of families with any balance >30 days overdue (N families >30 days). All three figures update in real-time after any payment is confirmed
- [ ] AC-03: Given the dashboard list is rendered, then each row shows: child name, parent name, invoice amount (total invoiced for current cycle), outstanding amount (remaining), invoice due date, days overdue label (calculated: "X days overdue" or "Due in X days"), and two quick-action buttons: "Send Reminder" and "Record Payment" (touch targets >= 44px each)
- [ ] AC-04: Given the days overdue label is displayed, then: invoices not yet due show "Due in X days" (no color flag); invoices 1–29 days overdue show "X days overdue" in amber with an amber dot indicator; invoices 30+ days overdue show "X days overdue" in a visually distinct style with a red dot indicator. Color is never the only indicator — the text label is always present
- [ ] AC-05: Given Rahul taps the sort control, then the list can be sorted by: Days Overdue descending (default), Days Overdue ascending, Outstanding Amount descending, Child name A–Z. The selected sort persists for the session
- [ ] AC-06: Given Rahul taps "Send Reminder" on any row, then a confirmation dialog appears: "Send a payment reminder to [Parent Name] for [Child Name]'s outstanding balance of ₹[amount]?" On confirm, a manual reminder is dispatched (BILLING-008 AC-05) and a success toast appears: "Reminder sent to [Parent Name]". The per-family reminder disable toggle is respected — if reminders are disabled for this family, Rahul sees: "Reminders are disabled for this family. Enable them in billing settings to send a reminder."
- [ ] AC-07: Given Rahul taps "Record Payment" on any row, then the Record Payment form (BILLING-006) opens pre-populated with the child's invoice and outstanding amount
- [ ] AC-08: Given all families have zero outstanding balances, then an empty state appears: "All families are up to date. No outstanding balances." with a "View payment history" link. The summary banner shows ₹0 / 0 families / 0 overdue
- [ ] AC-09: Given Rahul loads the dashboard while offline, then the last-synced list is shown with a banner: "Offline — showing data from [date and time]. Payment actions unavailable." "Send Reminder" and "Record Payment" quick-action buttons are disabled (greyed out with tooltip "Requires internet connection"). The summary banner remains visible using cached figures
- [ ] AC-10: Given the dashboard has more than 50 rows, then the list paginates (25 rows per page) with "Load more" at the bottom and a total count in the header. The summary banner always reflects all families, not just the current page

**Edge Cases & Error States:**
- [ ] EC-01: If GET /billing/outstanding returns a 5xx error, the screen shows: "Couldn't load outstanding balances — tap to retry." If a cached response exists (from within the last 24 hours), it is shown with an error banner: "Showing cached data — could not refresh."
- [ ] EC-02: If a payment is being processed (UPI webhook received but receipt not yet generated — invoice in a transitional state), the invoice row shows a "Payment processing..." indicator and the quick-action buttons are disabled for that row until the transition completes

**Non-Functional Requirements:**
- Performance: Dashboard loads within 2 seconds on 4G on minimum-spec Android and desktop Chrome. Summary figures are computed server-side, not in the client
- Offline: Read-only cached view available (AC-09); all write actions blocked offline
- Accessibility: Days overdue labels include text alongside color indicators (AC-04); touch targets >= 44px for all quick-action buttons; dashboard operable one-handed on mid-range Android; do not use more than 4 data columns in mobile list rows — overflow to second line
- Privacy: Outstanding balance data contains child names and financial figures; RBAC: admin role only; screen must not be visible to Priya or Dr. Sunita

**Dependencies:**
- Blocked by: BILLING-002 (invoices must exist), BILLING-003 (invoices in Sent status with due dates), BILLING-005 and BILLING-006 (payment updates reduce outstanding balance in real-time)
- Enables: BILLING-008 (manual reminder trigger), BILLING-006 (record payment quick-action)

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android and desktop Chrome
- [ ] Summary banner figures tested: total outstanding, families count, >30 days count — all accurate after payments
- [ ] Sort functionality (AC-05) tested for all four sort options
- [ ] Offline cached view (AC-09) tested: load dashboard online, disable connectivity, reopen — cached data visible, actions disabled
- [ ] Empty state (AC-08) tested
- [ ] EC-01 (server error) and EC-02 (transitional invoice state) tested
- [ ] Pagination tested with >50 rows
- [ ] Color + text label (AC-04) accessibility confirmed with design before merge
- [ ] RBAC: Priya cannot access Billing Dashboard — confirmed
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| BILLING-001 | Fee structure configuration per child | Rahul | M | P0 | AUTH-001, EMR-001, EMR-002 |
| BILLING-002 | Automated monthly invoice generation from attendance records | System / Rahul | L | P0 | BILLING-001, SCHED-004, INFRA-003 |
| BILLING-003 | Invoice review and send | Rahul | M | P0 | BILLING-002, BILLING-004, INFRA-004 |
| BILLING-004 | UPI payment link generation and delivery | System / Rahul | L | P0 | BILLING-003, INFRA-005 |
| BILLING-005 | UPI payment webhook reconciliation | System | L | P0 | BILLING-004, INFRA-005, INFRA-006 |
| BILLING-006 | Manual payment recording — cash, bank transfer, cheque | Rahul | M | P0 | BILLING-002, BILLING-003, INFRA-007 |
| BILLING-007 | Automated receipt generation and WhatsApp delivery | System | M | P0 | BILLING-005, BILLING-006, INFRA-004, INFRA-008 |
| BILLING-008 | Overdue invoice reminders | System / Rahul | L | P1 | BILLING-003, BILLING-004, INFRA-003, INFRA-004, INFRA-009 |
| BILLING-009 | Outstanding balance dashboard | Rahul | M | P0 | BILLING-002, BILLING-003, BILLING-005, BILLING-006 |

**Sprint recommendation:** BILLING-001, BILLING-006, and BILLING-009 (read-only shell) can be built in Sprint 1 in parallel once AUTH-001 and EMR-001 are confirmed. BILLING-002 and BILLING-003 are the core path and should be Sprint 2. BILLING-004, BILLING-005, and BILLING-007 are the payment loop and form Sprint 3 — they have a hard infrastructure dependency on UPI aggregator setup (INFRA-005) that must start immediately. BILLING-008 can be Sprint 4 — it is P1 (important, not P0) because manual reminder via BILLING-009 is the interim workaround.

---

## Pre-Build Decisions Required

| # | Decision | Owner | Needed by |
|---|---|---|---|
| PBD-01 | UPI payment aggregator selection: Razorpay, PayU, or Cashfree — evaluate sandbox API, webhook reliability, fee structure, and onboarding timeline for a small business | Product / Engineering | Before BILLING-004 sprint |
| PBD-02 | WhatsApp Business API (WABA) provider: use Meta's direct Cloud API or a BSP (Business Solution Provider) such as Interakt, AiSensy, or Wati — BSP reduces setup complexity for small center directors; evaluate DLT template management and WABA approval timeline (typically 2–4 weeks) | Product | Before BILLING-003 sprint (WABA gates invoice send delivery) |
| PBD-03 | DLT sender ID registration for transactional SMS (TRAI-mandated for all commercial SMS in India): choose SMS provider (Exotel, MSG91, or Kaleyra), register sender ID, register all message templates (Fee Due, Fee Reminder Day 7, Fee Reminder Day 14, Payment Receipt). Process takes 1–4 weeks | Product / Legal | Before BILLING-008 sprint and before BILLING-003 if SMS fallback is required at MVP |
| PBD-04 | WABA message template approval: draft and submit "Invoice Sent", "Fee Reminder Day 7", "Fee Reminder Day 14", and "Payment Receipt" templates to Meta for approval. Templates cannot be modified after approval without re-submission. Legal review of template language recommended before submission | Product / Legal | At least 2 weeks before BILLING-003 sprint |
| PBD-05 | Billing cycle configuration: is billing always calendar-month (1st to last day), or do some centers need rolling 30-day cycles? Confirm the default and whether Rahul can configure this per center. Decision affects BILLING-002 cron trigger logic | Product | Before BILLING-002 sprint |
| PBD-06 | Invoice number format: confirm center_code format (auto-generated or admin-set?) and whether invoice numbers must be sequential with no gaps (common Indian accounting requirement) or can have gaps. Affects BILLING-002 DB schema | Engineering / Product | Before BILLING-002 sprint |
| PBD-07 | Offline sync conflict resolution strategy for BILLING-006: if Rahul records a manual payment offline and a UPI payment comes in for the same invoice while he is offline, which record wins on sync? Current EC-02 behavior surfaces a conflict for manual resolution — confirm this is acceptable or define an automated resolution rule | Engineering / Product | Before BILLING-006 sprint |
| PBD-08 | Receipt PDF template: confirm required fields, center logo placement, and whether a GST number field is needed (even if GST billing is out of scope, some center directors may need it for their own records). Confirm with a sample center director before BILLING-007 sprint | Product | Before BILLING-007 sprint |

---

## ⚠️ Feature Factory Disclaimer

These stories were defined by journey document synthesis, competitive observation (Jane App, SimplePractice, Theralytics, Razorpay), and category assumptions — not by validated primary research with Indian autism therapy center directors.

**What we assumed but haven't validated:**
- [ASSUMPTION] Rahul currently spends significant time manually calculating fees and chasing payments via WhatsApp — the actual time burden and frequency of this pain has not been measured (H-12). If the pain is low, platform adoption for billing will be low regardless of feature quality
- [ASSUMPTION] Meena will tap a UPI payment link in a WhatsApp message and complete payment digitally rather than paying cash at the center or ignoring the link. UPI adoption in the specific demographic of autism therapy families in India is unconfirmed. If cash-first behavior dominates, BILLING-004 and BILLING-005 are low-value at MVP and BILLING-006 becomes the primary payment path
- [ASSUMPTION] Invoice auto-generation from attendance records (BILLING-002) delivers real value — this assumes attendance is captured digitally and reliably in the platform. If Priya's attendance marking adoption is low (Journey 3 not adopted), the core differentiator does not function. Rahul falls back to manual session counting, which is no better than his current Excel workflow
- [ASSUMPTION] Automated overdue fee reminders (BILLING-008) will not damage center-family relationships. Indian therapy center billing is relationship-sensitive; a tone-deaf automated reminder to a financially stressed family is a documented dropout accelerant (Tandfonline 2025). Template tone must be tested with real center directors before activation
- [ASSUMPTION] Rahul is willing and able to set up WhatsApp Business API — this requires Meta Business Manager verification, a dedicated business WhatsApp number, and ongoing Meta template approval. This is a non-trivial lift for a small center director with limited technical capacity and may be the largest real-world adoption barrier for this entire epic

**What a researcher would ask before building this:**
- How does Rahul collect fees today — what is his actual workflow step by step? Has he tried any digital payment tool (Razorpay payment pages, Google Pay Business) and abandoned it? What was the specific friction point? (H-12)
- What proportion of families at target centers pay by UPI vs. cash? Does this differ by metro vs. tier-2 city? (informs MVP priority — BILLING-004/005 vs. BILLING-006)
- Would automated fee reminders help Rahul or create relationship anxiety? Ask him about the last time he sent a fee reminder — what happened, how did he feel about it, how did the parent respond? (validates BILLING-008 risk level)

**What the Product Consultant would challenge:**
- The entire billing epic has a critical dependency on Journey 3 (Scheduling & Attendance). If attendance is not captured digitally at adequate quality, BILLING-002 produces inaccurate drafts that Rahul must manually correct every month — reducing net value below the Excel baseline. Gate the billing epic on a confirmed attendance data quality threshold in production before declaring BILLING-002 successful
- Consider whether the MVP billing feature is just: BILLING-001 (fee configuration) + BILLING-006 (manual payment recording) + BILLING-009 (outstanding dashboard) + a manual invoice PDF export. BILLING-002 through BILLING-005, BILLING-007, and BILLING-008 can be Phase 2 once attendance data quality is proven and WABA / UPI aggregator infrastructure is stable. Shipping a billing system that generates inaccurate invoices is worse than not shipping one

**Risk level per story:**
- BILLING-001 (fee structure): Low — lightweight CRUD; admin behavior; no infrastructure dependency
- BILLING-002 (auto invoice generation): Medium — depends on attendance module reliability and data quality
- BILLING-003 (invoice review and send): Low-Medium — well-defined UI workflow; WABA infrastructure gates delivery
- BILLING-004 (UPI payment link): Medium — UPI aggregator onboarding and API integration; idempotency is critical
- BILLING-005 (UPI webhook reconciliation): Medium-High — webhook reliability, idempotency, and edge cases require careful engineering; aggregator behavior in sandbox vs. production may differ
- BILLING-006 (manual payment recording): Low — offline-first CRUD; primary path for many centers
- BILLING-007 (receipt generation): Low-Medium — PDF generation is solved; WABA delivery reliability is the variable
- BILLING-008 (overdue reminders): Medium — relationship sensitivity in Indian small-practice context; DLT and WABA template approval timeline outside engineering control; tone testing needed before launch
- BILLING-009 (outstanding dashboard): Low — read-heavy; well-defined data model; primary navigation surface

Use the `/researcher` agent to validate H-12 (billing pain), H-09 (fee collection discomfort), and the UPI payment behavior assumption before sprint planning.
Use the `/product-consultant` agent to challenge the WABA scope, the billing-attendance dependency, and whether BILLING-002 through BILLING-005 belong in the MVP sprint.
Use the `/design-critique` agent to review the Outstanding Dashboard and Invoice Detail Screen before prototyping.
