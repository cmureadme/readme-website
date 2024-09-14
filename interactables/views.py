from django.shortcuts import render

# Create your views here.
def interactables_index(request):
    return render(request, "interactables/interactables.html")