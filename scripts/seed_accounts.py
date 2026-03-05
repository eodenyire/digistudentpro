"""
Seed script for accounts app - Creates 1000+ test users with various profiles
"""
import os
import sys
import django
from datetime import timedelta

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.utils import timezone
from faker import Faker
from apps.accounts.models import User, StudentProfile, MentorProfile, ParentGuardian
from apps.digiguide.models import Grade

fake = Faker()
Faker.seed(42)

def create_test_users(count=1000):
    """Create test users with different roles"""
    print(f"\n🧑‍💼 Creating {count} test users...")
    
    created_users = []
    roles = ['student', 'mentor', 'parent', 'teacher', 'admin']
    
    for i in range(count):
        role = roles[i % len(roles)]
        
        user = User.objects.create_user(
            username=f"user_{role}_{i:04d}",
            email=f"{role}_{i:04d}@digistudentpro.test",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=role,
            phone_number=fake.phone_number()[:15],
            is_verified=fake.boolean(chance_percent=70),
            date_of_birth=fake.date_of_birth(minimum_age=5, maximum_age=60),
            is_active=True
        )
        created_users.append(user)
        
        if (i + 1) % 100 == 0:
            print(f"  ✓ Created {i + 1} users")
    
    print(f"✅ Created {count} users")
    return created_users

def create_student_profiles(users):
    """Create student profiles for student users"""
    print(f"\n📚 Creating student profiles...")
    
    student_users = users[::5]  # Students are every 5th user (200 students)
    grades = list(Grade.objects.all())
    
    if not grades:
        print("⚠️  No grades found. Run digiguide seed script first.")
        return []
    
    created_profiles = []
    counties = [
        'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
        'Naivasha', 'Kiambu', 'Nyeri', 'Muranga', 'Uasin Gishu'
    ]
    
    for idx, user in enumerate(student_users):
        profile = StudentProfile.objects.create(
            user=user,
            student_id=f"STU-{timezone.now().year}-{idx:06d}",
            gender=fake.random_element(['M', 'F', 'O']),
            current_grade=fake.random_element(grades) if grades else None,
            school_name=f"{fake.word().title()} High School",
            county=fake.random_element(counties),
            interests=", ".join([fake.word() for _ in range(5)]),
            career_aspirations=fake.sentence(),
            has_parental_consent=fake.boolean(chance_percent=80),
            consent_date=timezone.now() - timedelta(days=fake.random_int(min=1, max=365))
        )
        created_profiles.append(profile)
    
    print(f"✅ Created {len(created_profiles)} student profiles")
    return created_profiles

def create_mentor_profiles(users):
    """Create mentor profiles for mentor users"""
    print(f"\n🎯 Creating mentor profiles...")
    
    mentor_users = users[1::5]  # Mentors are every 5th user starting at index 1 (200 mentors)
    professions = [
        'Software Engineer', 'Doctor', 'Lawyer', 'Accountant', 'Teacher',
        'Entrepreneur', 'Data Scientist', 'Architect', 'Pharmacist', 'Artist'
    ]
    expertise_areas = [
        'STEM', 'Mathematics', 'Science', 'Technology', 'Business',
        'Arts', 'Digital Skills', 'Leadership', 'Finance', 'Career Guidance'
    ]
    
    created_profiles = []
    verification_statuses = ['pending', 'verified', 'rejected', 'suspended']
    
    for idx, user in enumerate(mentor_users):
        profile = MentorProfile.objects.create(
            user=user,
            profession=fake.random_element(professions),
            organization=f"{fake.company()} Ltd",
            bio=fake.paragraph(nb_sentences=3),
            areas_of_expertise=", ".join(
                [fake.random_element(expertise_areas) for _ in range(3)]
            ),
            verification_status=fake.random_element(verification_statuses),
            badge_earned=fake.boolean(chance_percent=60),
            years_of_experience=fake.random_int(min=0, max=30),
            linkedin_url=fake.url() if fake.boolean() else None,
            verified_at=timezone.now() - timedelta(days=fake.random_int(min=1, max=180))
            if fake.boolean(chance_percent=70) else None
        )
        created_profiles.append(profile)
    
    print(f"✅ Created {len(created_profiles)} mentor profiles")
    return created_profiles

def create_parent_profiles(users, student_profiles):
    """Create parent/guardian profiles"""
    print(f"\n👨‍👩‍👧 Creating parent/guardian profiles...")
    
    parent_users = users[2::5]  # Parents are every 5th user starting at index 2 (200 parents)
    relationships = ['father', 'mother', 'guardian', 'sibling', 'other']
    
    created_profiles = []
    
    for idx, user in enumerate(parent_users):
        profile = ParentGuardian.objects.create(
            user=user,
            relationship=fake.random_element(relationships),
            phone_number=fake.phone_number()[:15],
            alternative_phone=fake.phone_number()[:15] if fake.boolean() else None,
            id_number=f"{fake.random_int(min=100000000, max=999999999)}"
        )
        
        # Assign random students to parent
        if student_profiles:
            num_students = fake.random_int(min=1, max=3)
            random_students = fake.random_elements(
                elements=student_profiles,
                length=min(num_students, len(student_profiles)),
                unique=True
            )
            profile.students.set(random_students)
        
        created_profiles.append(profile)
    
    print(f"✅ Created {len(created_profiles)} parent/guardian profiles")
    return created_profiles

def main():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 ACCOUNTS APP SEEDING")
    print("=" * 60)
    
    try:
        # Create users
        users = create_test_users(count=1000)
        
        # Create profiles
        student_profiles = create_student_profiles(users)
        mentor_profiles = create_mentor_profiles(users)
        parent_profiles = create_parent_profiles(users, student_profiles)
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: Accounts app seeded")
        print(f"   - {len(users)} users created")
        print(f"   - {len(student_profiles)} student profiles")
        print(f"   - {len(mentor_profiles)} mentor profiles")
        print(f"   - {len(parent_profiles)} parent profiles")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
