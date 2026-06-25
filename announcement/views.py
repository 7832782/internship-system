from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import models
from .models import Announcement
from .serializers import AnnouncementSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def announcement_list(request):
    """获取公告列表/创建公告"""
    if request.method == 'GET':
        # 管理员看到所有公告，普通用户只看到启用的
        if request.user.is_authenticated and request.user.is_admin:
            announcements = Announcement.objects.all()
        else:
            announcements = Announcement.objects.filter(is_active=True)
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 检查登录和权限
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': '请先登录'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_admin:
            return Response({
                'success': False,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            # 新公告自动排在最后
            max_order = Announcement.objects.aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0
            serializer.save(order=max_order + 1)
            return Response({
                'success': True,
                'message': '公告创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def announcement_move_up(request, pk):
    """公告上移"""
    if not request.user.is_admin:
        return Response({'success': False, 'message': '权限不足'}, status=403)
    try:
        current = Announcement.objects.get(pk=pk)
    except Announcement.DoesNotExist:
        return Response({'success': False, 'message': '公告不存在'}, status=404)

    prev = Announcement.objects.filter(order__lt=current.order).order_by('-order').first()
    if not prev:
        return Response({'success': False, 'message': '已经是第一条'}, status=400)

    current.order, prev.order = prev.order, current.order
    current.save(update_fields=['order'])
    prev.save(update_fields=['order'])
    return Response({'success': True, 'message': '上移成功'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def announcement_move_down(request, pk):
    """公告下移"""
    if not request.user.is_admin:
        return Response({'success': False, 'message': '权限不足'}, status=403)
    try:
        current = Announcement.objects.get(pk=pk)
    except Announcement.DoesNotExist:
        return Response({'success': False, 'message': '公告不存在'}, status=404)

    next_ = Announcement.objects.filter(order__gt=current.order).order_by('order').first()
    if not next_:
        return Response({'success': False, 'message': '已经是最后一条'}, status=400)

    current.order, next_.order = next_.order, current.order
    current.save(update_fields=['order'])
    next_.save(update_fields=['order'])
    return Response({'success': True, 'message': '下移成功'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def announcement_detail(request, pk):
    """获取/更新/删除单个公告"""
    try:
        announcement = Announcement.objects.get(pk=pk)
    except Announcement.DoesNotExist:
        return Response({
            'success': False,
            'message': '公告不存在'
        }, status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '公告更新成功',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        announcement.delete()
        return Response({
            'success': True,
            'message': '公告删除成功'
        })
