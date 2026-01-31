from patients.permissions import IsPatient
from patients.serializers import (
    PatientProfileCreateUpdateSerializer,
    PatientProfileReadSerializer,
)
from patients.services import get_or_create_patient_profile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class PatientMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def get_object(self):
        return get_or_create_patient_profile(self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PatientProfileCreateUpdateSerializer
        return PatientProfileReadSerializer
