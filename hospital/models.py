"""Domain models — Django ORM on PostgreSQL.

The booking rule (no overlapping appointment for a doctor) is enforced here, at the
data layer, so it holds regardless of which view or client creates an appointment.
"""

from datetime import timedelta

from django.db import models
from django.db.models import Q

SLOT = timedelta(minutes=30)


class Patient(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(blank=True)
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def search(cls, q: str):
        """Partial, case-insensitive match on name OR phone."""
        return cls.objects.filter(is_deleted=False).filter(
            Q(name__icontains=q) | Q(phone__icontains=q)
        )


class Doctor(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    specialization = models.CharField(max_length=120, db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def total_billed(self):
        completed = self.appointment_set.filter(status=Appointment.Status.COMPLETED).count()
        return completed * self.fee


class Appointment(models.Model):
    class Status(models.TextChoices):
        BOOKED = "booked"
        COMPLETED = "completed"
        CANCELLED = "cancelled"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BOOKED)

    class Meta:
        indexes = [models.Index(fields=["doctor", "start_time"])]

    @classmethod
    def has_overlap(cls, doctor_id, start, end) -> bool:
        """THE TWIST: any time-range overlap for the same doctor is a clash.

        Half-open interval test: existing.start < new.end AND existing.end > new.start.
        So 10:00-10:30 blocks 10:15-10:45 (overlap) but allows 10:30-11:00 (adjacent).
        """
        return cls.objects.filter(
            doctor_id=doctor_id, status=cls.Status.BOOKED,
            start_time__lt=end, end_time__gt=start,
        ).exists()

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time + SLOT
        super().save(*args, **kwargs)
