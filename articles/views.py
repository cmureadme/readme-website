from django.shortcuts import render

from django.http import HttpResponseRedirect
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
    articles = (
        Article.objects.filter(authors__name__contains=author)
        .order_by("-created_on")
        .filter(published=True)
    )
    aut = Author.objects.filter(name__contains=author).first()
    context = {
        "a": aut,
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
    posts = (
        Article.objects.filter(categories__name__contains=category)
        .order_by("-created_on")
        .filter(published=True)
    )
    context = {
        "category": category,
        "posts": posts,
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
    posts = Article.objects.filter(issues__name__contains=issue.name).order_by(
        "-created_on"
    )

    context = {
        "i": issue,
        "issue": issue.name,
        "posts": posts,
    }
    return render(request, "articles/issue.html", context)