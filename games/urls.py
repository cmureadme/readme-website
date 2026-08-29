from django.urls import path
from django.http import HttpResponseRedirect

from . import views

urlpatterns = [
    path("games", views.index, name="games"),
    path("games/unboundle", views.unboundle, name="games.unboundle"),
]
