from django.db import models


class SystemSetting(models.Model):
    """系统配置（键值对）"""
    key = models.CharField('配置键', max_length=100, primary_key=True)
    value = models.CharField('配置值', max_length=500, blank=True)

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
        db_table = 'system_settings'

    def __str__(self):
        return f'{self.key}={self.value}'
