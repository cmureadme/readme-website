# Generated by Django 5.1 on 2025-01-27 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_rename_issues_article_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='release_date',
            field=models.DateField(default=datetime.date.fromtimestamp(0)),
        ),
    ]