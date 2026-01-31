from django.urls import path
from doctors.views import DoctorMeView, PublicDoctorListView, VerifyDoctorView

urlpatterns = [
    path("", PublicDoctorListView.as_view(), name="public-doctors"),
    path("me/", DoctorMeView.as_view(), name="doctor-me"),
    path("<int:doctor_id>/verify/", VerifyDoctorView.as_view(), name="verify-doctor"),
]
