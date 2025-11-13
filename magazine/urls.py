from django.urls import path
from django.http import HttpResponseRedirect

from . import views

urlpatterns = [
    path("podcasts/artificial-intelligence-for-real-this-time", lambda request: HttpResponseRedirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")),

    path("", views.index, name="index"),

    path("stories", views.stories, name="stories"),

    path("staff", views.author_list, name="author_list"),
    path("staff/<author>/", views.author, name="author"),

    path("issues", views.issue_list, name="issue_list"),
    path("issues/<int:vol>/<int:num>", views.issue, name="issue"),

    path("cmupuritytest", views.purity_test, name="purity_test"),
    path("aboutus", views.about_us, name="about_us"),

    path("donate", views.donate, name = "donate"),

    path("article/<str:slug>/", views.article_page, name="article_page"),
]