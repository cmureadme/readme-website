# Generated by Django 5.1 on 2025-01-08 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_author_author_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_on',
            field=models.DateTimeField(),
        ),
    ]
