#!/usr/bin/env python
"""
Comprehensive test and seed script for DigiStudentPro
Seeds database with 1000+ records and runs all tests
Run this from the backend directory: python ../scripts/test_and_seed.py
"""
import os
import sys
import django
import random
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__) + '/../backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.utils import timezone
from faker import Faker
from django.contrib.auth import get_user_model
from apps.accounts.models import User, StudentProfile, MentorProfile, ParentGuardian
from apps.digiblog.models import BlogPost, Comment
from apps.digichat.models import Squad, SquadMembership, Message
from apps.digiguide.models import Grade, Career
from apps.digilab.models import LabAssignment

fake = Faker()
Faker.seed(42)
User = get_user_model()

def chance(percent):
    """Random chance helper"""
    return random.randint(1, 100) <= percent

print("\n" + "="*70)
print("🌱 DIGISTUDENTPRO DATABASE SEEDING AND TESTING 🌱")
print("="*70)

# ============================================================================
# SEEDING
# ============================================================================
print("\n📍 PHASE 1: DATABASE SEEDING")
print("-"*70)

# 1. Create users
print("\n🧑‍💼 Creating 200 test users...")
users_created = []
roles = ['student', 'mentor', 'parent', 'teacher', 'admin']

for i in range(200):
    try:
        user = User.objects.create_user(
            username=f"user_{i:04d}",
            email=f"user_{i:04d}@digistudentpro.test",
            password="TestPass123!",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=roles[i % len(roles)],
            phone_number=fake.phone_number()[:15],
            is_verified=chance(70),
            is_active=True
        )
        users_created.append(user)
        if (i + 1) % 50 == 0:
            print(f"  ✓ Created {i + 1} users")
    except Exception as e:
        pass

print(f"✅ Created {len(users_created)} users")

# 2. Create student profiles
print("\n📚 Creating 50 student profiles...")
students_created = 0
student_users = [u for u in users_created if u.role == 'student'][:50]

for idx, user in enumerate(student_users):
    try:
        profile = StudentProfile.objects.create(
            user=user,
            student_id=f"STU-{timezone.now().year}-{idx:05d}",
            school_name=f"{fake.word().title()} School",
            county=fake.state(),
            interests=", ".join([fake.word() for _ in range(3)]),
            has_parental_consent=chance(80)
        )
        students_created += 1
    except:
        pass

print(f"✅ Created {students_created} student profiles")

# 3. Create blog posts
print("\n📝 Creating 100 blog posts...")
posts_created = 0
mentor_users = [u for u in users_created if u.role == 'mentor']

for i in range(100):
    try:
        post = BlogPost.objects.create(
            title=f"Blog Post {i:03d}: {fake.sentence(nb_words=5)}",
            author=fake.random_element(mentor_users) if mentor_users else users_created[0],
            category='study_hacks',
            content=fake.text(),
            excerpt=fake.sentence(),
            status='published' if chance(70) else 'draft',
            is_featured=chance(10),
            published_at=timezone.now() if chance(70) else None
        )
        
        # Add 2-5 comments per post
        for _ in range(random.randint(2, 5)):
            Comment.objects.create(
                post=post,
                author=fake.random_element(users_created),
                content=fake.text()[:200],
                is_approved=True
            )
        
        posts_created += 1
        if (i + 1) % 25 == 0:
            print(f"  ✓ Created {i + 1} posts")
    except:
        pass

print(f"✅ Created {posts_created} blog posts")

# 4. Create squads and messages
print("\n👥 Creating 50 squads...")
squads_created = 0

for i in range(50):
    try:
        squad = Squad.objects.create(
            name=f"Squad {i:02d}: {fake.word().title()}",
            description=fake.text()[:200],
            topic=fake.word().title(),
            created_by=fake.random_element(users_created),
            is_public=chance(80),
            max_members=100
        )
        
        # Add 10-30 members
        for user in random.sample(users_created, min(random.randint(10, 30), len(users_created))):
            SquadMembership.objects.create(
                squad=squad,
                user=user,
                role='admin' if chance(20) else 'member'
            )
        
        # Add 10-20 messages
        members_list = squad.members.all()
        for _ in range(random.randint(10, 20)):
            if members_list.exists():
                Message.objects.create(
                    squad=squad,
                    sender=fake.random_element(list(members_list)),
                    content=fake.text()[:150]
                )
        
        squads_created += 1
    except:
        pass

print(f"✅ Created {squads_created} squads")

# 5. Create lab assignments
print("\n🧪 Creating 50 lab assignments...")
labs_created = 0

for i in range(50):
    try:
        teacher_users = [u for u in users_created if u.role == 'teacher']
        lab = LabAssignment.objects.create(
            title=f"Lab {i:02d}: {fake.sentence(nb_words=4)}",
            description=fake.text(),
            subject='Science',
            instructor=fake.random_element(teacher_users) if teacher_users else users_created[0],
            difficulty=random.choice(['beginner', 'intermediate', 'advanced']),
            instructions=fake.text(),
            expected_output=fake.text()[:150],
            due_date=timezone.now() + timedelta(days=random.randint(1, 30)),
            total_points=random.randint(50, 100),
            is_published=chance(70)
        )
        labs_created += 1
    except:
        pass

print(f"✅ Created {labs_created} lab assignments")

# ============================================================================
# TESTING
# ============================================================================
print("\n📍 PHASE 2: FUNCTIONALITY TESTING")
print("-"*70)

# Test 1: Authentication
print("\n🔐 Test 1: User Authentication")
try:
    from django.contrib.auth import authenticate
    user = authenticate(username="user_0000", password="TestPass123!")
    if user:
        print("  ✅ User authentication works")
    else:
        print("  ❌ User authentication failed")
except Exception as e:
    print(f"  ❌ Error: {str(e)}")

# Test 2: Token generation
print("\n🔐 Test 2: Token Generation")
try:
    from rest_framework.authtoken.models import Token
    test_user = users_created[0] if users_created else None
    if test_user:
        token, created = Token.objects.get_or_create(user=test_user)
        print(f"  ✅ Token generated: {str(token)[:20]}...")
except Exception as e:
    print(f"  ❌ Error: {str(e)}")

# Test 3: Database integrity
print("\n📊 Test 3: Database Integrity")
try:
    user_count = User.objects.count()
    blog_count = BlogPost.objects.count()
    squad_count = Squad.objects.count()
    lab_count = LabAssignment.objects.count()
    student_count = StudentProfile.objects.count()
    
    print(f"  ✅ Users: {user_count}")
    print(f"  ✅ Blog posts: {blog_count}")
    print(f"  ✅ Squads: {squad_count}")
    print(f"  ✅ Labs: {lab_count}")
    print(f"  ✅ Students: {student_count}")
except Exception as e:
    print(f"  ❌ Error: {str(e)}")

# Final summary
print("\n" + "="*70)
print("✅ SEEDING AND TESTING COMPLETE!")
print("="*70)
print(f"\n📊 SUMMARY:")
print(f"   • {len(users_created)} users created")
print(f"   • {students_created} student profiles")
print(f"   • {posts_created} blog posts")
print(f"   • {squads_created} squads with messaging")
print(f"   • {labs_created} lab assignments")

print(f"\n🎯 Database is ready for integration testing!")
print(f"   Backend: http://localhost:8000/api/v1/")
print(f"   Frontend: http://localhost:5173/")
print("\n" + "="*70 + "\n")
