from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class OrdinaryUserCreationForm(UserCreationForm):
    # 使用 widgets 属性来自定义输入框的显示方式
    birthday = forms.DateField(required=False, label='生日(选填)', widget=forms.DateInput(attrs={'placeholder': '年-月-日', 'class': 'date-input'}))
    avatar = forms.ImageField(required=False, label='头像(选填)')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'birthday', 'avatar')
