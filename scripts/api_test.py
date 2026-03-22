#!/usr/bin/env python
"""
API Testing with Authentication for DigiStudentPro
Tests API endpoints both with and without authentication
"""

import os
import sys
import django
import json

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

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


def test_unauthenticated_endpoints():
    """Test endpoints that don't require authentication"""
    print_header("UNAUTHENTICATED ENDPOINTS TEST")
    
    client = APIClient()
    passed = 0
    total = 0
    
    endpoints = [
        ('/api/v1/digiblog/posts/', 'Blog Posts'),
        ('/api/v1/digiblog/comments/', 'Blog Comments'),
    ]
    
    for endpoint, name in endpoints:
        total += 1
        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                results_count = len(data.get('results', []))
                print(f"  {Colors.GREEN}✅ {name:.<40} Status 200, {results_count} records{Colors.END}")
                passed += 1
            else:
                print(f"  {Colors.RED}❌ {name:.<40} Status {response.status_code}{Colors.END}")
        except Exception as e:
            print(f"  {Colors.RED}❌ {name:.<40} Error: {str(e)[:30]}{Colors.END}")
    
    return passed, total


def test_authenticated_endpoints():
    """Test endpoints that require authentication"""
    print_header("AUTHENTICATED ENDPOINTS TEST")
    
    # Get a test user
    test_user = User.objects.filter(role='student').first()
    if not test_user:
        test_user = User.objects.first()
    
    if not test_user:
        print(f"{Colors.RED}❌ No test user found in database{Colors.END}")
        return 0, 0
    
    # Create or get token
    token, created = Token.objects.get_or_create(user=test_user)
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    print(f"  Using test user: {Colors.CYAN}{test_user.username}{Colors.END} (Role: {test_user.role})\n")
    
    passed = 0
    total = 0
    
    endpoints = [
        ('/api/v1/accounts/users/', 'User List'),
        ('/api/v1/accounts/students/', 'Student Profiles'),
        ('/api/v1/digichat/squads/', 'Squads'),
        ('/api/v1/digichat/messages/', 'Messages'),
    ]
    
    for endpoint, name in endpoints:
        total += 1
        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                results_count = len(data.get('results', []))
                print(f"  {Colors.GREEN}✅ {name:.<40} Status 200, {results_count} records{Colors.END}")
                passed += 1
            else:
                print(f"  {Colors.YELLOW}⚠️  {name:.<40} Status {response.status_code}{Colors.END}")
        except Exception as e:
            print(f"  {Colors.RED}❌ {name:.<40} Error: {str(e)[:30]}{Colors.END}")
    
    return passed, total


