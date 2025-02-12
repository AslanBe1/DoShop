from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from User.forms import LoginForm, RegisterForm


# Create your views here.

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('shops:index')

            else:
                messages.add_message(request,messages.ERROR,'Invalid login')

    context = {
        'form': form,
    }

    return render(request, 'User/login.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('shops:index')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.save()
            return redirect('shops:index')

    context = {
        'form': form,
    }

    return render(request, 'User/register.html', context=context)