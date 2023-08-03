from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models.teams.models import Team, TeamMember


def get_teams_info(request):
    teams = Team.objects.all()

    data_list = [
        {
            'name' : team.name,
            'description' : team.description,
        }
        for team in teams
    ]

    return JsonResponse(data_list, safe=False)