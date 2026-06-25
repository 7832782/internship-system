"""
URL configuration for internship_system project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import admin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('internship.urls')),
    path('api/', include('registration.urls')),
    path('api/', include('supervision.urls')),
    path('api/', include('batch.urls')),
    path('api/', include('announcement.urls')),
    path('api/admin/', include('internship_system.admin_urls')),
    path('api/settings', admin_views.public_settings, name='public-settings'),
    # 前端页面 - 支持带和不带 .html 后缀
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login', TemplateView.as_view(template_name='login.html'), name='login'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login_html'),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home.html', TemplateView.as_view(template_name='home.html'), name='home_html'),
    path('internship', TemplateView.as_view(template_name='internship-form.html'), name='internship'),
    path('internship.html', TemplateView.as_view(template_name='internship-form.html'), name='internship_html'),
    path('internship-form', TemplateView.as_view(template_name='internship-form.html'), name='internship-form'),
    path('internship-form.html', TemplateView.as_view(template_name='internship-form.html'), name='internship-form_html'),
    path('admin-page', TemplateView.as_view(template_name='admin.html'), name='admin-page'),
    path('admin.html', TemplateView.as_view(template_name='admin.html'), name='admin_html'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
