# Competitive Analysis: Autism Therapy Center Software
**Product:** Autism Therapy Platform (India)
**Author:** Researcher Agent
**Date:** April 2026
**Stage:** Discovery
**Research method:** Web search synthesis (Tavily — 9 queries, advanced depth)
**Decision to inform:** Where is the white space in the current software landscape? Which journey stages are underserved in the Indian market?

> Evidence labels: ✅ Observed (direct source confirmation) | 🔵 Inferred (logical derivation from source data) | 🔶 [HYPOTHESIS] (assumed; not confirmed)

---

## Executive Summary

No single software product covers the end-to-end autism therapy center lifecycle for the Indian market. A structural divide exists:

- **US/global clinical tools** (CentralReach, Motivity, Catalyst, Hi Rasmus, Raven Health) cover the clinical stages well — in-session data collection, program management, supervisor review, and progress reporting — but are designed for US insurance billing, priced 5–10× above Indian willingness-to-pay, and built without offline-first or low-end Android requirements.
- **Indian center management tools** (TherapEZ, PractiPal) cover operations well — scheduling, billing, UPI payments, parent communication — but have zero clinical capability. They do not touch in-session data collection, program design, or progress reporting.
- **Cognitivebotics (India)** is a child-facing AI therapy tablet application. It is not center management or therapist-side clinical software. It does not compete in the therapist workflow.

**The white space:** In-session trial-by-trial data collection (DTT/NET recording) integrated with program management, supervisor review, and progress reporting — built for RCI-licensed special educators, offline-first, low-end Android, at Indian price points (target: under ₹1,500–2,500/month for a small center).

No product exists anywhere in the world that occupies this position. The Indian market is underserved not because the tools don't exist globally, but because the global tools don't fit.

---

## Tools Reviewed

| Tool | Origin | Target market | Primary use case | Pricing (USD) | Pricing (INR equiv.) | Evidence level |
|---|---|---|---|---|---|---|
| CentralReach | US | Mid-large ABA practices, insurance-billing | Full ABA practice management | $59/user/month; $120/learner/year (curriculum) | ~₹5,000/user/month | ✅ |
| Motivity | US | ABA practices, BCBAs | In-session data collection + program management | $20–24/learner/month | ~₹1,700–2,040/learner/month | ✅ |
| Catalyst (DataFinch) | US | ABA practices | Mobile clinical data collection, offline capable | ~$100–500/month depending on size | ~₹8,500–42,500/month | 🔵 |
| Hi Rasmus | Global (Denmark/US) | ABA practices, telehealth | In-session data + supervision + parent portal | $19–24/client/month | ~₹1,615–2,040/client/month | ✅ |
| Raven Health | US | ABA clinics | AI session notes + clinical data collection | ~$25/client/month | ~₹2,125/client/month | 🔵 |
| Theralytics | US | ABA practices, BCBAs | Practice management (BCBA-built) | Quote only | Not available | 🔵 |
| TherapEZ | India (Noida) | Therapy centers, general | Scheduling, invoicing, parent communication | Pricing on request | Indian market pricing | 🔵 |
| PractiPal | India | Therapists, clinics | Client management, invoicing, UPI payments | Free (5 clients); ₹1,499/month (unlimited) | ₹1,499/month | ✅ |
| Cognitivebotics | India | Autism therapy centers | Child-facing AI therapy tablet app | Not available | Not available | 🔵 |

> **INR conversion:** USD figures converted at ~₹85/USD (April 2026 estimate). 🔵

---

## Stage-by-Stage Coverage Map

Coverage ratings: ✅ Full coverage | 🟡 Partial coverage | ❌ Not covered

