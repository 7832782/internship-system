from django.urls import path, re_path
from . import views

urlpatterns = [
    path('internship', views.internship_detail, name='internship-detail'),
    path('download/my-report', views.download_internship, {'student_id': 'my-report'}, name='download-my-report'),
    re_path(r'^download/(?P<student_id>[a-zA-Z0-9]+)$', views.download_internship, name='download-internship'),
]
