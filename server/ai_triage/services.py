# ai_triage/services.py
import logging
from decimal import Decimal

from django.conf import settings
from doctors.models import DoctorProfile

logger = logging.getLogger(__name__)

SPECIALTIES = [
    "Cardiology",
    "Dermatology",
    "Neurology",
    "Pediatrics",
    "Psychiatry",
    "Orthopedics",
]

# Simple keyword mapping for mock AI
KEYWORD_SPECIALTY_MAP = {
    "chest pain": "Cardiology",
    "heart": "Cardiology",
    "rash": "Dermatology",
    "skin": "Dermatology",
    "headache": "Neurology",
    "brain": "Neurology",
    "child": "Pediatrics",
    "kid": "Pediatrics",
    "anxiety": "Psychiatry",
    "depression": "Psychiatry",
    "bone": "Orthopedics",
    "joint": "Orthopedics",
    "fracture": "Orthopedics",
}


def analyze_symptoms(symptoms_text: str) -> dict:
    """
    Mock AI triage: recommends a specialty and doctors based on simple keyword logic.
    Educational / development use only.
    """
    try:
        text_lower = symptoms_text.lower()
        predicted_specialty = "General"

        # Check keywords
        for keyword, specialty in KEYWORD_SPECIALTY_MAP.items():
            if keyword in text_lower:
                predicted_specialty = specialty
                break

        confidence_score = (
            Decimal("0.8") if predicted_specialty != "General" else Decimal("0.4")
        )

        # Fetch doctors
        doctors = DoctorProfile.objects.filter(
            specialty__iexact=predicted_specialty,
            is_verified=True,
        )

        doctors_list = [
            {
                "id": doctor.id,
                "name": doctor.user.email,
                "specialty": doctor.specialty,
                "years_experience": doctor.years_experience,
            }
            for doctor in doctors
        ]

        message = None
        # If no doctors found, show general message
        if not doctors_list:
            message = (
                f"Your symptoms suggest {predicted_specialty}. "
                "No verified doctor is currently available for this specialty."
            )

        return {
            "predicted_specialty": predicted_specialty,
            "confidence_score": confidence_score,
            "ai_model_version": "mock-v1",
            "recommended_doctors": doctors_list,
            "message": message or "AI recommendation generated successfully.",
        }

    except Exception as e:
        logger.exception("AI Triage Mock Error")
        return {
            "predicted_specialty": "General",
            "confidence_score": Decimal("0.5"),
            "ai_model_version": "mock-fallback",
            "recommended_doctors": [],
            "message": "AI service is currently unavailable. Please try again later.",
        }
