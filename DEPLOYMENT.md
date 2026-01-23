# Deployment Checklist for DigiStudentPro Backend

## ✅ Pre-Deployment Verification

### Code Quality
- [x] All Python files have valid syntax
- [x] No CodeQL security vulnerabilities
- [x] All code review issues resolved
- [x] Models properly structured with relationships
- [x] ViewSets implement proper permissions
- [x] Admin interfaces configured

### Documentation
- [x] Backend README.md created
- [x] Implementation summary documented
- [x] .env.example with all required variables
- [x] API endpoints documented in README

## 🚀 Deployment Steps

### 1. Server Setup
- [ ] Install Python 3.11+
- [ ] Install PostgreSQL 14+
- [ ] Install Redis 7+
- [ ] Configure firewall rules
- [ ] Set up SSL certificates

### 2. Application Setup
```bash
# Clone repository
git clone https://github.com/eodenyire/digistudentpro-.git
cd digistudentpro-/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/production.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with production values
```

### 3. Environment Configuration
Edit `.env` with production values:
```bash
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=digistudentpro
DB_USER=digistudentpro_user
DB_PASSWORD=<strong-password>
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=127.0.0.1
REDIS_PORT=6379

CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-password>

# Optional: AWS S3 for media storage
USE_S3=True
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_STORAGE_BUCKET_NAME=digistudentpro-media
AWS_S3_REGION_NAME=us-east-1

# Optional: Sentry for error tracking
SENTRY_DSN=<your-sentry-dsn>
```

### 4. Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE digistudentpro;
CREATE USER digistudentpro_user WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE digistudentpro TO digistudentpro_user;
\q

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py load_cbc_structure
python manage.py load_careers

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Service Configuration

#### Gunicorn (systemd service)
Create `/etc/systemd/system/digistudentpro.service`:
```ini
[Unit]
Description=DigiStudentPro Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/digistudentpro/backend
Environment="PATH=/var/www/digistudentpro/backend/venv/bin"
ExecStart=/var/www/digistudentpro/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Daphne for WebSockets (systemd service)
Create `/etc/systemd/system/digistudentpro-daphne.service`:
```ini
[Unit]
Description=DigiStudentPro Daphne (WebSocket) Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/digistudentpro/backend
Environment="PATH=/var/www/digistudentpro/backend/venv/bin"
ExecStart=/var/www/digistudentpro/backend/venv/bin/daphne \
    -b 127.0.0.1 \
    -p 8001 \
    config.asgi:application

[Install]
WantedBy=multi-user.target
```

#### Celery Worker (systemd service)
Create `/etc/systemd/system/digistudentpro-celery.service`:
```ini
[Unit]
Description=DigiStudentPro Celery Worker
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/digistudentpro/backend
Environment="PATH=/var/www/digistudentpro/backend/venv/bin"
ExecStart=/var/www/digistudentpro/backend/venv/bin/celery -A config worker -l info

[Install]
WantedBy=multi-user.target
```

#### Celery Beat (systemd service)
Create `/etc/systemd/system/digistudentpro-celerybeat.service`:
```ini
[Unit]
Description=DigiStudentPro Celery Beat
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/digistudentpro/backend
Environment="PATH=/var/www/digistudentpro/backend/venv/bin"
ExecStart=/var/www/digistudentpro/backend/venv/bin/celery -A config beat -l info

[Install]
WantedBy=multi-user.target
```

### 6. Nginx Configuration
Create `/etc/nginx/sites-available/digistudentpro`:
```nginx
upstream django {
    server 127.0.0.1:8000;
}

upstream daphne {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/digistudentpro/backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/digistudentpro/backend/media/;
    }

    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/digistudentpro /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Start Services
```bash
# Enable and start services
sudo systemctl enable digistudentpro digistudentpro-daphne digistudentpro-celery digistudentpro-celerybeat
sudo systemctl start digistudentpro digistudentpro-daphne digistudentpro-celery digistudentpro-celerybeat

# Check status
sudo systemctl status digistudentpro
sudo systemctl status digistudentpro-daphne
sudo systemctl status digistudentpro-celery
sudo systemctl status digistudentpro-celerybeat
```

## 🔒 Security Checklist

### Django Security
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS/SSL enabled
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] Database credentials secured

### Server Security
- [ ] Firewall configured (UFW/iptables)
- [ ] Only necessary ports open (80, 443, 22)
- [ ] SSH key-based authentication
- [ ] Disable root login
- [ ] Regular security updates enabled
- [ ] Fail2ban configured

### Application Security
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] File upload limits set
- [ ] Database backups automated
- [ ] Log rotation configured
- [ ] Monitoring/alerting set up

## 📊 Monitoring & Maintenance

### Health Checks
- [ ] Application responds on /admin
- [ ] API endpoints responding
- [ ] WebSocket connections working
- [ ] Celery tasks processing
- [ ] Database queries performing well
- [ ] Redis cache working

### Monitoring Tools
- [ ] Sentry for error tracking
- [ ] New Relic/DataDog (optional)
- [ ] Prometheus + Grafana (optional)
- [ ] Log aggregation (ELK stack)

### Backup Strategy
```bash
# Database backup script
#!/bin/bash
BACKUP_DIR=/var/backups/digistudentpro
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U digistudentpro_user digistudentpro > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

# Add to crontab: 0 2 * * * /path/to/backup.sh
```

### Log Monitoring
```bash
# View application logs
sudo journalctl -u digistudentpro -f

# View Celery logs
sudo journalctl -u digistudentpro-celery -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🧪 Post-Deployment Testing

### API Testing
```bash
# Test authentication
curl -X POST https://yourdomain.com/api/v1/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Test public endpoint
curl https://yourdomain.com/api/v1/digiguide/education-levels/

# Test WebSocket (using wscat)
wscat -c wss://yourdomain.com/ws/chat/squad/test-squad/
```

### Performance Testing
- [ ] Load testing with Apache Bench/Locust
- [ ] Database query optimization
- [ ] Redis cache hit rates
- [ ] Response time monitoring

## 📝 Documentation

### For Users
- [ ] API documentation published
- [ ] User guides created
- [ ] Admin documentation
- [ ] FAQ section

### For Developers
- [ ] Development setup guide
- [ ] Contributing guidelines
- [ ] Code style guide
- [ ] Database schema documentation

## 🎉 Launch Checklist

- [ ] All tests passing
- [ ] Security audit completed
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Team trained
- [ ] Support channels ready

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Contact:** eodenyire
