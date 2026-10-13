# Build Plan

Ordered plan I followed, with checkboxes reflecting the final state.

1. [x] Schema: patient, doctor, appointment on PostgreSQL + indexes (`db/dump.sql`)
2. [x] Patient CRUD + soft delete + validation
3. [x] Doctor CRUD
4. [x] Appointment booking — **the overlap twist first, test-driven**
5. [x] Search: patients (name/phone), doctors (specialization)
6. [x] Billing: completed × fee
7. [x] Analytics aggregate + dashboard landing page
8. [x] Tests for twist, search, billing
9. [x] Docs: FEATURES, API, REASONING, AI_LOG, this plan

## Sequencing rationale
I built the overlap rule in step 4 before the rest of booking, because it's the
riskiest requirement and everything else is standard CRUD. Writing its tests first
caught a boundary bug early (see AI_LOG).
