"""portfolio/admin.py"""

from django.contrib import admin
from portfolio.models import Project, ProjectTag, SkillCategory, Skill


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('name', 'level', 'level_percent', 'icon_class', 'order', 'is_active')


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'level_percent', 'order', 'is_active')
    list_filter = ('category', 'level', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'is_featured', 'is_active', 'order', 'created_at')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter = ('status', 'is_featured', 'is_active', 'tags')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'tagline', 'description', 'cover_image', 'status')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Classification', {
            'fields': ('tags', 'is_featured', 'is_active', 'order')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
