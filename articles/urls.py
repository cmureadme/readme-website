from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="article_index"),
    path("authors", views.article_author_index, name="article_author_index"),
    path("authors/<author>/", views.article_author, name="article_author"),

    path("tags", views.article_category_index, name="article_category_index"),
    path("tags/<category>/", views.article_category, name="article_category"),

    path("issues", views.article_issues_index, name="article_issues_index"),
    path("issues/<int:vol>/<int:num>", views.article_issue, name="article_issue"),

    path("article/<str:slug>/", views.article_detail, name="article_detail"),

    path('login/', views.index, name='login'),
    path('logout/', views.index, name='logout'),
    path('signup/', views.index, name='signup'),
]