from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path(
        "podcasts/artificial-intelligence-for-real-this-time",
        lambda request: HttpResponseRedirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ),
    path("", views.index, name="index"),
    path("stories", views.stories, name="stories"),
    path("staff/", views.author_list, name="author_list"),
    path("staff/<slug>/", views.author, name="author"),
    path("issue/", views.issue_list, name="issue_list"),
    path("issue/<int:vol>/<int:num>", views.issue, name="issue"),
    path("purity_test/", views.purity_test, name="purity_test"),
    path("about_us/", views.about_us, name="about_us"),
    path("random/", views.random_article, name="random"),
    path("article/<str:slug>/", views.article, name="article"),
    path("image/<str:slug>/", views.image_gag, name="image_gag"),
    path("image/", views.images, name="images"),
    # Redirects for old URIs (do not delete!)
    path("issues/", lambda request: redirect(views.issue_list, permanent=True)),
    path(
        "issues/<int:vol>/<int:num>", lambda request, vol, num: redirect(views.issue, permanent=True, vol=vol, num=num)
    ),
    path("cmupuritytest/", lambda request: redirect(views.purity_test, permanent=True)),
    path("aboutus/", lambda request: redirect(views.about_us, permanent=True)),
]
