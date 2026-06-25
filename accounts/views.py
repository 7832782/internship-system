from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from .models import User
from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer, ChangePasswordSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """获取 CSRF Token"""
    return Response({'csrf_token': get_token(request)})


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """用户登录"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
            'needChangePassword': user.check_password(user.student_id),
        })
    return Response({
        'success': False,
        'error': serializer.errors.get('non_field_errors', ['登录失败'])[0],
        'message': serializer.errors.get('non_field_errors', ['登录失败'])[0]
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """用户登出"""
    logout(request)
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([AllowAny])
def check_login(request):
    """检查登录状态"""
    if request.user.is_authenticated:
        user = request.user
        # 密码是否仍为学号（默认密码未修改），用于前端强制首次改密码逻辑
        need_change = user.check_password(user.student_id)
        return Response({
            'isLoggedIn': True,
            'user': UserSerializer(user).data,
            'needChangePassword': need_change,
        })
    return Response({'isLoggedIn': False})


def _first_error(errors):
    """从 DRF serializer.errors 中提取第一条人类可读的错误信息字符串"""
    if isinstance(errors, dict):
        for key in ('non_field_errors', '__all__'):
            msgs = errors.get(key)
            if msgs:
                return str(msgs[0]) if isinstance(msgs, list) else str(msgs)
        for key, val in errors.items():
            if isinstance(val, list) and val:
                return str(val[0])
            if isinstance(val, str):
                return val
            if isinstance(val, dict):
                return _first_error(val)
    if isinstance(errors, list) and errors:
        return str(errors[0])
    return str(errors)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """获取/更新用户资料"""
    user = request.user
    
    if request.method == 'GET':
        return Response(UserProfileSerializer(user).data)
    
    # POST - 更新资料
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        # 检查资料是否完整
        name = request.data.get('name', user.name)
        gender = request.data.get('gender', user.gender)
        college = request.data.get('college', user.college)
        major = request.data.get('major', user.major)
        class_number = request.data.get('class_number', user.class_number)
        
        if all([name, gender, college, major, class_number]):
            user.is_profile_complete = True

        serializer.save()
        user.save(update_fields=['is_profile_complete'])
        return Response({
            'success': True,
            'message': '资料更新成功',
            'user': UserSerializer(user).data
        })
    
    return Response({
        'success': False,
        'error': _first_error(serializer.errors),
        'message': _first_error(serializer.errors)
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({
            'success': True,
            'message': '密码修改成功'
        })
    return Response({
        'success': False,
        'error': _first_error(serializer.errors),
        'message': _first_error(serializer.errors)
    }, status=status.HTTP_400_BAD_REQUEST)
