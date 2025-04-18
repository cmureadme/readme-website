from django.contrib import admin

# Register your models here.
from django.contrib import admin
from articles.models import Issue, Author, Category, Comment, Article, ArticleImage, SocialMediaLink, IndexPage, PaidFor, RejectedHeadline
# from articles.models import Show, ShowPhoto
from articles.forms import ArticleAdminForm, AuthorAdminForm, RejectedHeadlineForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass 

class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 0  # how many images will be prompted to be added by default

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    inlines = [SocialMediaLinkInline]

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    pass

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0  # how many images will be prompted to be added by default


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    inlines = [ArticleImageInline]
    list_display = ["slug", "title", "vol_issue", "published", "front_page", "featured"]
    search_fields = ["slug", "title"]
    list_filter = ["categories", "issue__vol", "issue__num", "published", "front_page", "featured"]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

@admin.register(IndexPage)
class IndexPageAdmin(admin.ModelAdmin):
    pass

@admin.register(PaidFor)
class PaidForAdmin(admin.ModelAdmin):
    pass

@admin.register(RejectedHeadline)
class RejectedHeadlineAdmin(admin.ModelAdmin):
    form = RejectedHeadlineForm
    list_display = ["title", "vol_issue"]
    search_fields = ["title"]
    list_filter = ["issue__vol", "issue__num"]

    @admin.display(description="Vol, Issue")
    def vol_issue(self, obj):
        return f"{obj.issue.vol}.{obj.issue.num}"

# @admin.register(Show)
# class ShowAdmin(admin.ModelAdmin):

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         form.save_photos(form.instance)

