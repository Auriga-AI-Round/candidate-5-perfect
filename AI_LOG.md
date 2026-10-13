# AI Usage Log

How I used an AI assistant during this build, and how I verified its output rather
than pasting blindly.

## 1. Overlap algorithm
**Prompt:** "Given 30-minute appointment slots, how do I reject any overlapping
booking for the same doctor in Django ORM?"
**AI suggested:** a half-open interval filter `start_time__lt=end, end_time__gt=start`.
**What I did:** I didn't trust it on faith — I wrote three tests first
(`tests/test_hospital.py`): partial overlap rejected, adjacent slot allowed, different
doctor not blocked. The adjacent-slot case failed with the AI's first version (it used
`<=`/`>=`), so I corrected it to strict `<`/`>`. Lesson: the boundary condition is the
whole point of this task.

## 2. 409 vs 400
**Prompt:** "Right status code for a booking conflict?"
**AI suggested:** 409 Conflict. I confirmed against RFC 9110 (409 = request conflicts
with current resource state) before adopting it.

## 3. Analytics aggregate
**Prompt:** "Appointments per doctor as a Django aggregate."
**AI suggested:** `.values('doctor__name').annotate(count=Count('id'))`. I verified the
generated SQL with `.query` and checked it grouped correctly against seed data.

## What I rejected
The AI first proposed storing times as naive strings. I rejected that — I used
`DateTimeField` (timezone-aware) so overlap math is correct across DST and clients.
