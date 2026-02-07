# ai_triage/serializers.py
from ai_triage.models import SymptomAnalysis
from rest_framework import serializers


class SymptomAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomAnalysis
        fields = [
            "id",
            "patient",
            "symptoms_text",
            "predicted_specialty",
            "confidence_score",
            "ai_model_version",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "predicted_specialty",
            "confidence_score",
            "ai_model_version",
            "created_at",
            "patient",
        ]
