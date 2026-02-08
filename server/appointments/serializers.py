from doctors.serializers import DoctorProfileReadSerializer  # corrected import
from patients.serializers import PatientProfileReadSerializer
from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientProfileReadSerializer(read_only=True)
    doctor = DoctorProfileReadSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "status",
            "scheduled_time",
            "ai_reason",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at", "ai_reason", "patient"]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["doctor", "scheduled_time"]