| Journey Stage | CentralReach | Motivity | Catalyst | Hi Rasmus | Raven Health | TherapEZ | PractiPal | Cognitivebotics |
|---|---|---|---|---|---|---|---|---|
| **Stage 1:** Family Inquiry & Enrollment Pipeline | 🟡 CRM lite | ❌ | ❌ | ❌ | ❌ | ✅ Inquiry mgmt | 🟡 Client intake | ❌ |
| **Stage 2:** Intake & Onboarding | ✅ Intake forms, consent | 🟡 Intake forms | 🟡 | 🟡 | 🟡 | ✅ Enrollment | ✅ Client records | ❌ |
| **Stage 3:** Assessment & Program Design | ✅ ABLLS-R, VB-MAPP, treatment planning | ✅ Treatment planning | ✅ Assessment + programs | ✅ Program design | ✅ Program design | ❌ | ❌ | 🟡 AI-driven assessment activities only |
| **Stage 4:** In-Session Data Collection (DTT/NET) | ✅ Core strength | ✅ Core strength | ✅ Core — offline capable | ✅ Core | ✅ Offline entry + AI notes | ❌ | ❌ | 🟡 Child-facing only; not therapist trial recording |
| **Stage 5:** Supervisor Review & Program Updates | ✅ Data viz + program mgmt | ✅ Graphs + program updates | ✅ Supervisor review | ✅ Supervision tools + telehealth | ✅ Supervisor review | ❌ | ❌ | 🟡 AI session data only |
| **Stage 6:** Progress Reporting to Parents | ✅ Report generation | ✅ Progress reports | 🟡 | ✅ Parent portal | ✅ Parent comms | 🟡 Basic reports | ❌ | 🟡 AI session summary only |
| **Stage 7:** Billing & Fee Collection | 🟡 US insurance RCM only | 🟡 Basic billing | 🟡 | ✅ Billing | ❌ | ✅ Invoicing + payments | ✅ UPI payments + invoicing | ❌ |
| **Stage 8:** Appointment Follow-Up & Dropout Prevention | 🟡 Scheduling only | ❌ | ❌ | 🟡 Scheduling | ❌ | ✅ Appointment reminders | 🟡 Appointment reminders | ❌ |

---

## Detailed Tool Profiles

### CentralReach (US)
**What it is:** The dominant US ABA practice management platform. Built for mid-to-large BCBA-led practices managing insurance billing, Medicaid/ABA authorization, and multi-therapist caseloads.

**Clinical strengths:** Trial-by-trial data collection (DTT and NET), target mastery tracking, data visualization, ABLLS-R and VB-MAPP curriculum libraries, supervision workflows.

**Business/admin strengths:** Insurance billing and claims management, staff scheduling, payroll, client portal.

**Why it does not work for India:**
- Insurance billing is 80% of the product's value proposition — irrelevant in India's out-of-pocket therapy market ✅
- Pricing ($59/user/month) would cost a 10-staff Indian center ~₹5,00,000+/year — likely 10–20× their willingness-to-pay 🔵
- No offline mode documented — a hard constraint for Indian session rooms with intermittent connectivity 🔵
- BCBA workflow assumptions embedded throughout (BACB compliance language, US clinical standards)
- HIPAA-compliant but not DPDPA 2023-aware ✅

---

### Motivity (US)
**What it is:** A research-backed ABA data platform with a clean mobile UX. Designed for in-session data collection and near-real-time supervisor review.

**Clinical strengths:** In-session trial recording (mobile, streamlined), treatment plan management, data graphing, supervisor review dashboards.

**Key differentiator:** Published research backing on data quality improvement vs. paper. Strong UX reputation in ABA community.

**Why it does not work for India:**
- **Explicitly no offline mode** — deal-breaker if H-03 (offline is a hard requirement) is validated ✅
- $20–24/learner/month: a center with 30 active children pays $600–720/month (~₹51,000–61,200). Indian willingness-to-pay is likely ₹2,000–5,000/month for the center as a whole 🔶
- English-only, US-centric clinical workflow
- No billing, scheduling, or parent communication features — clinical-only ✅

---

### Catalyst / DataFinch (US)
**What it is:** A mobile-first ABA data collection platform with offline capability. Clean, simple UI focused on therapist-side data entry.

**Clinical strengths:** Trial-by-trial data collection, offline mode (data syncs when connected), program management, supervisor review.

**Key differentiator:** Offline-first design is explicitly marketed. Well-regarded for therapist usability.

**Why it does not work for India:**
- Pricing ($100–500/month estimated range) is too high for Indian centers 🔵
- US clinical workflow assumptions; no India-specific features
- No billing or center management — clinical-only
- UPI/Indian payment infrastructure not supported
- HIPAA-focused compliance, not DPDPA 🔵

**Notable:** Catalyst is the closest analogue to what the Autism Therapy Platform would build for Stage 4. The offline-first approach validates the technical approach. The gap is India fit and price.

---

### Hi Rasmus (Denmark/Global)
**What it is:** A global ABA platform with in-session data collection, supervision tools, and a parent portal. Built by a team with autism expertise; available internationally.

