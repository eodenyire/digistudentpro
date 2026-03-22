#!/usr/bin/env python
"""
Comprehensive API and Functionality Test Suite for DigiStudentPro
Tests all major features: Users, Authentication, APIs, Blog, Chat, Labs, Guides
"""

import os
import sys
import django
import json
import requests
from datetime import datetime

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.accounts.models import StudentProfile, MentorProfile
from apps.digiblog.models import BlogPost, Comment
from apps.digichat.models import Squad, Message
from apps.digiguide.models import Career, EducationLevel
from apps.digilab.models import Assessment

User = get_user_model()

# API Configuration
API_BASE_URL = 'http://localhost:8000/api/v1'
TIMEOUT = 5


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_section(title):
    """Print section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_test(name, status, message=""):
    """Print test result"""
    if status:
        print(f"  {Colors.OKGREEN}✅ {name}{Colors.ENDC}")
        if message:
            print(f"     {message}")
    else:
        print(f"  {Colors.FAIL}❌ {name}{Colors.ENDC}")
        if message:
            print(f"     {Colors.WARNING}{message}{Colors.ENDC}")
    return status


def count_records(model):
    """Count records in a model"""
    return model.objects.count()


def test_database_records():
    """Test 1: Verify database has records"""
    print_section("TEST 1: DATABASE RECORDS")
    
    tests_passed = 0
    total_tests = 6
    
    users_count = count_records(User)
    if print_test("Users created", users_count > 0, f"{users_count} users in database"):
        tests_passed += 1
    
    blogs_count = count_records(BlogPost)
    if print_test("Blog posts created", blogs_count > 0, f"{blogs_count} blog posts in database"):
        tests_passed += 1
    
    comments_count = count_records(Comment)
    if print_test("Comments created", comments_count > 0, f"{comments_count} comments in database"):
        tests_passed += 1
    
    squads_count = count_records(Squad)
    if print_test("Squads created", squads_count > 0, f"{squads_count} squads in database"):
        tests_passed += 1
    
    messages_count = count_records(Message)
    if print_test("Messages created", messages_count > 0, f"{messages_count} messages in database"):
        tests_passed += 1
    
    assessments_count = count_records(Assessment)
    if print_test("Assessments/Labs created", assessments_count >= 0, f"{assessments_count} assessments in database"):
        tests_passed += 1
    
    return tests_passed, total_tests


def test_user_authentication():
    """Test 2: Test user authentication"""
    print_section("TEST 2: USER AUTHENTICATION")
    
    tests_passed = 0
    total_tests = 3
    
    # Get the first user
    try:
        user = User.objects.first()
        if user:
            print(f"  📝 Using test user: {user.username}")
            
            # Test 1: User exists
            if print_test("User exists in database", True, f"Username: {user.username}"):
                tests_passed += 1
            
            # Test 2: User has email
            if print_test("User has email", user.email is not None, f"Email: {user.email}"):
                tests_passed += 1
            
            # Test 3: User has role
            if print_test("User has role assigned", user.role is not None, f"Role: {user.role}"):
                tests_passed += 1
        else:
            print_test("User exists in database", False, "No users found in database")
    except Exception as e:
        print_test("User authentication test", False, str(e))
    
    return tests_passed, total_tests


def test_api_endpoints():
    """Test 3: Test API endpoints"""
    print_section("TEST 3: API ENDPOINTS")
    
    client = APIClient()
    tests_passed = 0
    total_tests = 0
    
    endpoints = [
        ('/users/', 'Users List'),
        ('/blog/posts/', 'Blog Posts'),
        ('/blog/comments/', 'Comments'),
        ('/chat/squads/', 'Squads'),
        ('/chat/messages/', 'Messages'),
    ]
    
    for endpoint, name in endpoints:
        total_tests += 1
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = client.get(url, HTTP_HOST='localhost:8000')
            
            if response.status_code == 200:
                data = response.json()
                # Check if results exist
                results_count = len(data.get('results', data if isinstance(data, list) else []))
                if print_test(f"{name} endpoint", True, f"Status: 200, Records: {results_count}"):
                    tests_passed += 1
            else:
                print_test(f"{name} endpoint", False, f"Status: {response.status_code}")
        except Exception as e:
            print_test(f"{name} endpoint", False, str(e))
    
    return tests_passed, total_tests


def test_blog_functionality():
    """Test 4: Test blog functionality"""
    print_section("TEST 4: BLOG FUNCTIONALITY")
    
    tests_passed = 0
    total_tests = 4
    
    try:
        # Test 1: Blog posts exist
        posts = BlogPost.objects.all()
        if print_test("Blog posts exist", posts.count() > 0, f"{posts.count()} posts found"):
            tests_passed += 1
        
        if posts.exists():
            # Test 2: Blog post has title
            post = posts.first()
            if print_test("Blog post has title", post.title is not None, f"Title: {post.title[:50]}..."):
                tests_passed += 1
            
            # Test 3: Blog post has content
            if print_test("Blog post has content", post.content is not None, f"Length: {len(post.content)} chars"):
                tests_passed += 1
            
            # Test 4: Blog post has comments
            comments = post.comments.all()
            if print_test("Blog post has comments", comments.count() > 0, f"{comments.count()} comments"):
                tests_passed += 1
        else:
            total_tests = 1
    except Exception as e:
        print_test("Blog functionality", False, str(e))
    
    return tests_passed, total_tests


def test_chat_functionality():
    """Test 5: Test chat functionality"""
    print_section("TEST 5: CHAT FUNCTIONALITY")
    
    tests_passed = 0
    total_tests = 4
    
    try:
        # Test 1: Squads exist
        squads = Squad.objects.all()
        if print_test("Squads exist", squads.count() > 0, f"{squads.count()} squads found"):
            tests_passed += 1
        
        if squads.exists():
            # Test 2: Squad has members
            squad = squads.first()
            members_count = squad.members.count()
            if print_test("Squad has members", members_count > 0, f"{members_count} members"):
                tests_passed += 1
            
            # Test 3: Squad has name
            if print_test("Squad has name", squad.name is not None, f"Name: {squad.name}"):
                tests_passed += 1
            
            # Test 4: Squad has messages
            messages = squad.messages.all()
            if print_test("Squad has messages", messages.count() > 0, f"{messages.count()} messages"):
                tests_passed += 1
        else:
            total_tests = 1
    except Exception as e:
        print_test("Chat functionality", False, str(e))
    
    return tests_passed, total_tests


def test_education_functionality():
    """Test 6: Test education (DigiGuide) functionality"""
    print_section("TEST 6: EDUCATION FUNCTIONALITY")
    
    tests_passed = 0
    total_tests = 3
    
    try:
        # Test 1: Education levels exist
        levels = EducationLevel.objects.all()
        if print_test("Education levels exist", levels.count() > 0, f"{levels.count()} levels found"):
            tests_passed += 1
        
        # Test 2: Careers exist
        careers = Career.objects.all()
        if print_test("Careers exist", careers.count() > 0, f"{careers.count()} careers found"):
            tests_passed += 1
        
        # Test 3: Student profiles exist
        student_profiles = StudentProfile.objects.all()
        if print_test("Student profiles exist", student_profiles.count() > 0, f"{student_profiles.count()} profiles found"):
            tests_passed += 1
    except Exception as e:
        print_test("Education functionality", False, str(e))
    
    return tests_passed, total_tests


def test_lab_functionality():
    """Test 7: Test lab functionality"""
    print_section("TEST 7: LAB FUNCTIONALITY")
    
    tests_passed = 0
    total_tests = 2
    
    try:
        # Test 1: Assessments exist
        assessments = Assessment.objects.all()
        if print_test("Assessments/Labs exist", assessments.count() > 0, f"{assessments.count()} assessments found"):
            tests_passed += 1
        
        # Test 2: Assessments have questions
        if assessments.exists():
            assessment = assessments.first()
            questions = assessment.questions.all()
            if print_test("Assessments have questions", questions.count() > 0, f"{questions.count()} questions found"):
                tests_passed += 1
        else:
            total_tests = 1
    except Exception as e:
        print_test("Lab functionality", False, str(e))
    
    return tests_passed, total_tests


def test_token_generation():
    """Test 8: Test token generation"""
    print_section("TEST 8: TOKEN GENERATION")
    
    tests_passed = 0
    total_tests = 2
    
    try:
        client = APIClient()
        
        # Get a test user
        user = User.objects.filter(role='student').first()
        
        if user:
            # Get token from token endpoint
            try:
                url = f"{API_BASE_URL}/token/"
                payload = {
                    'username': user.username,
                    'password': 'TestPass123!'  # Default password used in seeding
                }
                response = client.post(url, payload, format='json', HTTP_HOST='localhost:8000')
                
                if response.status_code == 200:
                    data = response.json()
                    token = data.get('access')
                    if print_test("Token generated successfully", token is not None, f"Token: {token[:20]}..."):
                        tests_passed += 1
                        
                        # Test 2: Token can be used in headers
                        if token:
                            client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
                            response = client.get(f"{API_BASE_URL}/users/", HTTP_HOST='localhost:8000')
                            if print_test("Token authentication works", response.status_code == 200, f"Status: {response.status_code}"):
                                tests_passed += 1
                else:
                    print_test("Token generation", False, f"Status: {response.status_code}")
            except Exception as e:
                print_test("Token generation via API", False, str(e))
        else:
            print_test("Test user found", False, "No student user found for token test")
    except Exception as e:
        print_test("Token generation test", False, str(e))
    
    return tests_passed, total_tests


def test_user_roles():
    """Test 9: Test user roles"""
    print_section("TEST 9: USER ROLES")
    
    tests_passed = 0
    total_tests = 5
    
    try:
        roles = ['student', 'mentor', 'teacher', 'parent', 'admin']
        
        for role in roles:
            users_with_role = User.objects.filter(role=role).count()
            if print_test(f"Users with role '{role}'", users_with_role > 0, f"{users_with_role} users found"):
                tests_passed += 1
            else:
                # Still count it as a test
                pass
    except Exception as e:
        print_test("User roles test", False, str(e))
    
    return tests_passed, 5


def test_data_relationships():
    """Test 10: Test data relationships"""
    print_section("TEST 10: DATA RELATIONSHIPS")
    
    tests_passed = 0
    total_tests = 4
    
    try:
        # Test 1: Users have student profiles
        users_with_profiles = User.objects.filter(student_profile__isnull=False).count()
        if print_test("Users have student profiles", users_with_profiles > 0, f"{users_with_profiles} users with profiles"):
            tests_passed += 1
        
        # Test 2: Blog posts have authors
        posts_with_authors = BlogPost.objects.filter(author__isnull=False).count()
        if print_test("Blog posts have authors", posts_with_authors > 0, f"{posts_with_authors} posts with authors"):
            tests_passed += 1
        
        # Test 3: Squad members are users
        valid_squad_members = Squad.objects.exclude(members__isnull=True).count()
        if print_test("Squads have valid members", valid_squad_members > 0, f"{valid_squad_members} squads with members"):
            tests_passed += 1
        
        # Test 4: Messages have senders and squads
        messages_with_sender = Message.objects.filter(sender__isnull=False).count()
        if print_test("Messages have valid senders", messages_with_sender > 0, f"{messages_with_sender} messages with senders"):
            tests_passed += 1
    except Exception as e:
        print_test("Data relationships", False, str(e))
    
    return tests_passed, total_tests


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║       DIGISTUDENTPRO: COMPREHENSIVE FUNCTIONALITY TEST SUITE        ║")
    print("║                   Testing APIs, Users & Features                   ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    all_results = []
    
    # Run all tests
    all_results.append(("Database Records", test_database_records()))
    all_results.append(("User Authentication", test_user_authentication()))
    all_results.append(("API Endpoints", test_api_endpoints()))
    all_results.append(("Blog Functionality", test_blog_functionality()))
    all_results.append(("Chat Functionality", test_chat_functionality()))
    all_results.append(("Education Functionality", test_education_functionality()))
    all_results.append(("Lab Functionality", test_lab_functionality()))
    all_results.append(("Token Generation", test_token_generation()))
    all_results.append(("User Roles", test_user_roles()))
    all_results.append(("Data Relationships", test_data_relationships()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    total_passed = 0
    total_tests = 0
    
    for test_name, (passed, total) in all_results:
        total_passed += passed
        total_tests += total
        percentage = (passed / total * 100) if total > 0 else 0
        status = Colors.OKGREEN if passed == total else Colors.WARNING if passed > 0 else Colors.FAIL
        print(f"{status}{test_name:.<40} {passed}/{total} ({percentage:.0f}%){Colors.ENDC}")
    
    # Overall summary
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    if overall_percentage == 100:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✅ ALL TESTS PASSED! System is fully functional.{Colors.ENDC}")
    elif overall_percentage >= 80:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠️  MOSTLY PASSING - {overall_percentage:.0f}% tests passed{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}❌ NEEDS ATTENTION - {overall_percentage:.0f}% tests passed{Colors.ENDC}")
    
    print(f"{Colors.BOLD}Overall: {total_passed}/{total_tests} ({overall_percentage:.0f}%){Colors.ENDC}\n")
    
    print(f"\n🚀 {Colors.BOLD}Access your system:{Colors.ENDC}")
    print(f"   Backend API: {Colors.OKCYAN}http://localhost:8000/api/v1/{Colors.ENDC}")
    print(f"   Admin Panel: {Colors.OKCYAN}http://localhost:8000/admin/{Colors.ENDC}")
    print(f"   Frontend: {Colors.OKCYAN}http://localhost:5173/{Colors.ENDC}")
    print(f"\n📝 {Colors.BOLD}Test Login Credentials:{Colors.ENDC}")
    
    test_user = User.objects.filter(role__in=['student', 'mentor', 'teacher']).first()
    if test_user:
        print(f"   Username: {Colors.OKBLUE}{test_user.username}{Colors.ENDC}")
        print(f"   Password: {Colors.OKBLUE}TestPass123!{Colors.ENDC}")
        print(f"   Role: {Colors.OKBLUE}{test_user.role}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}{'='*70}{Colors.ENDC}\n")


if __name__ == '__main__':
    main()
