from django.db import models
from accounts.models import User


class Registration(models.Model):
    """实习情况登记表模型"""
    
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='registration',
        verbose_name='学生'
    )
    
    # 基本信息
    name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=10)
    college = models.CharField('学院', max_length=100)
    major = models.CharField('专业', max_length=100)
    
    # 实习信息
    company = models.CharField('实习单位', max_length=100)
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    total_days = models.IntegerField('实习天数', null=True, blank=True)
    
    # 自我评价
    self_evaluation = models.TextField('自我评价', blank=True)
    
    # 元数据
    submit_date = models.DateTimeField('提交日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '实习登记表'
        verbose_name_plural = '实习登记表'
        db_table = 'registrations'
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.company}"

    def to_export_dict(self):
        """返回用于 Excel 导出的数据字典"""
        s = self.student
        return {
            'studentId': s.student_id, 'name': self.name,
            'gender': self.gender, 'college': self.college, 'major': self.major,
            'company': self.company,
            'startDate': str(self.start_date) if self.start_date else '',
            'endDate': str(self.end_date) if self.end_date else '',
            'totalDays': str(self.total_days) if self.total_days is not None else '',
            'selfEvaluation': self.self_evaluation,
        }
