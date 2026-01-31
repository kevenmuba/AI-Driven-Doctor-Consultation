from django.shortcuts import get_object_or_404
from doctors.models import DoctorProfile
from doctors.permissions import IsAdmin, IsDoctor
from doctors.serializers import (
    DoctorProfileCreateUpdateSerializer,
    DoctorProfileReadSerializer,
)
from doctors.services import get_verified_doctors, verify_doctor
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DoctorMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self):
        return get_object_or_404(DoctorProfile, user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return DoctorProfileCreateUpdateSerializer
        return DoctorProfileReadSerializer


class PublicDoctorListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileReadSerializer

    def get_queryset(self):
        return get_verified_doctors()


class VerifyDoctorView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, doctor_id):
        doctor = verify_doctor(doctor_id)
        serializer = DoctorProfileReadSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
