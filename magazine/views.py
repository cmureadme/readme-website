from magazine.models import Article, ImageGag, Author, Issue, PaidFor, RejectedHeadline
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from django.conf import settings
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import random

import json

purity_test_items_file = "./purity_test_items.json"
with open(purity_test_items_file) as json_file:
    purity_test_items = json.load(json_file)


def index(request):
    latest_issue = Issue.objects.all().order_by("-vol", "-num")[0]
    second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[1]

    # Prevents front page from crashing if latest issue has very few articles
    # ie Latest issue is in the proccess of being uploaded
    i = 1
    while len(Article.objects.all().filter(Q(published=True) & Q(issue__name__contains=latest_issue.name))) <= 5:
        latest_issue = Issue.objects.all().order_by("-vol", "-num")[i]
        second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[i + 1]
        i += 1

    sidebar_articles_pool = Article.objects.all().filter(
        Q(published=True)
        & (Q(issue__name__contains=latest_issue.name) | Q(issue__name__contains=second_latest_issue.name))
    )
    sidebar_image_gags_pool = ImageGag.objects.all().filter(
        Q(published=True)
        & (Q(issue__name__contains=latest_issue.name) | Q(issue__name__contains=second_latest_issue.name))
    )

    sidebar_articles_pool_count = sidebar_articles_pool.count()
    sidebar_image_gags_pool_count = sidebar_image_gags_pool.count()

    sidebar_num_items = min(5, sidebar_articles_pool_count + sidebar_image_gags_pool_count)

    sidebar_num_articles = 0
    sidebar_num_image_gags = 0

    for i in range(sidebar_num_items):
        rand = random.random()

        if (
            rand * float(sidebar_articles_pool_count + sidebar_image_gags_pool_count - i)
            < sidebar_articles_pool_count - sidebar_num_articles
        ):
            sidebar_num_articles += 1
        else:
            sidebar_num_image_gags += 1

    sidebar_articles = [*sidebar_articles_pool.order_by("?")[0:sidebar_num_articles]]
    sidebar_image_gags = [*sidebar_image_gags_pool.order_by("?")[0:sidebar_num_image_gags]]

    sidebar = sidebar_articles + sidebar_image_gags
    random.shuffle(sidebar)

    secondary_articles_pool = Article.objects.filter(Q(published=True))
    secondary_image_gags_pool = ImageGag.objects.filter(Q(published=True))

    secondary_articles_pool_count = secondary_articles_pool.count()
    secondary_image_gags_pool_count = secondary_image_gags_pool.count()

    secondary_num_items = min(24, sidebar_articles_pool_count + sidebar_image_gags_pool_count)

    secondary_num_articles = 0
    secondary_num_image_gags = 0

    for i in range(secondary_num_items):
        rand = random.random()

        if (
            rand * float(secondary_articles_pool_count + secondary_image_gags_pool_count - i)
            < secondary_articles_pool_count - secondary_num_articles
        ):
            secondary_num_articles += 1
        else:
            secondary_num_image_gags += 1

    secondary_articles = [*secondary_articles_pool.order_by("?")[0:secondary_num_articles]]
    secondary_image_gags = [*secondary_image_gags_pool.order_by("?")[0:secondary_num_image_gags]]

    secondary = secondary_articles + secondary_image_gags
    random.shuffle(secondary)

    # Will pull from the best rejected headlines
    feat_rej_heads = RejectedHeadline.objects.all().filter(Q(featured=True)).order_by("?")
    if len(feat_rej_heads) > 20:
        feat_rej_heads = feat_rej_heads[:20]
    else:
        feat_rej_heads = feat_rej_heads[:]

    # Will pull from non featured rejected headlines
    non_feat_rej_heads = RejectedHeadline.objects.all().filter(Q(featured=False)).order_by("?")
    if len(non_feat_rej_heads) > 20:
        non_feat_rej_heads = non_feat_rej_heads[:20]
    else:
        non_feat_rej_heads = non_feat_rej_heads[:]

    all_rej_heads = feat_rej_heads + non_feat_rej_heads
    random.shuffle(all_rej_heads)

    feat_articles = {
        "largest": Article.objects.all()
        .filter(
            Q(published=True)
            & Q(front_page=True)
            & Q(issue__name__contains=latest_issue.name)
            & Q(images__isnull=False)
        )
        .order_by("?")[0],
        "column": Article.objects.all()
        .filter(
            Q(published=True)
            & (Q(front_page=True) | Q(featured=True))
            & Q(issue__name__contains=latest_issue.name)
            & Q(images__isnull=True)
        )
        .order_by("?")[0],
        "article": Article.objects.all()
        .filter(Q(published=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=True))
        .order_by("?")[0],
        "image": Article.objects.all()
        .filter(Q(published=True) & Q(issue__name__contains=latest_issue.name) & Q(images__isnull=False))
        .order_by("?")[0],
    }

    context = {
        "sidebar": sidebar,
        "secondary": secondary,
        "feat_articles": feat_articles,
        "MEDIA_URL": settings.MEDIA_URL,
        "rej_heads": all_rej_heads,
    }
    return render(request, "magazine/index.html", context)


