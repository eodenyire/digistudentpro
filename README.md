# DigiStudentPro - EdTech Ecosystem for Kenya's CBC

**A comprehensive digital learning platform tailored for Kenya's Competency-Based Curriculum (CBC), spanning Pre-Primary to University level.**

---

## 🎯 Vision

DigiStudentPro transforms education in Kenya by providing an integrated ecosystem that combines AI-powered career guidance, comprehensive learning resources, mentorship opportunities, and community engagement - all designed specifically for the CBC framework.

## 🏗️ Architecture Overview

DigiStudentPro consists of four core modules working together as a unified platform:

### 1️⃣ DigiGuide - The Intelligence Engine
*Predictive analytics and career guidance powered by student performance data*

**Key Features:**
- **Student Profile ("Golden Record")**: Comprehensive tracking of demographics, academic history, and interests
- **Career Database**: Master database of careers mapped to KUCCPS cluster requirements
- **AI Prediction Model**: Projects Grade 12 performance based on Grade 7-9 trajectory
- **Gap Analysis**: Identifies subject weaknesses and recommends remedial content
- **Dream Simulator**: Generates reverse roadmaps showing exact grades needed to achieve career goals

**Example:**
> *Student wants to study Medicine → System analyzes current Biology (B+), Chemistry (A-), Math (B) → Flags Physics gap → Suggests DigiLab content → Projects needed improvements*

### 2️⃣ DigiLab - The Knowledge Repository
*Comprehensive digital content library structured around CBC learning outcomes*

**Content Hierarchy:**
```
Education Level (e.g., Junior Secondary)
└── Grade (e.g., Grade 8)
    └── Subject (e.g., Integrated Science)
        └── Strand (e.g., Mixtures and Elements)
            └── Sub-Strand (Specific learning outcome)
                └── Resources (Text, Video, Audio, PDF, Assessments)
```

**Resource Types:**
- 📝 HTML-formatted text (mobile-optimized)
- 📄 PDF worksheets and past papers
- 🎥 Video lessons (embedded or hosted)
- 🎧 Audio content (podcasts, language lessons)
- ✅ Interactive assessments and quizzes

**Offline Support:** PWA capabilities for low-connectivity areas

### 3️⃣ DigiChat - The Mentorship Hub
*Secure, monitored platform connecting students with verified mentors*

**User Roles:**
- **Mentees**: Students seeking guidance
- **Mentors**: Verified professionals, teachers, counselors (with badges)

**Communication Channels:**
- **Direct Messaging (1-on-1)**: Private conversations with audit logs
- **Squads (Group Chats)**: Topic-based communities (e.g., "Future Medics", "Coding Club")
- **Q&A Forums**: StackOverflow-style questions with upvoting

**Safety Features:**
- Verified mentor badges
- Automated keyword flagging for child safety
- Admin audit capabilities
- Background checks for mentors
- Compliance with Kenya Data Protection Act 2019

### 4️⃣ DigiBlog - The Community Feed
*Educational content and engagement platform*

**Content Pillars:**
- 📚 Study Hacks
- 🧠 Mental Health
- 💰 Scholarship News
- 📋 CBC Updates
- 💻 Tech in Schools
- 🎓 Career Guidance

**Features:**
- Creator profiles with follow functionality
- Engagement metrics (likes, comments, shares)
- Curated feeds based on student grade level
- Mobile-first design

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Django 5.0+ (Python) | REST API, business logic, AI/ML integration |
| **Database** | PostgreSQL | Complex relationships, JSON fields |
| **Real-time** | Django Channels + Redis | WebSocket support for DigiChat |
| **Frontend** | React.js (planned) | Interactive, responsive UI |
| **API** | Django REST Framework | RESTful API endpoints |
| **Task Queue** | Celery + Redis | Async tasks (notifications, predictions) |
| **Storage** | AWS S3 / Local | Media files (videos, PDFs, images) |
| **Deployment** | Docker + AWS/GCP | Scalable cloud infrastructure |

---

## 📊 Database Schema Overview

### Core Entities

**Users & Profiles:**
- `User` (custom user model with roles)
- `StudentProfile` (the "Golden Record")
- `MentorProfile` (verified mentors)

**Education Structure (DigiGuide):**
- `EducationLevel` → `Grade` → `Subject`
- `AcademicRecord` (performance tracking)
- `Career` (KUCCPS-mapped careers)

**Content Management (DigiLab):**
- `Strand` → `SubStrand` → `LearningResource`

