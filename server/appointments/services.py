from .models import Appointment


def create_appointment(patient, doctor, scheduled_time, ai_reason=None):
    # Prevent double booking for doctor
    if Appointment.objects.filter(
        doctor=doctor, scheduled_time=scheduled_time, status__in=["PENDING", "ACCEPTED"]
    ).exists():
        raise ValueError("Doctor is already booked for this time.")

    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        scheduled_time=scheduled_time,
        ai_reason=ai_reason,
    )
    return appointment


def update_appointment_status(appointment, status):
    appointment.status = status
    appointment.save()
    return appointment
