"""
初始化数据脚本
创建管理员账号和基础数据
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_system.settings')
django.setup()

# 自动执行数据库迁移
from django.core.management import call_command
call_command('migrate', verbosity=0)

from accounts.models import User
from batch.models import Batch
from announcement.models import Announcement


def init_data():
    print("开始初始化数据...")
    
    # 创建管理员账号
    if not User.objects.filter(student_id='admin').exists():
        admin = User.objects.create_superuser(
            student_id='admin',
            username='admin',
            password='admin123',
            name='管理员',
            role='admin'
        )
        print(f"✓ 创建管理员账号: {admin.student_id}")
    else:
        print("✓ 管理员账号已存在")
    
    # 创建默认批次
    if not Batch.objects.filter(name='2024-1').exists():
        batch = Batch.objects.create(
            name='2024-1',
            deadline='2025-06-30 23:59'
        )
        print(f"✓ 创建默认批次: {batch.name}")
    else:
        print("✓ 默认批次已存在")
    
    # 创建使用说明公告
    if not Announcement.objects.filter(title='系统使用说明').exists():
        announcement = Announcement.objects.create(
            title='系统使用说明',
            content='''
欢迎使用专业实习报告系统！

1. 首次登录
   使用学号和初始密码（学号）登录，首次登录需修改密码。
   完善个人信息后方可填写实习信息。

2. 按顺序完成以下五个步骤
   ① 个人信息 — 确认学号、姓名、学院等基本信息
   ② 实习信息 — 填写实习单位、指导教师、实习时间等
   ③ 实习登记 — 填写自我鉴定
   ④ 实习报告 — 填写实习内容
   ⑤ 监管信息 — 填写实习监管
   每个步骤填写完成后点击"下一步"，全部完成后提交。

3. 修改已提交的内容
   再次点击"编辑实习信息"即可读取上一次提交的内容，
   修改后重新提交即可覆盖原记录，无需全部重填。

4. 下载文档
   提交完成后可下载 Word/Excel 格式的实习文档，
   打印并签字后提交。

5. 注意事项
   · 请确保填写的信息真实准确
   · 如有问题请联系学院教务老师
            ''',
            is_active=True
        )
        print(f"✓ 创建使用说明公告: {announcement.title}")
    else:
        print("✓ 使用说明公告已存在")
    
    print("\n数据初始化完成！")
    print("管理员账号: admin / admin123")


if __name__ == '__main__':
    init_data()
