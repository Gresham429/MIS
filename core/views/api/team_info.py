from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from core.models.teams.models import Team, TeamMember
from urllib.parse import unquote
from django.core import serializers
import json

def get_teams_info(request):
    teams = Team.objects.all()

    data_list = [
        {
            'id' : team.id,
            'name' : team.name,
            'description' : team.description,
        }
        for team in teams
    ]

    return JsonResponse(data_list, safe=False)   


def getPopUpContent(request, team_id):
    try:

        # 查询名称为team_name的团队的所有数据
        team = Team.objects.get(id = team_id)
        team_members = team.teammember_set.all()
        
        team_data = serializers.serialize('json', [team])
        team_members_data = serializers.serialize('json', team_members)
        return JsonResponse({'status': 'success', 'message': 'Get team information successfully', 
                             'team_data': team_data, 'team_members_data': team_members_data})
        
    except Exception as e:
        # 出现异常时返回错误信息
        return JsonResponse({'error': str(e)})


def get_oneteam_info(request, team_id) :
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': team.id, 'name': team.name, 'description': team.description})



def add_team(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        description = data.get('description')
        logo = data.get('logo')

        # 检查团队是否已存在
        existing_team = Team.objects.filter(name=name).first()
        if existing_team:
            return JsonResponse({'status': 'error', 'message': 'Team with this name already exists'}, status=400)

        team = Team.objects.create(name=name, description=description, logo=logo)
        
        return JsonResponse({'status': 'success', 'message': 'Team member added successfully!', 'id': team.id}, status=200)



def delete_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    if request.method == 'DELETE':
        team.delete()
        return JsonResponse({'status': 'success', 'message': 'Team deleted successfully'})


def update_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': team.id, 'name': team.name, 'description': team.description})

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        team.name = data.get('name', team.name)
        team.description = data.get('description', team.description)
        team.save()
        return JsonResponse({'status': 'success', 'message': 'Team updated successfully'})

    return JsonResponse({'error': 'wrong method'}, status=500)



def get_team_members(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
        team_members = team.teammember_set.all()

        team_member_data = []
        for member in team_members:
            member_data = {
                "id": member.id,
                "MIB_ID": member.MIB_ID,
                "student_id": member.student_id,
                "name": member.name,
                "email": member.email
            }
            team_member_data.append(member_data)

        return JsonResponse({"team_members": team_member_data})
    except Team.DoesNotExist:
        return JsonResponse({"error": "Team not found"}, status=404)