"""工具函数：批次截止时间检查"""

from django.utils import timezone
from batch.models import Batch


def check_batch_deadline(user):
    """检查用户所在批次是否已截止。

    返回 (passed: bool, message: str)
    - passed=True: 未超期或无需检查，可以提交
    - passed=False: 已超期，禁止提交，message 包含提示
    """
    # 管理员不检查
    if user.is_admin:
        return True, ''

    batch_name = user.batch
    if not batch_name or batch_name == '无':
        return True, ''

    try:
        batch = Batch.objects.get(name=batch_name)
    except Batch.DoesNotExist:
        return True, ''

    if timezone.now() > batch.deadline:
        return False, f'您所在的批次（{batch_name}）已于 {batch.deadline.strftime("%Y-%m-%d %H:%M")} 截止提交'

    return True, ''
