from django.urls import path

from .views import MessageListView, SendMessageView

urlpatterns = [
    path("rooms/<int:room_id>/messages/", MessageListView.as_view()),
    path("rooms/<int:room_id>/send/", SendMessageView.as_view()),
]