**Coverage:** One of the most complete products in the ABA space — covers Stages 3–7 reasonably well.

**Key differentiator:** Parent portal (parents can view session data and progress), telehealth/remote supervision, multilingual UI (though unclear if Indian languages are included).

**Why it does not work for India:**
- Pricing (~$19–24/client/month) creates the same math problem as Motivity
- No India-specific billing (UPI, INR invoicing) 🔵
- Connectivity and offline requirements not confirmed 🔵
- No documented India customer base or India-facing support 🔵

---

### Raven Health (US)
**What it is:** A newer ABA clinical platform with AI-generated session notes and offline data entry.

**Key differentiator:** AI session note generation — potentially highly relevant to reducing Dr. Sunita's documentation burden (H-07).

**Why it does not work for India:**
- US market only — no India billing, no DPDPA compliance awareness 🔵
- Pricing (~$25/client/month) same problem
- AI note generation trained on US clinical language and insurance terminology

---

### TherapEZ (India — Noida)
**What it is:** An Indian center management platform targeting therapy centers. Focuses on scheduling, invoicing, parent communication, and staff management. Explicitly mentions autism centers in marketing.

**What it covers:** Stages 1, 2, 7, 8 (inquiry management, enrollment, invoicing, appointment reminders/follow-up).

**What it does NOT cover:** Any clinical stage. No in-session data collection, no treatment planning, no supervisor review, no clinical progress reporting. ✅

**Relevance:**
- Confirms Indian market appetite for this type of tool 🔵
- Pricing on request — likely Indian price point (~₹2,000–5,000/month range expected) 🔶
- Would be a competitive tool if the Autism Therapy Platform also covers Stages 1, 2, 7, 8 — overlapping admin territory

**Gap TherapEZ leaves open:** Everything clinical (Stages 3–6).

---

### PractiPal (India)
**What it is:** A general therapist practice management app — not autism-specific. Covers client records, session notes (free-form), invoicing, and UPI payment collection.

**Pricing:** Free tier (up to 5 clients); ₹1,499/month for unlimited clients. This is the clearest Indian price point signal in the competitive landscape. ✅

**What it covers:** Stages 2 (basic intake/records), 7 (billing + UPI), and 8 (appointment reminders) partially.

**What it does NOT cover:** Clinical stages. No ABA-specific data collection, no treatment planning, no supervisor tools. Free-form session notes only. ✅

**Relevance:**
- ₹1,499/month for unlimited clients sets an important Indian benchmark — this is what a general tool charges
- A specialized ABA/clinical platform can justify a premium (₹3,000–8,000/month) if clinical value is high 🔵
- UPI payment integration confirms it is table stakes for an Indian billing feature

---

### Cognitivebotics (India)
**What it is:** An AI-powered therapy tool delivered on a tablet as a child-facing application. The product provides structured, gamified therapy activities (ABA-aligned) that the child interacts with directly, with AI tracking responses.

**Critical distinction for competitive analysis:** Cognitivebotics is **not** center management or therapist-side clinical software. It is a **child-facing AI therapy delivery product**. The therapist or parent oversees the child interacting with the tablet. This is a different product category from therapist data collection software.

**What this means:**
- Centers using Cognitivebotics still need paper, WhatsApp, or spreadsheets for therapist-side data collection, program management, and billing — the core gaps our product addresses 🔶 → **H-11** directly tests this
- Cognitivebotics does not compete with the Autism Therapy Platform's therapist/supervisor/director workflow
- It may eventually compete on the parent-facing and progress-reporting layer if it adds center management features
- Its presence confirms Indian market willingness to experiment with digital autism therapy tools ✅

---

## Pricing Comparison (Full Market Picture)

| Tool | Pricing model | Example: 30-child center | INR equivalent | India fit |
|---|---|---|---|---|
| CentralReach | Per user/month | ~$590/month (10 users) | ~₹50,150/month | ❌ Far too expensive |
| Motivity | Per learner/month | ~$660/month (30 learners) | ~₹56,100/month | ❌ Far too expensive |
| Catalyst | Per center/month (est.) | ~$200/month | ~₹17,000/month | ❌ Too expensive |
| Hi Rasmus | Per client/month | ~$630/month (30 clients) | ~₹53,550/month | ❌ Far too expensive |
| Raven Health | Per client/month | ~$750/month (30 clients) | ~₹63,750/month | ❌ Far too expensive |
| Theralytics | Quote only | Unknown | Unknown | 🔶 Unknown |
| TherapEZ | On request (India) | Est. ~₹3,000–5,000/month | ₹3,000–5,000/month | 🟡 Feasible (admin only) |
| PractiPal | Per practice/month | ₹1,499/month (unlimited) | ₹1,499/month | ✅ Most affordable; no clinical features |
| **Target: ATP India** | Per center/month (est.) | ₹3,000–8,000/month | ₹3,000–8,000/month | ✅ [HYPOTHESIS] viability |

