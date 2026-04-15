"""
portfolio/models.py

Models for projects and skills.
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# ─────────────────────────────────────────────────────────────────────────────
# SKILLS
# ─────────────────────────────────────────────────────────────────────────────

class SkillCategory(models.Model):
    """Groups skills into categories: Frontend, Backend, Tools, etc."""

    name = models.CharField(_('name'), max_length=100)
    icon_class = models.CharField(
        _('Bootstrap icon class'),
        max_length=60,
        default='bi-cpu',
        help_text=_('e.g. "bi-code-slash"')
    )
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('Skill Category')
        verbose_name_plural = _('Skill Categories')

    def __str__(self):
        return self.name


class Skill(models.Model):
    """An individual skill within a category."""

    LEVEL_CHOICES = [
        (1, _('Beginner')),
        (2, _('Elementary')),
        (3, _('Intermediate')),
        (4, _('Advanced')),
        (5, _('Expert')),
    ]

    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name=_('category')
    )
    name = models.CharField(_('name'), max_length=100)
    level = models.PositiveSmallIntegerField(
        _('proficiency level'),
        choices=LEVEL_CHOICES,
        default=3
    )
    level_percent = models.PositiveSmallIntegerField(
        _('level (%)'),
        default=70,
        help_text=_('Value 0–100 used for progress bars.')
    )
    icon_class = models.CharField(_('icon class'), max_length=60, blank=True)
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')

    def __str__(self):
        return f'{self.name} ({self.category})'


# ─────────────────────────────────────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────────────────────────────────────

class ProjectTag(models.Model):
    """Technology / topic tags for projects."""

    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Project Tag')
        verbose_name_plural = _('Project Tags')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    """A portfolio project entry."""

    STATUS_CHOICES = [
        ('completed', _('Completed')),
        ('in_progress', _('In Progress')),
        ('archived', _('Archived')),
    ]

    # Core fields
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=220, unique=True, blank=True)
    tagline = models.CharField(
        _('tagline'),
        max_length=300,
        blank=True,
        help_text=_('Short one-liner shown on project cards.')
    )
    description = models.TextField(_('description'))
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed'
    )

    # Media
    cover_image = models.ImageField(
        _('cover image'),
        upload_to='projects/',
        blank=True,
        null=True,
        help_text=_('Recommended: 1200×630px')
    )

    # Links
    github_url = models.URLField(_('GitHub URL'), blank=True)
    live_url = models.URLField(_('Live URL'), blank=True)

    # Relations
    tags = models.ManyToManyField(
        ProjectTag,
        blank=True,
        related_name='projects',
        verbose_name=_('tags')
    )

    # Meta
    is_featured = models.BooleanField(
        _('featured'),
        default=False,
        help_text=_('Show on homepage featured section.')
    )
    is_active = models.BooleanField(_('active'), default=True)
    order = models.PositiveSmallIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # SEO
    meta_description = models.CharField(
        _('meta description'),
        max_length=160,
        blank=True,
        help_text=_('SEO meta description (max 160 chars). Auto-generated if empty.')
    )

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_description and self.description:
            # Auto-generate meta description from the first 157 chars of description
            self.meta_description = self.description[:157].rsplit(' ', 1)[0] + '…'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    @property
    def cover_image_url(self):
        """Return cover image URL or a placeholder path."""
        if self.cover_image:
            return self.cover_image.url
        return '/static/images/project-placeholder.png'
