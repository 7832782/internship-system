from django.db import models


class Batch(models.Model):
    """批次管理模型"""
    
    name = models.CharField('批次名称', max_length=50)
    deadline = models.DateTimeField('截止时间')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '批次'
        verbose_name_plural = '批次'
        db_table = 'batches'
        ordering = ['created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_expired(self):
        """检查批次是否已过期（基于服务器时间）"""
        from django.utils import timezone
        return timezone.now() > self.deadline
