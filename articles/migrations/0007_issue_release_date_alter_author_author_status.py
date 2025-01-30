# Generated by Django 5.1 on 2025-01-27 05:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0006_alter_article_created_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="release_date",
            field=models.DateField(default=datetime.date(1969, 12, 31)),
        ),
        migrations.AlterField(
            model_name="author",
            name="author_status",
            field=models.CharField(
                choices=[
                    ("US", "Usual Suspect"),
                    ("IC", "Independent Contractor"),
                    ("EE", "Escapee"),
                ],
                default="US",
                help_text="Usual suspect for current writers or recurring characters, independent contractors for one off bits, escapee for alumni",
                max_length=2,
            ),
        ),
    ]
