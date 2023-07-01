from django.contrib import admin

# Register your models here.
from .models import Room, RoomMessage

class AdminRoomMessage(admin.ModelAdmin):
    model = RoomMessage
    list_display = (
        'room',
        'message',
        'created',
    )
# Register your models here.
admin.site.register(RoomMessage,AdminRoomMessage)
