from django.db import migrations
from django.apps.registry import Apps
import re


def imgswitch_to_markdown(apps: Apps, schema_editor):
    Article = apps.get_model("magazine", "Article")

    for obj in Article.objects.all():
        obj.body = re.sub(r"\{\{([^}]*)\}\}", lambda x: f"![]({x.group(1)})", obj.body)

        obj.save()


def markdown_to_imgswitch(apps: Apps, schema_editor):
    Article = apps.get_model("magazine", "Article")

    for obj in Article.objects.all():
        obj.body = re.sub(r"!\[\]\(([^\)]*)\)", lambda x: f"{{{{{x.group(1)}}}}}", obj.body)

        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("magazine", "0005_article_anon_authors_alter_article_authors"),
    ]

    operations = [
        migrations.RunPython(code=imgswitch_to_markdown, reverse_code=markdown_to_imgswitch),
    ]
