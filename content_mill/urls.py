from django.urls import path

from . import views

urlpatterns = [
    # path("log-in", views.log_in, name="log_in"),
    path("content-mill/", views.content_mill, name="content_mill"),
    path("content-mill/public/", views.public_index, name="public_index"),
    path("content-mill/public/stories/", views.public_index, name="public_stories"),
    path("content-mill/public/staff/", views.public_author_list, name="public_author_list"),
    path("content-mill/public/staff/<slug>/", views.public_author, name="public_author"),
    path("content-mill/public/issue/", views.public_issue_list, name="public_issue_list"),
    path("content-mill/public/issue/<int:vol>/<int:num>/", views.public_issue, name="public_issue"),
    path("content-mill/public/purity_test/", views.public_purity_test, name="public_purity_test"),
    path("content-mill/public/about_us/", views.public_about_us, name="public_about_us"),
    path("content-mill/public/article/<str:slug>/", views.public_article, name="public_article"),
    path("content-mill/public/image/<str:slug>/", views.public_image_gag, name="public_image_gag"),
    path("content-mill/public/image/", views.public_images, name="public_images"),
]
