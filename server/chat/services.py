from appointments.models import Appointment

from .models import ChatRoom


def get_or_create_chat_room(appointment: Appointment):
    if appointment.status != "ACCEPTED":
        raise ValueError("Chat is only available for accepted appointments.")

    chat_room, created = ChatRoom.objects.get_or_create(appointment=appointment)
    return chat_room


def complete_appointment(appointment):
    appointment.status = "COMPLETED"
    appointment.save()

    if hasattr(appointment, "chat_room"):
        appointment.chat_room.is_closed = True
        appointment.chat_room.save()

    return appointment
