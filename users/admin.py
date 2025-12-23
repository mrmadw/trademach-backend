from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


# Register your models here.

class UserAdminConfig(UserAdmin):
	search_fields = ('email', 'username', 'first_name',)
	list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff',)
	ordering = ('username',)
	list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff')

	fieldsets = (
		(None, {'fields': ('email', 'username', 'first_name',)}),
		('Permissions', {'fields': ('is_staff', 'is_active')}),
		('Personal', {'fields': ('about',)}),
		)

	add_fieldsets = (
		(None, {
			'classes': ('wide'),
			'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_staff',)
			}),
		)



admin.site.register(NewUser, UserAdminConfig)