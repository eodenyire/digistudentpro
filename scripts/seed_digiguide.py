"""
Seed script for digiguide app - Creates education structure and 1000+ records
"""
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from faker import Faker
from apps.digiguide.models import (
    EducationLevel, Grade, Subject, Cluster, ClusterSubjectRequirement,
    Career, AcademicRecord
)
from apps.accounts.models import StudentProfile

fake = Faker()
Faker.seed(42)

def create_education_levels():
    """Create Kenya education levels"""
    print(f"\n📚 Creating education levels...")
    
    levels_data = [
        {'name': 'Primary', 'code': 'PRIMARY', 'order': 1},
        {'name': 'Lower Secondary', 'code': 'LOWER_SEC', 'order': 2},
        {'name': 'Upper Secondary', 'code': 'UPPER_SEC', 'order': 3},
        {'name': 'Tertiary', 'code': 'TERTIARY', 'order': 4},
    ]
    
    levels = []
    for data in levels_data:
        level, created = EducationLevel.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        levels.append(level)
    
    print(f"✅ Created {len(levels)} education levels")
    return levels

def create_grades(levels):
    """Create grades for each level"""
    print(f"\n🎓 Creating grades...")
    
    grades_data = {
        'PRIMARY': [
            ('Grade 1', 'G1'), ('Grade 2', 'G2'), ('Grade 3', 'G3'),
            ('Grade 4', 'G4'), ('Grade 5', 'G5'), ('Grade 6', 'G6'),
        ],
        'LOWER_SEC': [
            ('Form 1', 'F1'), ('Form 2', 'F2'),
        ],
        'UPPER_SEC': [
            ('Form 3', 'F3'), ('Form 4', 'F4'),
        ],
        'TERTIARY': [
            ('Year 1', 'Y1'), ('Year 2', 'Y2'), ('Year 3', 'Y3'),
        ],
    }
    
    grades = []
    for level in levels:
        data = grades_data.get(level.code, [])
        for idx, (name, code) in enumerate(data):
            grade, created = Grade.objects.get_or_create(
                education_level=level,
                code=code,
                defaults={
                    'name': name,
                    'order': idx,
                    'age_range': f"{6 + idx}-{7 + idx} years"
                }
            )
            grades.append(grade)
    
    print(f"✅ Created {len(grades)} grades")
    return grades

def create_subjects(levels):
    """Create subjects for education levels"""
    print(f"\n📖 Creating subjects...")
    
    subjects_list = [
        'Mathematics', 'English', 'Kiswahili', 'Science', 'Social Studies',
        'Physical Education', 'ICT', 'Biology', 'Chemistry', 'Physics',
        'Business Studies', 'Geography', 'History', 'Literature', 'Grammar'
    ]
    
    subjects = []
    for name in subjects_list:
        subject, created = Subject.objects.get_or_create(
            code=name.upper().replace(' ', '_'),
            defaults={
                'name': name,
                'description': f"{name} curriculum content",
                'is_core': name in ['Mathematics', 'English', 'Kiswahili', 'Science']
            }
        )
        # Add to all levels
        subject.education_levels.set(levels)
        subjects.append(subject)
    
    print(f"✅ Created {len(subjects)} subjects")
    return subjects

def create_clusters(subjects):
    """Create KUCCPS clusters"""
    print(f"\n🎯 Creating KUCCPS clusters...")
    
    clusters_data = [
        ('CLUSTER001', 'Engineering', 'Engineering and related courses'),
        ('CLUSTER002', 'Medicine', 'Medicine and health professions'),
        ('CLUSTER003', 'Law', 'Law and legal studies'),
        ('CLUSTER004', 'Business', 'Business and commerce'),
        ('CLUSTER005', 'Education', 'Education and teaching'),
        ('CLUSTER006', 'Agriculture', 'Agriculture and natural resources'),
        ('CLUSTER007', 'Computing', 'Computing and IT'),
        ('CLUSTER008', 'Arts', 'Arts and humanities'),
        ('CLUSTER009', 'Social Sciences', 'Social sciences and development'),
        ('CLUSTER010', 'Pure Sciences', 'Pure sciences'),
    ]
    
    clusters = []
    for code, name, desc in clusters_data:
        cluster, created = Cluster.objects.get_or_create(
            code=code,
            defaults={'name': name, 'description': desc}
        )
        clusters.append(cluster)
    
    print(f"✅ Created {len(clusters)} clusters")
    return clusters

