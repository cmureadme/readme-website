from django import forms
from .models import Author, Article, ArticleImage, PaidFor, RejectedHeadline, Issue
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            "name",
            "img",
            "bio",
            "roles",
            "pronouns",
            "major",
            "year",
            "location",
            "fact",
            "email",
            "author_status",
        )


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "authors",
            "body",
            "slug",
            "issue",
            "published",
            "front_page",
            "featured",
            "created_on"
        )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, show):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = ArticleImage(show=show, image=upload)
            image.save()

class PaidForForm(forms.ModelForm):
    class Meta:
        model = PaidFor
        fields = (
            "title",
        )

class RejectedHeadlineForm(forms.ModelForm):
    class Meta:
        model = RejectedHeadline
        fields = (
            "title",
            "issue",
            "featured"
        )