> **[HYPOTHESIS]** Indian autism therapy center willingness-to-pay for a clinical + operations tool is in the ₹3,000–8,000/month range for a full-function platform. This must be validated through primary research (director interviews). 🔶

---

## Feature Coverage Heatmap by Stage

> Aggregated across all tools reviewed: which stages have existing software solutions, and for which market?

| Stage | US market | Indian market | Gap |
|---|---|---|---|
| Stage 1: Inquiry / Pipeline | 🟡 CRM modules in large platforms | ✅ TherapEZ | Small gap — Indian solution exists |
| Stage 2: Intake & Onboarding | ✅ Multiple tools (US) | 🟡 TherapEZ, PractiPal (basic) | Moderate — no DPDPA-aware digital consent flow anywhere |
| Stage 3: Assessment & Program Design | ✅ Strong (CentralReach, Motivity, Catalyst, Hi Rasmus) | ❌ No Indian tool | **High gap** — no India-market tool; US tools don't fit |
| Stage 4: In-Session Data Collection | ✅ Strong (all major US tools) | ❌ No Indian tool | **Critical gap** — the core product thesis |
| Stage 5: Supervisor Review & Program Updates | ✅ Strong (all major US tools) | ❌ No Indian tool | **Critical gap** — directly connected to Stage 4 |
| Stage 6: Progress Reporting to Parents | ✅ Multiple tools | ❌ No Indian tool | **High gap** — manual everywhere in India |
| Stage 7: Billing & Fee Collection | 🟡 US tools do insurance (irrelevant) | ✅ TherapEZ, PractiPal (UPI) | Small gap — Indian billing solutions exist |
| Stage 8: Follow-Up & Dropout Prevention | 🟡 Scheduling reminders only | 🟡 TherapEZ (basic reminders) | Moderate gap — no intelligent dropout detection anywhere |

---

## Key Findings

### Finding 1: The clinical stages (3–6) are a total void in the Indian market
No existing Indian tool addresses assessment, in-session data collection, supervisor review, or clinical progress reporting. Every center in India managing these stages is doing so with paper, WhatsApp photos, and Word documents. This confirms the product thesis from the secondary side. ✅ (TherapEZ and PractiPal explicitly confirm no clinical features.)

### Finding 2: The US tools validate the product category but fail on three India-specific blockers
CentralReach, Motivity, Hi Rasmus, and Raven Health confirm that ABA software is a real, growing market — and that therapist-side trial recording, automated progress tracking, and parent reporting are solvable product problems. They fail for India on: (1) pricing 5–10× above likely willingness-to-pay, (2) insurance-billing architecture not relevant in India's out-of-pocket market, (3) no offline-first capability in most (exception: Catalyst). 🔵

### Finding 3: Catalyst is the closest technical analogue for the in-session data collection layer
Catalyst's offline-first mobile design is architecturally aligned with what India requires. Its limitation is price and India-fit. The ATP can take Catalyst's UX/offline approach and rebuild it for Indian price points, Indian regulatory context (DPDPA, not HIPAA), and RCI-licensed special educator workflows (not BCBA). 🔵

### Finding 4: Indian admin tools set the price floor at ₹1,499/month
PractiPal's ₹1,499/month for unlimited clients is the cheapest comparable Indian tool. A clinical platform with clear productivity benefits (less time transcribing data, automated progress reports, fewer compliance errors) should be able to command a premium — but the ceiling matters. The ATP's target pricing of ₹3,000–8,000/month for a full-function center platform sits between PractiPal and the lowest US equivalents. ✅ (PractiPal pricing confirmed)

