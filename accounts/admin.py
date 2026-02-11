from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'age', 'phone', 'country', 'gender', 'is_staff']
    list_filter = ['country', 'gender', 'date_joined', 'last_login']
    search_fields = ['first_name', 'last_name', 'age', 'phone']


admin.site.site_header = 'StudyBuddy Adminstration'
admin.site.index_title = 'Welcome'
admin.site.site_title = 'StudyBuddy'
