# Generated migration for portfolio app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('icon_class', models.CharField(default='bi-cpu', help_text='e.g. "bi-code-slash"', max_length=60, verbose_name='Bootstrap icon class')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='display order')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Skill Category',
                'verbose_name_plural': 'Skill Categories',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('level', models.PositiveSmallIntegerField(choices=[(1, 'Beginner'), (2, 'Elementary'), (3, 'Intermediate'), (4, 'Advanced'), (5, 'Expert')], default=3, verbose_name='proficiency level')),
                ('level_percent', models.PositiveSmallIntegerField(default=70, help_text='Value 0–100 used for progress bars.', verbose_name='level (%)')),
                ('icon_class', models.CharField(blank=True, max_length=60, verbose_name='icon class')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='display order')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='portfolio.skillcategory', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ProjectTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Project Tag',
                'verbose_name_plural': 'Project Tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True, verbose_name='slug')),
                ('tagline', models.CharField(blank=True, help_text='Short one-liner shown on project cards.', max_length=300, verbose_name='tagline')),
                ('description', models.TextField(verbose_name='description')),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('in_progress', 'In Progress'), ('archived', 'Archived')], default='completed', max_length=20, verbose_name='status')),
                ('cover_image', models.ImageField(blank=True, help_text='Recommended: 1200×630px', null=True, upload_to='projects/', verbose_name='cover image')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub URL')),
                ('live_url', models.URLField(blank=True, verbose_name='Live URL')),
                ('is_featured', models.BooleanField(default=False, help_text='Show on homepage featured section.', verbose_name='featured')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='display order')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('meta_description', models.CharField(blank=True, help_text='SEO meta description (max 160 chars). Auto-generated if empty.', max_length=160, verbose_name='meta description')),
                ('tags', models.ManyToManyField(blank=True, related_name='projects', to='portfolio.projecttag', verbose_name='tags')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
