from patients.models import PatientProfile


def get_or_create_patient_profile(user):
    profile, _ = PatientProfile.objects.get_or_create(user=user)
    return profile
