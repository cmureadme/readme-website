from django.contrib import admin

# Register your models here.
from django.contrib import admin
from articles.models import Issue, Author, Category, Comment, Article, ArticleImage, SocialMediaLink, IndexPage, PaidFor
# from articles.models import Show, ShowPhoto
from articles.forms import ArticleAdminForm, AuthorAdminForm

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

@admin.register(IndexPage)
class IndexPageAdmin(admin.ModelAdmin):
    pass

@admin.register(PaidFor)
class PaidForAdmin(admin.ModelAdmin):
    pass

# @admin.register(Show)
# class ShowAdmin(admin.ModelAdmin):

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         form.save_photos(form.instance)

