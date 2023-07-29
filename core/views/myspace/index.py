from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="sign_in")
def myspace_index(request, username):
    return render(request, "myspace/myspace.html")
    