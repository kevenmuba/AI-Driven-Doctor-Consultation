# ai_triage/views.py
from patients.models import PatientProfile
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SymptomAnalysis
from .services import analyze_symptoms


class SymptomAnalysisCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        patient = PatientProfile.objects.filter(user=request.user).first()
        if not patient:
            return Response(
                {"detail": "Patient profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        symptoms_text = request.data.get("symptoms_text")
        if not symptoms_text:
            return Response(
                {"detail": "symptoms_text field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call AI service
        ai_result = analyze_symptoms(symptoms_text)

        # Save to database
        analysis = SymptomAnalysis.objects.create(
            patient=patient,
            symptoms_text=symptoms_text,
            predicted_specialty=ai_result["predicted_specialty"],
            confidence_score=ai_result["confidence_score"],
            ai_model_version=ai_result["ai_model_version"],
        )

        # Return result to frontend
        response_data = {
            "id": analysis.id,
            "symptoms_text": analysis.symptoms_text,
            "predicted_specialty": ai_result["predicted_specialty"],
            "confidence_score": ai_result["confidence_score"],
            "ai_model_version": ai_result["ai_model_version"],
            "recommended_doctors": ai_result["recommended_doctors"],
            "message": ai_result["message"],
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
