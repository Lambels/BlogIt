from django.contrib import admin
from .models import Account
from blogs.models import Blog
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AdminAccount(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email', 'username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AdminAccount)