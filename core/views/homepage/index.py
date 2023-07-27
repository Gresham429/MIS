from django.shortcuts import render, redirect


def homepage_index(request):
    return render(request, "homepage/homepage.html")
