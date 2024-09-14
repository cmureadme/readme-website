from django.urls import path

from . import views

urlpatterns = [
    path("", views.interactables_index, name="interactables"),
]