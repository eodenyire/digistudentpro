"""
Comprehensive test runner
Executes all tests in sequence: seeding → authentication → API integration
"""
import os
import sys
import time
import subprocess

def run_script(script_path, script_name):
    """Run a Python script and return success status"""
    print(f"\n{'=' * 70}")
    print(f"Running: {script_name}")
    print('=' * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {str(e)}")
        return False

def main():
    """Main test runner"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    start_time = time.time()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "🚀 COMPREHENSIVE TEST SUITE 🚀")
    print("=" * 70)
    print("\nThis will:")
    print("  1️⃣  Seed database with 5000+ test records")
    print("  2️⃣  Test authentication and login")
    print("  3️⃣  Test API endpoints and connectivity")
    print("\n" + "=" * 70)
    
    results = {}
    
    # Step 1: Seeding
    print("\n📍 STEP 1/3: Database Seeding")
    results['seeding'] = run_script(
        os.path.join(script_dir, 'seed_all.py'),
        'Database Seeding'
    )
    
    # Step 2: Authentication tests
    print("\n📍 STEP 2/3: Authentication Tests")
    results['authentication'] = run_script(
        os.path.join(script_dir, 'test_authentication.py'),
        'Authentication Tests'
    )
    
    # Step 3: API Integration tests
    print("\n📍 STEP 3/3: API Integration Tests")
    results['api_integration'] = run_script(
        os.path.join(script_dir, 'test_api_integration.py'),
        'API Integration Tests'
    )
    
    # Print final summary
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(" " * 25 + "✅ TEST SUITE COMPLETE ✅")
    print("=" * 70)
    
    print("\n📊 RESULTS SUMMARY:")
    print("-" * 70)
    
    all_passed = True
    for test_name, passed in results.items():
        icon = "✅" if passed else "❌"
        status = "PASSED" if passed else "FAILED"
        print(f"{icon} {test_name.upper():30s} {status}")
        if not passed:
            all_passed = False
    
    print("-" * 70)
    print(f"⏱️  Total time: {elapsed_time:.2f} seconds")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n✨ Your DigiStudentPro system is fully operational and tested!")
        print("✨ Database has 5000+ seeded records for testing")
        print("✨ Authentication working properly")
        print("✨ All API endpoints accessible")
    else:
        print("\n⚠️  Some tests failed. Check output above for details.")
    
    print("\n" + "=" * 70)
    print("📚 QUICK REFERENCE:")
    print("=" * 70)
    print("\nTo run tests individually:")
    print("  python scripts/seed_all.py                 # Seed database")
    print("  python scripts/test_authentication.py       # Auth tests")
    print("  python scripts/test_api_integration.py      # API tests")
    print("\nBackend Server: python manage.py runserver")
    print("Frontend Server: npm run dev")
    print("\n" + "=" * 70 + "\n")

if __name__ == '__main__':
    main()
