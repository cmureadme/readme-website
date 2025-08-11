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
    RejectedHeadline
)
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.db.models import Q

def index(request):
    latest_issue = Issue.objects.all().order_by("-vol", "-num")[0]
    second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[1]
    sidebar_articles = Article.objects.all().filter(Q(published=True) & (Q(issue__name__contains=latest_issue.name) | Q(issue__name__contains=second_latest_issue.name))).order_by("?")[0:5]
    secondary_articles = Article.objects.all().filter(Q(published=True)).order_by("?")
    secondary_articles_one = secondary_articles[0:3]
    secondary_articles_two = secondary_articles[3:6]

    all_rand_rej_heads = RejectedHeadline.objects.all().order_by("?")
    
    feat_articles = {
        "largest": Article.objects.all().filter(Q(published=True) & Q(front_page=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=False)).order_by("?")[0],
        "column": Article.objects.all().filter(Q(published=True) & (Q(front_page=True) | Q(featured=True)) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=True)).order_by("?")[0],
        "article": Article.objects.all().filter(Q(published=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=True)).order_by("?")[0],
        "image": Article.objects.all().filter(Q(published=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=False)).order_by("?")[0],
    }
    
    context = {
        "sidebar_articles": sidebar_articles,
        "secondary_articles_one": secondary_articles_one,
        "secondary_articles_two": secondary_articles_two,
        "feat_articles": feat_articles,
        "MEDIA_URL": settings.MEDIA_URL,
        "rej_heads": (all_rand_rej_heads if len(all_rand_rej_heads) < 20 else all_rand_rej_heads[:20])
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
        "-front_page",
        "-featured",
        "-true_created_on"
    )
    rejected_headlines = RejectedHeadline.objects.filter(issue__name__contains=issue.name)


    context = {
        "i": issue,
        "issue": issue.name,
        "articles": articles,
        "rejected_headlines": rejected_headlines
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
    articles = Article.objects.count()
    authors = Author.objects.count()
    rejected_headlines = RejectedHeadline.objects.count()
    context = {
        "articles": articles,
        "authors": authors,
        "rejected_headlines": rejected_headlines,
    }
    return render(request, "articles/about_us.html", context)

def paid_for(request):
    return {"paid_for": PaidFor.objects.order_by("?")[0]}

def donate(request):
    return render(request, "articles/donate.html")

    