def create_cluster_requirements(clusters, subjects):
    """Create subject requirements for clusters"""
    print(f"\n✅ Creating cluster subject requirements...")
    
    subject_list = list(subjects)
    grade_choices = ['A', 'B+', 'B', 'C+', 'C']
    
    requirement_count = 0
    for cluster in clusters:
        # Add 3-6 subjects per cluster
        num_subjects = fake.random_int(min=3, max=6)
        cluster_subjects = fake.random_elements(
            elements=subject_list,
            length=min(num_subjects, len(subject_list)),
            unique=True
        )
        
        for subject in cluster_subjects:
            _, created = ClusterSubjectRequirement.objects.get_or_create(
                cluster=cluster,
                subject=subject,
                defaults={
                    'minimum_grade': fake.random_element(grade_choices),
                    'is_mandatory': fake.boolean(chance_percent=70)
                }
            )
            if created:
                requirement_count += 1
    
    print(f"✅ Created {requirement_count} cluster requirements")

def create_careers(clusters):
    """Create career options"""
    print(f"\n💼 Creating careers...")
    
    careers_data = [
        # Engineering careers
        ('Software Engineer', 'Engineering'), ('Mechanical Engineer', 'Engineering'),
        ('Civil Engineer', 'Engineering'), ('Electrical Engineer', 'Engineering'),
        
        # Medical careers
        ('Doctor', 'Medicine'), ('Nurse', 'Medicine'), ('Pharmacist', 'Medicine'),
        ('Dentist', 'Medicine'),
        
        # Law careers
        ('Lawyer', 'Law'), ('Prosecutor', 'Law'), ('Judge', 'Law'),
        
        # Business careers
        ('Accountant', 'Business'), ('Financial Analyst', 'Business'),
        ('Business Manager', 'Business'), ('Entrepreneur', 'Business'),
        
        # IT careers
        ('Data Scientist', 'IT'), ('Network Admin', 'IT'), ('Database Admin', 'IT'),
        ('Cybersecurity Expert', 'IT'),
        
        # Education
        ('Teacher', 'Education'), ('School Principal', 'Education'),
        ('Curriculum Developer', 'Education'),
        
        # Agriculture
        ('Agricultural Scientist', 'Agriculture'), ('Farmer', 'Agriculture'),
    ]
    
    careers = []
    for name, industry in careers_data:
        career, created = Career.objects.get_or_create(
            name=name,
            defaults={
                'description': fake.paragraph(),
                'cluster': fake.random_element(list(clusters)),
                'salary_range': f"KES {fake.random_int(min=30000, max=500000):,} - {fake.random_int(min=100000, max=1000000):,}",
                'job_outlook': fake.paragraph(),
                'required_qualifications': fake.paragraph(),
                'skills_needed': ", ".join([fake.word() for _ in range(5)]),
                'related_courses': ", ".join([fake.word() for _ in range(3)]),
                'industry': industry,
                'is_active': True
            }
        )
        careers.append(career)
    
    print(f"✅ Created {len(careers)} careers")
    return careers

def create_academic_records():
    """Create academic records for students"""
    print(f"\n📊 Creating academic records...")
    
    students = StudentProfile.objects.all()[:1000]
    grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
    terms = [1, 2, 3]
    years = [2022, 2023, 2024]
    
    records = []
    for student in students:
        for year in years:
            for term in terms:
                record = AcademicRecord.objects.create(
                    student=student,
                    academic_year=year,
                    term=term,
                    subject=fake.word(),
                    grade=fake.random_element(grades),
                    marks_scored=fake.random_int(min=0, max=100),
                    total_marks=100,
                    remarks=fake.sentence(),
                    teacher_name=fake.name()
                )
                records.append(record)
    
    print(f"✅ Created {len(records)} academic records")
    return records

def main():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 DIGIGUIDE APP SEEDING")
    print("=" * 60)
    
    try:
        levels = create_education_levels()
        grades = create_grades(levels)
        subjects = create_subjects(levels)
        clusters = create_clusters(subjects)
        create_cluster_requirements(clusters, subjects)
        careers = create_careers(clusters)
        records = create_academic_records()
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: DigiGuide app seeded")
        print(f"   - {len(levels)} education levels")
        print(f"   - {len(grades)} grades")
        print(f"   - {len(subjects)} subjects")
        print(f"   - {len(clusters)} clusters")
        print(f"   - {len(careers)} careers")
        print(f"   - {len(records)} academic records")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
