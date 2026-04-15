# Generated migration for contact app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('subject', models.CharField(max_length=200, verbose_name='subject')),
                ('message', models.TextField(verbose_name='message')),
                ('status', models.CharField(choices=[('new', 'New'), ('read', 'Read'), ('replied', 'Replied'), ('archived', 'Archived')], default='new', max_length=20, verbose_name='status')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='sent at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'Contact Message',
                'verbose_name_plural': 'Contact Messages',
                'ordering': ['-created_at'],
            },
        ),
    ]
