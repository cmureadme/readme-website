from django.shortcuts import render

def index(request):
    return render(request, "games_home.html")

def unboundle(request):
    return render(request, "unboundle.html")