**Community (DigiChat & DigiBlog):**
- `Squad` (group chats)
- `BlogPost` (articles and content)

*Detailed schema documentation available in `/docs/DATABASE_SCHEMA.md`*

---

## 🇰🇪 Kenya CBC Context

### Education Levels Supported

| Level | Grades | Ages |
|-------|--------|------|
| Pre-Primary | PP1, PP2 | 4-6 years |
| Lower Primary | Grade 1-3 | 6-9 years |
| Upper Primary | Grade 4-6 | 9-12 years |
| Junior Secondary | Grade 7-9 | 12-15 years |
| Senior Secondary | Grade 10-12 | 15-18 years |
| University | Year 1-4+ | 18+ years |

### CBC Grading System

DigiStudentPro supports both traditional scores and CBC performance levels:
- **Exceeding Expectations**
- **Meeting Expectations**
- **Approaching Expectations**
- **Below Expectations**

### KUCCPS Integration

Career recommendations mapped to Kenya Universities and Colleges Central Placement Service (KUCCPS) cluster requirements.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- pip and virtualenv

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/eodenyire/digistudentpro-.git
cd digistudentpro-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements/development.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
cd backend
python manage.py migrate

# Load initial CBC structure
python manage.py load_cbc_structure

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000/admin` to access the Django admin panel.

---

## 📁 Project Structure

```
digistudentpro-/
├── backend/
│   ├── config/                 # Django project settings
│   │   ├── settings/
│   │   │   ├── base.py        # Common settings
│   │   │   ├── development.py # Dev-specific settings
│   │   │   └── production.py  # Production settings
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/
│   │   ├── accounts/          # User management
│   │   ├── digiguide/         # AI prediction engine
│   │   ├── digilab/           # Content management
│   │   ├── digichat/          # Mentorship platform
│   │   └── digiblog/          # Community content
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   ├── static/
│   ├── media/
│   └── manage.py
├── frontend/                   # React app (future)
├── docs/                       # Documentation
│   ├── DATABASE_SCHEMA.md
│   ├── API_DESIGN.md
│   ├── ARCHITECTURE.md
│   └── COMPLIANCE.md
├── .gitignore
├── README.md
├── docker-compose.yml
└── LICENSE
```

---

## 🔒 Compliance & Security

### Kenya Data Protection Act 2019

DigiStudentPro is designed with full compliance to Kenya's data protection regulations:

- ✅ **Parental Consent**: Required for users under 18
- ✅ **Data Minimization**: Only essential data collected
- ✅ **Right to Access**: Users can export their data
- ✅ **Right to Erasure**: Account deletion available
- ✅ **Data Security**: Encryption at rest and in transit
- ✅ **Audit Logs**: All data access tracked

### Child Safety (DigiChat)

- Automated keyword filtering
- Mentor background verification
- Admin monitoring capabilities
- Content moderation system
- Reporting mechanisms

*Full compliance documentation in `/docs/COMPLIANCE.md`*

---

## 🎯 Development Roadmap

### Phase 1: Foundation (Current)
- ✅ Project architecture defined
- ✅ Database models designed
- ✅ Django backend setup
- 🔄 Initial migrations
- 🔄 Admin interface configuration

### Phase 2: Core Features
- DigiGuide prediction algorithm (ML model)
- DigiLab content upload system
- User authentication & authorization
- REST API endpoints

### Phase 3: Interactive Features
- DigiChat real-time messaging
- Squad management
- Notification system

### Phase 4: Content & Engagement
- DigiBlog publishing system
- Comment and engagement features
- Search functionality

### Phase 5: Frontend Development
- React application
- Mobile-responsive design
- PWA for offline access

### Phase 6: AI & Analytics
- Performance prediction models
- Career recommendation engine
- Dashboard analytics

### Phase 7: Production
- Security audit
- Performance optimization
- Deployment to production
- User acceptance testing

---

## 🤝 Contributing

We welcome contributions from developers, educators, and content creators!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 for Python code
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Respect Kenya's cultural and educational context

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

**Project Lead:** eodenyire

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities:

- GitHub Issues: [Create an issue](https://github.com/eodenyire/digistudentpro-/issues)
- Email: [Your email - add later]

---

## 🙏 Acknowledgments

- Kenya Institute of Curriculum Development (KICD) for CBC framework
- KUCCPS for university placement guidelines
- All educators and mentors supporting Kenyan students

---

## 🌟 Star Us!

If you find DigiStudentPro useful, please consider giving us a star ⭐ on GitHub!

---

**Built with ❤️ for Kenyan learners**
