from django.contrib import admin
from .models import Supervision


@admin.register(Supervision)
class SupervisionAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'company', 'course_name', 'start_date', 'end_date', 'total_days', 'created_at']
    list_filter = ['college', 'internship_type', 'start_date', 'created_at']
    search_fields = ['student__student_id', 'name', 'company', 'internship_address']
    date_hierarchy = 'created_at'
