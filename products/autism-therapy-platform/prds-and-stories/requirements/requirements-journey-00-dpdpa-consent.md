# Requirements: Journey 0 — DPDPA Consent Management & Data Subject Rights

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 0 — DPDPA Consent Management & Data Subject Rights
**MVP status:** ✅ IN SCOPE — MVP (regulatory non-negotiable)
**Primary actor:** Rahul (Center Director / Data Fiduciary — captures and manages consent); Meena (Parent / Data Principal — gives and exercises consent rights)
**Supporting actors:** Dr. Sunita (notified on consent withdrawal for supervised children); Priya (sees consent gate on child records)
**Date:** 2026-05-05
**Story ID prefix:** CONSENT-
**Source documents:**
- `user-journeys/journey-00-dpdpa-consent-management.md`
- `user-journeys/journey-map.md`

**Governing law:** DPDPA 2023 (Digital Personal Data Protection Act). HIPAA does not apply in India.

---

## Design Non-Negotiables (apply to every story in this journey)

1. **Consent is a gate, not a form.** No clinical data write endpoint may succeed for a child without a confirmed consent record. This is enforced at the API layer — not just in the UI. A UI-only gate that can be bypassed by a direct API call is not a compliant gate.
2. **Consent records are immutable.** No UPDATE or DELETE operation on a consent record. Corrections, withdrawals, and re-consents are separate append-only events. The consent record schema must enforce this at the database level.
3. **No pre-checked checkboxes — ever.** DPDPA 2023 requires affirmative, unambiguous consent. A pre-checked consent checkbox is legally invalid consent. This is a non-negotiable hard requirement for the consent form UI.
4. **Consent requires connectivity.** The server timestamp on the consent record is the legally significant timestamp. Consent cannot be written from an offline queue. If the device is offline when consent is attempted, the form blocks with a connectivity error — not a "will sync later" message.
5. **The RPWD Act / DPDPA erasure conflict must never be auto-resolved by engineering.** If a parent requests erasure, the system must surface the potential conflict with RPWD Act 2016 documentation obligations and require a human decision from Rahul. The system cannot decide which law takes precedence.

---

## Epic: CONSENT — DPDPA Consent Management & Data Subject Rights

**Goal:** Ensure every child in the platform has a verified, legally defensible parental consent record before any health data is created, processed, or stored — and give parents the ability to exercise their DPDPA 2023 rights (withdrawal, data portability, erasure) through the platform, while surfacing the legal complexity of the DPDPA/RPWD conflict to center directors when erasure is requested.

**Copied from:** No direct competitor in the Indian market has a DPDPA-compliant consent flow — Indian tools (TherapEZ, PractiPal) have no clinical data layer and no DPDPA mechanism. US ABA tools (CentralReach, Motivity) have HIPAA consent flows adapted for the US context — structurally similar but not applicable under Indian law. This consent management system is purpose-built for DPDPA 2023 and the Indian therapy center operating context.

**Target users:** Rahul (Center Director — data fiduciary); Meena (Parent — data principal); Dr. Sunita and Priya (experience the consent gate as a system constraint on clinical data entry)

**Definition of Done:**
- [ ] No session note, therapy program, SOAP note, or clinical document can be created for a child whose consent status is not "active" — enforced at the API layer (HTTP 423 response)
- [ ] Consent record is written as an immutable, server-confirmed event — schema blocks UPDATE and DELETE
- [ ] Privacy notice is version-stamped; the notice version is stored with each consent record
- [ ] Three consent capture methods work: in-person (checkbox + digital signature), staff-assisted verbal (flagged for follow-up), and remote consent via shared link
- [ ] Consent withdrawal flow is completable from the parent portal in a single session
- [ ] Data portability export is available to parents via the parent portal (PDF of all held data)
- [ ] Erasure request flow surfaces the DPDPA/RPWD legal conflict to Rahul and requires explicit human decision
- [ ] Full consent event timeline (consent given, withdrawal, re-consent) is accessible to Rahul in a read-only audit log
- [ ] All features pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)

**Out of scope (this epic):**
- ABHA / ABDM consent flow — separate consent under ABDM rules (ABDM-002); handled in Journey 2
- Clinical data itself — this epic only manages the consent gate; actual data creation is in Journeys 2–11
- Multi-language consent notices (Phase 2 — Hindi and regional language versions)
- Automated DPDPA compliance reporting to regulators (Phase 2+)
- Consent for staff data processing — this epic covers parental consent for children's health data only

**[ASSUMPTION — NOT VALIDATED]** This epic assumes Indian therapy center directors (Rahul) are aware that DPDPA 2023 creates a binding compliance obligation for processing minors' health data. Primary research has not confirmed DPDPA awareness among Indian center directors as of May 2026. If centers are unaware, the consent flow will be experienced as unexpected friction at intake rather than a compliance relief.

---

## Story CONSENT-001: Privacy Notice Display Before Consent

**As a** Center Director (Rahul, facilitating for Meena) or Parent (Meena, on her own device)
**I want** the system to display a plain-language privacy notice — explaining what data is collected, why, who can see it, and what Meena's rights are — before the consent checkbox and signature appear
**So that** consent is genuinely informed, not a formality, and DPDPA 2023 Section 6(2) is met

**Inspired by:** DPDPA 2023 Section 6(2) — consent must be informed; no competitive reference — this is a regulatory requirement unique to this product context

**Context:** This screen is presented to Meena (in person or on her own device) immediately before the consent confirmation step. It is not a terms-and-conditions wall of text. It must be readable by a non-technical Indian parent at the level of a standard WhatsApp message. Rahul may need to explain it verbally in Tamil, Hindi, or Telugu if Meena cannot read English — the screen includes a "Explained verbally" toggle for this case.

**Acceptance Criteria:**

