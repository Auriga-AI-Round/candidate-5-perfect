# API

Base URL: `/api`. All responses are JSON. Every endpoint below maps to a route in
`hospital/urls.py` and a handler in `hospital/views.py`.

| Method | Path | Handler | Description |
|---|---|---|---|
| GET | `/api/patients` | `views.patients` | List patients; `?q=` searches name/phone |
| POST | `/api/patients` | `views.patients` | Create a patient (name required) |
| GET | `/api/doctors` | `views.doctors` | List doctors; `?specialization=` filters |
| POST | `/api/doctors` | `views.doctors` | Create a doctor |
| POST | `/api/appointments` | `views.book_appointment` | Book; 409 on 30-min overlap |
| GET | `/api/appointments` | `views.list_appointments` | List appointments |
| GET | `/api/doctors/{id}/billing` | `views.billing` | Completed × fee for a doctor |
| GET | `/api/analytics` | `views.analytics` | Appointments per doctor |

## Examples

### Book an appointment
```
POST /api/appointments
{ "patient_id": 1, "doctor_id": 2, "start_time": "2030-01-01T10:00:00" }
→ 201 { "id": 5 }
```

### Overlap rejected (the twist)
```
POST /api/appointments
{ "patient_id": 3, "doctor_id": 2, "start_time": "2030-01-01T10:15:00" }
→ 409 { "error": "doctor is already booked in an overlapping 30-min slot" }
```

### Search patients
```
GET /api/patients?q=alice   → [{ "id": 1, "name": "Alice", "phone": "555-1000" }]
```
