from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Internship
from .serializers import InternshipSerializer
from internship_system.docgen import generate_report
from internship_system.crud_base import make_detail_view


internship_detail = make_detail_view(Internship, InternshipSerializer, '实习报告')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_internship(request, student_id):
    """下载实习报告 Word 文档"""
    if student_id in ('my-report', 'my'):
        student_id = request.user.student_id
    if request.user.student_id != student_id and not request.user.is_admin:
        return Response({'success': False, 'message': '无权访问'}, status=403)

    try:
        obj = Internship.objects.select_related('student').get(student_id=student_id)
    except Internship.DoesNotExist:
        return Response({
            'success': False, 'message': '未找到实习记录，请先填写实习信息'
        }, status=404)

    data = obj.to_export_dict()
    file_stream = generate_report(data)
    filename = f"{data.get('studentId', student_id)}_{obj.name}_实习报告.docx"
    from django.http import FileResponse
    return FileResponse(file_stream, as_attachment=True, filename=filename)
