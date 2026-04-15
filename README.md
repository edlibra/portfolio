# Edlyn Exavier — Personal Portfolio

> Professional personal website and portfolio of **Edlyn Exavier** — Electronic Engineering Technology student, web developer, and tech builder.

**Live:** [edlynexavier.com](https://edlynexavier.com)

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · Django 4.2 |
| Database | PostgreSQL (production) · SQLite (development) |
| Frontend | Bootstrap 5 · Custom CSS (design system) · Vanilla JS |
| Typography | Syne · DM Sans (Google Fonts) |
| Icons | Bootstrap Icons 1.11 |
| Static files | WhiteNoise |
| WSGI server | Gunicorn |
| Containerisation | Docker · Docker Compose |
| SEO | JSON-LD · Open Graph · Twitter Card · sitemap.xml · robots.txt |

---

## Features

- **Hero** with animated avatar, floating icons, stats row
- **About** page with timeline, build grid, and opportunity tags
- **Projects** grid with tag filtering, detail pages, related projects
- **Skills** page with animated progress bars and badge cloud
- **Resume** page with DB-driven sections and PDF download
- **Contact** form with honeypot anti-spam, SMTP email notification, and DB storage
- **Full SEO**: per-page title/meta/OG/Twitter Card, JSON-LD (Person, WebSite, SoftwareSourceCode), canonical URLs, sitemap.xml, robots.txt
- **Django Admin** with organised models, inline editing, and slug auto-generation
- **Scroll animations** via IntersectionObserver, navbar glassmorphism, skill bar animations
- Fully **responsive** — mobile-first, tested at all breakpoints
- **Production-ready**: WhiteNoise, Gunicorn, environment variables, Docker support

---

## Project Structure

```
edlynexavier/
├── manage.py
├── requirements.txt
├── Procfile               # Heroku / Render
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── edlynexavier/          # Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                  # Home, About, Skills, Resume + Site models
├── portfolio/             # Projects + Skills data models
├── contact/               # Contact form, model, email
│
├── templates/
│   ├── base.html          # Full SEO head, JSON-LD, navbar, footer
│   ├── robots.txt
│   ├── partials/          # _navbar, _footer, _messages, _breadcrumbs
│   ├── core/              # home, about, skills, resume
│   ├── portfolio/         # projects, project_detail
│   ├── contact/           # contact
│   └── errors/            # 404, 500
│
├── static/
│   ├── css/main.css       # Full custom design system
│   ├── js/main.js         # Scroll animations, navbar, form UX
│   ├── images/            # profile.jpg, og-image.png, favicon.svg
│   └── files/             # edlyn-exavier-cv.pdf
│
└── fixtures/
    └── initial_data.json  # Seed: projects, skills, social links, resume items
```

---

## Local Installation

### Prerequisites
- Python 3.10+
- pip
- (Optional) PostgreSQL for production-like environment

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/edlynexavier/portfolio.git
cd portfolio

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Open .env and set your values (SECRET_KEY at minimum)

# 5. Apply database migrations
python manage.py migrate

# 6. Load seed data (projects, skills, social links, resume)
python manage.py loaddata fixtures/initial_data.json

# 7. Create admin superuser
python manage.py createsuperuser

# 8. Run development server
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.
Django admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | Django secret key |
| `DEBUG` | ✅ | `True` | Set `False` in production |
| `ALLOWED_HOSTS` | ✅ | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `SITE_URL` | ✅ | `https://edlynexavier.com` | Used in SEO canonical URLs |
| `DATABASE_URL` | — | — | Full DB URL (Render/Railway) |
| `DB_NAME` | — | — | PostgreSQL database name |
| `DB_USER` | — | — | PostgreSQL user |
| `DB_PASSWORD` | — | — | PostgreSQL password |
| `DB_HOST` | — | `localhost` | PostgreSQL host |
| `DB_PORT` | — | `5432` | PostgreSQL port |
| `EMAIL_BACKEND` | — | console | Django email backend class |
| `EMAIL_HOST` | — | `smtp.gmail.com` | SMTP host |
| `EMAIL_PORT` | — | `587` | SMTP port |
| `EMAIL_HOST_USER` | — | — | SMTP username |
| `EMAIL_HOST_PASSWORD` | — | — | SMTP password or app password |
| `CONTACT_EMAIL` | — | — | Destination for contact form emails |

---

## Collect Static Files (Production)

```bash
python manage.py collectstatic --noinput
```

---

## Deploy with Docker

```bash
# Build and start all services (web + PostgreSQL)
cp .env.example .env
# Fill in .env with production values

docker-compose up -d --build

# Load seed data
docker-compose exec web python manage.py loaddata fixtures/initial_data.json

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

---

## Deploy on VPS (Ubuntu + Nginx + Gunicorn)

```bash
# On your server:
git clone https://github.com/edlynexavier/portfolio.git /var/www/edlynexavier
cd /var/www/edlynexavier

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # fill in production values
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn edlynexavier.wsgi:application --bind 127.0.0.1:8000 --workers 3 --daemon
```

Nginx site config (simplified):
```nginx
server {
    listen 80;
    server_name edlynexavier.com www.edlynexavier.com;

    location /static/ {
        alias /var/www/edlynexavier/staticfiles/;
    }
    location /media/ {
        alias /var/www/edlynexavier/media/;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Deploy on Render / Railway

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Set start command: `gunicorn edlynexavier.wsgi:application`
4. Add all environment variables from `.env.example`
5. Add a PostgreSQL add-on and set `DATABASE_URL`

---

## Adding Content

All content is managed through the Django Admin at `/admin/`:

- **Projects**: Portfolio → Projects → Add Project
- **Skills**: Portfolio → Skill Categories → add Skills inline
- **Resume**: Core → Resume Sections → add Resume Items inline
- **Social Links**: Core → Social Links

---

## SEO Notes

- Each page has its own `<title>`, `meta description`, canonical URL, and Open Graph tags
- JSON-LD structured data: `Person`, `WebSite` (global), `SoftwareSourceCode` (project pages)
- `sitemap.xml` is auto-generated at `/sitemap.xml` and includes all active projects
- `robots.txt` is served at `/robots.txt`
- Breadcrumb navigation uses `BreadcrumbList` schema on inner pages
- Semantic HTML throughout: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Single `<h1>` per page, proper heading hierarchy

---

## Customisation Checklist

After setup, update these items:

- [ ] Replace `static/images/profile.jpg` with your actual photo
- [ ] Replace `static/files/edlyn-exavier-cv.pdf` with your real CV
- [ ] Create `static/images/og-image.png` (1200×630px) for social sharing
- [ ] Update GitHub and LinkedIn URLs in fixtures (or via Admin → Social Links)
- [ ] Update `CONTACT_EMAIL` in `.env`
- [ ] Update `SITE_URL` in `.env` to your actual domain
- [ ] Set `DEBUG=False` in production
- [ ] Generate a strong `SECRET_KEY`

---

## License

This project is personal and not open for redistribution without permission.

---

*Built with Django 4.2 · Bootstrap 5 · ♥ by Edlyn Exavier*
