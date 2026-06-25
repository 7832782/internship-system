from django.db import models
from accounts.models import User


class Internship(models.Model):
    """实习报告模型"""
    
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='internship',
        verbose_name='学生'
    )
    
    # 基本信息
    name = models.CharField('姓名', max_length=50)
    college = models.CharField('学院', max_length=100)
    major = models.CharField('专业', max_length=100)
    
    # 实习信息
    teacher = models.CharField('指导教师', max_length=50)
    company = models.CharField('实习单位', max_length=100)
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    total_days = models.IntegerField('实习天数', null=True, blank=True)
    
    # 报告内容
    internship_content = models.TextField('实习内容', blank=True)
    experience = models.TextField('实习体会', blank=True)
    suggestions = models.TextField('建议', blank=True)
    
    # 元数据
    submit_date = models.DateTimeField('提交日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '实习报告'
        verbose_name_plural = '实习报告'
        db_table = 'internships'
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.company}"

    def to_export_dict(self):
        """返回用于 Word 导出的数据字典"""
        s = self.student
        return {
            'college': self.college, 'major': self.major,
            'name': self.name, 'studentId': s.student_id,
            'teacher': self.teacher, 'company': self.company,
            'startDate': str(self.start_date) if self.start_date else '',
            'endDate': str(self.end_date) if self.end_date else '',
            'totalDays': str(self.total_days) if self.total_days is not None else '',
            'submitDate': str(self.submit_date.date()) if self.submit_date else '',
            'internshipContent': self.internship_content,
            'experience': self.experience,
            'suggestions': self.suggestions,
        }
