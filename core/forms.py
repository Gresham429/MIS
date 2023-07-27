from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class OrdinaryUserCreationForm(UserCreationForm):
    # 使用 widgets 属性来自定义输入框的显示方式
    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': '年/月/日', 'class': 'date-input'}))
    photo = forms.URLField(required=False, max_length=256, widget=forms.TextInput(attrs={'placeholder': '头像url', 'class': 'photo-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'birthday', 'photo')
