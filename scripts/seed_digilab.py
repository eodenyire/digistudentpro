"""
Seed script for digilab app - Creates 1000+ lab assignments and submissions
"""
import os
import sys
import django
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.utils import timezone
from faker import Faker
from apps.digilab.models import LabAssignment, LabSubmission
from apps.accounts.models import User, StudentProfile
from apps.digiguide.models import Grade

fake = Faker()
Faker.seed(42)

def create_lab_assignments(count=500):
    """Create lab assignments"""
    print(f"\n🧪 Creating {count} lab assignments...")
    
    instructors = list(User.objects.filter(role__in=['teacher', 'mentor']).all())[:100]
    if not instructors:
        instructors = list(User.objects.all())[:100]
    
    grades = list(Grade.objects.all())
    if not grades:
        print("⚠️  No grades found")
        return []
    
    assignments = []
    for i in range(count):
        assignment = LabAssignment.objects.create(
            title=f"Lab Assignment {i:04d}: {fake.sentence(nb_words=4)}",
            description=fake.paragraph(nb_sentences=5),
            subject=fake.word().title(),
            grade=fake.random_element(grades) if grades else None,
            instructor=fake.random_element(instructors),
            difficulty=fake.random_element(['beginner', 'intermediate', 'advanced']),
            instructions=fake.text(),
            expected_output=fake.text(),
            due_date=timezone.now() + timedelta(days=fake.random_int(min=1, max=90)),
            total_points=fake.random_int(min=10, max=100),
            estimated_hours=fake.random_int(min=1, max=10),
            is_published=fake.boolean(chance_percent=80),
            is_graded=fake.boolean(chance_percent=70)
        )
        assignments.append(assignment)
        
        if (i + 1) % 50 == 0:
            print(f"  ✓ Created {i + 1} assignments")
    
    print(f"✅ Created {count} lab assignments")
    return assignments

def create_lab_submissions(assignments):
    """Create lab submissions"""
    print(f"\n📤 Creating lab submissions...")
    
    students = StudentProfile.objects.all()[:1000]
    if not students:
        print("⚠️  No students found")
        return []
    
    submissions = []
    submission_count = 0
    
    for assignment in assignments:
        # Each assignment gets 2-10 submissions
        num_submissions = fake.random_int(min=2, max=10)
        available_students = list(students)
        
        for _ in range(min(num_submissions, len(available_students))):
            idx = fake.random_int(min=0, max=len(available_students) - 1)
            student = available_students.pop(idx)
            
            submission = LabSubmission.objects.create(
                assignment=assignment,
                student=student,
                submission_code=fake.text()[:500],
                submission_notes=fake.paragraph(),
                file_upload=None,  # In real scenario, this would have a file
                score=fake.random_int(min=0, max=assignment.total_points)
                if assignment.is_graded else None,
                feedback=fake.paragraph() if assignment.is_graded else None,
                is_submitted=True,
                submitted_at=timezone.now() - timedelta(
                    days=fake.random_int(min=1, max=30)
                ),
                graded_at=timezone.now() if assignment.is_graded else None,
                status=fake.random_element(['submitted', 'graded', 'pending_review'])
            )
            submissions.append(submission)
            submission_count += 1
        
        if submission_count % 500 == 0:
            print(f"  ✓ Created {submission_count} submissions")
    
    print(f"✅ Created {submission_count} submissions")
    return submissions

def main():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 DIGILAB APP SEEDING")
    print("=" * 60)
    
    try:
        assignments = create_lab_assignments(count=500)
        submissions = create_lab_submissions(assignments)
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: DigiLab app seeded")
        print(f"   - {len(assignments)} lab assignments")
        print(f"   - {len(submissions)} submissions")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
