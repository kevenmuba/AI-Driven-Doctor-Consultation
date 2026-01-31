from django.shortcuts import get_object_or_404
from doctors.models import DoctorAvailability, DoctorProfile
from doctors.permissions import IsAdmin, IsDoctor
from doctors.serializers import (
    DoctorAvailabilitySerializer,
    DoctorProfileCreateUpdateSerializer,
    DoctorProfileReadSerializer,
)
from doctors.services import check_overlap, get_verified_doctors, verify_doctor
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


class DoctorAvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return DoctorAvailability.objects.filter(
            doctor=self.request.user.doctor_profile
        )

    def perform_create(self, serializer):
        # Check overlapping
        check_overlap(
            doctor=self.request.user.doctor_profile,
            day_of_week=serializer.validated_data["day_of_week"],
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
        )
        serializer.save(doctor=self.request.user.doctor_profile)


class DoctorAvailabilityRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return DoctorAvailability.objects.filter(
            doctor=self.request.user.doctor_profile
        )

    def perform_update(self, serializer):
        check_overlap(
            doctor=self.request.user.doctor_profile,
            day_of_week=serializer.validated_data["day_of_week"],
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
            exclude_id=self.get_object().id,
        )
        serializer.save()
