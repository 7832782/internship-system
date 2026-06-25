from django.urls import path
from . import views

urlpatterns = [
    path('batches', views.batch_list, name='batch-list'),
    path('batches/<int:pk>', views.batch_detail, name='batch-detail'),
    path('check-batch-deadline', views.check_deadline, name='check-deadline'),
]
