# chat_extra_tags.py
from django import template
from ..models import Room

register = template.Library()


@register.simple_tag
def get_main_message():
    room = Room.objects.get(group_name='main')
    old_messages = room.messages.order_by('-created')[:50]
    return old_messages