- [ ] AC-01: Given Rahul taps "Add consent now" on the DPDPA consent banner (from the child record or intake flow), when the Privacy Notice screen loads, then it displays a version-stamped notice with six clearly labeled sections: (1) What data we collect, (2) Why we collect it, (3) Who can see it, (4) How long we keep it, (5) Your rights (access / correction / withdrawal / erasure / portability), (6) Contact us — all in plain English, no legal jargon or abbreviations without plain-language explanation.
- [ ] AC-02: Given the Privacy Notice is displayed, when the user has not yet scrolled to the bottom, then the "Proceed to consent" button is not active — a subtle scroll progress indicator shows how far remains. The button activates only after the user has scrolled to the end of the notice or after 60 seconds have elapsed (whichever comes first — the time fallback ensures accessibility for users who read slowly on low-end devices).
- [ ] AC-03: Given the Privacy Notice is loaded, when Rahul or Meena reviews it, then the notice text must render at minimum 16sp font, line height ≥ 1.5, on a 5.5-inch Android screen without requiring pinch-zoom to read.
- [ ] AC-04: Given the privacy notice is fetched from the server, when the version number is confirmed, then the version ID is stored in the UI session state — it will be written to the consent record at submission (CONSENT-002). If the server cannot confirm the current notice version (connectivity issue), the screen blocks with: "Unable to load consent form — check your connection and try again." Consent cannot proceed without a confirmed version.
- [ ] AC-05: Given Rahul needs to explain the notice verbally (Meena does not read English), when Rahul taps "Explained verbally in [language]" toggle at the bottom of the notice, then a language selector appears (English / Hindi / Tamil / Telugu / Other), Rahul selects the language, and this flag is stored in the consent session state — it will be written to the consent record as "verbal-explanation-provided: [language]" at submission.

**Edge Cases & Error States:**

- [ ] EC-01: If the privacy notice content fails to load from the server and no cached version exists, the entire consent flow blocks — no fallback consent with an empty notice. Error message: "Could not load the consent notice. Please check your connection and try again." No consent record is written.
- [ ] EC-02: If the notice has been updated since the last cached version and the device is offline, the screen blocks: "A newer version of our privacy notice is available. Please connect to the internet to load it before proceeding." The old version is not used — the legally significant requirement is that the parent consents to the current notice version.

**Non-Functional Requirements:**

- Performance: Privacy notice must load in < 1.5s when connectivity is available (content is a static JSON document — not dynamically generated per-request).
- Offline: This screen requires connectivity for the version confirmation step. Offline behavior: block with connectivity error.
- Accessibility: Font minimum 16sp. WCAG AA contrast (4.5:1 on body text). All links within the notice ≥ 44dp touch target. Readable by a non-technical parent without assistance (tested via comprehension check in design validation).
- Privacy: The notice itself does not create a data record — only viewing it. Data is written only at CONSENT-002 (consent submission).

**Dependencies:**
- Blocked by: AUTH-001 (Rahul must be authenticated); EMR-001 (child record must exist to have a consent context)
- Enables: CONSENT-002 (consent capture — cannot begin without confirmed privacy notice presentation)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Privacy notice renders legibly without pinch-zoom on 5.5-inch Android device
- [ ] Version ID confirmed to be stored in session state after notice load
- [ ] Offline behavior tested: notice blocks when server cannot confirm version
- [ ] "Explained verbally" flag persists through to consent submission (CONSENT-002)
- [ ] Code reviewed and merged

---

## Story CONSENT-002: Parental Consent Capture (In-Person)

**As a** Center Director (Rahul, facilitating on a shared device) or Parent (Meena, on her own device)
**I want to** complete the consent capture step — reading a summary, ticking an explicit checkbox, and signing digitally — so that the child's record is unlocked for clinical data entry
**So that** the center has a legally defensible DPDPA 2023 consent record on file and all clinical features become accessible for this child

**Inspired by:** DPDPA 2023 Section 9 (verifiable parental consent for minors); structural pattern from SimplePractice consent capture; consent form mechanics adapted for Indian regulatory context

**Context:** Meena is present at the center — either at the intake appointment (directly after Journey 2 enrollment) or at a follow-up visit. She is handed a shared tablet or uses the center's Android phone. The consent form is the final step before any clinical record can be created for her child. She is already familiar with the center at this point (Journey 1 and Journey 2 have occurred). Rahul may stand by to explain anything she does not understand.

**Acceptance Criteria:**

- [ ] AC-01: Given the Privacy Notice has been presented (CONSENT-001) and Rahul taps "Proceed to consent", when the Consent Capture screen loads, then it displays: (a) a one-line confirmation summary ("You are giving consent for [Centre name] to collect and process [Child name]'s health data for therapy purposes"); (b) an explicit opt-in checkbox — starting unchecked, labeled "I confirm I am the legal parent or guardian of [child name] and I consent to collection and processing of their health data as described in the privacy notice I have read"; (c) a digital signature field (minimum 200×100px, finger and stylus compatible); (d) a parent name field (pre-filled from child record but editable); (e) a relationship to child dropdown (Mother / Father / Legal guardian / Extended family caregiver / Other).
- [ ] AC-02: Given the Consent Capture screen is displayed, when Meena has not yet ticked the checkbox AND drawn a signature, then the "Confirm consent" button is disabled with label "Complete the consent above to proceed." The button activates only when both the checkbox is checked AND a signature is present — not one or the other.
- [ ] AC-03: Given Meena ticks the checkbox and draws her signature, when Rahul taps "Confirm consent", then the system calls `POST /children/{id}/consent` with: parent_name, relationship_to_child, consent_datetime_ist (server-confirmed), notice_version_id (from CONSENT-001 session state), method="in-person-digital", admin_actor_id, device_id. This call requires active connectivity — a failed write returns an error and retains the form; no partial data is stored.
- [ ] AC-04: Given the consent record is written successfully, when the response confirms, then: (a) the child record status transitions from "pending_consent" to "active"; (b) the orange consent banner is replaced by a green "DPDPA Consent: Confirmed [date]" badge in the record header; (c) all clinical data tabs (Session Notes, Therapy Program, SOAP Notes, Documents) are unlocked immediately; (d) haptic feedback fires on the submitting device; (e) a success screen is shown: "Consent confirmed. You can now begin adding clinical records for [child name]."
- [ ] AC-05: Given the consent record is submitted, when the audit trail is written, then an immutable AUDIT-001 event is created: event_type="CONSENT_CAPTURE", actor_id, actor_role, child_id, timestamp_ist, notice_version_id, method, "DPDPA_high_risk" flag=true. If the audit trail write fails, the entire consent transaction rolls back — no consent record is written without a corresponding audit log entry.

**Edge Cases & Error States:**

- [ ] EC-01: If the server returns a 5xx error on consent submission, the form shows: "Consent could not be saved — check your connection and try again. No data has been stored." The form retains all entered data (checkbox state, signature). No partial consent record is written. The child record status remains "pending_consent".
- [ ] EC-02: If Meena clears her signature before submitting and leaves the field blank, the "Confirm consent" button returns to disabled state. The signature field shows its placeholder again.
- [ ] EC-03: If Rahul navigates away from the Consent Capture screen before submitting, a confirmation dialog asks: "Leave without saving? Your consent form has not been submitted." If confirmed, no data is written and the child record remains in "pending_consent" state.
- [ ] EC-04: If a consent record already exists for this child (duplicate submission — e.g., Rahul accidentally re-enters the flow), the system detects the existing active consent record and redirects to the read-only consent record view with a message: "Consent for this child has already been confirmed on [date]."

