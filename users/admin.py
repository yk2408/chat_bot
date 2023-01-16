from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ChatLog


class UserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'date_joined', 'is_admin', 'is_staff')
    search_fields = ('email', 'full_name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(ChatLog)
