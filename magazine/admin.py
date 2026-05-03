from django.contrib import admin
from magazine.models import (
    Issue,
    Author,
    Article,
    ArticleImage,
    ImageGag,
    PaidFor,
    RejectedHeadline,
    AuthorAdminPermission
)
from magazine.forms import (
    ArticleAdminForm,
    AuthorAdminForm,
    ImageGagAdminForm,
    RejectedHeadlineForm,
    PaidForForm,
    IssueForm,
    AuthorAdminPermissionForm
)

from django.db.models import Q, QuerySet

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
        except:
            return qs.none()

    # These two functions stop url tampering

    # Will only let you edit authors you have perms to
    def has_change_permissions(self, request, obj=None):
        if request.user.is_superuser:
            return True

        try:
            return obj in request.user.authoradminpermission.author_profiles.all()
        except:
            return False
    
    def has_view_permissions(self, request, obj=None):
        if request.user.is_superuser:
            return True

        try:
            return obj in request.user.authoradminpermission.author_profiles.all()
        except:
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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    form = ArticleAdminForm
    inlines = [ArticleImageInline]
    list_display = ["slug", "title", "vol_issue", "published", "front_page", "featured"]
    list_editable = ["published", "front_page", "featured"]
    search_fields = ["slug", "title"]
    list_filter = ["issue", "authors"]
    actions = [make_published, un_publish, make_featured, un_feature, make_front_page, un_front_page]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"


@admin.register(ImageGag)
class ImageGagAdmin(admin.ModelAdmin):
    model = ImageGag
    form = ImageGagAdminForm
    list_display = ["slug", "vol_issue", "published", "front_page", "featured"]
    list_editable = ["published", "front_page", "featured"]
    search_fields = ["slug"]
    list_filter = ["issue", "artists"]
    actions = [make_published, un_publish, make_featured, un_feature, make_front_page, un_front_page]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"


@admin.register(PaidFor)
class PaidForAdmin(admin.ModelAdmin):
    model = PaidFor
    form = PaidForForm
    search_fields = ["title"]


@admin.register(RejectedHeadline)
class RejectedHeadlineAdmin(admin.ModelAdmin):
    model = RejectedHeadline
    form = RejectedHeadlineForm
    list_display = ["title", "vol_issue", "featured"]
    list_editable = ["featured"]
    search_fields = ["title"]
    list_filter = ["issue"]
    actions = [make_featured, un_feature]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

@admin.register(AuthorAdminPermission)
class AuthorAdminPermissionAdmin(admin.ModelAdmin):
    model = AuthorAdminPermission
    form = AuthorAdminPermissionForm
