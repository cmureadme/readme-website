# Generated by Django 5.1 on 2025-04-16 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_alter_rejectedheadline_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['issue__vol', 'issue__num', '-front_page', '-featured', 'slug']},
        ),
    ]
