"""Tests for the overlap twist, search, and billing — the mandatory behaviours.

Run: `python manage.py test`.
"""

from datetime import datetime

from django.test import TestCase

from hospital.models import Appointment, Doctor, Patient


class OverlapTwistTest(TestCase):
    def setUp(self):
        self.doc = Doctor.objects.create(name="House", specialization="Diagnostics", fee=300)
        self.pat = Patient.objects.create(name="Alice", phone="555-1000")

    def _book(self, hhmm):
        start = datetime.fromisoformat(f"2030-01-01T{hhmm}:00")
        a = Appointment(patient=self.pat, doctor=self.doc, start_time=start)
        a.save()
        return a

    def test_partial_overlap_is_rejected(self):
        self._book("10:00")  # 10:00-10:30
        start = datetime.fromisoformat("2030-01-01T10:15:00")
        end = datetime.fromisoformat("2030-01-01T10:45:00")
        self.assertTrue(Appointment.has_overlap(self.doc.id, start, end))

    def test_adjacent_slot_is_allowed(self):
        self._book("10:00")
        start = datetime.fromisoformat("2030-01-01T10:30:00")
        end = datetime.fromisoformat("2030-01-01T11:00:00")
        self.assertFalse(Appointment.has_overlap(self.doc.id, start, end))

    def test_different_doctor_not_blocked(self):
        self._book("10:00")
        other = Doctor.objects.create(name="Grey", specialization="Surgery", fee=250)
        start = datetime.fromisoformat("2030-01-01T10:00:00")
        end = datetime.fromisoformat("2030-01-01T10:30:00")
        self.assertFalse(Appointment.has_overlap(other.id, start, end))


class SearchTest(TestCase):
    def test_patient_search_name_and_phone(self):
        Patient.objects.create(name="Bob Smith", phone="555-2000")
        self.assertEqual(Patient.search("bob").count(), 1)
        self.assertEqual(Patient.search("2000").count(), 1)
        self.assertEqual(Patient.search("zzz").count(), 0)


class BillingTest(TestCase):
    def test_total_billed_counts_only_completed(self):
        doc = Doctor.objects.create(name="House", specialization="Diagnostics", fee=100)
        pat = Patient.objects.create(name="Alice", phone="1")
        start = datetime.fromisoformat("2030-01-01T09:00:00")
        Appointment.objects.create(patient=pat, doctor=doc, start_time=start,
                                   end_time=start, status="completed")
        self.assertEqual(doc.total_billed(), 100)
