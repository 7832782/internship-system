from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型，使用学号作为用户名"""
    
    # 学号作为主键，同时作为 username
    student_id = models.CharField('学号', max_length=20, unique=True, primary_key=True)
    
    # 基本信息
    name = models.CharField('姓名', max_length=50, blank=True)
    gender = models.CharField('性别', max_length=10, blank=True, choices=[
        ('男', '男'),
        ('女', '女'),
    ])
    college = models.CharField('学院', max_length=100, blank=True)
    major = models.CharField('专业', max_length=100, blank=True)
    class_number = models.CharField('班级', max_length=50, blank=True)
    
    # 批次和角色
    batch = models.CharField('批次', max_length=50, default='无')
    role = models.CharField('角色', max_length=20, default='student', choices=[
        ('student', '学生'),
        ('admin', '管理员'),
    ])
    
    # 资料完成状态
    is_profile_complete = models.BooleanField('资料是否完整', default=False)
    
    # username 字段 - 与 student_id 保持一致
    username = models.CharField('用户名', max_length=20, unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['student_id', 'name']
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'users'
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student_id} - {self.name or '未命名'}"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def save(self, *args, **kwargs):
        # 确保 username 始终与 student_id 保持同步
        if self.student_id:
            self.username = self.student_id
        super().save(*args, **kwargs)
