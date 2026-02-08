from django.urls import path

from .views import AppointmentCreateView, AppointmentStatusUpdateView

urlpatterns = [
    path("create/", AppointmentCreateView.as_view(), name="appointment-create"),
    path(
        "<int:id>/status/",
        AppointmentStatusUpdateView.as_view(),
        name="appointment-status-update",
    ),
]
