"""
URL configuration for readme_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.shortcuts import render

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("magazine.urls")),
    path("discord", lambda request: HttpResponseRedirect("https://discord.gg/8eR4C3wuty")),
    path(
        "instagram",
        lambda request: HttpResponseRedirect("https://www.instagram.com/readme.news/"),
    ),
    path("donate", lambda request: HttpResponseRedirect("https://commerce.cashnet.com/CMU231?cname=35")),
    path("404", lambda request: render(request, "404.html")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
