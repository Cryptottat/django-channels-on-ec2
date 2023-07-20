from django.contrib import admin

# Register your models here.
from .models import AutoUser


class AdminAutoUser(admin.ModelAdmin):
    model = AutoUser
    list_display = (
        'user_id',
        'user_pw',
        'name',
        'phone',
    )


# Register your models here.
admin.site.register(AutoUser, AdminAutoUser)
