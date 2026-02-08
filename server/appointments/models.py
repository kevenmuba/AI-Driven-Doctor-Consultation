from django.db import models
from doctors.models import DoctorProfile
from patients.models import PatientProfile


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed"),
    ]

    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="appointments"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    scheduled_time = models.DateTimeField()
    ai_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_time"]
        unique_together = ("doctor", "scheduled_time")  # prevent double booking

    def __str__(self):
        return f"{self.patient.user.email} → {self.doctor.user.email} @ {self.scheduled_time}"
