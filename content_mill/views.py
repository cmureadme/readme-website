from django.shortcuts import render

from magazine.views import index_context


def content_mill(request):
    context = {}

    return render(request, "content_mill/index.html", context)


def front_page(request):
    return render(request, "content_mill/front_page.html", index_context())