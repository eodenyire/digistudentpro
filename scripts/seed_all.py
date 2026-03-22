"""
Master seed script - Seeds all apps with test data
Run this to populate the entire database with 5000+ records
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

import django
django.setup()

from django.core.management import call_command

def main():
    """Master seeding function"""
    print("\n" + "=" * 70)
    print(" " * 15 + "🌱 DIGISTUDENTPRO DATABASE SEEDING 🌱")
    print("=" * 70)
    print("\nThis will populate all apps with test data.\n")
    
    start_time = time.time()
    
    try:
        # Step 1: DigiGuide (needs to run first for dependencies)
        print("\n🔹 STEP 1/5: DigiGuide App")
        print("-" * 70)
        exec(open(os.path.join(os.path.dirname(__file__), 'seed_digiguide.py')).read())
        
        # Wait a bit
        time.sleep(2)
        
        # Step 2: Accounts
        print("\n🔹 STEP 2/5: Accounts App")
        print("-" * 70)
        exec(open(os.path.join(os.path.dirname(__file__), 'seed_accounts.py')).read())
        
        time.sleep(2)
        
        # Step 3: DigiLab
        print("\n🔹 STEP 3/5: DigiLab App")
        print("-" * 70)
        exec(open(os.path.join(os.path.dirname(__file__), 'seed_digilab.py')).read())
        
        time.sleep(2)
        
        # Step 4: DiBlog
        print("\n🔹 STEP 4/5: DigiBlog App")
        print("-" * 70)
        exec(open(os.path.join(os.path.dirname(__file__), 'seed_digiblog.py')).read())
        
        time.sleep(2)
        
        # Step 5: DigiChat
        print("\n🔹 STEP 5/5: DigiChat App")
        print("-" * 70)
        exec(open(os.path.join(os.path.dirname(__file__), 'seed_digichat.py')).read())
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 70)
        print("✅ " + " " * 20 + "ALL SEEDING COMPLETE! ✅")
        print("=" * 70)
        print(f"\n⏱️  Total time: {elapsed_time:.2f} seconds")
        print("\n📊 SUMMARY:")
        print("   ✓ 1000+ Users created (Students, Mentors, Parents, Teachers)")
        print("   ✓ 1000+ Blog posts with comments and likes")
        print("   ✓ 100 Squads with 5000+ messages")
        print("   ✓ 1000+ Direct messages")
        print("   ✓ 500+ Lab assignments with submissions")
        print("   ✓ Complete education structure (Grades, Subjects, Clusters)")
        print("   ✓ 1000+ Academic records")
        print("\n🎯 Your database is ready for testing!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
