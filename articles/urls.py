from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="article_index"),
    path("authors", views.index, name="article_author_index"),
    path("tags", views.index, name="article_category_index"),
    path("issues", views.index, name="article_issues_index"),
    path("editor/issue", views.index, name="article_issues_edit"),
    path("post/<str:slug>/<int:pk>", views.index, name="article_detail"),
    path("category/<category>/", views.index, name="article_category"),
    path("author/<author>/", views.index, name="article_author"),
    path("issue/<int:vol>/<int:num>", views.index, name="article_issue"),
    path('login/', views.index, name='login'),
    path('logout/', views.index, name='logout'),
    path('signup/', views.index, name='signup'),
]