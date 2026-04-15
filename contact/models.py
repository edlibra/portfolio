"""
contact/models.py

ContactMessage model — stores submitted contact form entries.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    """Stores messages submitted through the contact form."""

    STATUS_CHOICES = [
        ('new', _('New')),
        ('read', _('Read')),
        ('replied', _('Replied')),
        ('archived', _('Archived')),
    ]

    name = models.CharField(_('name'), max_length=150)
    email = models.EmailField(_('email'))
    subject = models.CharField(_('subject'), max_length=200)
    message = models.TextField(_('message'))
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    ip_address = models.GenericIPAddressField(
        _('IP address'),
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(_('sent at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')

    def __str__(self):
        return f'{self.name} — {self.subject} ({self.created_at:%Y-%m-%d})'
