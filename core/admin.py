from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from core.models.user.user import OrdinaryUser

# Register your models here.

class OrdinaryUserInline(admin.TabularInline):
    model = OrdinaryUser
    can_delete = False
    verbose_name_plural = 'OrdinaryUser'

class UserAdmin(BaseUserAdmin):
    inlines = (OrdinaryUserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
