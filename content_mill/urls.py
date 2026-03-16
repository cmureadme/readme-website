from django.urls import path

from . import views

urlpatterns = [
    # path("log-in", views.log_in, name="log_in"),
    path("content-mill", views.content_mill, name="content_mill"),
    path("content-mill/front-page", views.front_page, name="front_page"),
]
