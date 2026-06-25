from django.urls import path, re_path
from . import admin_views

urlpatterns = [
    path('settings', admin_views.admin_settings, name='admin-settings'),

    # 批量操作（必须在具体实体路由之前，避免 batch-delete 等被 detail 路由吞掉）
    path('import-students', admin_views.admin_import_students, name='admin-import-students'),
    path('reset-all-passwords', admin_views.admin_reset_all_passwords, name='admin-reset-all-passwords'),
    re_path(r'^batch-export/(?P<entity_type>[a-z]+)$', admin_views.admin_batch_export, name='admin-batch-export'),
    re_path(r'^(?P<entity_type>[a-z]+)/batch-delete$', admin_views.admin_batch_delete, name='admin-batch-delete'),
    re_path(r'^(?P<entity_type>[a-z]+)/(?P<student_id>[^/]+)/export$', admin_views.admin_export_detail, name='admin-export-detail'),

    # 实习报告
    path('internship', admin_views.admin_internship_list, name='admin-internship-list'),
    re_path(r'^internship/(?P<student_id>[^/]+)$', admin_views.admin_internship_detail, name='admin-internship-detail'),
    # 实习登记
    path('registration', admin_views.admin_registration_list, name='admin-registration-list'),
    re_path(r'^registration/(?P<student_id>[^/]+)$', admin_views.admin_registration_detail, name='admin-registration-detail'),
    # 实习监管
    path('supervision', admin_views.admin_supervision_list, name='admin-supervision-list'),
    re_path(r'^supervision/(?P<student_id>[^/]+)$', admin_views.admin_supervision_detail, name='admin-supervision-detail'),
    # 用户管理
    path('users', admin_views.admin_user_list, name='admin-user-list'),
    re_path(r'^users/(?P<student_id>[^/]+)/reset-password$', admin_views.admin_reset_password, name='admin-reset-password'),
    re_path(r'^users/batch-reset-password$', admin_views.admin_batch_reset_password, name='admin-batch-reset-password'),
    re_path(r'^users/(?P<student_id>[^/]+)$', admin_views.admin_user_detail, name='admin-user-detail'),
]
