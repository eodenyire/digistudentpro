# DigiStudentPro Test Scripts

This directory contains comprehensive testing and seeding scripts for the DigiStudentPro platform.

## Scripts Overview

### 🌱 Seeding Scripts

#### `seed_all.py` - Master Seeding Script
Orchestrates all seeding scripts to populate the entire database with test data.

**What it creates:**
- 1000+ Users (Students, Mentors, Parents, Teachers, Admins)
- 100+ Student profiles with grades and attributes
- 100+ Mentor profiles with expertise areas
- 100+ Parent/Guardian profiles
- 500+ Lab assignments with submissions
- 1000+ Blog posts with comments and likes
- 100 Squads with 5000+ messages
- 1000+ Direct messages
- Full education system (Grades, Subjects, Clusters, Careers)
- 1000+ Academic records

**Usage:**
```bash
python scripts/seed_all.py
```

#### `seed_accounts.py`
Seeds the accounts app with users and their profiles.

**Creates:**
- 1000 users with different roles
- 200 student profiles
- 200 mentor profiles
- 200 parent/guardian profiles

**Usage:**
```bash
python scripts/seed_accounts.py
```

#### `seed_digiblog.py`
Seeds the blog app with posts, comments, likes, and follows.

**Creates:**
- 1000 blog posts
- Comments on each post
- Blog likes
- Author follows

**Usage:**
```bash
python scripts/seed_digiblog.py
```

#### `seed_digichat.py`
Seeds the chat app with squads and messages.

**Creates:**
- 100 squads (group chats)
- Squad memberships (5-100 members per squad)
- 5000+ squad messages
- 1000+ direct messages

**Usage:**
```bash
python scripts/seed_digichat.py
```

#### `seed_digiguide.py`
Seeds the guide app with education structure and records.

**Creates:**
- Education levels (Primary, Secondary, Tertiary)
- Grades for each level
- Subjects (15+)
- KUCCPS Clusters (10+)
- Careers (25+)
- Academic records for all students

**Usage:**
```bash
python scripts/seed_digiguide.py
```

#### `seed_digilab.py`
Seeds the lab app with assignments and submissions.

**Creates:**
- 500 lab assignments
- 5000+ submissions (varied statuses)
- Grades and feedback on submissions

**Usage:**
```bash
python scripts/seed_digilab.py
```

### 🧪 Test Scripts

#### `test_authentication.py`
Comprehensive authentication testing.

**Tests:**
- User creation
- Django user login
- Token generation
- Token-based API authentication
- Invalid credentials rejection
- Admin user creation
- Role-based access control

**Usage:**
```bash
python scripts/test_authentication.py
```

#### `test_api_integration.py`
Tests all API endpoints with real data.

**Tests:**
- API root endpoint access
- All API endpoints (accounts, blog, chat, guide, lab)
- Data integrity verification
- Database record counts

**Usage:**
```bash
python scripts/test_api_integration.py
```

### 🚀 Test Runners

#### `run_all_tests.py`
Master test runner that executes all tests in sequence.

**Execution order:**
1. Database seeding (creates 5000+ records)
2. Authentication tests
3. API integration tests

**Usage:**
```bash
python scripts/run_all_tests.py
```

#### `run_tests.sh`
Bash wrapper for easy execution.

**Usage:**
```bash
bash scripts/run_tests.sh
```

## Quick Start

### Option 1: Run Everything (Recommended)
```bash
python scripts/run_all_tests.py
```

This will:
1. Seed the database completely
2. Run authentication tests
3. Run API integration tests
4. Provide a comprehensive report

### Option 2: Run Individual Scripts
```bash
# Step 1: Seed database
python scripts/seed_all.py

# Step 2: Test authentication
python scripts/test_authentication.py

# Step 3: Test API
python scripts/test_api_integration.py
```

### Option 3: Seed Specific Apps
```bash
python scripts/seed_accounts.py       # Users and profiles
python scripts/seed_digiblog.py       # Blog content
python scripts/seed_digichat.py       # Chat/squads
python scripts/seed_digiguide.py      # Education structure
python scripts/seed_digilab.py        # Lab assignments
```

## Test Data Generated

After running all scripts, your database will have:

- **Users**: 1000+ (200 each: students, mentors, parents, teachers, admin)
- **Student Profiles**: 200 with grades, schools, and career interests
- **Mentor Profiles**: 200 with expertise areas and verification status
- **Parent Profiles**: 200 linked to students
- **Blog Posts**: 1000 with varied categories and statuses
- **Blog Comments**: 5000+ with threaded replies
- **Blog Likes**: 50,000+ across posts
- **Blog Follows**: 2500+ author follows
- **Squads**: 100 with up to 100 members each
- **Squad Messages**: 5000+ on various topics
- **Direct Messages**: 1000+ between users
- **Lab Assignments**: 500 with varied difficulty levels
- **Lab Submissions**: 5000+ with grades and feedback
- **Education Records**: Complete structure with 10+ clusters
- **Academic Records**: 3000+ student performance records

## Testing Features

### Authentication Tests
- ✅ User registration
- ✅ Login with valid credentials
- ✅ Token generation
- ✅ API token authentication
- ✅ Invalid credentials rejection
- ✅ Admin creation and access
- ✅ Role-based permissions

### API Integration Tests
- ✅ Endpoint connectivity
- ✅ Data retrieval
- ✅ Data integrity
- ✅ Database consistency
- ✅ Record counts across all apps

## Important Notes

1. **Database**: Tests use your development database. Consider backing up before large test runs.

2. **Faker Data**: All test data is generated using Faker library. Data is realistic but randomized.

3. **Performance**: First full seeding may take 2-5 minutes depending on system performance.

4. **Cleanup**: To reset the database:
   ```bash
   python manage.py flush --no-input
   ```

5. **Test Users**: Default test credentials:
   - Username: Any user created by scripts
   - Password: Same for all script-created users (use your own when testing login)

## Troubleshooting

### Script errors
If scripts fail, check:
1. Django is properly configured
2. Database is accessible
3. All dependencies installed: `pip install faker`
4. Migrations are applied: `python manage.py migrate`

### Import errors
Ensure you're running scripts from the correct directory:
```bash
cd /workspaces/digistudentpro
python scripts/seed_all.py
```

### Slow performance
- Seeding 5000+ records may take time
- First run creates indexes which helps future operations
- Subsequent runs should be faster

## Next Steps

After seeding and testing:
1. ✅ Access backend at `http://localhost:8000/api/v1/`
2. ✅ Access frontend at `http://localhost:5173/`
3. ✅ Log in with any created user
4. ✅ Test core functionality with real data
5. ✅ Verify all endpoints work correctly

## Support

For issues or questions about test scripts, check:
- Individual script documentation at the top of each file
- Console output from test runs (detailed error messages)
- Django debug mode logs

---

**Happy Testing! 🎉**
