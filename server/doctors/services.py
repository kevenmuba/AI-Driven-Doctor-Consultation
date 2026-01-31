from doctors.models import DoctorProfile


def create_doctor_profile(user, data):
    return DoctorProfile.objects.create(user=user, **data)


def get_verified_doctors():
    return DoctorProfile.objects.filter(is_verified=True)


def verify_doctor(doctor_id):
    doctor = DoctorProfile.objects.get(id=doctor_id)
    doctor.is_verified = True
    doctor.save()
    return doctor
