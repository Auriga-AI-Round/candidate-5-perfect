"""HTTP API — thin handlers over the models. Validation + correct status codes."""

from datetime import datetime

from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SLOT, Appointment, Doctor, Patient


@api_view(["GET", "POST"])
def patients(request):
    if request.method == "POST":
        d = request.data
        if not d.get("name"):
            return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
        p = Patient.objects.create(
            name=d["name"], gender=d.get("gender", ""),
            phone=d.get("phone", ""), email=d.get("email", ""),
        )
        return Response({"id": p.id}, status=status.HTTP_201_CREATED)
    q = request.query_params.get("q", "")
    qs = Patient.search(q) if q else Patient.objects.filter(is_deleted=False)
    return Response([{"id": p.id, "name": p.name, "phone": p.phone} for p in qs])


@api_view(["GET", "POST"])
def doctors(request):
    if request.method == "POST":
        d = request.data
        if not d.get("name"):
            return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
        doc = Doctor.objects.create(
            name=d["name"], specialization=d.get("specialization", ""),
            phone=d.get("phone", ""), email=d.get("email", ""), fee=d.get("fee", 0),
        )
        return Response({"id": doc.id}, status=status.HTTP_201_CREATED)
    spec = request.query_params.get("specialization", "")
    qs = Doctor.objects.all()
    if spec:
        qs = qs.filter(specialization__icontains=spec)
    return Response([{"id": d.id, "name": d.name, "specialization": d.specialization} for d in qs])


@api_view(["POST"])
def book_appointment(request):
    d = request.data
    try:
        start = datetime.fromisoformat(d["start_time"])
    except (KeyError, ValueError, TypeError):
        return Response({"error": "valid start_time (ISO) required"},
                        status=status.HTTP_400_BAD_REQUEST)
    if not d.get("patient_id") or not d.get("doctor_id"):
        return Response({"error": "patient_id and doctor_id are required"},
                        status=status.HTTP_400_BAD_REQUEST)
    end = start + SLOT
    if Appointment.has_overlap(d["doctor_id"], start, end):
        return Response(
            {"error": "doctor is already booked in an overlapping 30-min slot"},
            status=status.HTTP_409_CONFLICT,
        )
    appt = Appointment.objects.create(
        patient_id=d["patient_id"], doctor_id=d["doctor_id"],
        start_time=start, end_time=end,
    )
    return Response({"id": appt.id}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_appointments(request):
    rows = Appointment.objects.values("id", "patient_id", "doctor_id", "start_time", "status")
    return Response(list(rows))


@api_view(["GET"])
def billing(request, doctor_id):
    try:
        doc = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"error": "doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"doctor_id": doctor_id, "total_billed": float(doc.total_billed())})


@api_view(["GET"])
def analytics(request):
    """Appointments per doctor — powers the dashboard landing page."""
    data = (
        Appointment.objects.values("doctor__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return Response(list(data))
