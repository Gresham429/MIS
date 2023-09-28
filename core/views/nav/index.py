from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.forms.user_forms import OrdinaryUserCreationForm
from core.models.user.models import OrdinaryUser
import json
from alibaba.sms import send_sms_code
from django.http import JsonResponse
import random
import time

#手机号登录
def sms_sign_in(request):
    
    if request.method == 'POST':
        if 'send_sms' in request.POST:  # Check if sending SMS is requested
            mobile = request.POST.get('phonenumber', '')
            if not mobile:  # Check if mobile number is empty
                return JsonResponse({'message': '请先填写手机号'})
            
            if time.time()>request.session.get('duration',0):
                sms_code = '%06d' % random.randint(0, 999999)
                request.session['sms_code'] = sms_code
                request.session['duration'] = time.time()+60
                request.session['surpass'] = time.time()+180
                
                print(sms_code, '已发送')
                try:
                    response = send_sms_code(mobile, sms_code)
                    response_data = json.loads(response)
                    if response_data.get('Code') == 'OK':
                        message = '短信验证码已发送，请注意查收。'
                    else:
                        message = '短信验证码发送失败，请稍后重试。'
                except Exception as e:
                    message = '短信验证码发送失败：%s' % str(e)
        
                return JsonResponse({'message': message})
        
        #验证用户
        user = authenticate(request, sms_code = request.POST['sms'])
        if user is None:
            #验证失败
            return JsonResponse({'message': '验证码错误'})
        else:
            #验证成功后登录
            login(request, user)

            # 通过反向查询获取关联的OrdinaryUser实例
            ordinary_user = OrdinaryUser.objects.filter(user=user).first()

            # 检查头像文件是否存在
            if ordinary_user.avatar and ordinary_user.avatar.file:
                avatar_url = ordinary_user.avatar.url
            else:
                avatar_url = None

            # 检查生日是否存在并转换为str
            if ordinary_user.birthday:
                birthday_str = ordinary_user.birthday.strftime('%Y-%m-%d')
            else:
                birthday_str = "未设置生日"  # 或者设置一个默认值)

            #创建请求的会话数据并且重定向到主页
            # 将 OrdinaryUser 对象以json序列化字典形式保存到会话中
            request.session['ordinary_user'] = json.dumps({
                'username': ordinary_user.user.username,
                'email': ordinary_user.user.email,
                'birthday': birthday_str,
                'avatar_url': avatar_url,
                'mobile':ordinary_user.mobile,
            })
            return redirect('homepage_index')
    else:
        return render(request, "nav/sms_signin.html")

#账号密码登录
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

            # 检查头像文件是否存在
            if ordinary_user.avatar and ordinary_user.avatar.file:
                avatar_url = ordinary_user.avatar.url
            else:
                avatar_url = None

            # 检查生日是否存在并转换为str
            if ordinary_user.birthday:
                birthday_str = ordinary_user.birthday.strftime('%Y-%m-%d')
            else:
                birthday_str = "未设置生日"  # 或者设置一个默认值)

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

            # 检查头像文件是否存在
            if ordinary_user.avatar and ordinary_user.avatar.file:
                avatar_url = ordinary_user.avatar.url
            else:
                avatar_url = None

            # 检查生日是否存在并转换为str
            if ordinary_user.birthday:
                birthday_str = ordinary_user.birthday.strftime('%Y-%m-%d')
            else:
                birthday_str = "未设置生日"  # 或者设置一个默认值)

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


