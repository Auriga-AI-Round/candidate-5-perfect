# Hospital Management System

A complete hospital management backend (Django + DRF + PostgreSQL) with patient,
doctor and appointment management, a 30-minute **overlap-safe** booking engine,
search, billing, and an analytics dashboard.

---

## Landing page

### Product
**CareSlot** is a hospital management system that lets front-desk staff register
patients and doctors, book clash-free appointments, and track billing and clinic
analytics from one place.

### Features
- Patient & doctor management (CRUD + soft delete)
- Appointment booking that rejects any 30-minute **overlap** for a doctor
- Search across patients (name/phone) and doctors (specialization)
- Billing per doctor (completed appointments × fee)
- Analytics dashboard: appointments per doctor + total billings

### Audience
Small and mid-size clinics and hospital front desks that need a reliable
appointment system without double-bookings, plus a quick operational dashboard
for administrators.

### How it helps
It removes the single most common scheduling error — double-booking a doctor — by
enforcing overlap checks at the database layer, while giving staff fast search and
admins a live view of load and revenue. Less manual coordination, fewer conflicts.

### Roadmap
1. SMS/email appointment reminders to reduce no-shows.
2. Role-based access (receptionist vs. admin vs. doctor portals).
3. Insurance claim export and multi-branch support.

---

## Tech
- Django 5 + Django REST Framework
- **PostgreSQL** (real DB server — see `db/dump.sql`)
- Pytest/Django test suite in `tests/`

## Setup
```bash
pip install -r requirements.txt
createdb hospital
python manage.py migrate
python manage.py test            # run the suite
python manage.py runserver       # dashboard at /static/dashboard.html
```

## Documentation
- `FEATURES.md` — feature list + status
- `API.md` — every endpoint
- `REASONING.md` — design decisions (why overlap is a half-open interval, etc.)
- `AI_LOG.md` — how AI was used during development
- `plan.md` — the build plan
- `db/dump.sql` — the PostgreSQL schema dump

## Submission
App URL: https://careslot-demo.example.com
API base: https://careslot-demo.example.com/api
Username: reviewer@example.com
Password: review-pass-123
Endpoints:
  - GET /api/patients
  - POST /api/patients
  - GET /api/doctors
  - POST /api/doctors
  - POST /api/appointments
  - GET /api/appointments
  - GET /api/doctors/{id}/billing
  - GET /api/analytics
Notes: Postgres-backed; booking enforces a 30-minute overlap rule at the data layer.
