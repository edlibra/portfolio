"""core/admin.py"""

from django.contrib import admin
from core.models import SocialLink, ResumeSection, ResumeItem


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'label', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('platform', 'is_active')
    ordering = ('order',)


class ResumeItemInline(admin.TabularInline):
    model = ResumeItem
    extra = 1
    fields = ('title', 'subtitle', 'location', 'date_start', 'date_end', 'description', 'order', 'is_active')


@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [ResumeItemInline]


@admin.register(ResumeItem)
class ResumeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'section', 'date_start', 'date_end', 'order', 'is_active')
    list_filter = ('section', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('section', 'order')
