# Email: Engineering Alignment Meeting — 22 April 2026

> **To:** Engineering, Product
> **Subject:** Summary — ATP Engineering Alignment | 22 April 2026
> **Copy-paste ready from the line below**

---

Hi team,

Thanks for the time today. Quick summary of where we landed.

**What we covered**

We walked through the end-to-end lifecycle of an Indian autism therapy center across 8 journeys — enrollment, program design, session notes, progress reports, billing, scheduling, dropout prevention, and analytics. This gave engineering the full picture before we confirm what goes into the MVP.

**Key decision: MVP = clinical management tool, not therapy-specific platform**

After reviewing the journeys, the engineering team confirmed that six of the eight journeys — enrollment, session notes, billing, scheduling, dropout prevention, and analytics — can be built by reusing existing EMR components with relatively low incremental build effort.

The two exceptions are **J2 (Clinical Program Design)** and **J4 (Progress Reports)**. These are the most therapy-specific features and require net-new build. Both are **deferred to post-MVP**.

In-session behavioral data collection was also confirmed as **out of scope for MVP**. In the Indian out-of-pocket market there is no reimbursement driver requiring session-level data logging. This is an opportunity for US and international markets — not India Phase 1.

**MVP scope summary**

| Journey | MVP |
| --- | --- |
| J1 Enrollment and Intake | ✅ In |
| J2 Clinical Program Design | ❌ Out — post-MVP |
| J3 Session Notes | ✅ In |
| J4 Progress Reports | ❌ Out — post-MVP |
| J5 Billing | ✅ In |
| J6 Scheduling and Attendance | ✅ In |
| J7 Dropout Prevention | ✅ In |
| J8 Analytics Dashboard | ✅ In |
| In-Session Data Collection | ❌ Out — India MVP |

**Next steps**

- **Engineering** — Analyse reusability of existing EMR components for the 6 in-scope journeys and confirm feasibility
- **Product** — Run primary research with therapy centers to validate pain points and confirm that deferring J2 and J4 does not block therapist adoption
- **Product** — Update journey maps and flows to reflect the agreed MVP scope
- **Both** — Reconvene to confirm final MVP scope once engineering analysis and product research are complete

One flag worth noting: J2 and J4 are the features therapists are most likely to care about. If primary research shows they are adoption blockers, we will need to revisit this decision before locking scope.

Will share updated journey maps once revised.

Prahlad