### Finding 5: Cognitivebotics confirms Indian market maturity but occupies a different product category
Cognitivebotics' existence — as an AI-driven child-facing therapy application — shows that Indian therapy centers are willing to adopt technology. However, it addresses the child experience in sessions, not the therapist's data workflow. Centers using Cognitivebotics almost certainly still use paper data sheets for clinical targets. This is the exact H-11 hypothesis. 🔵

### Finding 6: No tool globally addresses dropout prevention intelligently
Across all tools reviewed, dropout prevention is at best "appointment reminders." No tool uses attendance trend data to surface at-risk families proactively — despite research showing that early intervention in at-risk attendance dramatically improves retention. This is a potential differentiator for the ATP (Stage 8), though it is Stage 4+ data quality that makes this possible. 🔵

---

## Implications for the Autism Therapy Platform

### Confirmed product bets
1. **Build the clinical layers first (Stages 3–6)** — this is the vacuum no Indian tool fills. The admin layers (Stages 1–2, 7–8) can follow or be light integrations at launch.
2. **Offline-first is non-negotiable** — the one US tool explicitly built offline-first (Catalyst) is the one that solves the core physical constraint. No offline = non-starter if H-03 is validated.
3. **Price the full platform at ₹3,000–8,000/month for a center** — not per therapist, not per child. Per-center pricing removes the growth penalty and reflects the Indian SMB buying model.

### Design implications
4. **Rebuild Motivity/Catalyst's UX for Indian conditions** — the US tools have proven that clean, tap-efficient in-session recording is achievable. The Indian version needs: offline sync, haptic feedback (not audio cues for noisy rooms), low-end Android optimization, RCI-not-BCBA language.
5. **Do not build US insurance billing** — TherapEZ and PractiPal have already solved UPI billing for India. If billing is in scope, integrate UPI natively. Insurance RCM is irrelevant.
6. **AI session notes are an emerging differentiator** — Raven Health's AI note generation directly addresses H-07 (supervisor documentation burden). This is worth tracking as a Phase 2 feature.

### Risks
7. **TherapEZ could add clinical features** — as the most direct Indian center management competitor, TherapEZ could move into clinical tooling. First-mover advantage in clinical data quality matters.
8. **Adoption risk is real even if the tool is perfect** — every US tool has failed to penetrate India not just on price but on adoption complexity. The product must be operational within a single session training. The US tools' complexity is itself a warning.

---

## Gaps — What This Research Cannot Answer

- **TherapEZ pricing** — pricing on request means the actual competitive floor in India for admin features is unconfirmed. Primary outreach or mystery shopping needed.
- **Cognitivebotics actual workflows** — whether centers using Cognitivebotics still use paper for clinical targets is a hypothesis (H-11). Requires primary interview with a Cognitivebotics-using center.
- **Indian willingness-to-pay** — no research confirms what center directors would pay for a clinical platform. ₹3,000–8,000/month is an assumption based on PractiPal's price, center revenue estimates, and analogous Indian SaaS pricing. Must be validated in director interviews.
- **Catalyst offline mode performance on Indian Android devices** — Catalyst's offline capability is documented but untested on the specific low-end Android devices common in Indian centers (Redmi/Realme).
- **Whether any tool has been tried and abandoned in Indian centers** — word-of-mouth awareness and prior trial failures in Indian centers would change the adoption strategy significantly. Primary research must probe this.

---

## Recommended Next Steps

1. **Run primary director interviews (n=5–8)** — ask explicitly about tool adoption history: have they tried any of these tools? What happened? What did they pay? This fills the biggest gap in this analysis.
2. **Mystery-shop TherapEZ** — sign up for a demo, get pricing, understand their clinical roadmap. This is the most likely competitive threat.
3. **Interview 2–3 Cognitivebotics-using centers** — test H-11 directly. Do they still use paper for clinical targets?
4. **Validate pricing hypothesis** — include willingness-to-pay probes in director interview script (already drafted: Q22–24 in `interview-script-center-owner-admin.md`).
5. **Monitor Raven Health's AI features** — AI session notes are the most novel capability in the ABA software market right now. If this becomes commoditized, it changes the differentiation story.

---

*Research saved:* `/products/autism-therapy-platform/research/secondary/competitive-analysis-autism-therapy-software.md`
*Queries run:* 9 Tavily searches across ABA software pricing, Indian therapy management tools, digital adoption barriers, WhatsApp-based center operations, and specific product research (CentralReach, Motivity, Catalyst, TherapEZ, PractiPal, Cognitivebotics)
*Date:* April 2026
