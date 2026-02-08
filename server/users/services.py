# users/services.py
import logging

from django.contrib.auth import authenticate
from django.db.models import Count
from doctors.models import DoctorProfile
from patients.models import PatientProfile
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

logger = logging.getLogger(__name__)


def register_user(validated_data: dict) -> User:
    """
    Handles user registration and profile creation.
    """
    profile_data = validated_data.pop("profile", {})

    # Normalize role
    role = validated_data["role"].upper()
    if role not in [choice[0] for choice in User.ROLE_CHOICES]:
        raise ValueError(f"{role} is not a valid role.")
    validated_data["role"] = role

    # Create user
    user = User.objects.create_user(**validated_data)

    # Create associated profile
    if role == "DOCTOR":
        DoctorProfile.objects.create(user=user, **profile_data)
    elif role == "PATIENT":
        PatientProfile.objects.create(user=user, **profile_data)

    return user


def login_user(email: str, password: str) -> dict:
    """
    Authenticates user and returns JWT tokens.
    """
    user = authenticate(email=email, password=password)
    if not user:
        return {
            "error": "INVALID_CREDENTIALS",
            "message": "Email or password incorrect",
        }

    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def toggle_user_active(user_id: int) -> User:
    """
    Toggle the active status of a user.
    """
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return user


def list_users(active: str = None):
    """
    Return all users, optionally filtered by active status.
    """
    qs = User.objects.all()
    if active is not None:
        if active.lower() == "true":
            qs = qs.filter(is_active=True)
        elif active.lower() == "false":
            qs = qs.filter(is_active=False)
    return qs


def get_system_stats():
    """
    Return counts for overall system stats.
    """
    total_users = User.objects.count()
    total_doctors = User.objects.filter(role="DOCTOR").count()
    total_patients = User.objects.filter(role="PATIENT").count()
    verified_doctors = DoctorProfile.objects.filter(is_verified=True).count()

    return {
        "total_users": total_users,
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "verified_doctors": verified_doctors,
    }
