from doctors.models import DoctorProfile
from patients.models import PatientProfile
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentCreateSerializer, AppointmentSerializer
from .services import create_appointment, update_appointment_status


class AppointmentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentCreateSerializer

    def post(self, request, *args, **kwargs):
        patient = PatientProfile.objects.filter(user=request.user).first()
        if not patient:
            return Response(
                {"detail": "Patient profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        doctor_id = request.data.get("doctor")
        scheduled_time = request.data.get("scheduled_time")

        if not doctor_id or not scheduled_time:
            return Response(
                {"detail": "doctor and scheduled_time are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            doctor = DoctorProfile.objects.get(id=doctor_id, is_verified=True)
        except DoctorProfile.DoesNotExist:
            return Response(
                {"detail": "Doctor not found or not verified."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # AI reason from last symptom analysis
        last_analysis = patient.symptom_analyses.order_by("-created_at").first()
        ai_reason = last_analysis.predicted_specialty if last_analysis else None

        try:
            appointment = create_appointment(
                patient=patient,
                doctor=doctor,
                scheduled_time=scheduled_time,
                ai_reason=ai_reason,
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentStatusUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        appointment = self.get_object()
        status_update = request.data.get("status")

        if status_update not in ["ACCEPTED", "REJECTED", "COMPLETED"]:
            return Response(
                {"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Only doctor can accept/reject
        if request.user != appointment.doctor.user:
            return Response(
                {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        appointment = update_appointment_status(appointment, status_update)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
