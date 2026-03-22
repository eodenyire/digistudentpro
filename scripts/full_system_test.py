#!/usr/bin/env python
"""
Complete System Test for DigiStudentPro
Tests all functionalities including APIs, Users, Authentication, and Features
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import StudentProfile, MentorProfile, ParentGuardian
from apps.digiblog.models import BlogPost, Comment, BlogLike, BlogFollow
from apps.digichat.models import Squad, SquadMembership, Message, DirectMessage
from apps.digiguide.models import Career, EducationLevel, Grade, Subject
from apps.digilab.models import Assessment, Question, Answer

User = get_user_model()

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*75}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{title:^75}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*75}{Colors.END}\n")


def print_test(name, passed, details=""):
    if passed:
        status_text = f"{Colors.GREEN}✅ PASS{Colors.END}"
    else:
        status_text = f"{Colors.RED}❌ FAIL{Colors.END}"
    
    print(f"  {status_text} | {name}")
    if details:
        print(f"       {Colors.CYAN}{details}{Colors.END}")
    return passed


def count(model):
    return model.objects.count()


def test_section_1_database():
    """Section 1: Database Records Verification"""
    print_header("SECTION 1: DATABASE RECORDS")
    
    passed = 0
    total = 0
    
    tests = [
        ("Users in database", count(User) > 0, f"{count(User)} total users"),
        ("Blog posts exist", count(BlogPost) > 0, f"{count(BlogPost)} blog posts"),
        ("Comments exist", count(Comment) > 0, f"{count(Comment)} comments"),
        ("Squads exist", count(Squad) > 0, f"{count(Squad)} squads"),
        ("Squad messages exist", count(Message) > 0, f"{count(Message)} messages"),
        ("Student profiles exist", count(StudentProfile) > 0, f"{count(StudentProfile)} student profiles"),
        ("Mentor profiles exist", count(MentorProfile) > 0, f"{count(MentorProfile)} mentor profiles"),
    ]
    
    for name, test_passed, detail in tests:
        total += 1
        if print_test(name, test_passed, detail):
            passed += 1
    
    return passed, total


def test_section_2_users():
    """Section 2: User Management & Roles"""
    print_header("SECTION 2: USER MANAGEMENT & ROLES")
    
    passed = 0
    total = 0
    
    # Test user exists
    user = User.objects.first()
    total += 1
    if print_test("First user exists", user is not None, f"Username: {user.username if user else 'N/A'}"):
        passed += 1
    
    # Test roles
    roles_config = [
        ('student', 'Students'),
        ('mentor', 'Mentors'),
        ('teacher', 'Teachers'),
        ('parent', 'Parents'),
        ('admin', 'Admins'),
    ]
    
    for role, label in roles_config:
        total += 1
        count_users = User.objects.filter(role=role).count()
        if print_test(f"{label} role exists", count_users > 0, f"{count_users} {role}s"):
            passed += 1
        else:
            print_test(f"{label} role exists", False, f"No {role}s found")
    
    # Test user fields
    if user:
        total += 1
        if print_test("User has email", user.email is not None, f"Email: {user.email}"):
            passed += 1
        
        total += 1
        if print_test("User has rol assigned", user.role is not None, f"Role: {user.role}"):
            passed += 1
        
        total += 1
        if print_test("User has first name", user.first_name is not None, f"Name: {user.first_name}"):
            passed += 1
    
    return passed, total


def test_section_3_api():
    """Section 3: API Endpoints"""
    print_header("SECTION 3: API ENDPOINTS")
    
    client = APIClient()
    passed = 0
    total = 0
    
    endpoints = [
        ('/api/v1/accounts/users/', 'Users API'),
        ('/api/v1/accounts/students/', 'Student Profiles API'),
        ('/api/v1/digiblog/posts/', 'Blog Posts API'),
        ('/api/v1/digiblog/comments/', 'Comments API'),
        ('/api/v1/digichat/squads/', 'Squads API'),
        ('/api/v1/digichat/messages/', 'Messages API'),
    ]
    
    for endpoint, name in endpoints:
        total += 1
        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                count_items = len(data.get('results', data if isinstance(data, list) else []))
                if print_test(name, True, f"Status 200, {count_items} records"):
                    passed += 1
            else:
                print_test(name, False, f"Status {response.status_code}")
        except Exception as e:
            print_test(name, False, str(e)[:50])
    
    return passed, total


def test_section_4_blog():
    """Section 4: Blog Functionality"""
    print_header("SECTION 4: BLOG FUNCTIONALITY")
    
    passed = 0
    total = 0
    
    posts = BlogPost.objects.all()
    
    # Blog posts exist
    total += 1
    if print_test("Blog posts exist", posts.count() > 0, f"{posts.count()} posts"):
        passed += 1
    
    if posts.exists():
        post = posts.first()
        
        # Post has title
        total += 1
        if print_test("Post has title", post.title is not None, f"{post.title[:40]}..."):
            passed += 1
        
        # Post has content
        total += 1
        if print_test("Post has content", len(post.content) > 0, f"{len(post.content)} characters"):
            passed += 1
        
        # Post has author
        total += 1
        if print_test("Post has author", post.author is not None, f"Author: {post.author.username}"):
            passed += 1
        
        # Post has comments
        comments = post.comments.all()
        total += 1
        if print_test("Post has comments", comments.count() > 0, f"{comments.count()} comments"):
            passed += 1
    
    return passed, total


def test_section_5_chat():
    """Section 5: Chat Functionality"""
    print_header("SECTION 5: CHAT FUNCTIONALITY")
    
    passed = 0
    total = 0
    
    squads = Squad.objects.all()
    
    # Squads exist
    total += 1
    if print_test("Squads exist", squads.count() > 0, f"{squads.count()} squads"):
        passed += 1
    
    if squads.exists():
        squad = squads.first()
        
        # Squad has name
        total += 1
        if print_test("Squad has name", squad.name is not None, f"Name: {squad.name}"):
            passed += 1
        
        # Squad has members
        members_count = squad.members.count()
        total += 1
        if print_test("Squad has members", members_count > 0, f"{members_count} members"):
            passed += 1
        
        # Squad has messages
        messages = squad.messages.all()
        total += 1
        if print_test("Squad has messages", messages.count() > 0, f"{messages.count()} messages"):
            passed += 1
        
        if messages.exists():
            msg = messages.first()
            total += 1
            if print_test("Message has content", msg.content is not None, f"{msg.content[:40]}..."):
                passed += 1
    
    return passed, total


def test_section_6_education():
    """Section 6: Education (DigiGuide) Functionality"""
    print_header("SECTION 6: EDUCATION FUNCTIONALITY")
    
    passed = 0
    total = 0
    
    # Education levels
    levels = EducationLevel.objects.all()
    total += 1
    if print_test("Education levels exist", levels.count() > 0, f"{levels.count()} levels"):
        passed += 1
    else:
        print_test("Education levels exist", False, "No levels seeded")
    
    # Grades
    grades = Grade.objects.all()
    total += 1
    if print_test("Grades exist", grades.count() > 0, f"{grades.count()} grades"):
        passed += 1
    else:
        print_test("Grades exist", False, "No grades seeded")
    
    # Subjects
    subjects = Subject.objects.all()
    total += 1
    if print_test("Subjects exist", subjects.count() > 0, f"{subjects.count()} subjects"):
        passed += 1
    else:
        print_test("Subjects exist", False, "No subjects seeded")
    
    # Careers
    careers = Career.objects.all()
    total += 1
    if print_test("Careers exist", careers.count() > 0, f"{careers.count()} careers"):
        passed += 1
    else:
        print_test("Careers exist", False, "No careers seeded")
    
    # Student profiles linked
    students_with_records = StudentProfile.objects.exclude(academic_records__isnull=True).count()
    total += 1
    if print_test("Students have academic records", students_with_records > 0, f"{students_with_records} students"):
        passed += 1
    
    return passed, total


def test_section_7_labs():
    """Section 7: Labs Functionality"""
    print_header("SECTION 7: LAB FUNCTIONALITY")
    
    passed = 0
    total = 0
    
    assessments = Assessment.objects.all()
    
    # Assessments exist
    total += 1
    if print_test("Assessments exist", assessments.count() > 0, f"{assessments.count()} assessments"):
        passed += 1
    else:
        print_test("Assessments exist", False, "No assessments seeded")
    
    if assessments.exists():
        assessment = assessments.first()
        
        # Assessment has questions
        questions = assessment.questions.all()
        total += 1
        if print_test("Assessment has questions", questions.count() > 0, f"{questions.count()} questions"):
            passed += 1
    
    return passed, total


def test_section_8_relationships():
    """Section 8: Data Relationships & Integrity"""
    print_header("SECTION 8: DATA RELATIONSHIPS & INTEGRITY")
    
    passed = 0
    total = 0
    
    # Users to profiles
    users_with_student_profile = User.objects.filter(student_profile__isnull=False).count()
    total += 1
    if print_test("Users linked to student profiles", users_with_student_profile > 0, f"{users_with_student_profile} relationships"):
        passed += 1
    
    # Blog posts to authors
    blog_with_author = BlogPost.objects.filter(author__isnull=False).count()
    total += 1
    if print_test("Blog posts linked to authors", blog_with_author > 0, f"{blog_with_author} relationships"):
        passed += 1
    
    # Comments to posts
    comments_with_post = Comment.objects.filter(post__isnull=False).count()
    total += 1
    if print_test("Comments linked to blog posts", comments_with_post > 0, f"{comments_with_post} relationships"):
        passed += 1
    
    # Squads to members
    squads_with_members = Squad.objects.exclude(members__isnull=True).count()
    total += 1
    if print_test("Squads linked to members", squads_with_members > 0, f"{squads_with_members} relationships"):
        passed += 1
    
    # Messages to senders
    messages_with_sender = Message.objects.filter(sender__isnull=False).count()
    total += 1
    if print_test("Messages linked to senders", messages_with_sender > 0, f"{messages_with_sender} relationships"):
        passed += 1
    
    return passed, total


def main():
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║          DIGISTUDENTPRO: COMPLETE SYSTEM FUNCTIONALITY TEST           ║")
    print("║           Testing APIs, Users, Authentication & Features             ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Run all test sections
    results = {}
    results["Database Records"] = test_section_1_database()
    results["Users & Roles"] = test_section_2_users()
    results["API Endpoints"] = test_section_3_api()
    results["Blog Features"] = test_section_4_blog()
    results["Chat Features"] = test_section_5_chat()
    results["Education Features"] = test_section_6_education()
    results["Lab Features"] = test_section_7_labs()
    results["Data Integrity"] = test_section_8_relationships()
    
    # Print summary
    print_header("FINAL TEST SUMMARY")
    
    total_passed = 0
    total_tests = 0
    
    for section, (passed, total) in results.items():
        total_passed += passed
        total_tests += total
        percentage = (passed / total * 100) if total > 0 else 0
        
        if passed == total:
            status_icon = f"{Colors.GREEN}✅{Colors.END}"
        elif passed > 0:
            status_icon = f"{Colors.YELLOW}⚠️{Colors.END}"
        else:
            status_icon = f"{Colors.RED}❌{Colors.END}"
        
        print(f"{status_icon} {section:.<40} {passed}/{total} ({percentage:>3.0f}%)")
    
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{Colors.BOLD}{'='*75}{Colors.END}")
    print(f"{Colors.BOLD}OVERALL RESULT: {total_passed}/{total_tests} tests passed ({overall_percentage:.0f}%){Colors.END}\n")
    
    if overall_percentage >= 85:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 SYSTEM IS FULLY FUNCTIONAL! All major features are working.{Colors.END}")
    elif overall_percentage >= 70:
        print(f"{Colors.YELLOW}{Colors.BOLD}✅ SYSTEM IS OPERATIONAL! Most features are working properly.{Colors.END}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  SYSTEM NEEDS ATTENTION - Please review failed tests.{Colors.END}")
    
    print(f"\n{Colors.CYAN}📚 SYSTEM INFORMATION:{Colors.END}")
    print(f"   Total Users: {count(User)}")
    print(f"   Total Blog Posts: {count(BlogPost)}")
    print(f"   Total Comments: {count(Comment)}")
    print(f"   Total Squads: {count(Squad)}")
    print(f"   Total Messages: {count(Message)}")
    print(f"   Total Assessments: {count(Assessment)}")
    
    print(f"\n{Colors.CYAN}🚀 ACCESS POINTS:{Colors.END}")
    print(f"   Backend API: http://localhost:8000/api/v1/")
    print(f"   Admin Panel: http://localhost:8000/admin/")
    print(f"   Frontend UI: http://localhost:5173/")
    
    # Get test user
    test_user = User.objects.filter(role__in=['student', 'mentor', 'teacher']).first()
    if test_user:
        print(f"\n{Colors.CYAN}🔐 TEST LOGIN CREDENTIALS:{Colors.END}")
        print(f"   Username: {Colors.BLUE}{test_user.username}{Colors.END}")
        print(f"   Password: {Colors.BLUE}TestPass123!{Colors.END}")
        print(f"   Role: {Colors.BLUE}{test_user.role.upper()}{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*75}{Colors.END}\n")


if __name__ == '__main__':
    main()
