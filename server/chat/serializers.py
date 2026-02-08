from rest_framework import serializers

from .models import ChatMessage, ChatRoom


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source="sender.email")

    class Meta:
        model = ChatMessage
        fields = ["id", "sender_email", "message", "created_at"]


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ["id", "appointment", "is_closed", "created_at", "messages"]
