"""
core/models.py

Site-wide models: social links, site settings, resume items.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class SocialLink(models.Model):
    """Social media / professional network links displayed in the footer and contact page."""

    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('email', 'Email'),
        ('other', 'Other'),
    ]

    platform = models.CharField(_('platform'), max_length=20, choices=PLATFORM_CHOICES)
    label = models.CharField(_('label'), max_length=100, help_text=_('Display label, e.g. "GitHub"'))
    url = models.URLField(_('URL'), help_text=_('Full URL including https://'))
    icon_class = models.CharField(
        _('Bootstrap icon class'),
        max_length=60,
        default='bi-link-45deg',
        help_text=_('Bootstrap Icons class, e.g. "bi-github"')
    )
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')

    def __str__(self):
        return f'{self.get_platform_display()} — {self.label}'


class ResumeSection(models.Model):
    """A section in the resume (Education, Experience, Certifications…)."""

    title = models.CharField(_('section title'), max_length=100)
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('Resume Section')
        verbose_name_plural = _('Resume Sections')

    def __str__(self):
        return self.title


class ResumeItem(models.Model):
    """An individual entry inside a resume section."""

    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('section')
    )
    title = models.CharField(_('title / role'), max_length=200)
    subtitle = models.CharField(
        _('institution / company'),
        max_length=200,
        blank=True
    )
    location = models.CharField(_('location'), max_length=200, blank=True)
    date_start = models.CharField(_('start date'), max_length=50, blank=True, help_text=_('e.g. "Sept 2022"'))
    date_end = models.CharField(_('end date'), max_length=50, blank=True, help_text=_('e.g. "Present"'))
    description = models.TextField(_('description'), blank=True)
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('Resume Item')
        verbose_name_plural = _('Resume Items')

    def __str__(self):
        return f'{self.title} @ {self.subtitle}'

    @property
    def date_range(self):
        if self.date_start and self.date_end:
            return f'{self.date_start} – {self.date_end}'
        return self.date_start or self.date_end or ''
