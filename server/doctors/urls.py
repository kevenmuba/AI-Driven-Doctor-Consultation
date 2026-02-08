from django.urls import path
from doctors.views import (
    AllDoctorsListView,
    DoctorAvailabilityListCreateView,
    DoctorAvailabilityRetrieveUpdateDestroyView,
    DoctorMeView,
    PublicDoctorListView,
    ToggleVerifyDoctorView,
    VerifyDoctorView,
)

urlpatterns = [
    path("public/", PublicDoctorListView.as_view(), name="public-doctors"),
    path("me/", DoctorMeView.as_view(), name="doctor-me"),
    path("<int:doctor_id>/verify/", VerifyDoctorView.as_view(), name="verify-doctor"),
    path("all/", AllDoctorsListView.as_view(), name="all-doctors"),
    path(
        "<int:doctor_id>/verify-toggle/",
        ToggleVerifyDoctorView.as_view(),
        name="toggle-doctor-verification",
    ),
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
