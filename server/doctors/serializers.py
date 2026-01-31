from doctors.models import DoctorAvailability, DoctorProfile
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


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ["id", "day_of_week", "start_time", "end_time"]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("start_time must be before end_time")
        return data

    def validate_day_of_week(self, value):
        if value not in dict(DoctorAvailability.DAYS_OF_WEEK).keys():
            raise serializers.ValidationError("Invalid day_of_week")
        return value
