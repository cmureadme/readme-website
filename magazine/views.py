from magazine.models import Article, ImageGag, Author, Issue, PaidFor, Piece, RejectedHeadline
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from django.conf import settings
from django.db.models import Q, QuerySet

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import random

import json

from enum import Enum

purity_test_items_file = "./purity_test_items.json"
with open(purity_test_items_file) as json_file:
    purity_test_items = json.load(json_file)


def index(request):
    latest_issue = Issue.objects.all().order_by("-vol", "-num")[0]
    second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[1]

    # Prevents front page from crashing if latest issue has very few articles
    # ie Latest issue is in the proccess of being uploaded
    i = 1
    while len(Article.objects.all().filter(Q(published=True) & Q(issue=latest_issue))) <= 5:
        latest_issue = Issue.objects.all().order_by("-vol", "-num")[i]
        second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[i + 1]
        i += 1

    # incase for some reason we uploaded the lastest issues before we finished uploading the second latest issue
    while len(Article.objects.all().filter(Q(published=True) & Q(issue=second_latest_issue))) <= 5:
        second_latest_issue = Issue.objects.all().order_by("-vol", "-num")[i + 1]
        i += 1

    sidebar_articles_pool = Article.objects.all().filter(
        Q(published=True) & (Q(issue=latest_issue) | Q(issue=second_latest_issue))
    )
    sidebar_image_gags_pool = ImageGag.objects.all().filter(
        Q(published=True) & (Q(issue=latest_issue) | Q(issue=second_latest_issue))
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
    if len(feat_rej_heads) > 10:
        feat_rej_heads = feat_rej_heads[:10]
    else:
        feat_rej_heads = feat_rej_heads[:]

    # Will pull from non featured rejected headlines
    all_rej_heads = feat_rej_heads + [*RejectedHeadline.objects.all().filter(Q(featured=False)).order_by("?")]
    if len(all_rej_heads) > 20:
        all_rej_heads = all_rej_heads[:20]
    else:
        all_rej_heads = all_rej_heads[:]

    random.shuffle(all_rej_heads)

    feat_articles = {
        "largest": Article.objects.all()
        .filter(Q(published=True) & Q(front_page=True) & Q(issue=latest_issue) & Q(images__isnull=False))
        .order_by("?")[0],
        "column": Article.objects.all()
        .filter(
            Q(published=True) & (Q(front_page=True) | Q(featured=True)) & Q(issue=latest_issue) & Q(images__isnull=True)
        )
        .order_by("?")[0],
        "article": Article.objects.all()
        .filter(Q(published=True) & Q(issue=latest_issue) & Q(images__isnull=True))
        .order_by("?")[0],
        "image": Article.objects.all()
        .filter(Q(published=True) & Q(issue=latest_issue) & Q(images__isnull=False))
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

    pieces = [
        piece
        for piece in order_pieces(
            Article.objects,
            ImageGag.objects,
            [PieceOrdering.ISSUE_DESC, PieceOrdering.TRUE_CREATED_ON_DESC, PieceOrdering.SLUG_ASC],
        )
        if any(maker.root_slug() == author.slug for maker in piece.makers())
    ]

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
        "pieces": page_obj,
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

    pieces = order_pieces(
        Article.objects.filter(issue=issue),
        ImageGag.objects.filter(issue=issue),
        [
            PieceOrdering.FRONT_PAGE_FIRST,
            PieceOrdering.FEATURED_FIRST,
            PieceOrdering.SLUG_ASC,
        ],
    )

    rejected_headlines = RejectedHeadline.objects.filter(issue=issue)

    context = {
        "issue": issue,
        "pieces": pieces,
        "rejected_headlines": rejected_headlines,
    }
    return render(request, "magazine/issue.html", context)


def article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404

    context = {"article": article}

    return render(request, "magazine/article.html", context)


def image_gag(request, slug):
    try:
        image_gag = ImageGag.objects.get(slug=slug)
    except ImageGag.DoesNotExist:
        raise Http404

    context = {"image_gag": image_gag}

    return render(request, "magazine/image_gag.html", context)


def about_us(request):
    pieces = Article.objects.count() + ImageGag.objects.count()
    authors = Author.objects.count()
    rejected_headlines = RejectedHeadline.objects.count()
    issues = Issue.objects.count()
    context = {
        "pieces": pieces,
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
    pieces = order_pieces(
        Article.objects,
        ImageGag.objects,
        [
            PieceOrdering.ISSUE_DESC,
            PieceOrdering.TRUE_CREATED_ON_DESC,
            PieceOrdering.FRONT_PAGE_FIRST,
            PieceOrdering.FEATURED_FIRST,
            PieceOrdering.SLUG_ASC,
        ],
    )

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

    context = {"page_obj": page_obj, "pieces": page_obj}
    return render(request, "magazine/stories.html", context)


def random_article(request):
    return redirect(reverse("article", args=[Article.objects.order_by("?").first().slug]))


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

    context = {"page_obj": page_obj, "image_gags": page_obj}
    return render(request, "magazine/images.html", context)


class PieceOrdering(Enum):
    ISSUE_DESC = 0
    FRONT_PAGE_FIRST = 1
    FEATURED_FIRST = 2
    TRUE_CREATED_ON_DESC = 3
    SLUG_ASC = 4


def order_pieces(
    articles: QuerySet[Article], image_gags: QuerySet[ImageGag], ordering: list[PieceOrdering]
) -> list[Piece]:
    def pieces_lt(p: Piece, q: Piece, ordering: list[PieceOrdering]) -> bool:
        for ord in ordering:
            match ord:
                case PieceOrdering.ISSUE_DESC:
                    if p.issue.vol < q.issue.vol:
                        return False
                    elif p.issue.vol > q.issue.vol:
                        return True
                    else:
                        if p.issue.num < q.issue.num:
                            return False
                        elif p.issue.num > q.issue.num:
                            return True
                case PieceOrdering.FRONT_PAGE_FIRST:
                    if p.front_page != q.front_page:
                        return p.front_page
                case PieceOrdering.FEATURED_FIRST:
                    if p.featured != q.featured:
                        return p.featured
                case PieceOrdering.TRUE_CREATED_ON_DESC:
                    if p.true_created_on < q.true_created_on:
                        return False
                    elif p.true_created_on > q.true_created_on:
                        return True
                case PieceOrdering.SLUG_ASC:
                    if p.slug < q.slug:
                        return True
                    elif p.slug > q.slug:
                        return False

        return False

    qs_ordering = []

    for ord in ordering:
        match ord:
            case PieceOrdering.ISSUE_DESC:
                qs_ordering.append("-issue__vol")
                qs_ordering.append("-issue__num")
            case PieceOrdering.FRONT_PAGE_FIRST:
                qs_ordering.append("-front_page")
            case PieceOrdering.FEATURED_FIRST:
                qs_ordering.append("-featured")
            case PieceOrdering.TRUE_CREATED_ON_DESC:
                qs_ordering.append("-true_created_on")
            case PieceOrdering.SLUG_ASC:
                qs_ordering.append("slug")

    articles = [*articles.order_by(*qs_ordering)]
    image_gags = [*image_gags.order_by(*qs_ordering)]

    pieces = []
    i = 0
    j = 0
    while i < len(articles) and j < len(image_gags):
        if pieces_lt(articles[i], image_gags[j], ordering):
            pieces.append(articles[i])
            i += 1
        else:
            pieces.append(image_gags[j])
            j += 1
    pieces += articles[i:]
    pieces += image_gags[j:]

    return pieces


# <!--

#     THE RTOSH PLAN:

#     1. Fix markdown vs. imgswitch issue in tags [partially done, should do something to separate image IDs from their slugs if that makes sense]
#     2. Create separate mechanism for image-only articles [done]
#     3. Add image dimensions to articleimages model
#     4. Improve image rendering (load images on demand, show properly-sized light gray placeholder until then)
#     5. Improve rendering of image-only articles in all places they're shown (index cards [large, sidebar, and main], stories/staff cards, article page) [done]

# -->
