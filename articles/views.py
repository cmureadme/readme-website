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
