# Generated migration for core app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('github', 'GitHub'), ('linkedin', 'LinkedIn'), ('twitter', 'Twitter / X'), ('instagram', 'Instagram'), ('youtube', 'YouTube'), ('email', 'Email'), ('other', 'Other')], max_length=20, verbose_name='platform')),
                ('label', models.CharField(help_text='Display label, e.g. "GitHub"', max_length=100, verbose_name='label')),
                ('url', models.URLField(help_text='Full URL including https://', verbose_name='URL')),
                ('icon_class', models.CharField(default='bi-link-45deg', help_text='Bootstrap Icons class, e.g. "bi-github"', max_length=60, verbose_name='Bootstrap icon class')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='display order')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Social Link',
                'verbose_name_plural': 'Social Links',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ResumeSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='section title')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='display order')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Resume Section',
                'verbose_name_plural': 'Resume Sections',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ResumeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title / role')),
                ('subtitle', models.CharField(blank=True, max_length=200, verbose_name='institution / company')),
                ('location', models.CharField(blank=True, max_length=200, verbose_name='location')),
                ('date_start', models.CharField(blank=True, help_text='e.g. "Sept 2022"', max_length=50, verbose_name='start date')),
                ('date_end', models.CharField(blank=True, help_text='e.g. "Present"', max_length=50, verbose_name='end date')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='display order')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.resumesection', verbose_name='section')),
            ],
            options={
                'verbose_name': 'Resume Item',
                'verbose_name_plural': 'Resume Items',
                'ordering': ['order'],
            },
        ),
    ]
