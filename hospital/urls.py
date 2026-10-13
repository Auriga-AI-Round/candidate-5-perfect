"""URL routing — one line per endpoint listed in API.md."""

from django.urls import path

from . import views

urlpatterns = [
    path("api/patients", views.patients),
    path("api/doctors", views.doctors),
    path("api/appointments", views.book_appointment),            # POST
    path("api/appointments/list", views.list_appointments),      # GET
    path("api/doctors/<int:doctor_id>/billing", views.billing),
    path("api/analytics", views.analytics),
]
