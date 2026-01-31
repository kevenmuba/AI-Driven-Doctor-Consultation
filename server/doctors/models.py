# doctors/models.py
from django.db import models
from users.models import User


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialty = models.CharField(max_length=100)
    years_experience = models.PositiveIntegerField()
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class DoctorAvailability(models.Model):
    DAYS_OF_WEEK = [
        ("MONDAY", "Monday"),
        ("TUESDAY", "Tuesday"),
        ("WEDNESDAY", "Wednesday"),
        ("THURSDAY", "Thursday"),
        ("FRIDAY", "Friday"),
        ("SATURDAY", "Saturday"),
        ("SUNDAY", "Sunday"),
    ]

    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="availabilities"
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor", "day_of_week", "start_time", "end_time")

    def __str__(self):
        return f"{self.doctor.user.email} - {self.day_of_week} {self.start_time}-{self.end_time}"

    def clean(self):
        # Ensure start_time < end_time
        if self.start_time >= self.end_time:
            from django.core.exceptions import ValidationError

            raise ValidationError("start_time must be before end_time")
