"""
contact/forms.py — Formulaire de contact avec honeypot anti-spam.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from contact.models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulaire de contact public avec protection anti-spam basique (honeypot)."""

    # Honeypot : champ caché — si rempli, c'est un bot
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
        label=''
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your full name'),
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('your@email.com'),
                'autocomplete': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('What is this about?'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': _('Tell me about your project, opportunity, or question…'),
            }),
        }
        labels = {
            'name':    _('Full Name'),
            'email':   _('Email Address'),
            'subject': _('Subject'),
            'message': _('Message'),
        }

    def clean_website(self):
        """Honeypot : rejette la soumission si le champ caché est rempli."""
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError(_('Spam detected.'))
        return value

    def clean_message(self):
        """Vérifie que le message est suffisamment long."""
        message = self.cleaned_data.get('message', '')
        if len(message.strip()) < 20:
            raise forms.ValidationError(
                _('Your message is too short. Please provide more detail (at least 20 characters).')
            )
        return message
