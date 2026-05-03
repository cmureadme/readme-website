from django import forms
from .models import Author, Article, ArticleImage, ImageGag, PaidFor, RejectedHeadline, Issue, AuthorAdminPermission
from django.core.validators import validate_image_file_extension


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            "name",
            "slug",
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
            "anon_authors",
            "body",
            "slug",
            "issue",
            "published",
            "front_page",
            "featured",
            "created_on",
        )

    def clean(self):
        # In forms stage to have access to the authors many to many relationship
        cleaned_data = super().clean()
        authors = cleaned_data.get("authors")
        anon_authors = cleaned_data.get("anon_authors", 0)

        # Check if at least one author or anonymous author is provided
        if (not authors or authors.count() == 0) and anon_authors <= 0:
            raise forms.ValidationError(
                "Need to include at least one author or set anonymous authors to a number greater than 0."
            )
        if anon_authors < 0:
            raise forms.ValidationError("Can't have negative anonymous authors")
        return cleaned_data

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, show):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = ArticleImage(show=show, image=upload)
            image.save()


class ImageGagAdminForm(forms.ModelForm):
    class Meta:
        model = ImageGag
        fields = (
            "artists",
            "anon_artists",
            "image",
            "alt_text",
            "caption",
            "slug",
            "issue",
            "published",
            "front_page",
            "featured",
            "created_on",
        )

    def clean(self):
        # In forms stage to have access to the artists many to many relationship
        cleaned_data = super().clean()
        artists = cleaned_data.get("artists")
        anon_artists = cleaned_data.get("anon_artists", 0)

        # Check if at least one artist or anonymous artist is provided
        if (not artists or artists.count() == 0) and anon_artists <= 0:
            raise forms.ValidationError(
                "Need to include at least one artist or set anonymous artists to a number greater than 0."
            )
        if anon_artists < 0:
            raise forms.ValidationError("Can't have negative anonymous artists")
        return cleaned_data


class PaidForForm(forms.ModelForm):
    class Meta:
        model = PaidFor
        fields = ("title",)


class RejectedHeadlineForm(forms.ModelForm):
    class Meta:
        model = RejectedHeadline
        fields = ("title", "issue", "featured")


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (
            "short_name",
            "long_name",
            "vol",
            "num",
            "archive",
            "paid_for",
            "free",
            "three_dollars",
            "release_date",
        )

class AuthorAdminPermissionForm(forms.ModelForm):
    class Meta:
        model = AuthorAdminPermission
        fields = ("admin_user", "author_profiles")
