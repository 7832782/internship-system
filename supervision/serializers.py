from rest_framework import serializers
from .models import Supervision


class SupervisionSerializer(serializers.ModelSerializer):
    """实习监管信息序列化器"""

    class Meta:
        model = Supervision
        fields = '__all__'
        read_only_fields = ['student', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'enrollment_year': {'required': False, 'allow_blank': True},
            'college': {'required': False, 'allow_blank': True},
            'class_number': {'required': False, 'allow_blank': True},
            'course_name': {'required': False, 'allow_blank': True},
            'course_code': {'required': False, 'allow_blank': True},
            'credits': {'required': False, 'allow_blank': True},
            'internship_type': {'required': False, 'allow_blank': True},
            'internship_org_form': {'required': False, 'allow_blank': True},
            'internship_method': {'required': False, 'allow_blank': True},
            'academic_year': {'required': False, 'allow_blank': True},
            'is_school_base': {'required': False, 'allow_blank': True},
            'is_digital_base': {'required': False, 'allow_blank': True},
            'is_overseas_base': {'required': False, 'allow_blank': True},
            'company': {'required': False, 'allow_blank': True},
            'company_credit_code': {'required': False, 'allow_blank': True},
            'internship_area_code': {'required': False, 'allow_blank': True},
            'internship_address': {'required': False, 'allow_blank': True},
            'has_liability_insurance': {'required': False, 'allow_blank': True},
            'has_accident_insurance': {'required': False, 'allow_blank': True},
            'has_safety_training': {'required': False, 'allow_blank': True},
            'has_tripartite_agreement': {'required': False, 'allow_blank': True},
            'company_acquisition_method': {'required': False, 'allow_blank': True},
            'has_emergency_plan': {'required': False, 'allow_blank': True},
            'start_date': {'required': False, 'allow_null': True},
            'end_date': {'required': False, 'allow_null': True},
            'total_days': {'required': False, 'allow_null': True},
            'internship_position': {'required': False, 'allow_blank': True},
            'internship_salary': {'required': False, 'allow_blank': True},
            'company_supervisor': {'required': False, 'allow_blank': True},
            'teacher': {'required': False, 'allow_blank': True},
        }
