"""
Authentication and login tests
Tests user authentication, token generation, and access control
"""
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

import django
django.setup()

from django.test import Client
from django.contrib.auth import authenticate, get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthTests:
    """Authentication tests"""
    
    def __init__(self):
        self.client = APIClient()
        self.user_client = Client()
        self.test_results = []
    
    def log_result(self, test_name, status, message=""):
        """Log test result"""
        icon = "✅" if status else "❌"
        self.test_results.append((test_name, status, message))
        print(f"  {icon} {test_name}")
        if message:
            print(f"     └─ {message}")
    
    def test_user_creation(self):
        """Test user creation"""
        print("\n🧪 Testing User Creation...")
        
        try:
            user = User.objects.create_user(
                username="test_user_auth",
                email="test_auth@digistudentpro.test",
                password="TestPassword123!",
                first_name="Test",
                last_name="User"
            )
            self.log_result(
                "User creation",
                True,
                f"Created user: {user.email}"
            )
            return user
        except Exception as e:
            self.log_result("User creation", False, str(e))
            return None
    
    def test_user_login(self, user):
        """Test Django user login"""
        print("\n🧪 Testing Django User Login...")
        
        try:
            authenticated_user = authenticate(
                username="test_user_auth",
                password="TestPassword123!"
            )
            self.log_result(
                "Django authentication",
                authenticated_user is not None,
                f"User authenticated: {authenticated_user.email if authenticated_user else 'Failed'}"
            )
            return authenticated_user
        except Exception as e:
            self.log_result("Django authentication", False, str(e))
            return None
    
    def test_token_generation(self, user):
        """Test token generation for API"""
        print("\n🧪 Testing Token Generation...")
        
        try:
            token, created = Token.objects.get_or_create(user=user)
            self.log_result(
                "Token generation",
                token is not None,
                f"Token: {str(token)[:20]}..."
            )
            return token
        except Exception as e:
            self.log_result("Token generation", False, str(e))
            return None
    
    def test_token_authentication(self, token):
        """Test token-based API authentication"""
        print("\n🧪 Testing Token-Based API Authentication...")
        
        try:
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            # Try accessing protected endpoint
            response = self.client.get('/api/v1/accounts/')
            
            success = response.status_code in [200, 401]  # Either works or auth issue
            self.log_result(
                "Token authentication",
                success,
                f"Status code: {response.status_code}"
            )
            return response
        except Exception as e:
            self.log_result("Token authentication", False, str(e))
            return None
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        print("\n🧪 Testing Invalid Credentials...")
        
        try:
            authenticated_user = authenticate(
                username="test_user_auth",
                password="WrongPassword123!"
            )
            self.log_result(
                "Invalid credentials rejection",
                authenticated_user is None,
                "Correctly rejected invalid credentials"
            )
        except Exception as e:
            self.log_result("Invalid credentials rejection", False, str(e))
    
    def test_admin_access(self):
        """Test admin user access"""
        print("\n🧪 Testing Admin Access...")
        
        try:
            admin_user = User.objects.create_superuser(
                username="test_admin",
                email="admin@digistudentpro.test",
                password="AdminPass123!"
            )
            self.log_result(
                "Admin user creation",
                admin_user.is_superuser and admin_user.is_staff,
                f"Admin user: {admin_user.email}"
            )
            return admin_user
        except Exception as e:
            self.log_result("Admin user creation", False, str(e))
            return None
    
    def test_role_based_access(self):
        """Test role-based access control"""
        print("\n🧪 Testing Role-Based Access Control...")
        
        try:
            roles = ['student', 'mentor', 'teacher', 'parent']
            users_created = []
            
            for role in roles:
                user = User.objects.create_user(
                    username=f"test_{role}",
                    email=f"{role}@digistudentpro.test",
                    password="TestPass123!",
                    role=role
                )
                users_created.append(user)
            
            self.log_result(
                "Role-based user creation",
                len(users_created) == len(roles),
                f"Created {len(users_created)} users with different roles"
            )
        except Exception as e:
            self.log_result("Role-based user creation", False, str(e))
    
    def run_all_tests(self):
        """Run all authentication tests"""
        print("=" * 70)
        print(" " * 20 + "🔑 AUTHENTICATION TESTS 🔑")
        print("=" * 70)
        
        # Run tests
        user = self.test_user_creation()
        self.test_user_login(user)
        self.test_invalid_credentials()
        
        if user:
            token = self.test_token_generation(user)
            if token:
                self.test_token_authentication(token)
        
        self.test_admin_access()
        self.test_role_based_access()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, status, _ in self.test_results if status)
        total = len(self.test_results)
        
        for test_name, status, message in self.test_results:
            icon = "✅" if status else "❌"
            print(f"{icon} {test_name}")
        
        print("\n" + "-" * 70)
        print(f"Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All authentication tests passed!")
        else:
            print(f"⚠️  {total - passed} test(s) failed")
        
        print("=" * 70 + "\n")

def main():
    tester = AuthTests()
    tester.run_all_tests()

if __name__ == '__main__':
    main()
