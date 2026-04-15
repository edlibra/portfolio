# Deployment Guide — edlynexavier.com

This guide covers three deployment paths: **VPS (Ubuntu)**, **Render**, and **Docker**.

---

## Option A — VPS (Ubuntu 22.04 + Nginx + Gunicorn)

### 1. Server prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip nginx postgresql postgresql-contrib git certbot python3-certbot-nginx
```

### 2. PostgreSQL setup

```bash
sudo -u postgres psql

CREATE DATABASE edlynexavier_db;
CREATE USER edlynexavier_user WITH PASSWORD 'your_secure_password';
ALTER ROLE edlynexavier_user SET client_encoding TO 'utf8';
ALTER ROLE edlynexavier_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE edlynexavier_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE edlynexavier_db TO edlynexavier_user;
\q
```

### 3. Clone & configure

```bash
sudo mkdir -p /var/www/edlynexavier
sudo chown $USER:$USER /var/www/edlynexavier

git clone https://github.com/edlynexavier/portfolio.git /var/www/edlynexavier
cd /var/www/edlynexavier

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # fill in all production values
```

### 4. Production `.env` settings

```env
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=edlynexavier.com,www.edlynexavier.com
SITE_URL=https://edlynexavier.com

DB_NAME=edlynexavier_db
DB_USER=edlynexavier_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
CONTACT_EMAIL=hello@edlynexavier.com
```

### 5. Database, seed, static files

```bash
python manage.py migrate
python manage.py seed                   # or: loaddata fixtures/initial_data.json
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 6. Gunicorn log directory

```bash
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
```

### 7. Systemd service

```bash
# Copy the service file
sudo cp deploy/edlynexavier.service /etc/systemd/system/edlynexavier.service

# Edit paths/user if needed
sudo nano /etc/systemd/system/edlynexavier.service

sudo systemctl daemon-reload
sudo systemctl enable edlynexavier
sudo systemctl start edlynexavier
sudo systemctl status edlynexavier
```

### 8. Nginx

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/edlynexavier
sudo ln -s /etc/nginx/sites-available/edlynexavier /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 9. SSL with Certbot (Let's Encrypt)

```bash
sudo certbot --nginx -d edlynexavier.com -d www.edlynexavier.com
# Follow prompts — certbot will auto-update nginx config
sudo systemctl reload nginx
```

### 10. Future deploys

```bash
cd /var/www/edlynexavier
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

---

## Option B — Render.com

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repo
4. Configure:
   - **Environment**: Python
   - **Build command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start command**: `gunicorn edlynexavier.wsgi:application`
5. Add a **PostgreSQL** database add-on
6. Set all environment variables from `.env.example`
7. Set `DATABASE_URL` from the Render PostgreSQL connection string
8. Deploy → run seed: in Render shell → `python manage.py seed`

---

## Option C — Docker Compose

```bash
# Clone project
git clone https://github.com/edlynexavier/portfolio.git
cd portfolio

# Configure environment
cp .env.example .env
# Fill in .env — set DEBUG=False for production

# Build and start
docker-compose up -d --build

# Run migrations (first time)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed
docker-compose exec web python manage.py createsuperuser

# Stop
docker-compose down
```

---

## Post-deployment checklist

- [ ] `DEBUG=False` in production `.env`
- [ ] Strong `SECRET_KEY` (50+ chars random)
- [ ] `ALLOWED_HOSTS` set to your domain
- [ ] PostgreSQL configured (not SQLite)
- [ ] SMTP email credentials set
- [ ] SSL certificate installed (`https://` works)
- [ ] `static/images/profile.jpg` — your real photo uploaded
- [ ] `static/files/edlyn-exavier-cv.pdf` — your real CV uploaded
- [ ] `static/images/og-image.png` — 1200×630px OG image
- [ ] Admin superuser created
- [ ] Seed data loaded or content entered via admin
- [ ] `sitemap.xml` accessible at `https://edlynexavier.com/sitemap.xml`
- [ ] `robots.txt` accessible at `https://edlynexavier.com/robots.txt`
- [ ] Submit sitemap to Google Search Console
- [ ] Test contact form (email delivery)
- [ ] Test on mobile devices
- [ ] Run Google PageSpeed Insights

---

## Generating a secure SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Troubleshooting

**Static files not loading in production:**
```bash
python manage.py collectstatic --noinput --clear
sudo systemctl restart edlynexavier
```

**Database connection error:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql
# Test connection
psql -U edlynexavier_user -d edlynexavier_db -h localhost
```

**500 error in production:**
```bash
# Check Gunicorn logs
sudo journalctl -u edlynexavier -n 50 --no-pager
# Check Nginx error log
sudo tail -50 /var/log/nginx/edlynexavier_error.log
```

**Email not sending:**
- For Gmail: use an [App Password](https://support.google.com/accounts/answer/185833), not your main password
- Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env`
- Test in Django shell: `python manage.py shell` → `from django.core.mail import send_mail; send_mail('Test', 'Body', 'from@x.com', ['to@x.com'])`
