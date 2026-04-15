"""core/sitemaps.py — Static page sitemap entries."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    protocol = 'https'

    # Priority per URL name
    _priorities = {
        'core:home': 1.0,
        'core:about': 0.8,
        'core:skills': 0.7,
        'core:resume': 0.7,
        'contact:contact': 0.6,
    }

    def items(self):
        return ['core:home', 'core:about', 'core:skills', 'core:resume', 'contact:contact']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self._priorities.get(item, 0.5)