def author_list(request):
    context = {
        "usual_suspects": Author.objects.filter(author_status="US", alias_of=None),
        "independent_contractors": Author.objects.filter(author_status="IC", alias_of=None),
        "escapees": Author.objects.filter(author_status="EE", alias_of=None),
    }
    return render(request, "magazine/author_list.html", context)


def author(request, author):
    try:
        author = Author.objects.get(slug=author)
    except Author.DoesNotExist:
        raise Http404

    if author.root_slug() != author.slug:
        return redirect(reverse("author", args=[author.root_slug()]))

    articles = [
        article
        for article in Article.objects.order_by("-issue__vol", "-issue__num", "-true_created_on").filter(published=True)
        if any(article_author.root_slug() == author.slug for article_author in article.authors.all())
    ]
    image_gags = [
        image_gag
        for image_gag in ImageGag.objects.order_by("-issue__vol", "-issue__num", "-true_created_on").filter(
            published=True
        )
        if any(image_gag_author.root_slug() == author.slug for image_gag_author in image_gag.artists.all())
    ]

    pieces = []
    i = 0
    j = 0
    while i < len(articles) and j < len(image_gags):
        print(i, j, articles[i].slug, image_gags[j].slug, articles[i].issue, image_gags[j].issue)
        if articles[i].issue.vol > image_gags[j].issue.vol or (
            articles[i].issue.vol == image_gags[j].issue.vol
            and (
                articles[i].issue.num > image_gags[j].issue.num
                or (
                    articles[i].issue.num == image_gags[j].issue.num
                    and articles[i].true_created_on > image_gags[j].true_created_on
                )
            )
        ):
            pieces.append(articles[i])
            i += 1
        else:
            pieces.append(image_gags[j])
            j += 1
    pieces += articles[i:]
    pieces += image_gags[j:]

    page_num = request.GET.get("page", 1)
    paginator = Paginator(pieces, per_page=10)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "author": author,
        "page_obj": page_obj,
    }
    return render(request, "magazine/author.html", context)


def issue_list(request):
    issues = Issue.objects.all().order_by("vol", "num")
    issues_by_volume = {}

    for issue in issues:
        volume = issue.vol
        if volume not in issues_by_volume:
            issues_by_volume[volume] = []
        issues_by_volume[volume].append(issue)

    context = {
        "issues": issues,
        "issues_by_volume": issues_by_volume,
    }
    return render(request, "magazine/issue_list.html", context)


