from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from core.models.teams.models import Team, TeamMember
from django.core import serializers
import json


def add_team_member(request):
    if request.method == 'POST':
        try:
            # 接收前端传来的数据
            data = request.POST  # 解析 JSON 数据
            team_name = data.get('team_name')
            member_data = {
                'MIB_ID': data.get('MIB_ID'),
                'student_id': data.get('student_id'),
                'name': data.get('name'),
                'email': data.get('email')
            }

            # 查找符合条件的团队对象
            matching_teams = Team.objects.filter(name=team_name)

            if matching_teams.exists():
                # 如果至少有一个匹配的团队
                team = matching_teams.first()  # 取第一个匹配的团队对象

                # 创建 TeamMember 对象并赋值
                new_member = TeamMember(**member_data)
                new_member.save()

                # 将 TeamMember 对象与团队关联
                team.teammember_set.add(new_member)

                return JsonResponse({'status': 'success', 'message': 'Teammember added successfully!'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Team with this name does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'try error': str(e)})
    else:
        print(request.method)
        return JsonResponse({'status': 'error', 'message': 'Received non-POST request'})
    

def delete_team_member(request, member_id) :
    if request.method == 'DELETE':
        try:
            team_member = TeamMember.objects.get(id=member_id)
            team_member.delete()
            return JsonResponse({'status': 'success', 'message': 'Member deleted successfully'})
        except TeamMember.DoesNotExist:
            return JsonResponse({'error': 'TeamMember not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Only DELETE reuqests are supported'}, status=404)
    
def getMemberInfo(request, member_id):
    if request.method == 'GET':
        try:
            team_member = TeamMember.objects.get(id=member_id)
            team_member_data = serializers.serialize('json', [team_member])
            return JsonResponse({'status': 'success', 'message': 'Get member information successfully', 'team_member': team_member_data})
        except TeamMember.DoesNotExist:
            return JsonResponse({'error': 'TeamMember not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET reuqests are supported'}, status=404)
