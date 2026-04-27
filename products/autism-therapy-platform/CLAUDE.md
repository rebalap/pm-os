# Product Context: Autism Therapy Platform (India)

Load this file when working on any feature for the Autism Therapy Platform.

---

## What This Product Is

An enterprise software platform for autism therapy centers in India. It provides tools
for therapists and special educators to manage therapy programs, collect session data,
track child progress, and coordinate with parents — within a data-private, India-specific
environment designed for the realities of Indian clinical practice.

> **India context note:** BCBA and RBT certifications (US-based, issued by BACB) are rare
> in India. The primary clinical workforce is RCI-licensed special educators and behavioral
> therapists trained in ABA. Design, language, and workflows must reflect this reality.

## Current Stage
See `stage-tracker.md` for where each workstream currently stands.

## Target Users

| User | Role | Core job | Pain today |
| --- | --- | --- | --- |
| Special Educator / Behavior Therapist | Delivers ABA and skill-building therapy | Log behavioral data and program progress during live sessions | Data collection is done on paper or WhatsApp; no structured tool exists |
| Senior Therapist / Clinical Supervisor | Designs therapy programs, supervises junior staff | Review session data, update programs, write progress reports | Reporting is manual and time-consuming; data lives in notebooks and spreadsheets |
| Center Director / Founder | Runs the center (often a clinician themselves) | Track attendance, billing, staff utilization, parent communication | No single system; uses a patchwork of WhatsApp, Excel, and paper |
| Parent / Family | Child's primary caregiver (extended family often involved) | Stay informed, practice home programs, track progress | Receives clinical reports they don't understand; updates happen over WhatsApp informally |

## Business Context

- Indian therapy centers are typically small (5–20 staff), often founder-led by a therapist who started the center
- No dominant software competitor — most centers use Excel, Google Sheets, WhatsApp, and paper
- Therapy is primarily **out-of-pocket** — no insurance mandates for ABA in India (unlike the US)
- Price sensitivity is high; willingness-to-pay is lower than US market but growing in metro cities
- Government schemes (UDID, RPWD Act 2016, Divyangjan) create documentation and compliance requirements
- Clinical staff adoption is the make-or-break variable — if therapists don't use it during sessions, the product fails
- WhatsApp is deeply embedded in parent communication; any solution competes with this behavior
- Multi-language context: staff and parents may prefer regional languages over English

## Key Constraints

- **Data privacy** — India's Digital Personal Data Protection Act (DPDPA 2023) applies; sensitive health data of minors requires careful handling and consent
- **Device diversity** — staff commonly use low-to-mid-range Android phones; do not assume iOS or high-end hardware
- **Connectivity** — sessions may occur in areas with poor or intermittent mobile data; offline capability is important
- **Non-technical users** — many therapists are not tech-savvy; onboarding must be minimal, UI must be self-explanatory
- **One-handed, in-session data entry** — therapists cannot pause sessions to navigate complex UIs; core data collection must be ≤ 2 taps
- **Noisy environments** — some sessions involve loud or active children; haptic feedback preferred over audio cues
- **Multi-language** — English UI may not work for all staff; consider Hindi and regional language support in Phase 2+
- **WhatsApp dependency** — parent communication currently happens on WhatsApp; the product must offer clear value over this behavior, not just replace it

## Regulatory & Compliance Context

- **RCI (Rehabilitation Council of India)** — the statutory body licensing special educators and rehabilitation professionals; the Indian equivalent of BACB
- **RPWD Act 2016 (Rights of Persons with Disabilities Act)** — mandates inclusion, documentation, and access for persons with disabilities including autism
- **DPDPA 2023** — India's data protection law; applies to personal and health data; consent requirements for processing data of minors
- **UDID (Unique Disability ID)** — government-issued disability certificate; centers often need to document this for compliance and parent reference
- There is **no HIPAA** in India — do not apply US HIPAA frameworks; use DPDPA 2023 and RCI guidelines as the regulatory reference

## Domain Terminology

- **ABA** — Applied Behavior Analysis (the therapy methodology; growing in India but not yet mainstream in all centers)
- **Special Educator** — RCI-licensed professional who delivers therapy; the primary clinical role in Indian autism centers
- **Behavior Therapist** — a therapist trained specifically in behavioral intervention; may or may not hold RCI license
- **Clinical Supervisor / Senior Therapist** — designs programs, supervises junior staff; may hold a BCBA (rare) or be a senior RCI-licensed professional
- **RCI** — Rehabilitation Council of India; the statutory licensing body for special educators and rehabilitation professionals
- **BCBA** — Board Certified Behavior Analyst (US credential from BACB); present in India but rare; fewer than ~500 in the country
- **Treatment plan / Therapy program** — the individualized program for each child, typically updated monthly or quarterly
- **Session note** — documentation of what happened in a session; required for internal records and parent reporting
- **Target behavior** — a specific skill or behavior being tracked (increasing desired skills or decreasing problem behaviors)
- **Discrete Trial Training (DTT)** — structured, repetitive ABA teaching method; common in Indian centers
- **Natural Environment Teaching (NET)** — play-based, less structured ABA method; growing in use
- **Maladaptive behavior** — problem behaviors being reduced (e.g., self-harm, aggression, tantrums)
- **Home program** — activities prescribed for parents to practice with the child between sessions; a key output of therapy
- **Shadow teacher** — a 1:1 aide who supports a child with autism in a mainstream school setting; often coordinated with the therapy center
- **Inclusion** — the process of integrating children with autism into mainstream schools; a key goal for many families
- **UDID** — Unique Disability ID; government-issued disability certificate used for accessing schemes and benefits
- **Divyangjan** — Government of India umbrella term and scheme for persons with disabilities

## Active Workstreams

> Update as workstreams open or close. Reference stage-tracker.md for detail.

- [Add active workstreams here as they begin]

## Key Research Findings

> Summarize validated findings here. Link to full docs in research/.

- [Add validated findings as they are confirmed]

## Important Assumptions Still Open

> [ASSUMPTION] = not yet validated by research

- [ASSUMPTION] Special educators find paper/WhatsApp-based data collection disruptive enough to pay for a software alternative
- [ASSUMPTION] Clinical supervisors spend significant uncompensated time on manual progress report writing
- [ASSUMPTION] Center directors would pay for a unified tool if it reduced their admin burden, even at Indian price points
- [ASSUMPTION] Parents want structured progress updates beyond WhatsApp messages, and would engage with a parent-facing portal
- [ASSUMPTION] Offline-first is a hard requirement for most centers (vs. a nice-to-have)
- [ASSUMPTION] English-only UI is acceptable for therapist-facing features in metro markets at launch
- [ASSUMPTION] WhatsApp cannot realistically be replaced for parent communication — the product must integrate with or complement it
