from django.urls import path
from django.http import HttpResponseRedirect

from . import views

urlpatterns = [
    path("podcasts/artificial-intelligence-for-real-this-time", lambda request: HttpResponseRedirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")),

    path("", views.index, name="article_index"),
    path("people", views.article_author_index, name="article_author_index"),
    path("people/<author>/", views.article_author, name="article_author"),

    path("tags", views.article_category_index, name="article_category_index"),
    path("tags/<category>/", views.article_category, name="article_category"),

    path("issues", views.article_issues_index, name="article_issues_index"),
    path("issues/<int:vol>/<int:num>", views.article_issue, name="article_issue"),

    path("aboutus", views.about_us, name="about_us"),

    path("donate", views.donate, name = "donate"),

    path("article/<str:slug>/", views.article_detail, name="article_detail"),

    path('login/', views.index, name='login'),
    path('logout/', views.index, name='logout'),
    path('signup/', views.index, name='signup'),
]