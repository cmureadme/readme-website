import os
import uuid

from django import forms
from .models import Author, Article, ArticleImage, ImageGag, PaidFor, RejectedHeadline, Issue, AuthorAdminPermission
from django.core.validators import validate_image_file_extension
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.html import format_html
from django.forms.widgets import ClearableFileInput


temp_storage = FileSystemStorage(location=settings.TEMP_UPLOAD_ROOT)


class StagedFileInput(ClearableFileInput):
    """
    Normally renders like a regular file input. If `staged_filename` is
    set (meaning we've recovered/stashed a file across a failed submit),
    renders a collapsed status line instead, with the real file input
    tucked inside a <details> toggle in case the user wants to swap it.
    """

    staged_filename = None

    def render(self, name, value, attrs=None, renderer=None):
        base_input = super().render(name, value, attrs, renderer)
        if self.staged_filename:
            return format_html(
                "<details>"
                '<summary style="cursor: pointer; color: #2e7d32; font-weight: bold;">'
                '✓ "{}" already uploaded — click to replace</summary>'
                '<div style="margin-top: 8px;">{}</div>'
                "</details>",
                self.staged_filename,
                base_input,
            )
        return base_input


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
            "byline",
            "slug",
            "body",
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
            "title",
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
    # Carries a pointer to a temp copy of the PDF across failed submissions
    archive_temp_path = forms.CharField(widget=forms.HiddenInput(), required=False)

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
        widgets = {
            "archive": StagedFileInput(),
        }

    def _clean_fields(self):
        super()._clean_fields()

        uploaded = self.files.get("archive")
        temp_path = self.cleaned_data.get("archive_temp_path")
        recovered = False

        if uploaded:
            # New file chosen this round -> stash a copy in case something
            # else on the form fails validation.
            temp_path = self._stash_temp_file(uploaded)
            self.data = self.data.copy()
            self.data["archive_temp_path"] = temp_path
            self.cleaned_data["archive_temp_path"] = temp_path
            recovered = True

        elif temp_path and not self.cleaned_data.get("archive"):
            # No new file, but we have one stashed from a previous failed
            # attempt -> reuse it and clear the "required" error.
            if temp_storage.exists(temp_path):
                with temp_storage.open(temp_path, "rb") as f:
                    content = f.read()
                filename = os.path.basename(temp_path).split("__", 1)[-1]
                self.cleaned_data["archive"] = ContentFile(content, name=filename)
                self._errors.pop("archive", None)
                recovered = True
            else:
                temp_path = None
                self.add_error(
                    None,
                    "Your previously uploaded PDF could not be recovered — please upload it again.",
                )

        if recovered and temp_path:
            filename = os.path.basename(temp_path).split("__", 1)[-1]
            self.fields["archive"].widget.staged_filename = filename

    def _stash_temp_file(self, uploaded_file):
        key = f"{uuid.uuid4().hex}__{uploaded_file.name}"
        return temp_storage.save(key, uploaded_file)

    def save(self, commit=True):
        instance = super().save(commit=False)
        temp_path = self.cleaned_data.get("archive_temp_path")
        if commit:
            instance.save()
            self.save_m2m()
        if temp_path and temp_storage.exists(temp_path):
            temp_storage.delete(temp_path)
        return instance


class AuthorAdminPermissionForm(forms.ModelForm):
    class Meta:
        model = AuthorAdminPermission
        fields = ("admin_user", "author_profiles")
