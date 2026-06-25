from django.db import models
from accounts.models import User


class Supervision(models.Model):
    """实习监管信息模型"""
    
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='supervision',
        verbose_name='学生'
    )
    
    # 基本信息
    name = models.CharField('姓名', max_length=50)
    enrollment_year = models.CharField('入学年份', max_length=4, blank=True)
    college = models.CharField('学院', max_length=100)
    class_number = models.CharField('班级', max_length=50, blank=True)
    
    # 课程信息
    course_name = models.CharField('课程名称', max_length=100, default='专业实习')
    course_code = models.CharField('课程代码', max_length=20, default='CSE450')
    credits = models.CharField('学分', max_length=20, default='4（4）')
    internship_type = models.CharField('实习类型', max_length=50, default='专业实习')
    internship_org_form = models.CharField('组织形式', max_length=50, default='集中实习')
    internship_method = models.CharField('实习方式', max_length=50, default='现场实习')
    academic_year = models.CharField('学年', max_length=50, default='2024-2025学年')
    
    # 实习基地信息
    is_school_base = models.CharField('是否校内基地', max_length=10, default='否')
    is_digital_base = models.CharField('是否数字化基地', max_length=10, default='否')
    is_overseas_base = models.CharField('是否境外基地', max_length=10, default='否')
    
    # 实习单位信息
    company = models.CharField('实习单位', max_length=100)
    company_credit_code = models.CharField('统一社会信用代码', max_length=50, blank=True)
    internship_area_code = models.CharField('实习地区代码', max_length=20, blank=True)
    internship_address = models.CharField('实习详细地址', max_length=200)
    
    # 安全保障
    has_liability_insurance = models.CharField('是否有责任保险', max_length=10, default='是')
    has_accident_insurance = models.CharField('是否有意外险', max_length=10, default='是')
    has_safety_training = models.CharField('是否有安全培训', max_length=10, default='是')
    has_tripartite_agreement = models.CharField('是否有三方协议', max_length=10, default='是')
    company_acquisition_method = models.CharField('单位获取方式', max_length=50, blank=True)
    has_emergency_plan = models.CharField('是否有应急预案', max_length=10, default='是')
    
    # 实习时间和岗位
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    total_days = models.IntegerField('实习天数', null=True, blank=True)
    internship_position = models.CharField('实习岗位', max_length=100, blank=True)
    internship_salary = models.CharField('实习薪资', max_length=50, blank=True)
    company_supervisor = models.CharField('企业导师', max_length=50, blank=True)
    teacher = models.CharField('校内导师', max_length=50, blank=True)
    
    # 元数据
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '实习监管信息'
        verbose_name_plural = '实习监管信息'
        db_table = 'supervisions'
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.company}"

    def to_export_dict(self):
        """返回用于 Excel 导出的数据字典"""
        s = self.student
        return {
            'studentId': s.student_id, 'name': self.name,
            'enrollmentYear': self.enrollment_year, 'college': self.college,
            'classNumber': self.class_number, 'courseName': self.course_name,
            'courseCode': self.course_code, 'credits': self.credits,
            'internshipType': self.internship_type, 'internshipOrgForm': self.internship_org_form,
            'internshipMethod': self.internship_method, 'academicYear': self.academic_year,
            'teacher': self.teacher, 'company': self.company,
            'companyCreditCode': self.company_credit_code,
            'internshipAreaCode': self.internship_area_code,
            'internshipAddress': self.internship_address,
            'hasLiabilityInsurance': self.has_liability_insurance,
            'hasAccidentInsurance': self.has_accident_insurance,
            'hasSafetyTraining': self.has_safety_training,
            'hasTripartiteAgreement': self.has_tripartite_agreement,
            'companyAcquisitionMethod': self.company_acquisition_method,
            'hasEmergencyPlan': self.has_emergency_plan,
            'isSchoolBase': self.is_school_base, 'isDigitalBase': self.is_digital_base,
            'isOverseasBase': self.is_overseas_base,
            'startDate': str(self.start_date) if self.start_date else '',
            'endDate': str(self.end_date) if self.end_date else '',
            'totalDays': str(self.total_days) if self.total_days is not None else '',
            'internshipPosition': self.internship_position,
            'internshipSalary': self.internship_salary,
            'companySupervisor': self.company_supervisor,
        }
