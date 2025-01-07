# Generated by Django 5.1 on 2025-01-07 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0004_indexpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="author_status",
            field=models.CharField(
                choices=[
                    ("US", "Usual Suspect"),
                    ("IC", "Independant Contractor"),
                    ("EE", "Escapee"),
                ],
                default="US",
                max_length=2,
            ),
        ),
    ]