**Non-Functional Requirements:**

- Performance: Consent Capture screen must load in < 1s. Consent record submission must complete (including audit log write) in < 3s on a standard 4G connection.
- Offline: Consent cannot be captured offline. Connectivity error shown if device is offline when "Confirm consent" is tapped.
- Accessibility: Checkbox touch target ≥ 44dp. "Confirm consent" button text must use the word "confirm" — not "accept" or "agree" (DPDPA precision). Button minimum 48dp height. Signature field must be operable with a finger on a low-end Android touch screen.
- Privacy: ⚠️ DPDPA 2023 — the consent record is the legal compliance mechanism for processing a minor's sensitive health data. Schema: consent records must have no UPDATE or DELETE endpoints. Write-once only. Signature image stored encrypted; not displayed to any user after submission.

**Dependencies:**
- Blocked by: CONSENT-001 (privacy notice must be displayed and version confirmed); EMR-001 (child record must exist with status "pending_consent")
- Enables: All clinical data write features for this child — NOTE-001, PROG-XXX, SOAP notes, document uploads; CONSENT-004 (gate enforcement depends on consent record existing)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Pre-checked checkbox state tested: confirmed it is impossible to submit with checkbox pre-checked on page load
- [ ] Consent record atomicity tested: server error mid-write confirmed to result in zero partial records
- [ ] Audit trail write confirmed: every successful consent submission has a corresponding AUDIT-001 event
- [ ] Child record status transition "pending_consent" → "active" confirmed in QA
- [ ] Clinical tabs unlock immediately after consent confirmed — confirmed on minimum-spec device
- [ ] EC-04 (duplicate submission) behavior verified
- [ ] Code reviewed and merged

---

## Story CONSENT-003: Remote Consent via Shared Link

**As a** Center Director (Rahul)
**I want to** generate a secure, time-limited consent link and share it with Meena via WhatsApp — so she can complete the consent form on her own Android phone at home before the next visit
**So that** the center can collect digital consent without requiring Meena to be physically present at the center with a shared device

**Inspired by:** DPDPA 2023 Section 9 (verifiable consent — does not require in-person); DocuSign / HelloSign remote signature pattern adapted for Indian regulatory context; consent link pattern from US healthcare intake platforms

**Context:** Meena was not present at the intake appointment, or the in-person consent was skipped for logistical reasons. Rahul needs to collect digital consent before the first therapy session begins. Rahul shares a WhatsApp link. Meena opens it on her own Android phone at home. The link must be accessible on a low-end Android browser without requiring a platform app install. The consent record created via the link must be indistinguishable in validity from an in-person consent — the method is recorded but the legal status is equivalent.

**Acceptance Criteria:**

- [ ] AC-01: Given a child record exists with consent status "pending_consent", when Rahul opens the Consent tab on the child's record and taps "Generate consent link", then the system creates a secure, single-use consent link with a 7-day expiry. The link is displayed in a shareable format with a "Copy link" and "Share via WhatsApp" action.
- [ ] AC-02: Given the link is shared with Meena, when she opens it on any Android browser (Chrome, Samsung Browser) without logging into the platform, then the Privacy Notice is presented first (CONSENT-001 flow — same notice, same version), followed by the consent form with the child's name pre-filled from the link's associated child record. Meena cannot see any other child's data via this link.
- [ ] AC-03: Given Meena completes the privacy notice and consent form on the link, when she taps "Confirm consent", then the system writes the consent record with method="remote-link-digital", link_id (for audit correlation), parent_name (entered by Meena), relationship_to_child, server-confirmed timestamp_ist, notice_version_id, device metadata (user-agent). The consent record is written to the same child record that Rahul generated the link for.
- [ ] AC-04: Given the remote consent is confirmed, when the record is written, then: (a) Rahul's app receives an in-app notification within 60 seconds: "Consent confirmed for [child name] by [parent name]"; (b) the child record status transitions to "active" immediately; (c) the "Staff-assisted verbal" flag on the record (if present) is superseded — the record now shows "Consent: Confirmed digitally [date] via remote link."
- [ ] AC-05: Given the consent link has been opened, when it is used successfully, then the link becomes invalid for any subsequent use. A second attempt to open the same link shows: "This consent link has already been used. Contact [centre name] if you have questions."
- [ ] AC-06: Given the consent link was generated but Meena has not used it after 7 days, when Rahul opens the child's Consent tab, then the expired link is shown with status "Expired" and a "Generate new link" option. The expired link generates an error if someone attempts to access it: "This consent link has expired. Please contact [centre name] to request a new one."

**Edge Cases & Error States:**

- [ ] EC-01: If Meena opens the link on a device where the platform app is installed and she is logged in as a different user (e.g., a staff member's device), the link flow operates in its own isolated context — it does not use the logged-in staff session. The consent is attributed to the link's associated parent, not the logged-in staff account.
- [ ] EC-02: If Meena begins the remote consent form but does not submit before the 7-day expiry, her in-progress form state is lost. The link shows as expired. Rahul must generate a new link.
- [ ] EC-03: If Rahul generates multiple links for the same child (e.g., the first was sent to the wrong number), all prior unconfirmed links for the same child are invalidated when a new link is generated. Only the most recently generated link is active at any time.

**Non-Functional Requirements:**

- Performance: Link landing page must load within 2s on a 3G connection (Indian rural connectivity baseline). Page must not require JavaScript frameworks that bloat load time on low-end Android browsers.
- Offline: Remote consent requires connectivity — Meena must be online to submit. Offline behavior: form saves draft locally on Meena's device; submit blocked with connectivity error until online.
- Accessibility: Remote consent link must be completable by a non-technical Indian parent without any platform account or app installation. Font minimum 16sp. Touch targets ≥ 44dp. No CAPTCHA or authentication barrier.
- Privacy: ⚠️ DPDPA 2023 — the link must be a secure token (minimum 32-character random URL-safe string); must not contain child name or child ID in the URL; must expire after 7 days or first use; link generation and use are logged in the audit trail.

**Dependencies:**
- Blocked by: EMR-001 (child record with "pending_consent" status must exist); CONSENT-001 and CONSENT-002 (same privacy notice and consent form logic is reused)
- Enables: CONSENT-004 (once consent confirmed via remote link, gate lifts identically to in-person consent)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+) — both the link-generation side (Rahul) and the link-consumption side (Meena on a different device with no platform account)
- [ ] Link expiry after 7 days confirmed in QA
- [ ] Single-use invalidation confirmed: second access to a used link shows expired state
- [ ] Consent record method="remote-link-digital" confirmed in database QA check
- [ ] EC-03 (new link invalidates prior links for same child) confirmed
- [ ] Code reviewed and merged

