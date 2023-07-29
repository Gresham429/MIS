from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json


@login_required(login_url='sign_in')
def teams_index(request):
    # 从会话中获取保存的 OrdinaryUser 数据
    json_data = request.session.get('ordinary_user', None)

    if json_data:
        # 将 JSON 数据反序列化回字典
        ordinary_user_data = json.loads(json_data)

        # 现在你可以将字典直接传递给模板
        return render(request, "teams/teams.html", ordinary_user_data)

    # 如果会话中没有保存 OrdinaryUser 数据，返回一个空字典
    return render(request, "teams/teams.html", {})