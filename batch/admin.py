from django.contrib import admin
from .models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'deadline', 'is_expired', 'created_at']
    list_filter = ['deadline']
    search_fields = ['name']
    date_hierarchy = 'created_at'
