from django.db import models


class Announcement(models.Model):
    """系统公告模型"""
    
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    is_active = models.BooleanField('是否启用', default=True)
    order = models.IntegerField('排序', default=0, help_text='数字越小越靠前')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        db_table = 'announcements'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
