from django.db import models
from django.contrib import admin
from magazine.models import (
    Issue,
    Author,
    Article,
    ArticleImage,
    ImageGag,
    PaidFor,
    RejectedHeadline,
    AuthorAdminPermission,
)
from magazine.forms import (
    ArticleAdminForm,
    AuthorAdminForm,
    ImageGagAdminForm,
    RejectedHeadlineForm,
    PaidForForm,
    IssueForm,
    AuthorAdminPermissionForm,
)
from markdownx.widgets import AdminMarkdownxWidget


@admin.action(description="Make piece(s) published")
def make_published(modelAdmin, request, queryset):
    queryset.update(published=True)


@admin.action(description="Make piece(s) not published")
def un_publish(modelAdmin, request, queryset):
    queryset.update(published=False)


@admin.action(description="Make piece(s) featured")
def make_featured(modelAdmin, request, queryset):
    queryset.update(featured=True)


@admin.action(description="Make piece(s) not featured")
def un_feature(modelAdmin, request, queryset):
    queryset.update(featured=False)


@admin.action(description="Make piece(s) front page")
def make_front_page(modelAdmin, request, queryset):
    queryset.update(front_page=True)


@admin.action(description="Make piece(s) not front page")
def un_front_page(modelAdmin, request, queryset):
    queryset.update(front_page=False)


@admin.action(description="Make author(s) usual suspect")
def make_us(modelAdmin, request, queryset):
    queryset.update(author_status="US")


@admin.action(description="Make author(s) independent contractor")
def make_ic(modelAdmin, request, queryset):
    queryset.update(author_status="IC")


@admin.action(description="Make author(s) escapee")
def make_ee(modelAdmin, request, queryset):
    queryset.update(author_status="EE")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    form = AuthorAdminForm
    list_display = ["name", "author_status"]
    search_fields = ["name"]
    list_filter = ["author_status"]
    actions = [make_us, make_ic, make_ee]

    # Will only show authors you're allowed to edit
    # This is for the overall list of objects, but doesn't stop URL tampering
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            allowed = request.user.authoradminpermission.author_profiles.all()
            return qs.filter(pk__in=allowed)
        except request.user.authoradminpermissions.RelatedObjectDoesNotExist:
            return qs.none()

    # These two functions stop url tampering

    # Will only let you edit authors you have perms to
    def has_change_permissions(self, request, obj=None):
        if request.user.is_superuser:
            return True

        try:
            return obj in request.user.authoradminpermission.author_profiles.all()
        except request.user.authoradminpermissions.RelatedObjectDoesNotExist:
            return False

    def has_view_permissions(self, request, obj=None):
        if request.user.is_superuser:
            return True

        try:
            return obj in request.user.authoradminpermission.author_profiles.all()
        except request.user.authoradminpermissions.RelatedObjectDoesNotExist:
            return False

    # Explicitly prevents non superusers from deleting authors
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    model = Issue
    form = IssueForm
    list_display = ["short_name", "long_name", "vol_issue"]
    search_fields = ["short_name", "long_name"]
    list_filter = ["vol"]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.vol}.{obj.num}"


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0  # how many images will be prompted to be added by default


class IssueListFilter(admin.SimpleListFilter):
    template = "../templates/admin/scrollable_filter.html"
    title = "issue"
    parameter_name = "issue"

    def get_title(self):
        return "issue"

    def get_choices(self, request):
        return Issue.objects.all()

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(issue_id=self.value())

    def lookups(self, request, model_admin):
        return [(iss.id, f"{iss.fold()} {iss.short_name}") for iss in Issue.objects.all()]


class PaidForIssueListFilter(IssueListFilter):
    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(id__exact=self.value())

    def lookups(self, request, model_admin):
        return [(iss.paid_for_id, f"{iss.fold()} {iss.short_name}") for iss in Issue.objects.all()]


