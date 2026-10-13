# Reasoning & Design Decisions

## Why the overlap check is a half-open interval
The task requires rejecting *any* 30-minute overlap for a doctor, not just an exact
start clash. Two intervals `[s1,e1)` and `[s2,e2)` overlap iff `s1 < e2 AND e1 > s2`.
I implemented exactly that in `Appointment.has_overlap`. Using half-open intervals
means adjacent slots (10:00–10:30 then 10:30–11:00) are allowed, while 10:15–10:45 is
correctly rejected. Doing it in a classmethod on the model keeps the rule at the data
layer, so every code path (API, admin, future importer) is protected — not just one view.

## Why 409 instead of 400 for a clash
A validation error (missing field) is the client's fault in shape → 400. A booking
conflict is a *state* conflict → 409 Conflict, which lets clients distinguish "fix your
request" from "that slot is taken, pick another."

## Why PostgreSQL and an index on (doctor_id, start_time)
Overlap queries filter by doctor and a time range on every booking, so a composite
index on `(doctor, start_time)` keeps the check O(log n). SQLite was rejected because
the task mandates a real DB server and because concurrent bookings need row-level
behaviour SQLite handles poorly.

## Trade-offs / what I'd do next
- Booking is checked but not wrapped in `SELECT … FOR UPDATE`; under heavy concurrency
  I'd add a transaction + lock (or a DB exclusion constraint on a tstzrange) to make the
  overlap guard race-proof. Noted in the roadmap.
- Billing counts completed appointments at read time; for scale I'd denormalize.
