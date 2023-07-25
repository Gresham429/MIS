from django.shortcuts import render


def homepage_index(request):
    return render(request, "homepage/homepage.html")