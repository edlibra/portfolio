"""
core/views.py — Vues des pages principales : accueil, à propos, compétences, CV.
"""

from django.shortcuts import render

from core.models import SocialLink, ResumeSection
from portfolio.models import Project, SkillCategory


def home(request):
    """Page d'accueil."""
    featured_projects = Project.objects.filter(
        is_active=True, is_featured=True
    ).order_by('-created_at')[:3]

    skill_categories = SkillCategory.objects.filter(
        is_active=True
    ).prefetch_related('skills').order_by('order')[:4]

    context = {
        'page_title': 'Edlyn Exavier — Développeur & Bâtisseur Tech',
        'meta_description': (
            'Edlyn Exavier — étudiant en technologie du génie électronique, '
            'développeur web et bâtisseur tech basé au Canada. '
            'Découvrez mes projets, compétences et parcours.'
        ),
        'og_type': 'website',
        'canonical_url': '/',
        'featured_projects': featured_projects,
        'skill_categories': skill_categories,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """Page à propos."""
    context = {
        'page_title': 'À propos — Edlyn Exavier',
        'meta_description': (
            'Découvrez le parcours d\'Edlyn Exavier : étudiant en génie électronique, '
            'développeur web et passionné de technologie basé au Canada.'
        ),
        'og_type': 'profile',
        'canonical_url': '/about/',
    }
    return render(request, 'core/about.html', context)


def skills(request):
    """Page compétences."""
    skill_categories = SkillCategory.objects.filter(
        is_active=True
    ).prefetch_related('skills').order_by('order')

    context = {
        'page_title': 'Compétences — Edlyn Exavier',
        'meta_description': (
            'Compétences techniques d\'Edlyn Exavier : Python, Django, '
            'développement web, électronique, support IT et plus.'
        ),
        'og_type': 'website',
        'canonical_url': '/skills/',
        'skill_categories': skill_categories,
    }
    return render(request, 'core/skills.html', context)


def resume(request):
    """Page CV."""
    resume_sections = ResumeSection.objects.filter(
        is_active=True
    ).prefetch_related('items').order_by('order')

    context = {
        'page_title': 'CV — Edlyn Exavier',
        'meta_description': (
            'CV professionnel d\'Edlyn Exavier : formation, expérience, '
            'certifications et compétences techniques.'
        ),
        'og_type': 'website',
        'canonical_url': '/resume/',
        'resume_sections': resume_sections,
    }
    return render(request, 'core/resume.html', context)


def error_404(request, exception):
    context = {
        'page_title': '404 — Page introuvable | Edlyn Exavier',
        'meta_description': 'La page que vous cherchez n\'existe pas.',
    }
    return render(request, 'errors/404.html', context, status=404)


def error_500(request):
    context = {
        'page_title': '500 — Erreur serveur | Edlyn Exavier',
        'meta_description': 'Une erreur interne s\'est produite.',
    }
    return render(request, 'errors/500.html', context, status=500)
