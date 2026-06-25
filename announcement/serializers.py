from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    """公告序列化器"""
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
