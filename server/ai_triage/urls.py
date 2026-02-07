from ai_triage.views import SymptomAnalysisCreateView
from django.urls import path

urlpatterns = [
    path("analyze/", SymptomAnalysisCreateView.as_view(), name="symptom-analyze"),
]
