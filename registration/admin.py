from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'company', 'start_date', 'end_date', 'total_days', 'submit_date']
    list_filter = ['college', 'start_date', 'submit_date']
    search_fields = ['student__student_id', 'name', 'company']
    date_hierarchy = 'submit_date'
