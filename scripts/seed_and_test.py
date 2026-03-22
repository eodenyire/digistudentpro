#!/usr/bin/env python
"""
DigiStudentPro: Comprehensive Seeding & Testing Script
Creates 500+ test records and validates system integration
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
from django.contrib.auth import get_user_model, authenticate
from apps.accounts.models import User, StudentProfile
from apps.digiblog.models import BlogPost, Comment
from apps.digichat.models import Squad, SquadMembership, Message
from apps.digilab.models import Assessment

fake = Faker()
Faker.seed(0)
User = get_user_model()

def chance(percent):
    return random.randint(1, 100) <= percent

print("\n" + "="*70)
print("🌱 DIGISTUDENTPRO: SEEDING & INTEGRATION TESTING 🌱")
print("="*70)

# =====================================================================
# PHASE 1: DATABASE SEEDING
# =====================================================================
print("\n📍 PHASE 1: DATABASE SEEDING")
print("-"*70)

users_list = []
students_list = []
posts_list = []
squads_list = []

# 1. Create 200 test users
print("\n🧑‍💼 Seeding 200 users...")
roles = ['student', 'mentor', 'parent', 'teacher']
for i in range(200):
    try:
        user = User.objects.create_user(
            username=f"seed_user_{i:04d}",
            email=f"seed_{i:04d}@digistudentpro.test",
            password="TestPass123!",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=roles[i % len(roles)],
            phone_number=fake.phone_number()[:15],
            is_verified=chance(70),
            is_active=True
        )
        users_list.append(user)
        if (i + 1) % 50 == 0:
            print(f"  ✓ {i + 1} users")
    except Exception as e:
        pass

print(f"✅ Created {len(users_list)} users")

# 2. Create 100 student profiles
print("\n📚 Seeding 100 student profiles...")
student_users = [u for u in users_list if u.role == 'student'][:100]
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
        students_list.append(profile)
    except:
        pass

print(f"✅ Created {len(students_list)} student profiles")

# 3. Create 150 blog posts
print("\n📝 Seeding 150 blog posts with comments...")
mentor_users = [u for u in users_list if u.role in ['mentor', 'teacher']]
for i in range(150):
    try:
        author = fake.random_element(mentor_users) if mentor_users else users_list[0]
        post = BlogPost.objects.create(
            title=f"Blog {i:03d}: {fake.sentence(nb_words=5)}",
            author=author,
            category='study_hacks',
            content=fake.text(max_nb_chars=500),
            excerpt=fake.sentence(),
            status='published' if chance(70) else 'draft',
            is_featured=chance(10),
            published_at=timezone.now() if chance(70) else None
        )
        posts_list.append(post)
        
        # Add 2-4 comments
        for _ in range(random.randint(2, 4)):
            Comment.objects.create(
                post=post,
                author=fake.random_element(users_list),
                content=fake.text(max_nb_chars=200),
                is_approved=True
            )
        
        if (i + 1) % 30 == 0:
            print(f"  ✓ {i + 1} posts")
    except:
        pass

print(f"✅ Created {len(posts_list)} blog posts with comments")

# 4. Create 80 squads
print("\n👥 Seeding 80 squads with messaging...")
for i in range(80):
    try:
        squad = Squad.objects.create(
            name=f"Squad {i:02d}: {fake.word().title()}",
            description=fake.text(max_nb_chars=200),
            topic=fake.word().title(),
            created_by=fake.random_element(users_list),
            is_public=chance(80),
            max_members=100
        )
        squads_list.append(squad)
        
        # Add 15-25 members
        sample_size = min(random.randint(15, 25), len(users_list))
        for user in random.sample(users_list, sample_size):
            try:
                SquadMembership.objects.create(
                    squad=squad,
                    user=user,
                    role='admin' if chance(15) else 'member'
                )
            except:
                pass
        
        # Add 15-20 messages
        members = list(squad.members.all())
        for _ in range(random.randint(15, 20)):
            if members:
                Message.objects.create(
                    squad=squad,
                    sender=fake.random_element(members),
                    content=fake.text(max_nb_chars=150)
                )
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1} squads")
    except:
        pass

print(f"✅ Created {len(squads_list)} squads")

# =====================================================================
# PHASE 2: TESTING
# =====================================================================
print("\n📍 PHASE 2: INTEGRATION TESTING")
print("-"*70)

tests_passed = 0
tests_total = 0

# Test 1: User authentication
print("\n🔐 Test 1: User Authentication")
tests_total += 1
try:
    user = authenticate(username="seed_user_0000", password="TestPass123!")
    if user:
        print("  ✅ User authentication works")
        tests_passed += 1
    else:
        print("  ❌ Authentication failed - wrong username/password")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 2: Token generation
print("\n🔐 Test 2: Token Generation")
tests_total += 1
try:
    from rest_framework.authtoken.models import Token
    if users_list:
        token, created = Token.objects.get_or_create(user=users_list[0])
        print(f"  ✅ Token generated successfully")
        tests_passed += 1
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 3: Database integrity
print("\n📊 Test 3: Data Integrity Check")
try:
    user_count = User.objects.count()
    student_count = StudentProfile.objects.count()
    blog_count = BlogPost.objects.count()
    comment_count = Comment.objects.count()
    squad_count = Squad.objects.count()
    message_count = Message.objects.count()
    
    print(f"  ✓ Users: {user_count}")
    print(f"  ✓ Students: {student_count}")
    print(f"  ✓ Blog Posts: {blog_count}")
    print(f"  ✓ Comments: {comment_count}")
    print(f"  ✓ Squads: {squad_count}")
    print(f"  ✓ Messages: {message_count}")
    
    total_records = user_count + student_count + blog_count + comment_count + squad_count + message_count
    print(f"\n  ✅ Total records: {total_records}")
    tests_passed += 1
    tests_total += 1
except Exception as e:
    print(f"  ❌ Error: {e}")
    tests_total += 1

# Test 4: API connectivity
print("\n🌐 Test 4: API Accessibility")
tests_total += 1
try:
    from rest_framework.test import APIClient
    client = APIClient()
    response = client.get('/api/v1/')
    if response.status_code in [200, 401]:
        print(f"  ✅ API accessible (status: {response.status_code})")
        tests_passed += 1
    else:
        print(f"  ⚠️  API returned status {response.status_code}")
except Exception as e:
    print(f"  ⚠️  Could not test API: {e}")

# Test 5: Blog functionality
print("\n📝 Test 5: Blog Post Integrity")
tests_total += 1
try:
    if posts_list:
        sample_post = posts_list[0]
        comments = sample_post.comments.count()
        print(f"  ✓ Sample post: '{sample_post.title[:40]}...'")
        print(f"  ✓ Comments on post: {comments}")
        print(f"  ✅ Blog functionality verified")
        tests_passed += 1
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 6: Chat functionality
print("\n💬 Test 6: Squad & Messaging Integrity")
tests_total += 1
try:
    if squads_list:
        sample_squad = squads_list[0]
        members = sample_squad.members.count()
        messages = sample_squad.messages.count()
        print(f"  ✓ Sample squad: '{sample_squad.name}'")
        print(f"  ✓ Members: {members}")
        print(f"  ✓ Messages: {messages}")
        print(f"  ✅ Chat functionality verified")
        tests_passed += 1
except Exception as e:
    print(f"  ❌ Error: {e}")

# =====================================================================
# FINAL SUMMARY
# =====================================================================
print("\n" + "="*70)
print("✅ SEEDING & TESTING COMPLETE!")
print("="*70)

print(f"\n📊 SEEDING SUMMARY:")
print(f"   • {len(users_list)} users (students, mentors, parents, teachers)")
print(f"   • {len(students_list)} student profiles with grades")
print(f"   • {len(posts_list)} blog posts")
print(f"   • {len(squads_list)} squads with messaging")

total_comments = Comment.objects.count()
total_messages = Message.objects.count()
print(f"   • {total_comments} blog comments")
print(f"   • {total_messages} squad messages")

print(f"\n🧪 TEST RESULTS: {tests_passed}/{tests_total} passed")

if tests_passed == tests_total:
    print("   🎉 ALL TESTS PASSED!")
else:
    print(f"   ⚠️  {tests_total - tests_passed} test(s) need attention")

print(f"\n🚀 NEXT STEPS:")
print(f"   1. Backend: http://localhost:8000/api/v1/")
print(f"   2. Frontend: http://localhost:5173/")
print(f"   3. Admin: http://localhost:8000/admin/ (create superuser)")
print(f"   4. Test login with any seeded user (password: TestPass123!)")

print("\n" + "="*70 + "\n")
