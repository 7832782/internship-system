from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    """实习情况登记表序列化器"""

    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['student', 'submit_date', 'updated_at']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'gender': {'required': False, 'allow_blank': True},
            'college': {'required': False, 'allow_blank': True},
            'major': {'required': False, 'allow_blank': True},
            'company': {'required': False, 'allow_blank': True},
            'start_date': {'required': False, 'allow_null': True},
            'end_date': {'required': False, 'allow_null': True},
            'total_days': {'required': False, 'allow_null': True},
        }
