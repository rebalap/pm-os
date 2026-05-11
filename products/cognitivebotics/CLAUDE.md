# Product Context: Cognitivebotics

Load this file when working on any feature for the Cognitivebotics product.

---

## What This Product Is

Cognitivebotics is an AI-powered digital learning platform that extends evidence-based therapy for neurodiverse children beyond the clinic and into the home. Therapists use a web application to design personalized learning plans; children engage with those plans through a gamified mobile/iPad app; parents participate through training videos and behavior journaling tools.

The product is **not** a clinic management or EHR system. Its core value proposition is closing the gap between clinic sessions and daily home practice — converting passive screen time into structured, therapeutically guided learning.

**Conditions served:** Autism Spectrum Disorder, ADHD, Down Syndrome, and other learning differences.
**Age range:** 2–18 years.

> **India context note:** The clinical workforce in India is primarily RCI-licensed special educators and behavioral therapists. BCBA certification (US-based, BACB-issued) is rare in India — fewer than ~500 nationally. The product has a BCBA on its clinical team but must be designed to serve non-BCBA practitioners who form the majority of the market.

## Company Background

- **Founded by** Udaya Dintyala, motivated by his son Ram's autism intervention journey
- **CEO:** Dr. Raja Sekhar G | **CTO:** Sudheer Narra | **Co-founder & Advisor:** Meenakshi Kumar
- **Clinical team:** Anastasia Trofilova (BCBA), Dr. Srinivas Puvvada (Program Director)
- **Board advisors:** Dr. Mark Aszkenasy (NHS UK autism specialist), Eugene Huang (Chairman, TIS Taiwan)
- **Headquarters:** India; international expansion signals in UK and Taiwan

## Clinical Evidence

A 12-month observational study (published in JMIR Neurotechnology, 2025) examined the platform with 40 participants (ages 2–18, single center, India):

| Measure | Improvement | Significance |
|---|---|---|
| CARS (autism severity score) | −15.18% | P<.001 |
| Vineland Social Age | +56.84% | P<.001 |
| Receptive language (REEL) | +56.22% | P<.001 |
| Expressive language (REEL) | +59.93% | P<.001 |

Control group showed smaller, non-significant gains. Study limitations: small sample (n=40), single center, high attrition (59%). This is the first published validation of the platform.

## Current Stage

See `stage-tracker.md` for where each workstream currently stands.

## Target Users

| User | Role | Core job | Pain today |
|---|---|---|---|
| Therapist / Special Educator | Designs and assigns learning plans | Configure programs for each child; monitor home-session data | No structured tool for remote delivery; relies on ad-hoc parent WhatsApp updates |
| Parent / Family | Primary home-practice partner | Conduct home sessions, journal behaviors, receive training | Unsure what to do between clinic appointments; informal WhatsApp guidance only |
| Child (neurodiverse, 2–18) | Learner | Engage with gamified learning content | Passive screen time; no purposeful learning structure |
| Therapy Center Admin / Director | Manages therapist workflows and client relationships | Assign therapists, track engagement, manage licensing | Lacks visibility into between-session engagement and parent compliance |
| School / Institutional Professional | Supports inclusion and IEP delivery | Coordinate individualized plans with external therapy providers | Siloed from therapy center data; no shared progress record |

## Business Model

- **B2B2C:** Platform is sold to therapy centers and schools (B2B); therapists then deploy it with their parent/child clients (B2C through the center)
- Therapy centers may bundle or resell the software as part of their service packages
- Subscription-based pricing; exact tiers not public
- Multi-segment packaging: per-therapist costs, physical and virtual session hours, ILP assignments, device costs
- Growth partnerships (e.g., Butterfly Learnings) include features for licensing, exclusivity, co-creation, and reporting at scale

## Key Constraints

