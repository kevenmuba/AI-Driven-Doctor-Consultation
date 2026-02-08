from rest_framework.permissions import BasePermission


class IsChatParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        appointment = obj.appointment

        return appointment.patient.user == user or appointment.doctor.user == user
