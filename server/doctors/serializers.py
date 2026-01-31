from doctors.models import DoctorProfile
from rest_framework import serializers


class DoctorProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["specialty", "years_experience", "bio"]


class DoctorProfileReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "email",
            "specialty",
            "years_experience",
            "bio",
            "is_verified",
        ]
