# Features

All features below are implemented and backed by code in `hospital/` and tested in
`tests/`. File references are given so each claim can be verified against source.

## Patient management (simple)
- Create / list / retrieve / soft-delete patients — `hospital/views.py:patients`,
  `hospital/models.py:Patient`
- Validation: name required (400 on missing) — `hospital/views.py:patients`

## Doctor management (simple)
- Create / list doctors with specialization + fee — `hospital/views.py:doctors`,
  `hospital/models.py:Doctor`

## Appointment booking (complex)
- Book a 30-minute appointment — `hospital/views.py:book_appointment`
- **No double-booking / overlap twist**: any time-range overlap for the same doctor
  is rejected with HTTP 409 — `hospital/models.py:Appointment.has_overlap`
- Cancel / complete status transitions — `hospital/models.py:Appointment.Status`

## Search (implicit requirement)
- Patients by name or phone (partial, case-insensitive) —
  `hospital/models.py:Patient.search`, `hospital/views.py:patients?q=`
- Doctors by specialization — `hospital/views.py:doctors?specialization=`

## Billing (complex)
- Per-doctor billing = completed appointments × fee —
  `hospital/models.py:Doctor.total_billed`, `hospital/views.py:billing`

## Analytics (complex / bonus)
- Appointments-per-doctor aggregate — `hospital/views.py:analytics`
- Dashboard UI consuming it — `static/dashboard.html`

## Status summary
| Feature | Status |
|---|---|
| Patient CRUD | ✅ done |
| Doctor CRUD | ✅ done |
| Appointment booking | ✅ done |
| 30-min overlap rejection (twist) | ✅ done |
| Search | ✅ done |
| Billing | ✅ done |
| Analytics dashboard | ✅ done |