def issue(request, vol, num):
    try:
        issue = Issue.objects.get(num=num, vol=vol)
    except Issue.DoesNotExist:
        raise Http404

    articles = [
        *Article.objects.filter(issue__name__contains=issue.name).order_by(
            "-front_page", "-featured", "-true_created_on"
        )
    ]
    image_gags = [
        *ImageGag.objects.filter(issue__name__contains=issue.name).order_by(
            "-front_page", "-featured", "-true_created_on"
        )
    ]

    pieces = []
    i = 0
    j = 0
    while i < len(articles) and j < len(image_gags):
        if (
            articles[i].front_page
            and not image_gags[j].front_page
            or (
                articles[i].front_page == image_gags[j].front_page
                and (
                    articles[i].featured
                    and not image_gags[j].featured
                    or (
                        articles[i].featured == image_gags[j].featured
                        and articles[i].true_created_on > image_gags[j].true_created_on
                    )
                )
            )
        ):
            pieces.append(articles[i])
            i += 1
        else:
            pieces.append(image_gags[j])
            j += 1
    pieces += articles[i:]
    image_gags += image_gags[j:]

    rejected_headlines = RejectedHeadline.objects.filter(issue__name__contains=issue.name)

    context = {
        "issue": issue,
        "articles": pieces,
        "rejected_headlines": rejected_headlines,
    }
    return render(request, "magazine/issue.html", context)


def article_page(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404

    context = {"article": article}

    return render(request, "magazine/article_page.html", context)


def image_gag(request, slug):
    try:
        image_gag = ImageGag.objects.get(slug=slug)
    except ImageGag.DoesNotExist:
        raise Http404

    context = {"image_gag": image_gag}

    return render(request, "magazine/image_gag.html", context)


def about_us(request):
    articles = Article.objects.count()
    authors = Author.objects.count()
    rejected_headlines = RejectedHeadline.objects.count()
    issues = Issue.objects.count()
    context = {
        "articles": articles,
        "authors": authors,
        "rejected_headlines": rejected_headlines,
        "issues": issues,
    }
    return render(request, "magazine/about_us.html", context)


def paid_for(request):
    return {"paid_for": PaidFor.objects.order_by("?")[0]}


def purity_test(request):
    context = {"items": purity_test_items}
    return render(request, "magazine/purity_test.html", context)


def stories(request):
    articles = [
        *Article.objects.filter().order_by("-issue__vol", "-issue__num", "-front_page", "-featured", "-true_created_on")
    ]
    image_gags = [
        *ImageGag.objects.filter().order_by(
            "-issue__vol", "-issue__num", "-front_page", "-featured", "-true_created_on"
        )
    ]

    pieces = []
    i = 0
    j = 0
    while i < len(articles) and j < len(image_gags):
        if articles[i].issue.vol > image_gags[j].issue.vol or (
            articles[i].issue.vol == image_gags[j].issue.vol
            and (
                articles[i].issue.num > image_gags[j].issue.num
                or (
                    articles[i].issue.num == image_gags[j].issue.num
                    and articles[i].front_page
                    and not image_gags[j].front_page
                    or (
                        articles[i].front_page == image_gags[j].front_page
                        and (
                            articles[i].featured
                            and not image_gags[j].featured
                            or (
                                articles[i].featured == image_gags[j].featured
                                and articles[i].true_created_on > image_gags[j].true_created_on
                            )
                        )
                    )
                )
            )
        ):
            pieces.append(articles[i])
            i += 1
        else:
            pieces.append(image_gags[j])
            j += 1
    pieces += articles[i:]
    image_gags += image_gags[j:]

    page_num = request.GET.get("page", 1)
    paginator = Paginator(pieces, per_page=25)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {"page_obj": page_obj}
    return render(request, "magazine/stories.html", context)


def random_article(request):
    return redirect(reverse("article_page", args=[Article.objects.order_by("?").first().slug]))


# Returns all images chronologically
def images(request):
    image_gags = ImageGag.objects.filter().order_by(
        "-issue__vol", "-issue__num", "-front_page", "-featured", "-true_created_on"
    )

    page_num = request.GET.get("page", 1)
    paginator = Paginator(image_gags, per_page=25)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {"page_obj": page_obj}
    return render(request, "magazine/images.html", context)
