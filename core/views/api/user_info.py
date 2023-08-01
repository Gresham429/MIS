from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models.user.models import OrdinaryUser


@login_required(login_url='sign_in')
def get_user_info(request):
    user = request.user
    ordinary_user = OrdinaryUser.objects.filter(user=user).first()

    # 检查头像文件是否存在
    if ordinary_user.avatar and ordinary_user.avatar.file:
        avatar_url = ordinary_user.avatar.url
    else:
        avatar_url = None

    data = {
        'username': ordinary_user.user.username,
        'avatar_url': ordinary_user.avatar.url,
        'email': ordinary_user.user.email,
        'birthday': ordinary_user.birthday,
        'signature': ordinary_user.signature,
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
        signature = request.POST.get('signature')

        # 更新用户信息
        if email:
            user.email = email
            ordinary_user.user.email = email
        if birthday:
            ordinary_user.birthday = birthday
        if signature:
            ordinary_user.signature = signature

        user.save()
        ordinary_user.save()

        # 返回更新后的用户信息
        data = {
            'email': user.email,
            'birthday': ordinary_user.birthday,
            'signature': ordinary_user.signature,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


