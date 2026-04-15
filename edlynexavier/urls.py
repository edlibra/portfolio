"""
URL configuration — edlynexavier.com
Architecture bilingue avec i18n_patterns.

Structure des URLs :
  /fr/          → version française (langue par défaut)
  /en/          → version anglaise
  /sitemap.xml  → hors préfixe langue (SEO)
  /robots.txt   → hors préfixe langue
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from core.sitemaps import StaticViewSitemap
from portfolio.sitemaps import ProjectSitemap

# ── Registre sitemap ──────────────────────────────────────────────────────────
sitemaps = {
    'static':   StaticViewSitemap,
    'projects': ProjectSitemap,
}

# ── URLs hors i18n (pas de préfixe /fr/ /en/) ────────────────────────────────
urlpatterns = [
    # Sitemap et robots sans préfixe langue — bon pour le SEO
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots'
    ),
    # Endpoint Django pour changer la langue (POST)
    path('i18n/', include('django.conf.urls.i18n')),
]

# ── URLs avec préfixe i18n (/fr/, /en/) ──────────────────────────────────────
urlpatterns += i18n_patterns(
    # Admin Django
    path('admin/', admin.site.urls),

    # Pages principales
    path('', include('core.urls', namespace='core')),

    # Portfolio / projets
    path('projects/', include('portfolio.urls', namespace='portfolio')),

    # Contact
    path('contact/', include('contact.urls', namespace='contact')),

    # Préfixe langue par défaut → /fr/ visible dans l'URL
    prefix_default_language=True,
)

# ── Fichiers media en développement ───────────────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ── Gestionnaires d'erreurs ───────────────────────────────────────────────────
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
