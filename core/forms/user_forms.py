from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
from django.db import models

class OrdinaryUserCreationForm(UserCreationForm):
    # 使用 widgets 属性来自定义输入框的显示方式
    birthday = forms.DateField(required=False, label='生日(选填)', widget=forms.DateInput(attrs={'placeholder': '年-月-日', 'class': 'date-input'}))
    avatar = forms.ImageField(required=False, label='头像(选填)')
    captcha = CaptchaField(label='验证码')
    # mobile = models.CharField(max_length = 11, unique=True, label='手机号')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'birthday', 'avatar', 'captcha')

