"""通用 CRUD 视图工厂——消除 internship/registration/supervision 三份重复代码"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse

from accounts.models import User
from .utils import check_batch_deadline


def make_detail_view(model_class, serializer_class, entity_name):
    """工厂函数：生成学生端 GET / POST / PUT 三合一的详情视图函数。

    返回的视图函数已带有 @api_view 和 @permission_classes 装饰器。
    """
    @api_view(['GET', 'POST', 'PUT'])
    @permission_classes([IsAuthenticated])
    def view_fn(request):
        user = request.user

        if request.method == 'GET':
            if user.is_admin:
                student_id = request.query_params.get('student_id')
                if student_id:
                    try:
                        target_user = User.objects.get(student_id=student_id)
                    except User.DoesNotExist:
                        return Response({
                            'success': False,
                            'message': '学生不存在'
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    target_user = user
            else:
                target_user = user

            try:
                obj = model_class.objects.get(student=target_user)
                return Response(serializer_class(obj).data)
            except model_class.DoesNotExist:
                return Response({
                    'exists': False,
                    'message': f'尚未提交{entity_name}'
                })

        elif request.method == 'POST':
            ok, msg = check_batch_deadline(user)
            if not ok:
                return Response({'success': False, 'message': msg},
                                status=status.HTTP_403_FORBIDDEN)

            if model_class.objects.filter(student=user).exists():
                return Response({
                    'success': False,
                    'message': f'已存在{entity_name}，请使用更新功能'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(student=user)
                return Response({
                    'success': True,
                    'message': f'{entity_name}提交成功',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            ok, msg = check_batch_deadline(user)
            if not ok:
                return Response({'success': False, 'message': msg},
                                status=status.HTTP_403_FORBIDDEN)

            try:
                obj = model_class.objects.get(student=user)
            except model_class.DoesNotExist:
                return Response({
                    'success': False,
                    'message': f'{entity_name}不存在'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': f'{entity_name}更新成功',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': False, 'message': '不支持的请求方法'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return view_fn
