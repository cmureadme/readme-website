from django.shortcuts import render

from magazine.models import Article, ImageGag
from magazine.views import index, stories, author_list, author, issue_list, issue, purity_test, about_us, article, image_gag, images


def cm_context(request):
    return {
        "cm__user_slug": "roan-tysh",
        "cm__curr_issue_vol": 5,
        "cm__curr_issue_num": 5
    }


def content_mill(request):
    context = {
        **cm_context(request)
    }

    return render(request, "content_mill/index.html", context)


def cm_render(request, template_name, context, *args, **kw_args):
    return render(request, "content_mill/public.html", {
        "cm__template_name": template_name,
        **cm_context(request),
        **context
    })


def public_index(request):
    return index(request, cm_render)


def public_stories(request):
    return stories(request, cm_render)


def public_author_list(request):
    return author_list(request, cm_render)


def public_author(request, slug):
    return author(request, slug, cm_render)


def public_issue_list(request):
    return issue_list(request, cm_render)


def public_issue(request, vol, num):
    return issue(request, vol, num, cm_render)


def public_purity_test(request):
    return purity_test(request, cm_render)


def public_about_us(request):
    return about_us(request, cm_render)


def public_article(request, slug):
    return article(request, slug, cm_render)


def public_image_gag(request, slug):
    return image_gag(request, slug, cm_render)


def public_images(request):
    return images(request, cm_render)


def create_story(request):
    context = {
        **cm_context(request),
        "used_slugs": [*(article.slug for article in Article.objects.all()), *(image_gag.slug for image_gag in ImageGag.objects.all())],
        "article": Article.objects.first()
    }

    return render(request, "content_mill/create_story.html", context)