from django.contrib import admin
from .models import Internship


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['student', 'name', 'company', 'teacher', 'start_date', 'end_date', 'total_days', 'submit_date']
    list_filter = ['college', 'start_date', 'submit_date']
    search_fields = ['student__student_id', 'name', 'company', 'teacher']
    date_hierarchy = 'submit_date'
