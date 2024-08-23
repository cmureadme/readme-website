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
)
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def index(request):
    articles = Article.objects.all().order_by("-created_on").filter(published=True)
    context = {
        "articles": articles,
    }
    return render(request, "articles/index.html", context)


def article_author_index(request):
    authors = Author.objects.all()
    context = {
        "authors": authors,
    }
    return render(request, "articles/authorlist.html", context)


def article_author(request, author):
    author = Author.objects.get(pk=author)
    articles = (
        Article.objects.filter(authors__pk=author)
        .order_by("-created_on")
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
    return render(request, "articles/categorylist.html", context)


def article_category(request, category):
    articles = (
        Article.objects.filter(categories__name__contains=category)
        .order_by("-created_on")
        .filter(published=True)
    )
    context = {
        "category": category,
        "articles": articles,
    }
    return render(request, "articles/category.html", context)


def article_issues_index(request):
    issues = Issue.objects.all().order_by("vol")
    issues_by_volume = {}

    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)
    issue = issues
    return render(
        request,
        "articles/issuelist.html",
        {"issues": issue, "issues_by_volume": issues_by_volume},
    )


def article_issue(request, vol, num):
    issue = Issue.objects.get(num=num, vol=vol)
    articles = Article.objects.filter(issues__name__contains=issue.name).order_by(
        "-created_on"
    )

    context = {
        "i": issue,
        "issue": issue.name,
        "articles": articles,
    }
    return render(request, "articles/issue.html", context)


# TODO REMEMBER TO CHANGE POST TO ARTICLE
def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
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
