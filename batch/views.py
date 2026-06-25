from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Batch
from .serializers import BatchSerializer
from internship_system.utils import check_batch_deadline


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def batch_list(request):
    """获取批次列表/创建批次"""
    if request.method == 'GET':
        batches = Batch.objects.all()
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # 检查是否为管理员
        if not request.user.is_admin:
            return Response({
                'success': False,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '批次创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_deadline(request):
    """检查当前用户所在批次是否已截止（服务端时间）"""
    ok, msg = check_batch_deadline(request.user)
    return Response({
        'canSubmit': ok,
        'message': msg if not ok else ''
    })


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def batch_detail(request, pk):
    """获取/更新/删除批次"""
    try:
        batch = Batch.objects.get(pk=pk)
    except Batch.DoesNotExist:
        return Response({
            'success': False,
            'message': '批次不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BatchSerializer(batch)
        return Response(serializer.data)
    
    # 以下操作需要管理员权限
    if not request.user.is_admin:
        return Response({
            'success': False,
            'message': '权限不足'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = BatchSerializer(batch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '批次更新成功',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        batch.delete()
        return Response({
            'success': True,
            'message': '批次删除成功'
        })
