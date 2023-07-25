from django.shortcuts import render


def teams_index(request):
    return render(request, "teams/teams.html")
