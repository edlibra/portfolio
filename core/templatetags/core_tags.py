"""
core/templatetags/core_tags.py

Custom template filters and tags for the edlynexavier project.
"""

from django import template

register = template.Library()


@register.filter(name='split')
def split_filter(value, delimiter=','):
    """
    Split a string by a delimiter and return a list.

    Usage in templates:
        {% for item in "a,b,c"|split:"," %}
        {% for item in my_string|split %}   {# defaults to comma #}
    """
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]


@register.filter(name='times')
def times_filter(number):
    """Return a range for use in {% for %} loops."""
    try:
        return range(int(number))
    except (TypeError, ValueError):
        return range(0)


@register.filter(name='percentage')
def percentage_filter(value, total):
    """Calculate a percentage."""
    try:
        return round((float(value) / float(total)) * 100, 1)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0


@register.simple_tag(takes_context=True)
def active_url(context, url_name, css_class='active'):
    """
    Return a CSS class if the current URL matches url_name.

    Usage:
        <li class="{% active_url 'core:home' %}">
    """
    request = context.get('request')
    if not request:
        return ''
    try:
        from django.urls import resolve, reverse
        current = resolve(request.path_info)
        namespace = current.namespace
        name = current.url_name
        full_name = f'{namespace}:{name}' if namespace else name
        if full_name == url_name:
            return css_class
    except Exception:
        pass
    return ''
