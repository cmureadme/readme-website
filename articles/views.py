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


def article_category_index(request):
    categories = Category.objects.all().order_by("name")
    context = {
        "categories": categories,
    }
    return render(request, "articles/categorylist.html", context)


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