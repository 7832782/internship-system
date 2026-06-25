from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['student_id', 'name', 'gender', 'college', 'major', 'class_number', 'batch', 'role', 'is_profile_complete']
    list_filter = ['role', 'gender', 'college', 'batch', 'is_profile_complete']
    search_fields = ['student_id', 'name', 'college', 'major']
    
    fieldsets = (
        (None, {'fields': ('student_id', 'password')}),
        ('个人信息', {'fields': ('name', 'gender', 'college', 'major', 'class_number')}),
        ('权限', {'fields': ('role', 'is_profile_complete', 'is_active', 'is_staff', 'is_superuser')}),
        ('批次', {'fields': ('batch',)}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'name', 'password1', 'password2', 'role'),
        }),
    )
    
    ordering = ['student_id']
