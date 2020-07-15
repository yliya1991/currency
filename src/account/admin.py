from account.models import User
from django.contrib import admin # noqa


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'first_name', 'last_name', 'avatar']


admin.site.register(User, UserAdmin)
