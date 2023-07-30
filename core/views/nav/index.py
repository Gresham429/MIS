from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.forms import OrdinaryUserCreationForm
from core.models.user.user import OrdinaryUser

import json


#登录
def sign_in(request):
    if request.method == 'POST':
        #验证用户
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            #验证失败
            return render(request, "nav/signin.html", {'fault':'用户名或密码错误'})
        else:
            #验证成功后登录
            login(request, user)

            # 通过反向查询获取关联的OrdinaryUser实例
            ordinary_user = OrdinaryUser.objects.filter(user=user).first()

            if ordinary_user.avatar is None:
                avatar_url = None
            else:
                avatar_url = ordinary_user.avatar.url

            # 将 'date' 对象转换为字符串
            birthday_str = ordinary_user.birthday.strftime('%Y-%m-%d')

            #创建请求的会话数据并且重定向到主页
            # 将 OrdinaryUser 对象以json序列化字典形式保存到会话中
            request.session['ordinary_user'] = json.dumps({
                'username': ordinary_user.user.username,
                'email': ordinary_user.user.email,
                'birthday': birthday_str,
                'avatar_url': avatar_url,
            })
            return redirect('homepage_index')
    else:
        return render(request, "nav/signin.html")

#注册
def sign_up(request):
    if request.method == 'POST':
        registered_form = OrdinaryUserCreationForm(request.POST, request.FILES)
        if registered_form.is_valid():
            #保存注册表单正确时的用户信息
            registered_form.save()
            user = authenticate(username=registered_form.cleaned_data['username'], password=registered_form.cleaned_data['password1'])
            user.email = registered_form.cleaned_data['email']
            user.save()

            #创建普通用户实例并与新创建的用户关联
            birthday=registered_form.cleaned_data['birthday']
            avatar=registered_form.cleaned_data['avatar']
            OrdinaryUser.objects.create(user=user, birthday=birthday, avatar=avatar)

            #登录刚刚注册的用户
            login(request, user)

            # 通过反向查询获取关联的OrdinaryUser实例
            ordinary_user = OrdinaryUser.objects.filter(user=user).first()

            if ordinary_user.avatar is None:
                avatar_url = None
            else:
                avatar_url = ordinary_user.avatar.url

            # 将 'date' 对象转换为字符串
            birthday_str = ordinary_user.birthday.strftime('%Y-%m-%d')

            #创建请求的会话数据并且重定向到主页
            # 将 OrdinaryUser 对象以json序列化字典形式保存到会话中
            request.session['ordinary_user'] = json.dumps({
                'username': ordinary_user.user.username,
                'email': ordinary_user.user.email,
                'birthday': birthday_str,
                'avatar_url': avatar_url,
            })
            return redirect('homepage_index')
    else:
        registered_form = OrdinaryUserCreationForm()
    
    content = {'registered_form': registered_form}
    return render(request, "nav/signup.html", content)

#登出
def sign_out(request):
    logout(request)
    
    # 获取来源页面 URL
    referer = request.META.get('HTTP_REFERER')

    return redirect(referer)