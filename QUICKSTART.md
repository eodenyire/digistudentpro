# 🚀 DigiStudentPro - Full Stack Quick Start Guide

Complete guide to run the DigiStudentPro platform (Backend + Frontend)

---

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: 14 or higher (or use SQLite for development)
- **Git**: Latest version

### Verify Prerequisites
```bash
python --version    # Should be 3.11+
node --version      # Should be v18+
npm --version       # Should be 9+
psql --version      # Should be 14+ (optional)
```

---

## 🗄️ Database Setup (PostgreSQL - Recommended)

### Option 1: PostgreSQL (Production-like)
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE DATABASE digistudentpro;
CREATE USER digistudent WITH PASSWORD 'your_secure_password';
ALTER ROLE digistudent SET client_encoding TO 'utf8';
ALTER ROLE digistudent SET default_transaction_isolation TO 'read committed';
ALTER ROLE digistudent SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE digistudentpro TO digistudent;
\q
```

### Option 2: SQLite (Development)
No setup required - SQLite works out of the box!

---

## 🔧 Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements/development.txt
```

### 4. Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

**Required settings in `.env`:**
```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DATABASE_URL=postgresql://digistudent:your_secure_password@localhost:5432/digistudentpro

# Or use SQLite (simpler for development)
# DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # minutes (7 days)

# Email (optional for now)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional but recommended)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 7. Load Sample Data (Optional)
```bash
# If you have fixtures for sample data
python manage.py loaddata sample_data.json
```

### 8. Start Backend Server
```bash
python manage.py runserver
```

✅ Backend should now be running at: **http://localhost:8000**

### Verify Backend
Open browser and visit:
- API Root: http://localhost:8000/api/v1/
- Admin Panel: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/docs/ (if configured)

---

## 🎨 Frontend Setup

### 1. Open New Terminal (keep backend running)
```bash
# Navigate to frontend directory
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env
```

**`.env` should contain:**
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_BASE_URL=ws://localhost:8000/ws
VITE_APP_NAME=DigiStudentPro
VITE_APP_VERSION=1.0.0
VITE_ENABLE_CHAT=true
VITE_ENABLE_BLOG=true
```

### 4. Start Frontend Development Server
```bash
npm run dev
```

✅ Frontend should now be running at: **http://localhost:3000**

---

## ✅ Verification Steps

### 1. Check Backend Health
```bash
# In a new terminal
curl http://localhost:8000/api/v1/
# Should return API root response
```

### 2. Check Frontend
Open browser: http://localhost:3000
- Should see DigiStudentPro landing page
- Navigation should work
- No console errors

### 3. Test Authentication Flow
1. Click "Sign Up" / "Get Started"
2. Fill registration form
3. Register new account
4. Login with credentials
5. Should redirect to dashboard

### 4. Test API Integration
1. After login, navigate to "DigiGuide" → "Careers"
2. Should load careers from backend
3. Try search and filters
4. Navigate to other modules (DigiLab, DigiChat, DigiBlog)

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>

# Or use different port
python manage.py runserver 8080
# Update frontend .env: VITE_API_BASE_URL=http://localhost:8080/api/v1
```

### Issue 2: Database connection error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify database exists
sudo -u postgres psql -l | grep digistudentpro

# Check connection string in .env
cat .env | grep DATABASE_URL
```

### Issue 3: Frontend won't start
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is in use
lsof -i :3000
kill -9 <PID>
```

### Issue 4: CORS errors
Make sure backend `settings.py` has:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Issue 5: Module not found errors
```bash
# Backend
pip install -r requirements/development.txt

# Frontend
cd frontend
npm install
```

---

## 📝 Development Workflow

### Daily Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Making Backend Changes
```bash
# After model changes
python manage.py makemigrations
python manage.py migrate

# After adding dependencies
pip freeze > requirements/development.txt
```

### Making Frontend Changes
```bash
# After adding dependencies
cd frontend
npm install <package-name>

# Type checking
npm run type-check

# Build for production
npm run build
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests (when added)
```bash
cd frontend
npm run test
```

---

## 🚀 Production Build

### Backend
```bash
# Update .env
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# Collect static files
python manage.py collectstatic --noinput

# Use production server (gunicorn)
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm run build

# Output in dist/ folder
# Deploy to Vercel, Netlify, or static hosting
```

---

## 🔑 Default Test Accounts

After creating superuser, you can create test accounts:

```bash
python manage.py shell
```

```python
from apps.accounts.models import User

# Create student
student = User.objects.create_user(
    username='student1',
    email='student@test.com',
    password='testpass123',
    role='student',
    first_name='John',
    last_name='Doe'
)

# Create mentor
mentor = User.objects.create_user(
    username='mentor1',
    email='mentor@test.com',
    password='testpass123',
    role='mentor',
    first_name='Jane',
    last_name='Smith'
)
```

---

## 📚 Useful Commands

### Backend
```bash
# Create new app
python manage.py startapp app_name

# Database shell
python manage.py dbshell

# Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# Show migrations
python manage.py showmigrations
```

### Frontend
```bash
# Install package
npm install <package-name>

# Remove package
npm uninstall <package-name>

# Update packages
npm update

# Check for outdated packages
npm outdated

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main application |
| Backend API | http://localhost:8000/api/v1/ | REST API |
| Admin Panel | http://localhost:8000/admin/ | Django admin |
| API Docs | http://localhost:8000/api/docs/ | API documentation |

---

## 📞 Getting Help

### Check Logs
```bash
# Backend logs
# Already visible in terminal where you ran runserver

# Frontend logs
# Check browser console (F12)
```

### Common Log Files
```bash
# Django logs (if configured)
tail -f logs/django.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

---

## 🎯 Next Steps

After successful setup:

1. ✅ Explore the admin panel
2. ✅ Create sample data (users, careers, resources)
3. ✅ Test all CRUD operations
4. ✅ Try the authentication flow
5. ✅ Navigate through all modules
6. ✅ Test responsive design (resize browser)
7. ✅ Check browser console for errors
8. ✅ Review API responses in Network tab

---

## 🎓 Learning Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **TanStack Query**: https://tanstack.com/query/latest
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

**Happy Coding! 🚀**

For issues or questions, check the documentation or create an issue on GitHub.

*DigiStudentPro - Empowering Kenya's Education Through Technology 🇰🇪*
