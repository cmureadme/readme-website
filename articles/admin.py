from django.contrib import admin

# Register your models here.
from django.contrib import admin
from articles.models import Issue, Author, Article, ArticleImage, SocialMediaLink, PaidFor, RejectedHeadline
from articles.forms import ArticleAdminForm, AuthorAdminForm, RejectedHeadlineForm

class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 0  # how many links will be prompted to be added by default

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    inlines = [SocialMediaLinkInline]
    list_display = ["name", "author_status"]
    search_fields = ["name"]
    list_filter = ["author_status"]

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    model = Issue

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0  # how many images will be prompted to be added by default


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    inlines = [ArticleImageInline]
    list_display = ["slug", "title", "vol_issue", "published", "front_page", "featured"]
    search_fields = ["slug", "title"]
    list_filter = ["issue", "authors"]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

@admin.register(PaidFor)
class PaidForAdmin(admin.ModelAdmin):
    model = PaidFor

@admin.register(RejectedHeadline)
class RejectedHeadlineAdmin(admin.ModelAdmin):
    form = RejectedHeadlineForm
    list_display = ["title", "vol_issue", "featured"]
    search_fields = ["title"]
    list_filter = ["issue"]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"