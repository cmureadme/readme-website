from django.contrib import admin
from magazine.models import (
    Issue,
    Author,
    Article,
    ArticleImage,
    ImageGag,
    PaidFor,
    RejectedHeadline,
)
from magazine.forms import (
    ArticleAdminForm,
    AuthorAdminForm,
    ImageGagAdminForm,
    RejectedHeadlineForm,
    PaidForForm,
    IssueForm,
)


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


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    form = AuthorAdminForm
    list_display = ["name", "author_status"]
    search_fields = ["name"]
    list_filter = ["author_status"]


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

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"
