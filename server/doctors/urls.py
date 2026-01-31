from django.urls import path
from doctors.views import (
    DoctorAvailabilityListCreateView,
    DoctorAvailabilityRetrieveUpdateDestroyView,
    DoctorMeView,
    PublicDoctorListView,
    VerifyDoctorView,
)

urlpatterns = [
    path("", PublicDoctorListView.as_view(), name="public-doctors"),
    path("me/", DoctorMeView.as_view(), name="doctor-me"),
    path("<int:doctor_id>/verify/", VerifyDoctorView.as_view(), name="verify-doctor"),
    path(
        "availability/",
        DoctorAvailabilityListCreateView.as_view(),
        name="availability-list-create",
    ),
    path(
        "availability/<int:pk>/",
        DoctorAvailabilityRetrieveUpdateDestroyView.as_view(),
        name="availability-detail",
    ),
]
