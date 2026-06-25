from rest_framework import serializers
from .models import Batch


class BatchSerializer(serializers.ModelSerializer):
    """批次序列化器"""

    class Meta:
        model = Batch
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        if value == '无':
            raise serializers.ValidationError('批次名不能为"无"')
        # 检查唯一性（排除当前记录）
        instance = getattr(self, 'instance', None)
        qs = Batch.objects.filter(name=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError(f'批次名 "{value}" 已存在')
        return value