class AuthorListFilter(admin.SimpleListFilter):
    template = "../templates/admin/scrollable_filter.html"
    title = "author"
    parameter_name = "author"

    def get_title(self):
        return "author"

    def get_choices(self, request):
        return Author.objects.all()

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter()
        return queryset.filter(authors__id__exact=self.value())

    def lookups(self, request, model_admin):
        return [(au.id, str(au)) for au in Author.objects.all()]


class ArtistListFilter(AuthorListFilter):
    template = "../templates/admin/scrollable_filter.html"
    title = "artist"
    parameter_name = "artist"

    def get_title(self):
        return "artist"

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter()
        return queryset.filter(artists__id__exact=self.value())


class AltTextExistenceFilter(admin.SimpleListFilter):
    title = "alt text existence"
    parameter_name = "alt text existence"

    def get_title(self):
        return "alt text existence"

    def get_choices(self, request):
        return ["Yes", "No"]

    def lookups(self, request, model_admin):
        return [(1, "Images with alt text"), (0, "Images without alt text")]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter()
        if self.value() == 1:
            return queryset.exclude(alt_text__iexact="")
        if self.value() == 0:
            return queryset.filter(alt_text__iexact="")


class ArticleImageAltTextExistenceFilter(AltTextExistenceFilter):
    def lookups(self, request, model_admin):
        return [(1, "All images with alt text"), (0, "Images without alt text")]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter()
        queryset = queryset.exclude(images__exact=None)
        print(self.value())
        if self.value() == 1:
            return queryset.exclude(images__alt_text__iexact="")
        if self.value() == 0:
            return queryset.filter(images__alt_text__iexact="")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    form = ArticleAdminForm
    inlines = [ArticleImageInline]
    list_display = ["slug", "title", "vol_issue", "published", "front_page", "featured"]
    list_editable = ["published", "front_page", "featured"]
    search_fields = ["slug", "title"]
    list_filter = [IssueListFilter, AuthorListFilter, ArticleImageAltTextExistenceFilter]
    actions = [make_published, un_publish, make_featured, un_feature, make_front_page, un_front_page]
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

    # Custom ordering of drop down menus
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "issue":
            kwargs["queryset"] = Issue.objects.order_by("-vol", "-num", "short_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.related_model == Author:
            kwargs["queryset"] = Author.objects.ordered_by_status()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(ImageGag)
class ImageGagAdmin(admin.ModelAdmin):
    model = ImageGag
    form = ImageGagAdminForm
    list_display = ["slug", "title", "vol_issue", "published", "front_page", "featured", "has_alt_text"]
    list_editable = ["published", "front_page", "featured"]
    search_fields = ["title", "slug"]
    list_filter = [IssueListFilter, ArtistListFilter, AltTextExistenceFilter]
    actions = [make_published, un_publish, make_featured, un_feature, make_front_page, un_front_page]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

    @admin.display(description="Has alt text")
    def has_alt_text(self, obj):
        return obj.alt_text != ""

    # Custom ordering of drop down menus
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "issue":
            kwargs["queryset"] = Issue.objects.order_by("-vol", "-num", "short_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.related_model == Author:
            kwargs["queryset"] = Author.objects.ordered_by_status()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(PaidFor)
class PaidForAdmin(admin.ModelAdmin):
    model = PaidFor
    form = PaidForForm
    search_fields = ["title"]
    list_filter = [PaidForIssueListFilter]


@admin.register(RejectedHeadline)
class RejectedHeadlineAdmin(admin.ModelAdmin):
    model = RejectedHeadline
    form = RejectedHeadlineForm
    list_display = ["title", "vol_issue", "featured"]
    list_editable = ["featured"]
    search_fields = ["title"]
    list_filter = [IssueListFilter]
    actions = [make_featured, un_feature]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

    # Custom ordering of drop down menus
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "issue":
            kwargs["queryset"] = Issue.objects.order_by("-vol", "-num", "short_name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AuthorAdminPermission)
class AuthorAdminPermissionAdmin(admin.ModelAdmin):
    model = AuthorAdminPermission
    form = AuthorAdminPermissionForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.related_model == Author:
            kwargs["queryset"] = Author.objects.ordered_by_status()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
