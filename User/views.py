import random
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from User.models import User
from config.settings import EMAIL_HOST_USER
from User.forms import LoginForm, RegisterForm


# Create your views here.
def generate_verification_code():
    return str(random.randint(100000,999999))

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
            get_name_by_email = user.email.split('@')[0]
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.set_password(form.cleaned_data['password'])
            verification_code = generate_verification_code()
            request.session['verification_code'] = verification_code

            request.session['user_data'] = {
                'email': user.email,
                'password': form.cleaned_data['password'],
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
            send_mail(
                f'{get_name_by_email}',
                f'{get_name_by_email}\'s account has been successfully created\nYour Code {verification_code}',
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('user:verify_code')

    context = {
        'form': form,
    }

    return render(request, 'User/register.html', context=context)


def verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        stored_code = request.session.get('verification_code')
        user_data = request.session.get('user_data')

        if entered_code == stored_code:
            del request.session['verification_code']
            del request.session['user_data']
            user = User.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser']
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.add_message(request, messages.SUCCESS, 'Your Code has been verified')
            return redirect('shops:index')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid code')

    return render(request, 'User/enter_number.html')