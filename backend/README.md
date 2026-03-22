# DigiStudentPro Backend

Django 5.0+ REST API backend for the DigiStudentPro EdTech platform.

## 🏗️ Project Structure

```
backend/
├── config/                    # Django project configuration
│   ├── settings/
│   │   ├── base.py           # Common settings
│   │   ├── development.py    # Development settings
│   │   └── production.py     # Production settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI application
│   ├── asgi.py               # ASGI application (for WebSockets)
│   └── celery.py             # Celery configuration
├── apps/
│   ├── accounts/             # User management & profiles
│   ├── digiguide/            # Career guidance & AI predictions
│   ├── digilab/              # Learning resources & assessments
│   ├── digichat/             # Real-time messaging & squads
│   └── digiblog/             # Community blog & content
├── static/                   # Static files
├── media/                    # User-uploaded files
├── templates/                # Django templates
├── logs/                     # Application logs
├── requirements/             # Python dependencies
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── manage.py                 # Django management script
└── .env.example              # Environment variables template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ (optional, SQLite for development)
- Redis 7+ (for Celery & Channels)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/eodenyire/digistudentpro-.git
cd digistudentpro-/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements/development.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load initial data (optional)**
```bash
python manage.py load_cbc_structure
python manage.py load_careers
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000/admin` to access the admin panel.

## 📚 Apps Overview

### 1. **Accounts** - User Management
- Custom User model with multiple roles (student, mentor, parent, teacher, admin)
- StudentProfile with academic tracking
- MentorProfile with verification system
- ParentGuardian for parental consent

**Models:**
- `User` - Custom user model extending AbstractUser
- `StudentProfile` - Student information and preferences
- `MentorProfile` - Mentor credentials and verification
- `ParentGuardian` - Parent/guardian linkage to students

**API Endpoints:**
- `/api/v1/accounts/users/` - User management
- `/api/v1/accounts/students/` - Student profiles
- `/api/v1/accounts/mentors/` - Mentor profiles
- `/api/v1/accounts/parents/` - Parent/guardian profiles

### 2. **DigiGuide** - Career Guidance
- CBC education structure (levels, grades, subjects)
- Career database with KUCCPS cluster mapping
- Academic record tracking
- AI-powered career predictions

**Models:**
- `EducationLevel` - Pre-primary to University
- `Grade` - Grade levels within each education level
- `Subject` - Subjects taught at different levels
- `Cluster` - KUCCPS clusters with requirements
- `Career` - Career options with qualifications
- `AcademicRecord` - Student performance tracking
- `CareerPrediction` - AI predictions and gap analysis

**API Endpoints:**
- `/api/v1/digiguide/education-levels/`
- `/api/v1/digiguide/grades/`
- `/api/v1/digiguide/subjects/`
- `/api/v1/digiguide/clusters/`
- `/api/v1/digiguide/careers/`
- `/api/v1/digiguide/academic-records/`
- `/api/v1/digiguide/predictions/`

### 3. **DigiLab** - Learning Resources
- Hierarchical content structure (Strand → SubStrand → Resource)
- Multiple resource types (text, video, audio, PDF, assessment)
- Progress tracking for students
- Assessment system with questions and attempts

**Models:**
- `Strand` - Main learning topics
- `SubStrand` - Specific learning outcomes
- `LearningResource` - Content resources
- `ResourceProgress` - Student progress tracking
- `Assessment` - Quiz/assessment configuration
- `Question` - Assessment questions
- `Answer` - Answer options
- `AssessmentAttempt` - Student assessment attempts

**API Endpoints:**
- `/api/v1/digilab/strands/`
- `/api/v1/digilab/sub-strands/`
- `/api/v1/digilab/resources/`
- `/api/v1/digilab/progress/`
- `/api/v1/digilab/assessments/`
- `/api/v1/digilab/attempts/`

### 4. **DigiChat** - Mentorship Platform
- Squad-based group chats
- 1-on-1 direct messaging
- Real-time WebSocket support
- Message reporting and moderation

**Models:**
- `Squad` - Group chat communities
- `SquadMembership` - User roles in squads
- `Message` - Squad messages
- `DirectMessage` - 1-on-1 messages
- `MessageReport` - Safety reporting system

**API Endpoints:**
- `/api/v1/digichat/squads/`
- `/api/v1/digichat/memberships/`
- `/api/v1/digichat/messages/`
- `/api/v1/digichat/direct-messages/`
- `/api/v1/digichat/reports/`

**WebSocket Endpoints:**
- `ws/chat/squad/<squad_slug>/` - Squad chat
- `ws/chat/dm/<user_id>/` - Direct messages

### 5. **DigiBlog** - Community Content
- Blog posts with categories
- Nested comments
- Like/engagement system
- Author following

**Models:**
- `BlogPost` - Articles and content
- `Comment` - Comments with replies
- `BlogLike` - Like tracking
- `BlogFollow` - Follow authors

**API Endpoints:**
- `/api/v1/digiblog/posts/`
- `/api/v1/digiblog/comments/`
- `/api/v1/digiblog/likes/`
- `/api/v1/digiblog/follows/`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication via `djangorestframework-simplejwt`.

**Authentication Endpoints:**
- `POST /api/v1/auth/jwt/create/` - Obtain JWT token
- `POST /api/v1/auth/jwt/refresh/` - Refresh JWT token
- `POST /api/v1/auth/jwt/verify/` - Verify JWT token
- `POST /api/v1/auth/users/` - User registration (via Djoser)

**Usage:**
```bash
# Obtain token
curl -X POST http://localhost:8000/api/v1/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Use token in requests
curl http://localhost:8000/api/v1/accounts/users/me/ \
  -H "Authorization: Bearer <your_access_token>"
