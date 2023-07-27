from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.forms import OrdinaryUserCreationForm
from core.models.user.user import OrdinaryUser


def sign_in(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "nav/signin.html", {'fault':'用户名或密码错误'})
        else:
            login(request, user)
            return redirect('homepage_index')
    else:
        return render(request, "nav/signin.html")

def sign_up(request):
    if request.method == 'POST':
        registered_form = OrdinaryUserCreationForm(request.POST)
        if registered_form.is_valid():
            registered_form.save()
            user = authenticate(username=registered_form.cleaned_data['username'], password=registered_form.cleaned_data['password1'])
            user.email = registered_form.cleaned_data['email']
            OrdinaryUser(user=user, birthday=registered_form.cleaned_data['birthday'], photo=registered_form.cleaned_data['photo']).save()
            login(request, user)
            return redirect('homepage_index')
    else:
        registered_form = OrdinaryUserCreationForm()
    
    content = {'registered_form': registered_form}
    return render(request, "nav/signup.html", content)

def sign_out(request):
    logout(request)
    return redirect('homepage_index')