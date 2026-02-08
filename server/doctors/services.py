from django.core.exceptions import ValidationError
from doctors.models import DoctorAvailability, DoctorProfile


def create_doctor_profile(user, data):
    return DoctorProfile.objects.create(user=user, **data)


def get_all_doctors(verified=None):
    qs = DoctorProfile.objects.all()
    if verified is True:
        qs = qs.filter(is_verified=True)
    elif verified is False:
        qs = qs.filter(is_verified=False)
    return qs


def get_verified_doctors():
    return DoctorProfile.objects.filter(is_verified=True)


def verify_doctor(doctor_id):
    doctor = DoctorProfile.objects.get(id=doctor_id)
    doctor.is_verified = True
    doctor.save()
    return doctor


def toggle_doctor_verification(doctor_id):
    doctor = DoctorProfile.objects.get(id=doctor_id)
    doctor.is_verified = not doctor.is_verified  # toggle True/False
    doctor.save()
    return doctor


def check_overlap(doctor, day_of_week, start_time, end_time, exclude_id=None):
    qs = DoctorAvailability.objects.filter(doctor=doctor, day_of_week=day_of_week)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    for slot in qs:
        if start_time < slot.end_time and end_time > slot.start_time:
            raise ValidationError("This time slot overlaps with existing availability")
