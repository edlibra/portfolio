"""
contact/views.py — Affichage et traitement du formulaire de contact.
"""

import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from contact.forms import ContactForm
from contact.models import ContactMessage

logger = logging.getLogger(__name__)


def contact(request):
    """
    Affiche et traite le formulaire de contact.
    GET  → affiche le formulaire vide.
    POST → valide → enregistre → email → redirection avec message de succès.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = _get_client_ip(request)
            msg.save()

            _send_notification_email(msg)

            messages.success(
                request,
                _('Thank you for reaching out! I received your message and will get back to you as soon as possible.')
            )
            return redirect('contact:contact')

        else:
            messages.error(
                request,
                _('There was an issue with your submission. Please check the form below.')
            )
    else:
        form = ContactForm()

    context = {
        'page_title': 'Contact — Edlyn Exavier',
        'meta_description': (
            'Contactez Edlyn Exavier. Disponible pour des stages, '
            'du freelance et des collaborations techniques.'
        ),
        'og_type': 'website',
        'canonical_url': '/contact/',
        'form': form,
    }
    return render(request, 'contact/contact.html', context)


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _send_notification_email(msg: ContactMessage):
    subject = f'[edlynexavier.com] Nouveau message de {msg.name} : {msg.subject}'
    body = (
        f'Nom : {msg.name}\n'
        f'Email : {msg.email}\n'
        f'Sujet : {msg.subject}\n\n'
        f'Message :\n{msg.message}\n\n'
        f'---\nIP : {msg.ip_address}'
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
    except BadHeaderError:
        logger.warning('BadHeaderError lors de l\'envoi du courriel de contact.')
    except Exception as e:
        logger.error('Échec d\'envoi du courriel de contact : %s', e)
