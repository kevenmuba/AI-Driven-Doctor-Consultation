from patients.models import PatientProfile
from rest_framework import serializers


class PatientProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["age", "gender", "medical_history"]


class PatientProfileReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = PatientProfile
        fields = ["id", "email", "age", "gender", "medical_history"]
