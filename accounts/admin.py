from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'age',
        'phone',
        'country',
        'gender',
        'is_staff',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'country',
        'gender',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Change Additional Information', {
            'fields': (
                'age',
                'phone',
                'gender',
                'country',
                'profile_picture',
            )
        }),
    ) # change form

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Creation Additional Information', {
            'fields': (
                'age',
                'phone',
                'gender',
                'country',
                'profile_picture',
            )
        }),
    ) # creation form

admin.site.site_header = 'StudyBuddy Adminstration'
admin.site.index_title = 'Welcome'
admin.site.site_title = 'StudyBuddy'
