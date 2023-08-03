from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from core.models.user.models import OrdinaryUser
from core.models.devices.models import Devices
from core.models.chat_field.models import Message
from core.models.teams.models import Team, TeamMember


# Register your models here.

class OrdinaryUserInline(admin.TabularInline):
    model = OrdinaryUser
    can_delete = False
    verbose_name_plural = 'OrdinaryUser'

class UserAdmin(BaseUserAdmin):
    inlines = (OrdinaryUserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Devices)
admin.site.register(Message)
admin.site.register(Team)
admin.site.register(TeamMember)