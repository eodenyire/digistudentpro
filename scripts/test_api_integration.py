"""
API integration tests
Tests all API endpoints with real data to verify connectivity and functionality
"""
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

import django
django.setup()

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from apps.accounts.models import StudentProfile
from apps.digiblog.models import BlogPost
from apps.digichat.models import Squad
from apps.digilab.models import LabAssignment

User = get_user_model()

class APIIntegrationTests:
    """API Integration tests"""
    
    def __init__(self):
        self.client = APIClient()
        self.test_results = []
        self.test_user = None
        self.test_token = None
    
    def log_result(self, test_name, status, message=""):
        """Log test result"""
        icon = "✅" if status else "❌"
        self.test_results.append((test_name, status, message))
        print(f"  {icon} {test_name}")
        if message:
            print(f"     └─ {message}")
    
    def setup_test_user(self):
        """Setup test user with token"""
        print("\n🔧 Setting up test user...")
        
        try:
            # Get or create test user
            user, created = User.objects.get_or_create(
                email="api_test@digistudentpro.test",
                defaults={
                    'username': 'api_test_user',
                    'first_name': 'API',
                    'last_name': 'Test'
                }
            )
            
            if created:
                user.set_password('APITest123!')
                user.save()
            
            # Get or create token
            token, _ = Token.objects.get_or_create(user=user)
            
            self.test_user = user
            self.test_token = token
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            
            print(f"  ✓ Test user configured: {user.email}")
            
        except Exception as e:
            print(f"  ❌ Error setting up test user: {str(e)}")
    
    def test_api_root(self):
        """Test API root endpoint"""
        print("\n🧪 Testing API Endpoints...")
        
        try:
            response = self.client.get('/api/v1/')
            status = response.status_code == 200
            self.log_result(
                "API root access",
                status,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.log_result("API root access", False, str(e))
    
    def test_accounts_endpoint(self):
        """Test accounts endpoint"""
        try:
            response = self.client.get('/api/v1/accounts/')
            status = response.status_code in [200, 401]
            count = len(response.data) if hasattr(response, 'data') else 0
            self.log_result(
                "Accounts endpoint",
                status,
                f"Status: {response.status_code}, Records: {count}"
            )
        except Exception as e:
            self.log_result("Accounts endpoint", False, str(e))
    
    def test_blog_endpoint(self):
        """Test blog endpoint"""
        try:
            response = self.client.get('/api/v1/digiblog/')
            status = response.status_code in [200, 401]
            count = len(response.data) if hasattr(response, 'data') else 0
            self.log_result(
                "Blog endpoint",
                status,
                f"Status: {response.status_code}, Records: {count}"
            )
        except Exception as e:
            self.log_result("Blog endpoint", False, str(e))
    
    def test_chat_endpoint(self):
        """Test chat endpoint"""
        try:
            response = self.client.get('/api/v1/digichat/')
            status = response.status_code in [200, 401]
            count = len(response.data) if hasattr(response, 'data') else 0
            self.log_result(
                "Chat endpoint",
                status,
                f"Status: {response.status_code}, Records: {count}"
            )
        except Exception as e:
            self.log_result("Chat endpoint", False, str(e))
    
    def test_guide_endpoint(self):
        """Test guide endpoint"""
        try:
            response = self.client.get('/api/v1/digiguide/')
            status = response.status_code in [200, 401]
            count = len(response.data) if hasattr(response, 'data') else 0
            self.log_result(
                "Guide endpoint",
                status,
                f"Status: {response.status_code}, Records: {count}"
            )
        except Exception as e:
            self.log_result("Guide endpoint", False, str(e))
    
    def test_lab_endpoint(self):
        """Test lab endpoint"""
        try:
            response = self.client.get('/api/v1/digilab/')
            status = response.status_code in [200, 401]
            count = len(response.data) if hasattr(response, 'data') else 0
            self.log_result(
                "Lab endpoint",
                status,
                f"Status: {response.status_code}, Records: {count}"
            )
        except Exception as e:
            self.log_result("Lab endpoint", False, str(e))
    
    def test_data_integrity(self):
        """Test data integrity in database"""
        print("\n🧪 Testing Data Integrity...")
        
        # Check users
        try:
            user_count = User.objects.count()
            status = user_count > 10
            self.log_result(
                "User count",
                status,
                f"Users in database: {user_count}"
            )
        except Exception as e:
            self.log_result("User count", False, str(e))
        
        # Check students
        try:
            student_count = StudentProfile.objects.count()
            status = student_count > 0
            self.log_result(
                "Student records",
                status,
                f"Students: {student_count}"
            )
        except Exception as e:
            self.log_result("Student records", False, str(e))
        
        # Check blog posts
        try:
            blog_count = BlogPost.objects.count()
            status = blog_count > 0
            self.log_result(
                "Blog posts",
                status,
                f"Posts: {blog_count}"
            )
        except Exception as e:
            self.log_result("Blog posts", False, str(e))
        
        # Check squads
        try:
            squad_count = Squad.objects.count()
            status = squad_count > 0
            self.log_result(
                "Squads",
                status,
                f"Squads: {squad_count}"
            )
        except Exception as e:
            self.log_result("Squads", False, str(e))
        
        # Check labs
        try:
            lab_count = LabAssignment.objects.count()
            status = lab_count > 0
            self.log_result(
                "Lab assignments",
                status,
                f"Labs: {lab_count}"
            )
        except Exception as e:
            self.log_result("Lab assignments", False, str(e))
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 70)
        print(" " * 15 + "🔗 API INTEGRATION TESTS 🔗")
        print("=" * 70)
        
        self.setup_test_user()
        
        print("\n🧪 Testing Endpoint Connectivity...")
        self.test_api_root()
        self.test_accounts_endpoint()
        self.test_blog_endpoint()
        self.test_chat_endpoint()
        self.test_guide_endpoint()
        self.test_lab_endpoint()
        
        self.test_data_integrity()
        
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
            print("🎉 All API integration tests passed!")
        else:
            print(f"⚠️  {total - passed} test(s) failed")
        
        print("=" * 70 + "\n")

def main():
    tester = APIIntegrationTests()
    tester.run_all_tests()

if __name__ == '__main__':
    main()
