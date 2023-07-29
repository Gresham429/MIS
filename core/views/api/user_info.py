from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models.user.user import OrdinaryUser


@login_required(login_url='sign_in')
def get_user_info(request):
    user = request.user
    ordinary_user = OrdinaryUser.objects.filter(user=user).first()
    data = {
        'username': ordinary_user.user.username,
        'email': ordinary_user.user.email,
        'birthday': ordinary_user.birthday,
    }
    return JsonResponse(data)

@login_required(login_url='sign_in')
def update_user_info(request):
    if request.method == 'POST':
        user : User = request.user
        ordinary_user : OrdinaryUser = OrdinaryUser.objects.filter(user=user).first()

        # 获取POST请求中的数据
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')

        # 更新用户信息
        if email:
            user.email = email
            ordinary_user.user.email = email
        if birthday:
            ordinary_user.birthday = birthday

        user.save()
        ordinary_user.save()

        # 返回更新后的用户信息
        data = {
            'email': user.email,
            'birthday': ordinary_user.birthday,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