```

## 🛠️ Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Format code
black .
isort .

# Lint code
flake8
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Running Celery Worker
```bash
celery -A config worker -l info
```

### Running Celery Beat (for scheduled tasks)
```bash
celery -A config beat -l info
```

### Running Channels/Daphne (for WebSockets)
```bash
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

## 📊 Database Schema

### Key Relationships

- **User → StudentProfile** (One-to-One)
- **User → MentorProfile** (One-to-One)
- **User → ParentGuardian** (One-to-One)
- **StudentProfile → AcademicRecord** (One-to-Many)
- **StudentProfile → CareerPrediction** (One-to-Many)
- **Subject → Strand** (One-to-Many)
- **Strand → SubStrand** (One-to-Many)
- **SubStrand → LearningResource** (One-to-Many)
- **Squad → Message** (One-to-Many)
- **User ↔ Squad** (Many-to-Many through SquadMembership)
- **BlogPost → Comment** (One-to-Many)

## 🚢 Deployment

### Production Settings

1. Set `DEBUG=False` in environment
2. Configure PostgreSQL database
3. Set up Redis for caching and Celery
4. Configure email backend
5. Set up media file storage (AWS S3 recommended)
6. Configure Sentry for error tracking (optional)

### Environment Variables

See `.env.example` for required environment variables.

### Running with Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Docker Support
Docker configuration can be added for containerized deployment.

## 📝 API Documentation

API documentation is available via Django REST Framework's browsable API:
- Visit `http://localhost:8000/api/v1/` when running the development server

## 🔒 Security Features

- Custom user model with proper password hashing
- JWT-based authentication
- CORS configuration
- SQL injection protection (Django ORM)
- XSS protection
- CSRF protection
- Parental consent tracking for minors
- Message flagging and reporting
- Mentor verification system

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Run code quality checks
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 👥 Authors

- **eodenyire** - Project Lead

## 🙏 Acknowledgments

- Kenya Institute of Curriculum Development (KICD)
- KUCCPS for university placement guidelines
- All contributors to the project

---

**Built with ❤️ for Kenyan learners**
# README
This project is a Django application that incorporates machine learning models and serves them via API.
