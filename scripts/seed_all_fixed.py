#!/usr/bin/env python
"""
Master seed script - Fixed version with proper imports
Runs all seed scripts in the correct order
"""
import os
import sys
import time

# Setup Django path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

import django
django.setup()

def main():
    """Master seeding function"""
    print("\n" + "=" * 70)
    print(" " * 15 + "🌱 DIGISTUDENTPRO DATABASE SEEDING 🌱")
    print("=" * 70)
    print("\nThis will populate all apps with test data in 5 steps.\n")
    
    start_time = time.time()
    
    try:
        # Import seed functions
        from seed_digiguide import main as seed_digiguide
        from seed_accounts import main as seed_accounts
        from seed_digilab import main as seed_digilab
        from seed_digiblog import main as seed_digiblog
        from seed_digichat import main as seed_digichat
        
        # Step 1: DigiGuide (needs to run first for dependencies)
        print("\n🔹 STEP 1/5: DigiGuide App")
        print("-" * 70)
        seed_digiguide()
        time.sleep(1)
        
        # Step 2: Accounts
        print("\n🔹 STEP 2/5: Accounts App")
        print("-" * 70)
        seed_accounts()
        time.sleep(1)
        
        # Step 3: DigiLab
        print("\n🔹 STEP 3/5: DigiLab App")
        print("-" * 70)
        seed_digilab()
        time.sleep(1)
        
        # Step 4: DiBlog
        print("\n🔹 STEP 4/5: DigiBlog App")
        print("-" * 70)
        seed_digiblog()
        time.sleep(1)
        
        # Step 5: DigiChat
        print("\n🔹 STEP 5/5: DigiChat App")
        print("-" * 70)
        seed_digichat()
        
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
