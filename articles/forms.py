# blog/forms.py

from django import forms
from .models import Author, Category, Article, ArticleImage
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )


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
            "categories",
            "slug",
            "issue",
            "published",
            "created_on",
        )
    # photos = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    #     label=gettext("Add photos"),
    #     required=False,
    # )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, show):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = ArticleImage(show=show, image=upload)
            image.save()

