"""
portfolio/views.py

Views for projects list and detail, plus skills display.
"""

import json

from django.shortcuts import render, get_object_or_404

from portfolio.models import Project, ProjectTag, SkillCategory


def projects(request):
    """
    All projects, with optional tag filtering.
    """
    tag_slug = request.GET.get('tag')
    all_projects = Project.objects.filter(is_active=True).prefetch_related('tags')

    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(ProjectTag, slug=tag_slug)
        all_projects = all_projects.filter(tags=active_tag)

    all_tags = ProjectTag.objects.filter(projects__is_active=True).distinct()

    context = {
        'page_title': 'Projects — Edlyn Exavier',
        'meta_description': (
            'Portfolio of Edlyn Exavier — web applications, electronics projects, '
            'and technical builds using Python, Django, and more.'
        ),
        'og_type': 'website',
        'canonical_url': '/projects/',
        'projects': all_projects,
        'all_tags': all_tags,
        'active_tag': active_tag,
        # Breadcrumbs
        'breadcrumbs': [
            {'label': 'Projects', 'url': None},
        ],
    }
    return render(request, 'portfolio/projects.html', context)


def project_detail(request, slug):
    """Single project detail page."""
    project = get_object_or_404(Project, slug=slug, is_active=True)

    # Related projects: same tags, exclude current
    related = Project.objects.filter(
        is_active=True,
        tags__in=project.tags.all()
    ).exclude(pk=project.pk).distinct()[:3]

    # Schema.org JSON-LD data
    json_ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": project.title,
        "description": project.meta_description or project.description[:160],
        "author": {
            "@type": "Person",
            "name": "Edlyn Exavier",
            "url": "https://edlynexavier.com"
        },
    }
    if project.github_url:
        json_ld["codeRepository"] = project.github_url
    if project.live_url:
        json_ld["url"] = project.live_url

    context = {
        'page_title': f'{project.title} — Edlyn Exavier',
        'meta_description': project.meta_description or project.description[:155],
        'og_type': 'article',
        'canonical_url': project.get_absolute_url(),
        'og_image': project.cover_image_url,
        'project': project,
        'related_projects': related,
        'json_ld': json.dumps(json_ld, indent=2),
        # Breadcrumbs
        'breadcrumbs': [
            {'label': 'Projects', 'url': '/projects/'},
            {'label': project.title, 'url': None},
        ],
    }
    return render(request, 'portfolio/project_detail.html', context)
