from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import re


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    studentId = serializers.CharField(source='student_id', read_only=True)
    classNumber = serializers.CharField(source='class_number', read_only=True)
    isProfileComplete = serializers.BooleanField(source='is_profile_complete', read_only=True)
    
    class Meta:
        model = User
        fields = ['studentId', 'username', 'name', 'gender', 'college', 'major', 'classNumber', 
                  'batch', 'role', 'isProfileComplete', 'last_login', 'date_joined']
        read_only_fields = ['last_login', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    
    class Meta:
        model = User
        fields = ['student_id', 'name', 'gender', 'college', 'major', 'class_number', 'batch']


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    studentId = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        student_id = data.get('studentId')
        password = data.get('password')
        
        if student_id and password:
            user = authenticate(username=student_id, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('用户已被禁用')
                data['user'] = user
            else:
                raise serializers.ValidationError('学号或密码错误')
        else:
            raise serializers.ValidationError('请提供学号和密码')
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器——统一 camelCase 入参，内部映射"""
    oldPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True, min_length=6, max_length=20)

    def validate(self, data):
        old = data.get('oldPassword', '')
        new = data.get('newPassword', '')
        if not old:
            raise serializers.ValidationError('请提供原密码')
        if not new or len(new) < 6:
            raise serializers.ValidationError('新密码至少6位')
        if len(new) > 20:
            raise serializers.ValidationError('新密码不能超过20位')
        if not re.match(r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]+$", new):
            raise serializers.ValidationError('密码只能包含字母、数字和常用符号')
        user = self.context['request'].user
        if not user.check_password(old):
            raise serializers.ValidationError('原密码错误')
        if old == new:
            raise serializers.ValidationError('新密码不能与原密码相同')
        if new == user.student_id:
            raise serializers.ValidationError('新密码不能为学号')
        # 内部统一为 snake_case 供视图层使用
        data['old_password'] = old
        data['new_password'] = new
        return data
