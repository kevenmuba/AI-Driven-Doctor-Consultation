from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    ListUsersView,
    LoginView,
    MeView,
    RegisterView,
    SystemStatsView,
    ToggleUserActiveView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    # Phase 7 - Admin Controls
    path("all/", ListUsersView.as_view(), name="list_users"),  # GET /users/all/
    path(
        "<int:user_id>/toggle_active/",
        ToggleUserActiveView.as_view(),
        name="toggle_user_active",
    ),  # PATCH
    path("stats/", SystemStatsView.as_view(), name="system_stats"),  # GET
]
