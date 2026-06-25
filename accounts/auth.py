from django.conf import settings
from rest_framework.authentication import SessionAuthentication


class SessionAuthentication(SessionAuthentication):
    """自定义 SessionAuthentication，使用项目设置中的 CSRF 开关"""

    def enforce_csrf(self, request):
        enforce = getattr(settings, 'REST_SESSION_AUTH_ENFORCE_CSRF', True)
        if not enforce:
            return
        return super().enforce_csrf(request)
