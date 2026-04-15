#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# deploy/deploy.sh — VPS deployment script for edlynexavier.com
#
# Usage (on your server):
#   chmod +x deploy.sh
#   ./deploy.sh
#
# Assumes: Ubuntu 22.04+, Python 3.11+, Nginx, Git already installed.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
APP_DIR="/var/www/edlynexavier"
VENV_DIR="$APP_DIR/venv"
REPO_URL="https://github.com/edlynexavier/portfolio.git"
BRANCH="main"
SERVICE_NAME="edlynexavier"

echo "═══════════════════════════════════════════"
echo "  Deploying edlynexavier.com"
echo "═══════════════════════════════════════════"

# ── 1. Pull latest code ───────────────────────────────────────────────────────
if [ -d "$APP_DIR/.git" ]; then
    echo "→ Pulling latest changes..."
    cd "$APP_DIR"
    git fetch origin
    git reset --hard "origin/$BRANCH"
else
    echo "→ Cloning repository..."
    sudo mkdir -p "$APP_DIR"
    sudo chown "$USER":"$USER" "$APP_DIR"
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# ── 2. Virtual environment ────────────────────────────────────────────────────
echo "→ Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# ── 3. Install / update dependencies ─────────────────────────────────────────
echo "→ Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# ── 4. .env file check ────────────────────────────────────────────────────────
if [ ! -f "$APP_DIR/.env" ]; then
    echo "⚠ WARNING: .env file not found!"
    echo "  Copy .env.example to .env and fill in production values."
    echo "  Then re-run this script."
    exit 1
fi

# ── 5. Migrations ─────────────────────────────────────────────────────────────
echo "→ Running database migrations..."
python manage.py migrate --noinput

# ── 6. Collect static files ───────────────────────────────────────────────────
echo "→ Collecting static files..."
python manage.py collectstatic --noinput --clear

# ── 7. Restart Gunicorn ───────────────────────────────────────────────────────
echo "→ Restarting application server..."
if systemctl is-active --quiet "$SERVICE_NAME"; then
    sudo systemctl restart "$SERVICE_NAME"
else
    sudo systemctl start "$SERVICE_NAME"
fi

# ── 8. Reload Nginx ───────────────────────────────────────────────────────────
echo "→ Reloading Nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "═══════════════════════════════════════════"
echo "  ✓ Deployment complete!"
echo "  Site: https://edlynexavier.com"
echo "═══════════════════════════════════════════"
