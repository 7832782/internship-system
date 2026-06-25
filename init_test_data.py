"""生成测试数据：20 个学生 + 实习报告/登记/监管"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_system.settings')
django.setup()

from datetime import date, datetime
from accounts.models import User
from internship.models import Internship
from registration.models import Registration
from supervision.models import Supervision
from batch.models import Batch

COLLEGES = ['计算机与软件学院', '电子与信息工程学院', '数学与统计学院', '物理与光电工程学院', '化学与环境工程学院']
MAJORS = ['计算机科学与技术', '软件工程', '电子信息工程', '通信工程', '数学与应用数学',
          '物理学', '光电信息科学与工程', '化学', '环境工程', '人工智能']
COMPANIES = ['腾讯科技', '阿里巴巴', '百度', '字节跳动', '华为技术',
             '中兴通讯', '大疆创新', '商汤科技', '科大讯飞', '比亚迪',
             '美团', '京东', '网易', '小米科技', '拼多多',
             '快手', '哔哩哔哩', '蔚来汽车', '中国平安', '华大基因']
TEACHERS = ['张教授', '李教授', '王教授', '陈教授', '刘教授',
            '赵教授', '周教授', '吴教授', '郑教授', '孙教授']

def create_test_data():
    # 更新批次有效期
    batch, _ = Batch.objects.get_or_create(name='2024-1')
    batch.deadline = date(2027, 12, 31)
    batch.save()
    print('[批次] 2024-1 截止日期已更新为 2027-12-31')

    # 创建额外批次
    Batch.objects.get_or_create(name='2025-1', defaults={'deadline': date(2028, 6, 30)})

    count = 0
    for i in range(1, 21):
        sid = f'2024{str(i).zfill(4)}'
        if User.objects.filter(student_id=sid).exists():
            print(f'[跳过] {sid} 已存在')
            continue

        college = COLLEGES[i % len(COLLEGES)]
        major = MAJORS[i % len(MAJORS)]
        company = COMPANIES[i % len(COMPANIES)]
        teacher = TEACHERS[i % len(TEACHERS)]

        # 创建用户
        user = User.objects.create_user(
            username=sid,
            student_id=sid,
            password=sid,
            name=f'测试学生{i}',
            gender='男' if i % 2 == 1 else '女',
            college=college,
            major=major,
            class_number=str(i % 5 + 1).zfill(2),
            batch='2024-1',
        )
        user.is_profile_complete = True
        user.save()
        print(f'[用户] {sid} 测试学生{i} / {college} / 密码={sid}')

        # 实习报告
        Internship.objects.create(
            student=user,
            name=user.name, college=user.college, major=user.major,
            teacher=teacher, company=company,
            start_date=date(2026, 3, 1), end_date=date(2026, 5, 30),
            total_days=90,
            internship_content=f'在{company}参与后端开发工作，负责API接口设计与实现，'
                              f'参与了{["需求评审","系统设计","编码实现","测试部署"][i%4]}阶段的工作',
            experience=f'通过这次实习，深入了解了企业级开发流程，提升了{["编程","沟通","项目管理","团队协作"][i%4]}能力',
            suggestions='建议增加更多实践环节',
        )
        print(f'  [实习报告] OK')

        # 实习登记
        Registration.objects.create(
            student=user,
            name=user.name, gender=user.gender,
            college=user.college, major=user.major,
            company=company,
            start_date=date(2026, 3, 1), end_date=date(2026, 5, 30),
            total_days=90,
            self_evaluation=f'在{company}实习期间，工作认真负责，完成了各项任务，得到了导师的认可。',
        )
        print(f'  [实习登记] OK')

        # 实习监管
        Supervision.objects.create(
            student=user,
            name=user.name, enrollment_year='2022',
            college=user.college, class_number=user.class_number,
            course_name='专业实习', course_code='CSE450', credits='4（4）',
            internship_type='专业实习', internship_org_form='集中实习', internship_method='现场实习',
            academic_year='2024-2025学年',
            is_school_base='否', is_digital_base='否', is_overseas_base='否',
            company=company, company_credit_code=f'91440300MA{i:05d}XXXX',
            internship_area_code=f'广东省深圳市南山区-440305',
            internship_address=f'深圳市南山区{["科技园","粤海街道","高新区"][i%3]}XX号',
            has_liability_insurance='是', has_accident_insurance='是',
            has_safety_training='是', has_tripartite_agreement='是',
            company_acquisition_method='学校组织联系' if i % 2 == 0 else '学生自行联系',
            has_emergency_plan='是',
            start_date=date(2026, 3, 1), end_date=date(2026, 5, 30), total_days=90,
            internship_position=['后端开发','前端开发','数据分析','测试工程师','产品经理'][i%5],
            internship_salary=f'{3000 + i * 200}',
            company_supervisor=f'企业导师{i}', teacher=teacher,
        )
        print(f'  [实习监管] OK')
        count += 1

    print(f'\n完成！共创建 {count} 个测试学生。')
    print(f'管理员: admin / admin123')
    print(f'学生账号: 20240001~20240020，密码为学号')

if __name__ == '__main__':
    create_test_data()
