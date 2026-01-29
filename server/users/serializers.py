# users/serializers.py
from doctors.models import DoctorProfile
from patients.models import PatientProfile
from rest_framework import serializers
from users.models import User


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["id", "specialty", "years_experience", "bio", "is_verified"]


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["id", "age", "gender", "medical_history"]


class UserRegisterSerializer(serializers.ModelSerializer):
    profile = serializers.DictField(write_only=True, required=False)
    role = serializers.CharField()  # override the default to handle case-insensitive

    class Meta:
        model = User
        fields = ["id", "email", "password", "role", "profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_role(self, value):
        """Normalize role to uppercase to match model choices."""
        value_upper = value.upper()
        if value_upper not in [choice[0] for choice in User.ROLE_CHOICES]:
            raise serializers.ValidationError(f"{value} is not a valid role.")
        return value_upper

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})

        # Normalize role before creating the user
        validated_data["role"] = validated_data["role"].upper()

        user = User.objects.create_user(**validated_data)

        # Create profile depending on role
        if user.role == "DOCTOR":
            DoctorProfile.objects.create(user=user, **profile_data)
        elif user.role == "PATIENT":
            PatientProfile.objects.create(user=user, **profile_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
