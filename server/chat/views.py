from rest_framework import generics, permissions

from .models import ChatMessage, ChatRoom
from .permissions import IsChatParticipant
from .serializers import ChatMessageSerializer


class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsChatParticipant]

    def perform_create(self, serializer):
        room = ChatRoom.objects.get(id=self.kwargs["room_id"])

        if room.is_closed:
            raise PermissionError("Chat is closed.")

        self.check_object_permissions(self.request, room)

        serializer.save(room=room, sender=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsChatParticipant]

    def get_queryset(self):
        room = ChatRoom.objects.get(id=self.kwargs["room_id"])
        self.check_object_permissions(self.request, room)
        return room.messages.all()