---

## Story CONSENT-004: Consent Gate Enforcement Across Clinical Features

**As a** Platform System
**I want to** block all clinical data write operations for any child whose consent status is not "active" — at both the API layer and the UI layer
**So that** no child health data can be created, stored, or processed without confirmed parental consent, regardless of which feature or screen is used to attempt the write

**Inspired by:** DPDPA 2023 Section 9 (mandatory gate for processing minors' health data); architectural consent gate pattern from CentralReach and Motivity clinical platforms

**Context:** This is an infrastructure story — it has no primary UI of its own. Its output is a set of consistent behaviors across every clinical feature in the product. The gate must be enforceable: a therapist or director who knows the API cannot bypass it via a direct call. This story defines the system's behavior in the "pending_consent", "consent_withdrawn", and "erasure_requested" child record states.

**Acceptance Criteria:**

- [ ] AC-01: Given any child record exists with consent_status ≠ "active" (i.e., status is "pending_consent", "consent_withdrawn", or "erasure_requested"), when any authenticated user calls any clinical data write endpoint for that child — including but not limited to: `POST /sessions/{id}/notes`, `POST /children/{id}/programs`, `POST /children/{id}/soap-notes`, `POST /children/{id}/documents`, `POST /sessions` (session creation), `PATCH /sessions/{id}/attendance` — then the API returns HTTP 423 (Locked) with a response body: `{"error": "consent_required", "message": "Parental consent is required before clinical data can be added for this child.", "consent_status": "<current status>"}`.
- [ ] AC-02: Given a child record has consent_status ≠ "active" and an authenticated user opens that child's profile in any UI screen, when the clinical data tabs (Session Notes, Therapy Programs, SOAP Notes, Documents, Clinical Assessments) are displayed, then: (a) tabs are visually greyed out with a lock icon; (b) tapping a locked tab shows a tooltip: "Parental consent required — tap 'Add consent' to proceed" for status="pending_consent", or "Consent has been withdrawn — no new records can be added" for status="consent_withdrawn"; (c) a non-dismissible banner is shown at the top of the record in the appropriate state color (orange for pending, yellow for withdrawn).
- [ ] AC-03: Given a child record has consent_status = "pending_consent", when the consent banner is shown, then a "Add consent now" CTA button is present and visible in the banner — this is the only entry point to the consent capture flow from the child record. The button is accessible to Director and Admin roles only; therapist role sees the banner but not the CTA button.
- [ ] AC-04: Given a child record has consent_status = "active", when any clinical write endpoint is called, then the API does not apply the consent lock — the clinical write proceeds subject to normal RBAC checks. The consent gate check must add ≤ 50ms overhead to any endpoint response time (indexed lookup on child_record.consent_status — not a full consent record query per call).
- [ ] AC-05: Given a child record's consent_status is updated (e.g., withdrawal confirmed at CONSENT-005), when the status change propagates, then all active UI sessions viewing that child's record reflect the updated state within 60 seconds (server-sent event or polling — polling interval ≤ 60s acceptable for MVP). A therapist who had that child's session notes screen open during withdrawal sees the lock state applied on the next data refresh.

**Edge Cases & Error States:**

- [ ] EC-01: If a background job (e.g., billing cycle, reminder scheduler) attempts to read or write clinical data for a child with consent_status ≠ "active", the job skips that child's record, logs a warning event, and does not fail the overall job. The skip event is visible to Rahul in the admin dashboard with a note: "X records skipped — parental consent not confirmed."
- [ ] EC-02: If the consent_status field is missing or null on a child record (data integrity issue), the API treats it as "pending_consent" — the conservative default. The record is flagged for admin review.

**Non-Functional Requirements:**

- Performance: Consent gate check must add ≤ 50ms to any clinical endpoint. Gate check is an indexed single-field lookup — not a join or subquery.
- Offline: The UI consent gate check uses cached child record consent_status. Conservative default: if status is unknown (no cache), lock clinical tabs. The API gate is always enforced server-side regardless of device connectivity state.
- Accessibility: Lock icon on greyed tabs must not be the only signal — text label "Consent required" must accompany the icon (not color and icon alone).
- Privacy: ⚠️ DPDPA 2023 — this story is the technical implementation of the legal consent requirement. Any regression in this gate that allows clinical data to be written without confirmed consent is a DPDPA compliance failure. Gate enforcement must be included in regression tests for every API release.

**Dependencies:**
- Blocked by: CONSENT-002 (consent record schema must exist for gate to query); AUTH-001 (RBAC roles determine who sees the "Add consent" CTA vs. just the locked state)
- Enables: All clinical feature stories (NOTE-001, PROG-XXX, etc.) — consent gate is the prerequisite gate for the entire clinical layer

**Definition of Done:**
- [ ] AC-01 API gate verified: direct API call to each clinical write endpoint returns 423 for a child with consent_status="pending_consent" — tested with Postman or equivalent, not just UI testing
- [ ] AC-02 UI gate verified: all clinical tabs locked and labeled correctly on minimum-spec Android
- [ ] AC-04 performance verified: consent gate check adds ≤ 50ms to endpoint response time under load test
- [ ] EC-02 null-status default verified: missing consent_status treated as pending_consent (conservative default)
- [ ] Regression test suite updated: consent gate check added to CI pipeline for all clinical write endpoints
- [ ] Code reviewed and merged

---

## Story CONSENT-005: Consent Withdrawal

**As a** Parent (Meena)
**I want to** withdraw my consent for data processing — from the parent portal — and have that withdrawal take effect immediately, stopping any further clinical records from being created for my child
**So that** I can exercise my DPDPA 2023 Section 6(4) right to withdraw consent at any time without having to contact the center or justify my decision

**Inspired by:** DPDPA 2023 Section 6(4) — right to withdraw consent without delay; parent self-service privacy settings pattern from SimplePractice and Jane App

**Context:** Meena has a parent portal account. Her child's therapy journey has reached a point where she wants to withdraw consent — perhaps she is moving, changing centers, or has a dispute with the center. This is a rare but critical workflow. The withdrawal must be processed in the same session she requests it. Existing clinical records are not deleted by withdrawal — only future data creation is blocked. Dr. Sunita and Rahul must be notified immediately so they can manage the operational impact (cancel upcoming sessions, inform Priya).

**Acceptance Criteria:**

- [ ] AC-01: Given Meena is logged into the parent portal, when she navigates to Account > Privacy > My Consent, then the screen shows: current consent status (Active), date consent was given, a plain-language description of what consent covers, and a "Withdraw consent" button. The withdrawal button is only shown when consent_status = "active".
- [ ] AC-02: Given Meena taps "Withdraw consent", when the withdrawal explanation screen loads, then it displays a plain-language explanation: "If you withdraw consent, [Centre name] will stop creating new therapy records for [child name]. Existing records will remain unless you separately request erasure. The centre will be notified. Are you sure you want to continue?" A secondary CTA "Learn about data erasure" links to CONSENT-007 info page. The primary action is "Yes, withdraw my consent" and a secondary "Cancel" option.
- [ ] AC-03: Given Meena taps "Yes, withdraw my consent", when the system processes the withdrawal, then: (a) `POST /children/{id}/consent/withdraw` is called and must complete within the same session — no queued processing; (b) the withdrawal record is written as an immutable audit event: actor=parent, action="CONSENT_WITHDRAWAL", timestamp_ist, "DPDPA_high_risk" flag=true; (c) child record status transitions to "consent_withdrawn" immediately; (d) all clinical write endpoints for this child return 423 (Locked) immediately; (e) the parent portal shows: "Consent withdrawn on [date]. No new records are being created for [child name]."
- [ ] AC-04: Given the withdrawal is confirmed, within 60 seconds, then Dr. Sunita (if assigned as supervisor for this child) and Rahul receive in-app notifications: "[Child first name]'s parent has withdrawn data processing consent. New clinical records cannot be created for this child."
- [ ] AC-05: Given the withdrawal is confirmed, when Meena returns to the parent portal on a later date, then she sees: consent status "Withdrawn [date]", existing records remain readable by the center (with a plain-language note explaining this), and an option "Re-consent" — which initiates a new consent capture through CONSENT-002 (creates a new, separate consent record; the withdrawal record is not deleted).

**Edge Cases & Error States:**

- [ ] EC-01: If Rahul has an active session note draft open for this child at the moment of withdrawal, the draft can be completed and saved — any session note for a session that began before the withdrawal timestamp is allowed to be finalized. No new session note creation is permitted after the withdrawal timestamp.
- [ ] EC-02: If the withdrawal API call fails (server error), the child's consent_status is NOT changed. Meena sees: "Withdrawal could not be processed — check your connection and try again." The withdrawal form retains its state. No partial withdrawal state exists.
- [ ] EC-03: If Meena initiates withdrawal but the parent portal session times out mid-flow, the withdrawal is not processed. On next login, the consent remains Active and the withdrawal flow can be resumed.

**Non-Functional Requirements:**

- Performance: Withdrawal confirmation must be processed (consent_status transition + notification delivery) in ≤ 60 seconds of Meena's confirmation tap.
- Offline: Withdrawal requires connectivity (same server-confirmation requirement as consent capture). Offline: block with connectivity error.
- Accessibility: All text on the explanation screen must pass the same plain-language standard as the privacy notice (CONSENT-001). Parent portal is accessed on Meena's personal Android — minimum 16sp font, ≥ 44dp touch targets.
- Privacy: ⚠️ DPDPA 2023 Section 6(4) — withdrawal must be processed without delay. No justification required from Meena. The withdrawal record is immutable — it cannot be edited or deleted by any staff or admin action.

**Dependencies:**
- Blocked by: CONSENT-002 (withdrawal only makes sense if consent was previously captured); Parent portal authentication (RBAC-005 — Meena must have a parent portal account)
- Enables: CONSENT-007 (erasure request — withdrawal often precedes or accompanies an erasure request)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Clinical write endpoints confirmed to return 423 immediately after withdrawal (same session test — write attempt within 5 seconds of confirmed withdrawal)
- [ ] Notification delivery to Rahul and Dr. Sunita confirmed within 60 seconds
- [ ] EC-01 (session note draft finalization allowed after withdrawal) confirmed in QA
- [ ] Withdrawal record immutability confirmed: no UPDATE or DELETE endpoint exists for withdrawal records
- [ ] Code reviewed and merged

---

## Story CONSENT-006: Data Portability — Parent Record Download

**As a** Parent (Meena)
**I want to** request and download a PDF containing all data the center holds about my child
**So that** I can exercise my DPDPA 2023 Section 12 right to data portability — understanding what information the center has and taking it to another provider if needed

**Inspired by:** DPDPA 2023 Section 12 (data portability — mandatory, unjustifiable right); GDPR Article 20 portability pattern (structural analog — regulatory principle is similar); export pattern from SimplePractice and Jane App

**Context:** Meena may request this after withdrawing consent, before moving to a new center, or simply to review what is on record. The request must be processed without delay and without requiring Meena to explain herself. For centers with long-running therapy histories, the PDF may take up to 24 hours to generate for large records.

**Acceptance Criteria:**

- [ ] AC-01: Given Meena is logged into the parent portal, when she navigates to Account > My Child's Data, then she sees a "Download all records" button with a plain-language explanation: "You have the right to a copy of all information we hold about [child name]. This includes session records, progress notes, and intake information." No clinical jargon. No requirement to explain why she wants it.
- [ ] AC-02: Given Meena taps "Download all records", when the request is submitted, then: (a) `POST /parent/children/{id}/data-export-request` is called; (b) an audit log entry is created: actor=parent, action="DATA_PORTABILITY_REQUEST", "DPDPA_S12" flag, timestamp; (c) Meena sees a confirmation: "Your request has been received. Your records will be ready to download shortly." The request cannot be blocked or require Rahul's approval — it is Meena's unconditional right.
- [ ] AC-03: Given the export request is submitted, when the PDF generation job runs, then the PDF includes: cover note (centre name, child name, data as of date), all intake form data, all session records (dates, attendance, session notes if present), therapy program versions, progress reports, uploaded documents index. The PDF must NOT include other families' data, staff salary/HR data, or Rahul's internal admin notes not related to this child.
- [ ] AC-04: Given the child's record has less than 12 months of data, when the export is requested, then the PDF is available for download immediately (< 10 seconds generation time for small records). For records with more than 12 months of data, the PDF is generated as a background job and Meena receives an in-app notification when it is ready — target delivery: within 24 hours; DPDPA-compliant target: within 30 days.
- [ ] AC-05: Given the PDF is ready, when Meena taps the download notification, then the PDF is accessible via a secure, time-limited download URL (expires 48 hours after generation). Meena can re-request a new export if the link expires.

**Edge Cases & Error States:**

- [ ] EC-01: If the PDF generation job fails, Meena does not receive an error notification (she should not need to troubleshoot server-side jobs). Instead, Rahul receives an admin alert: "Data export for [child name] failed to generate — please investigate." The 30-day DPDPA clock is not reset by the failure; the obligation to deliver remains.
- [ ] EC-02: If Meena has submitted multiple export requests within 30 days, the system queues them but sends only the most recent export — earlier requests are superseded. Meena sees the most recent request's status in her portal.

**Non-Functional Requirements:**

- Performance: Small record PDF (< 12 months data) must generate in < 10 seconds. Large record PDF generation time is uncapped but must complete within 24 hours for platform target compliance.
- Offline: Export request submission requires connectivity. Download link can be cached for offline access after download (on Meena's device — standard PDF handling).
- Privacy: ⚠️ DPDPA 2023 — the export PDF contains all clinical data for a minor in one document. The download URL must be a signed, time-limited token. The URL must not be guessable. Download action is logged in the audit trail.

**Dependencies:**
- Blocked by: Parent portal authentication (RBAC-005); child record data (the export job reads from all clinical tables for this child)
- Enables: CONSENT-007 (parents who see their data often follow up with erasure requests)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] PDF content verified: includes all required data categories, excludes all excluded categories
- [ ] Small record immediate-generation confirmed (< 10 seconds on test record with < 12 months data)
- [ ] Audit log entry confirmed on every export request
- [ ] EC-01 admin alert confirmed when generation fails
- [ ] Download URL expires after 48 hours — confirmed in QA
- [ ] Code reviewed and merged

---

## Story CONSENT-007: Data Erasure Request and RPWD Conflict Handling

**As a** Parent (Meena) requesting erasure / Center Director (Rahul) reviewing and deciding
**I want** the system to accept Meena's erasure request, surface the potential conflict between DPDPA 2023 right to erasure and RPWD Act 2016 documentation retention obligations, and require Rahul to make an explicit, legally accountable decision before any data is deleted
**So that** Meena's DPDPA Section 12(c) right is respected while ensuring that the center is not inadvertently placed in violation of RPWD Act 2016 documentation requirements

**Inspired by:** DPDPA 2023 Section 12(c) (mandatory right to erasure); RPWD Act 2016 (documentation retention obligation for therapy programs); this is an India-specific legal conflict with no direct analog in US/EU platforms

**Context:** This is the most legally complex workflow in the entire product. The system must not auto-resolve the legal conflict between two Indian statutes. It must surface the conflict clearly to Rahul, require his decision, document that decision immutably, and then execute exactly what he decides. Engineering does not determine which law takes precedence — a human does. The erasure flow must be fully completable from the parent portal (Meena's side) and the admin queue (Rahul's side). This story covers both actors.

**Acceptance Criteria:**

- [ ] AC-01: Given Meena navigates to Account > Privacy > Request data erasure in the parent portal, when she reads the irreversibility warning ("Requesting erasure will permanently delete all records about [child name]. This cannot be undone.") and types "DELETE" in the confirmation field, then `POST /children/{id}/erasure-request` is called: audit event created (actor=parent, "DPDPA_S12C", "DPDPA_high_risk" flag, timestamp); child record status transitions to "erasure_requested"; an admin task is created in Rahul's queue with a 30-day processing clock starting at the request timestamp.
- [ ] AC-02: Given the erasure request is submitted, when Rahul opens the admin task, then the system presents the Erasure Review screen with: (a) plain-language explanation of the DPDPA/RPWD conflict — not legal jargon; (b) three clearly labeled option cards: Option A — Full erasure (Rahul accepts legal responsibility for the RPWD documentation decision); Option B — Partial erasure with RPWD retention (erase PII and session content; retain anonymised therapy program documentation); Option C — Defer for legal review (30-day clock continues); (c) a 30-day countdown showing days remaining; (d) an informational link "What does RPWD Act 2016 require?" in plain language.
- [ ] AC-03: Given Rahul selects Option A (full erasure) or Option B (partial erasure), when he confirms with the final confirmation dialog, then: an immutable decision record is written (actor=Rahul, decision=A or B, timestamp, "DPDPA_high_risk" flag); the appropriate deletion or anonymisation job runs within 24 hours; Meena's parent portal is updated to reflect completion with a plain-language explanation of what was done.
- [ ] AC-04: Given Option A (full erasure) is confirmed, when the deletion job completes, then: all clinical data records (session notes, therapy programs, SOAP notes, intake form data, uploaded documents, assessments, session records) are hard-deleted from active storage — soft delete is NOT sufficient for a DPDPA erasure request; the consent record is retained as an immutable, anonymised hash in the audit log (it is evidence of lawful processing, not clinical data); a final audit log entry records the completion.
- [ ] AC-05: Given Option B (partial erasure) is confirmed, when the partial erasure job completes, then: personal contact fields (guardian name, mobile, address), session note free-text content, and SOAP note content are deleted; therapy program structure (targets, prompt levels, mastery data) is retained in anonymised form with a retention_justification_note ("RPWD Act 2016 — retained per centre director decision [date]"); Meena's parent portal shows which categories were deleted and which were retained and why (plain language).
- [ ] AC-06: Given the erasure request is pending and the 30-day DPDPA deadline has not been met, when days 15, 25, and 30 pass from the request timestamp, then Rahul receives escalating in-app (and email, for day 25 and 30) reminders: "You have [N] days remaining to process [child name]'s erasure request under DPDPA 2023."

**Edge Cases & Error States:**

- [ ] EC-01: If Rahul selects Option C (defer) at day 29 of the 30-day window, the system does not block the defer — Rahul is legally responsible for the deadline. The system shows a high-urgency warning: "You have 1 day remaining before the DPDPA deadline. Deferring further may constitute a non-compliance event." The defer is still allowed — the system informs but does not override human judgment.
- [ ] EC-02: If the deletion job fails mid-execution (server error during hard delete), the erasure is not partially applied. The job retries up to 3 times. If all retries fail, the admin task is flagged "Erasure failed — requires manual intervention" and Rahul is notified. The erasure request remains in "pending" state; the 30-day clock continues. No partial state is committed.
- [ ] EC-03: If Meena submits an erasure request for a child who still has active upcoming sessions, the system does not block the request — DPDPA rights cannot be blocked because the center finds them inconvenient. The erasure request proceeds. Rahul's admin task includes a note: "This child has [N] upcoming sessions. Consider cancelling sessions before confirming erasure."

**Non-Functional Requirements:**

- Performance: Erasure review screen must load in < 1.5s. Hard delete job for a typical child record (2 years of data) must complete in < 5 minutes.
- Offline: Erasure request submission and Rahul's decision confirmation both require connectivity. The Erasure Review screen can be viewed offline from cache, but no decision can be submitted offline.
- Accessibility: Option cards on the Erasure Review screen must not use color alone to differentiate options. Ensure the "Option B — recommended" label is reviewed with legal before shipping (see Designer Handoff in journey document). Desktop browser compatibility for the Erasure Review screen (Rahul may review on a laptop with a legal advisor present).
- Privacy: ⚠️ DPDPA 2023 Section 12(c) — hard delete is required; soft delete ("deleted" flag) does not satisfy DPDPA erasure. The consent record and audit log entries are the only data that must be retained after erasure (evidence of lawful processing history).

**Dependencies:**
- Blocked by: CONSENT-005 (erasure often follows withdrawal); Parent portal authentication (RBAC-005); Admin task queue infrastructure
- Enables: No downstream story dependency — erasure is a terminal event for the child's clinical record

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Hard delete confirmed: clinical records for the test child are confirmed to be absent from all database tables after full erasure (not soft-deleted)
- [ ] Partial erasure confirmed: retained anonymised program data has no PII fields; consent record hash retained in audit log
- [ ] 30-day reminder cadence tested: day 15, 25, 30 reminders fire at correct intervals
- [ ] EC-02 (failed deletion job retries and admin notification) confirmed
- [ ] EC-03 (active sessions do not block request) confirmed
- [ ] Legal review of Option B "recommended" label completed before UI ships
- [ ] Code reviewed and merged

---

## Story CONSENT-008: Consent Audit Log and Compliance Export

**As a** Center Director (Rahul)
**I want to** view a complete, immutable timeline of all consent events for any child — and export a compliance-ready PDF of the audit log for any child or for the entire center
**So that** I can respond to regulatory inquiries or internal audits with documented evidence of DPDPA compliance without manual record reconstruction

**Inspired by:** DPDPA 2023 accountability obligation (data fiduciary must maintain records of consent); audit log pattern from CentralReach and Motivity compliance modules

**Context:** Rahul is the data fiduciary under DPDPA 2023. He is responsible for demonstrating compliance if a regulatory inquiry occurs. The audit log must be readable on his admin dashboard, searchable, and exportable as a PDF for sharing with regulators or legal counsel. All consent events — initial capture, withdrawals, re-consents, portability requests, erasure decisions — must appear in the timeline.

**Acceptance Criteria:**

- [ ] AC-01: Given Rahul opens a child's record and navigates to the Consent tab, when he views the consent timeline, then it displays all consent events for that child in reverse chronological order with: event type, actor (name and role), timestamp (IST), method (in-person / remote / staff-assisted / withdrawal / erasure), privacy notice version, and a "View details" action for each event.
- [ ] AC-02: Given Rahul taps "Export consent log (PDF)" on a child's Consent tab, when the PDF is generated, then it contains all consent events for that child in a compliance-ready format with: center name, child name (first name + anonymised last name), event history table, generated date, and a note: "This document is generated from the platform's immutable audit log." The PDF is available for download immediately for typical records.
- [ ] AC-03: Given Rahul opens the admin compliance view (Settings > Compliance), when he views the center-wide consent status, then he sees: total children enrolled, count by consent status (Active / Pending / Withdrawn / Erasure requested), children with "Staff-assisted verbal" flags still pending digital consent upgrade, and a "Export all consent status (CSV)" action.
- [ ] AC-04: Given the center-wide CSV export is requested, when Rahul downloads it, then it contains one row per child with: child_id (anonymised), consent_status, consent_date, method, notice_version, last_event_type, last_event_date. No clinical data included. This CSV is a compliance dashboard artifact, not a clinical report.
- [ ] AC-05: Given any consent event is written (CONSENT-002, CONSENT-003, CONSENT-005, CONSENT-007), when the event is recorded, then the audit trail is append-only — no event can be modified or deleted by any user action, admin action, or API call. The schema must enforce this at the database level (no UPDATE or DELETE on audit_events table).

**Edge Cases & Error States:**

- [ ] EC-01: If the audit log for a child shows a consent capture event but the child record's current consent_status does not match the expected state from the event sequence (data integrity discrepancy), a data integrity flag is shown on the Consent tab: "Consent status inconsistency detected — contact support." This is surfaced to Rahul and to the platform admin, not silently ignored.

**Non-Functional Requirements:**

- Performance: Consent timeline loads in < 1.5s for a typical child record (up to 20 consent events over a multi-year therapy history). PDF generation for a single child's consent log completes in < 5 seconds.
- Offline: Consent timeline is readable from cache. Export requires connectivity.
- Privacy: ⚠️ DPDPA 2023 — consent audit log access is restricted to Center Director and Admin roles only. Therapist role (Priya) and Supervisor role (Dr. Sunita) see only the "Consent confirmed [date]" badge — not the full event timeline.

**Dependencies:**
- Blocked by: AUDIT-001 (audit log infrastructure must exist and be append-only); CONSENT-002, CONSENT-003, CONSENT-005, CONSENT-007 (these stories generate the events that populate the log)
- Enables: DPDPA regulatory inquiry response workflow; no technical downstream dependency

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Audit log immutability confirmed: attempted UPDATE and DELETE on audit_events table confirmed to be blocked at DB schema level
- [ ] Center-wide CSV export verified: contains no clinical data fields
- [ ] EC-01 (data integrity flag) verified
- [ ] Consent timeline correctly shows events from CONSENT-002, CONSENT-003, CONSENT-005, and CONSENT-007
- [ ] Code reviewed and merged

---

## Backlog Table

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| CONSENT-001 | Privacy Notice Display | Meena / Rahul | S | P0 | AUTH-001, EMR-001 |
| CONSENT-002 | Parental Consent Capture (In-Person) | Rahul / Meena | M | P0 | CONSENT-001 |
| CONSENT-003 | Remote Consent via Shared Link | Rahul / Meena | M | P1 | CONSENT-001, CONSENT-002 |
| CONSENT-004 | Consent Gate Enforcement Across Clinical Features | System | L | P0 | CONSENT-002, AUTH-001 |
| CONSENT-005 | Consent Withdrawal | Meena | M | P1 | CONSENT-002, RBAC-005 |
| CONSENT-006 | Data Portability — Parent Record Download | Meena | L | P2 | RBAC-005 |
| CONSENT-007 | Data Erasure Request and RPWD Conflict Handling | Meena / Rahul | XL | P2 | CONSENT-005, RBAC-005 |
| CONSENT-008 | Consent Audit Log and Compliance Export | Rahul | M | P1 | AUDIT-001, CONSENT-002 |

**Complexity key:** S = 1 day; M = 2–3 days; L = 3–5 days; XL = must be split before sprint planning
**Priority key:** P0 = product cannot function without this; P1 = ships with v1 of this journey; P2 = next iteration

**Build sequence (hard ordering enforced by dependency chain):**
1. CONSENT-001 (privacy notice — prerequisite UX for consent capture)
2. CONSENT-002 (in-person consent capture — core compliance mechanism)
3. CONSENT-004 (gate enforcement — must be enforced as soon as first consent records exist)
4. CONSENT-008 (audit log — should be in place before any real consent records are created)
5. CONSENT-003 (remote consent — extends the capture method, same backend as CONSENT-002)
6. CONSENT-005 (withdrawal — parent data subject rights)
7. CONSENT-006 (data portability — parent data subject rights, lower frequency)
8. CONSENT-007 (erasure — most complex, lowest frequency; split into sub-stories before sprint planning)

**Note on CONSENT-007 (Erasure) sprint readiness:**
CONSENT-007 is marked XL — it must be split before entering a sprint. Suggested split:
- CONSENT-007a: Erasure request submission (Meena's side — portal, typed DELETE, request creation, admin task)
- CONSENT-007b: RPWD conflict review screen (Rahul's side — decision cards, conflict explanation, defer/confirm flow)
- CONSENT-007c: Hard delete execution job (backend — Option A full erasure cascading delete)
- CONSENT-007d: Partial erasure anonymisation job (backend — Option B PII deletion + program structure anonymisation)

Additionally, CONSENT-007 requires a formal legal opinion on the DPDPA/RPWD conflict before the Erasure Review screen copy can be finalized. Engineering should not begin CONSENT-007b until legal review is complete.

---

## ⚠️ Feature Factory Disclaimer

These requirements were defined from journey document synthesis (journey-00-dpdpa-consent-management.md), DPDPA 2023 statutory reading, and structural adaptation from US/EU health SaaS consent patterns — not from validated primary research with Indian therapy centers, parents, or Indian legal counsel.

**What we assumed but haven't validated:**

- [ASSUMPTION] Indian therapy center directors (Rahul) understand that DPDPA 2023 creates a binding compliance obligation for processing minors' health data and will see the consent flow as a compliance relief rather than friction. Primary research has not confirmed DPDPA awareness among Indian center directors.
- [ASSUMPTION] Indian parents (Meena) are willing and able to engage with a structured digital consent screen on a shared tablet or their own Android phone. Tech literacy and comprehension of a plain-language privacy notice have not been tested with this specific parent population.
- [ASSUMPTION] The RPWD Act 2016 creates a real, felt documentation retention obligation that meaningfully constrains erasure decisions at Indian private therapy centers. The specific record categories and retention periods required under RPWD Act have not been confirmed with Indian legal counsel.
- [ASSUMPTION] Parents will use the self-service parent portal to exercise data subject rights (withdrawal, portability, erasure) rather than contacting the center via WhatsApp. If the parent portal has low adoption, all data subject rights will arrive via WhatsApp and require admin-mediated processing in the admin panel.
- [ASSUMPTION] The "staff-assisted verbal consent" fallback will be used responsibly and followed up with digital consent at the next visit. The rate at which verbal consent gets upgraded to digital consent is unknown.

**What a researcher would ask before building this:**

- Have any Indian therapy center directors received a DPDPA inquiry or complaint? What is their current awareness level of DPDPA 2023 obligations for minors' health data?
- Can we observe an actual intake session and test whether a parent understands and engages with a consent screen? What does she do when handed a tablet showing the privacy notice?
- What does a formal Indian legal opinion on the DPDPA/RPWD conflict say? Specifically: what records must a center retain under RPWD Act 2016, for how long, and does this obligation override DPDPA erasure rights in all cases or only for certain record types?

**What the Product Consultant would challenge:**

- CONSENT-006 (data portability) and CONSENT-007 (erasure) are low-frequency, high-complexity features. The Product Consultant would challenge whether these belong in v1 or whether Phase 1 should deliver only CONSENT-001 through CONSENT-005 and CONSENT-008 — covering the mandatory consent capture and withdrawal rights — with portability and erasure following in Phase 2 when (a) primary research confirms how often Indian parents actually exercise these rights and (b) legal counsel has signed off on the RPWD/DPDPA conflict resolution.
- The parent portal assumption deserves scrutiny before building the self-service data subject rights paths (B-i through B-iii). An admin-mediated fallback (Rahul processes requests received via WhatsApp through an admin panel) may be more resilient as a Phase 1 approach, with the parent self-service portal following once portal adoption is established.

**Risk level per story:**

- CONSENT-001, CONSENT-002, CONSENT-004: **Low risk** — regulatory non-negotiable; product cannot legally store clinical data without these
- CONSENT-003, CONSENT-005, CONSENT-008: **Medium risk** — compliance-driven but uncertain whether the specific UX patterns match Indian parent behavior
- CONSENT-006: **Medium-High risk** — legally required right but self-service portal path is assumption-heavy; admin-mediated fallback may be more appropriate for Phase 1
- CONSENT-007: **High risk** — legally complex; RPWD/DPDPA conflict requires formal legal opinion before shipping; erasure execution is irreversible; split into sub-stories and gate on legal review before sprint planning

Use the `/research` agent to validate DPDPA awareness (H-06) and parent consent UX comprehension before sprint planning.
Use the `/scope` agent to challenge whether CONSENT-006 and CONSENT-007 belong in v1 or Phase 2.
Use the `/design-critique` agent to review the Privacy Notice screen and the Erasure Review screen before prototyping — both involve high-stakes interactions on low-end Android hardware.
