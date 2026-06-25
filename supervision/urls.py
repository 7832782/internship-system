from django.urls import path
from . import views

urlpatterns = [
    path('supervision', views.supervision_detail, name='supervision-detail'),
    path('download-supervision/<str:student_id>', views.download_supervision, name='download-supervision'),
    path('download/my-supervision', views.download_supervision, {'student_id': 'my-supervision'}, name='download-my-supervision'),
]