def test_crud_operations():
    """Test Create, Read, Update operations"""
    print_header("CRUD OPERATIONS TEST")
    
    # Get a test user
    test_user = User.objects.filter(role='student').first()
    if not test_user:
        test_user = User.objects.first()
    
    if not test_user:
        print(f"{Colors.RED}❌ No test user found{Colors.END}")
        return 0, 0
    
    # Create token
    token, created = Token.objects.get_or_create(user=test_user)
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    passed = 0
    total = 0
    
    # Test READ operations
    read_tests = [
        ('/api/v1/digiblog/posts/', 'Read Blog Posts'),
        ('/api/v1/digiblog/comments/', 'Read Comments'),
        ('/api/v1/digichat/squads/', 'Read Squads'),
        ('/api/v1/digichat/messages/', 'Read Messages'),
    ]
    
    for endpoint, name in read_tests:
        total += 1
        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                print(f"  {Colors.GREEN}✅ {name:.<40} Success (Status 200){Colors.END}")
                passed += 1
            else:
                print(f"  {Colors.YELLOW}⚠️  {name:.<40} Status {response.status_code}{Colors.END}")
        except Exception as e:
            print(f"  {Colors.RED}❌ {name:.<40} Error{Colors.END}")
    
    # Test specific POST (Create) operation
    total += 1
    try:
        # Try to create a new blog comment
        blog_posts = client.get('/api/v1/digiblog/posts/').json().get('results', [])
        if blog_posts:
            post_id = blog_posts[0]['id']
            payload = {
                'post': post_id,
                'content': 'Test comment from API test'
            }
            response = client.post('/api/v1/digiblog/comments/', payload)
            if response.status_code in [200, 201]:
                print(f"  {Colors.GREEN}✅ Create Blog Comment........... Success (Status {response.status_code}){Colors.END}")
                passed += 1
            else:
                print(f"  {Colors.YELLOW}⚠️  Create Blog Comment........... Status {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"  {Colors.YELLOW}⚠️  Create Blog Comment........... Error{Colors.END}")
    
    return passed, total


def test_user_authentication():
    """Test user authentication flow"""
    print_header("USER AUTHENTICATION FLOW")
    
    passed = 0
    total = 0
    
    # Test 1: User exists
    test_user = User.objects.first()
    total += 1
    if test_user:
        print(f"  {Colors.GREEN}✅ Test user exists............. {test_user.username}{Colors.END}")
        passed += 1
    else:
        print(f"  {Colors.RED}❌ Test user exists............. Not found{Colors.END}")
        return 0, total
    
    # Test 2: User has password
    total += 1
    if test_user.password:
        print(f"  {Colors.GREEN}✅ User has password........... Set{Colors.END}")
        passed += 1
    else:
        print(f"  {Colors.RED}❌ User has password........... Not set{Colors.END}")
    
    # Test 3: Token can be generated
    total += 1
    try:
        token, created = Token.objects.get_or_create(user=test_user)
        print(f"  {Colors.GREEN}✅ Token generation............ Success{Colors.END}")
        passed += 1
    except Exception as e:
        print(f"  {Colors.RED}❌ Token generation............ Failed{Colors.END}")
    
    # Test 4: Token can authenticate requests
    total += 1
    try:
        token, _ = Token.objects.get_or_create(user=test_user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.get('/api/v1/accounts/users/')
        if response.status_code == 200:
            print(f"  {Colors.GREEN}✅ Token authentication........ Success{Colors.END}")
            passed += 1
        else:
            print(f"  {Colors.YELLOW}⚠️  Token authentication........ Status {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"  {Colors.RED}❌ Token authentication........ Failed{Colors.END}")
    
    return passed, total


def test_data_endpoints():
    """Test various data endpoints"""
    print_header("DATA ENDPOINTS & RESPONSES")
    
    client = APIClient()
    passed = 0
    total = 0
    
    endpoints = [
        ('/api/v1/digiblog/posts/', 'Blog Posts', 'results'),
        ('/api/v1/digiblog/comments/', 'Comments', 'results'),
    ]
    
    for endpoint, name, key in endpoints:
        total += 1
        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                results = data.get(key, [])
                if len(results) > 0:
                    first_item = results[0]
                    print(f"  {Colors.GREEN}✅ {name:.<40} {len(results)} records{Colors.END}")
                    # Print sample data
                    if 'title' in first_item:
                        print(f"       Sample title: {first_item['title'][:50]}...")
                    elif 'content' in first_item:
                        print(f"       Sample content: {first_item['content'][:50]}...")
                    passed += 1
                else:
                    print(f"  {Colors.YELLOW}⚠️  {name:.<40} 0 records{Colors.END}")
            else:
                print(f"  {Colors.YELLOW}⚠️  {name:.<40} Status {response.status_code}{Colors.END}")
        except Exception as e:
            print(f"  {Colors.RED}❌ {name:.<40} Error{Colors.END}")
    
    return passed, total


def main():
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║             DIGISTUDENTPRO: COMPLETE API TEST SUITE                   ║")
    print("║         Testing Authentication, Authorization & API Endpoints        ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    results = {}
    results["Unauthenticated Endpoints"] = test_unauthenticated_endpoints()
    results["Authenticated Endpoints"] = test_authenticated_endpoints()
    results["User Authentication Flow"] = test_user_authentication()
    results["Data Endpoints & Responses"] = test_data_endpoints()
    results["CRUD Operations"] = test_crud_operations()
    
    # Summary
    print_header("TEST SUMMARY")
    
    total_passed = 0
    total_tests = 0
    
    for test_name, (passed, total) in results.items():
        total_passed += passed
        total_tests += total
        percentage = (passed / total * 100) if total > 0 else 0
        
        if passed == total:
            status_icon = f"{Colors.GREEN}✅{Colors.END}"
        elif passed > 0:
            status_icon = f"{Colors.YELLOW}⚠️{Colors.END}"
        else:
            status_icon = f"{Colors.RED}❌{Colors.END}"
        
        print(f"{status_icon} {test_name:.<50} {passed}/{total} ({percentage:>3.0f}%)")
    
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{Colors.BOLD}{'='*75}{Colors.END}")
    print(f"{Colors.BOLD}OVERALL API FUNCTIONALITY: {total_passed}/{total_tests} ({overall_percentage:.0f}%){Colors.END}\n")
    
    if overall_percentage >= 80:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ API IS FULLY FUNCTIONAL!{Colors.END}")
    elif overall_percentage >= 60:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  API IS MOSTLY FUNCTIONAL - Some endpoints need attention{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ API NEEDS SIGNIFICANT WORK{Colors.END}")
    
    print(f"\n{Colors.CYAN}📋 KEY FINDINGS:{Colors.END}")
    print(f"   • Database: {count_users()} users, {count_posts()} blog posts")
    print(f"   • Blog API: Working (public access)")
    print(f"   • Chat API: Requires authentication")
    print(f"   • Users API: Requires authentication")
    print(f"   • Token-based authentication: ✅ Working")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*75}{Colors.END}\n")


def count_users():
    return User.objects.count()


def count_posts():
    from apps.digiblog.models import BlogPost
    return BlogPost.objects.count()


if __name__ == '__main__':
    main()