- **Home use is the primary context** — the child-facing app must work for parents with minimal clinical training; assume low digital literacy for some parent segments
- **Therapist web app is clinic or desk use** — can assume more screen space, less time pressure than in-session tools
- **Offline resilience** — connectivity in Indian homes varies; sessions should not fail mid-play due to intermittent data
- **Device diversity** — parents commonly use low-to-mid-range Android phones; do not assume iOS or high-end hardware
- **Multi-language** — English UI may not serve all parents; Hindi and regional languages are a near-term need; Arabic content is required for Middle Eastern expansion
- **Permission and consent** — must make data collection and communication permissions explicit; sensitive health data of minors applies under DPDPA 2023
- **Non-clinical parent users** — training and behavior journaling must be self-explanatory; zero clinical jargon in parent-facing surfaces
- **WhatsApp dependency** — current parent-therapist communication happens over WhatsApp; the platform must offer clear incremental value over this behavior, not simply try to replace it

## Regulatory & Compliance Context

- **DPDPA 2023** — India's Digital Personal Data Protection Act; applies to personal and health data of minors; consent requirements must be explicit
- **RCI** — Rehabilitation Council of India; the statutory licensing body for special educators; primary clinical credential in India (not BCBA)
- **RPWD Act 2016** — Rights of Persons with Disabilities Act; governs documentation and access requirements for persons with autism and other disabilities
- **No HIPAA** — do not apply US HIPAA frameworks; use DPDPA 2023 and RCI guidelines as the regulatory reference

## Platform Architecture

| Surface | Primary user | Access |
|---|---|---|
| Web application (desktop) | Therapist / Clinician | Browser (Windows, Safari) |
| Mobile / iPad app | Parent and child | iOS App Store, Google Play |
| Admin portal | Center Director / Admin | Web |

## Domain Terminology

- **ILP** — Individualized Learning Plan; the personalized program assigned to each child
- **LO** — Learning Objective; a skill cluster within an ILP
- **Mastery** — a task correct for 3 consecutive days; 4 mastered tasks = LO mastered
- **Prompted response** — child response after therapist or parent prompt
- **Independent response** — child response without prompting
- **Attempts** — total trials in a session, used alongside prompted/independent counts
- **Days played** — engagement metric; number of days child completed a session
- **Sessions** — physical (clinic) or virtual (home) therapy interactions
- **No-show** — scheduled session missed by the child/family
- **Cancellation** — session cancelled before the scheduled time
- **Social story** — personalized narrative to teach social behavior; AI-generation is a planned feature
- **Skill categories (12)** — Attending, Imitation, Receptive Language, Expressive Language, Visual Processing, Social, Play, Self-Help, Reading & Writing, Arithmetic, Group Collaboration

## AI Capabilities (Current & Planned)

- **AI insights:** Analysis of eye contact, voice modulation, posture, and emotion during sessions
- **Personalized plan generation:** AI-assisted ILP creation based on child profile and progress data
- **Social story generation:** AI-drafted narratives personalized to the child (planned)
- **Adaptive content delivery:** Adjusting difficulty and pacing based on session performance data

## Active Workstreams

> Update this section as workstreams open or close. Reference `stage-tracker.md` for detail.

- [ ] Add active workstreams here

## Key Research Findings

> Summarize validated findings here; link to research docs when available.

- **[VALIDATED ✓ 2025]** Platform use over 12 months produces statistically significant improvements in autism severity, social development, and language — per JMIR Neurotechnology observational study (n=40, India)
- [ ] Add additional validated findings as they are confirmed

## Important Assumptions Still Open

> [ASSUMPTION] = not yet validated by internal research or user evidence

- [ASSUMPTION] Parents in Indian therapy center cohorts have sufficient digital literacy to use the mobile app independently between sessions
- [ASSUMPTION] Therapists find the web-based ILP builder faster and more useful than their current manual planning methods
- [ASSUMPTION] Home-session completion rates are high enough to generate meaningful progress data (attrition was 59% in the clinical study)
- [ASSUMPTION] Therapy center directors will pay for the platform primarily because it improves parent engagement and retention, not because of clinical outcomes data
- [ASSUMPTION] Arabic content requirements for Middle Eastern clients can be served by translating existing content without rebuilding the content model
- [ASSUMPTION] WhatsApp cannot be fully replaced for parent-therapist communication — the product must integrate with or complement it
