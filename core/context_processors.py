"""
core/context_processors.py

Inject global SEO metadata and site settings into every template context.
"""

from django.conf import settings
from core.models import SocialLink


def seo_defaults(request):
    """
    Provide default SEO values to every template.
    Individual views can override these by passing their own context keys.
    """
    seo = getattr(settings, 'SEO', {})
    return {
        'SEO': seo,
        'SITE_NAME': seo.get('SITE_NAME', 'Edlyn Exavier'),
        'SITE_URL': seo.get('BASE_URL', 'https://edlynexavier.com'),
        'DEFAULT_OG_IMAGE': seo.get('OG_IMAGE', '/static/images/og-image.png'),
    }


def site_settings(request):
    """
    Provide social links and other site-wide objects to every template.
    Uses select_related for performance; cached per request.
    """
    social_links = SocialLink.objects.filter(is_active=True).order_by('order')
    return {
        'global_social_links': social_links,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'DEBUG': settings.DEBUG,
    }
