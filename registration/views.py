from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Registration
from .serializers import RegistrationSerializer
from internship_system.docgen import generate_registration_excel
from internship_system.crud_base import make_detail_view


registration_detail = make_detail_view(Registration, RegistrationSerializer, '实习登记表')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_registration(request, student_id):
    """下载实习登记表 Excel"""
    if student_id in ('my-registration', 'my'):
        student_id = request.user.student_id
    if request.user.student_id != student_id and not request.user.is_admin:
        return Response({'success': False, 'message': '无权访问'}, status=403)

    try:
        obj = Registration.objects.select_related('student').get(student_id=student_id)
    except Registration.DoesNotExist:
        return Response({
            'success': False, 'message': '未找到登记记录，请先填写实习信息'
        }, status=404)

    data = obj.to_export_dict()
    file_stream = generate_registration_excel(data)
    filename = f"{data.get('studentId', student_id)}_{obj.name}_实习情况登记表.xlsx"
    from django.http import FileResponse
    return FileResponse(file_stream, as_attachment=True, filename=filename)
