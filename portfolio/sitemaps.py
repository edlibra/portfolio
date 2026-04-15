"""portfolio/sitemaps.py"""

from django.contrib.sitemaps import Sitemap
from portfolio.models import Project


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
