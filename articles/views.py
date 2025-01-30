from django.shortcuts import render

from django.http import HttpResponseRedirect
import markdown
from articles.forms import (
    CommentForm,
)
from articles.models import (
    Article,
    Comment,
    Author,
    Issue,
    Category,
    IndexPage,
    PaidFor,
)
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.conf import settings

def index(request):
    rand_articles = Article.objects.all().filter(published=True).order_by("?")[0:5]
    feat_articles = IndexPage.objects.all()[0]
    context = {
        "rand_articles": rand_articles,
        "feat_articles": feat_articles,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "articles/index.html", context)


def article_author_index(request):
    context = {
        "usual_suspects": Author.objects.filter(author_status="US"),
        "independent_contractors": Author.objects.filter(author_status="IC"),
        "escapees": Author.objects.filter(author_status="EE"),
    }
    return render(request, "articles/author_list.html", context)


def article_author(request, author):
    author = Author.objects.get(pk=author)
    articles = (
        Article.objects.filter(authors__pk=author)
        .order_by("-true_created_on")
        .filter(published=True)
    )
    context = {
        "author": author,
        "articles": articles,
    }
    return render(request, "articles/author.html", context)


def article_category_index(request):
    categories = Category.objects.all().order_by("name")
    context = {
        "categories": categories,
    }
    return render(request, "articles/category_list.html", context)


def article_category(request, category):
    articles = (
        Article.objects.filter(categories__name__contains=category)
        .order_by("-true_created_on")
        .filter(published=True)
    )
    context = {
        "category": category,
        "articles": articles,
    }
    return render(request, "articles/category.html", context)


def article_issues_index(request):
    issues = Issue.objects.all().order_by("vol", "num")
    issues_by_volume = {}

    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)
    return render(
        request,
        "articles/issue_list.html",
        {"issues": issues, "issues_by_volume": issues_by_volume},
    )


def article_issue(request, vol, num):
    issue = Issue.objects.get(num=num, vol=vol)
    articles = Article.objects.filter(issue__name__contains=issue.name).order_by(
        "-true_created_on"
    )

    context = {
        "i": issue,
        "issue": issue.name,
        "articles": articles,
    }
    return render(request, "articles/issue.html", context)


# TODO REMEMBER TO CHANGE POST TO ARTICLE
def article_detail(request, slug):
    article = Article.objects.get(pk=slug)
    # comments = Comment.objects.filter(post=post)
    # form = CommentForm()

    # NOTE avoid double mding?
    # md = markdown.Markdown(extensions=["fenced_code"])
    # content = md.convert(article.body)

    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = Comment(
    #             author=form.cleaned_data["author"],
    #             body=form.cleaned_data["body"],
    #             post=post,
    #         )
    #         comment.save()
    #         return HttpResponseRedirect(request.path_info)

    context = {
        "article": article,
        # "comments": comments,
        # "form": CommentForm(),
    }

    return render(request, "articles/article_page.html", context)

def about_us(request):
    return render(request, "articles/about_us.html")

def base(request):
    rand_paid_for = PaidFor.objects.all().order_by("?")[0]
    context = {"rand_paid_for": rand_paid_for}
    return render(request, context)