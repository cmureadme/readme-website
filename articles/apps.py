"""
this is just here so settings.py is able to discover this app (articles) via INSTALLED_APPS
"""

from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"
