from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration_detail, name='registration-detail'),
    path('download-registration/<str:student_id>', views.download_registration, name='download-registration'),
    path('download/my-registration', views.download_registration, {'student_id': 'my-registration'}, name='download-my-registration'),
]
