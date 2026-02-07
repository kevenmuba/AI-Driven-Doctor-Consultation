from django.db import models
from patients.models import PatientProfile


class SymptomAnalysis(models.Model):
    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name="symptom_analyses"
    )
    symptoms_text = models.TextField()
    predicted_specialty = models.CharField(max_length=100)
    confidence_score = models.DecimalField(max_digits=4, decimal_places=2)
    ai_model_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.email} - {self.predicted_specialty}"
