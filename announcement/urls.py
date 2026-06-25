from django.urls import path, re_path
from . import views

urlpatterns = [
    path('announcements', views.announcement_list, name='announcement-list'),
    re_path(r'^announcements/(?P<pk>\d+)$', views.announcement_detail, name='announcement-detail'),
    re_path(r'^announcements/(?P<pk>\d+)/move-up$', views.announcement_move_up, name='announcement-move-up'),
    re_path(r'^announcements/(?P<pk>\d+)/move-down$', views.announcement_move_down, name='announcement-move-down'),
]
