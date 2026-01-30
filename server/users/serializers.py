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


class UserProfileSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(read_only=True)
    patient_profile = PatientProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "doctor_profile",
            "patient_profile",
        ]
        read_only_fields = ["email", "role"]


class UserProfileUpdateSerializer(serializers.Serializer):
    profile = serializers.DictField()

    def update(self, instance, validated_data):
        profile_data = validated_data.get("profile", {})

        if instance.role == "DOCTOR":
            profile, _ = DoctorProfile.objects.get_or_create(user=instance)
        elif instance.role == "PATIENT":
            profile, _ = PatientProfile.objects.get_or_create(user=instance)
        else:
            raise serializers.ValidationError("Admins have no editable profile.")

        for attr, value in profile_data.items():
            if hasattr(profile, attr):
                setattr(profile, attr, value)

        profile.save()
        return instance
