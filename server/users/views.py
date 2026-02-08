# users/views.py
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserRegisterSerializer,
)
from users.services import (
    get_system_stats,
    list_users,
    login_user,
    register_user,
    toggle_user_active,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register_user(serializer.validated_data)
        return Response(
            UserRegisterSerializer(user).data, status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login_user(
            serializer.validated_data["email"], serializer.validated_data["password"]
        )

        if "error" in result:
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        return Response(result, status=status.HTTP_200_OK)


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)


# Custom permission for admin
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class ToggleUserActiveView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = toggle_user_active(user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ListUsersView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        active_param = self.request.query_params.get("active")
        return list_users(active_param)


class SystemStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = get_system_stats()
        return Response(stats, status=status.HTTP_200_OK)
