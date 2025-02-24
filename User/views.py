# import random
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from User.models import User
from config.settings import DEFAULT_FROM_EMAIL
from User.forms import LoginForm, RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from User.custom_token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages


# Create your views here.
# def generate_verification_code():
#     return str(random.randint(100000,999999))

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
    if request.method ==     'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            get_name_by_email = user.email.split('@')[0]
            user.set_password(user.password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            subject = 'Verify your account'
            message = render_to_string('User/email-verification/verify_email_message.html',{
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            data = 'You have been send email verification link ✉️'
            return HttpResponse(f'<h2>{data}</h2>')

            # user.set_password(form.cleaned_data['password'])
            # verification_code = generate_verification_code()
            # request.session['verification_code'] = verification_code

            # request.session['user_data'] = {
            #     'email': user.email,
            #     'password': form.cleaned_data['password'],
            #     'is_staff': user.is_staff,
            #     'is_superuser': user.is_superuser,
            # }
    context = {
            'form': form,
        }
    return render(request, 'User/register.html', context=context)


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('user:verify-email-complete')

    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'User/email-verification/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'User/email-verification/verify_email_complete.html')

# def verify_code(request):
#     if request.method == 'POST':
#         entered_code = request.POST.get('code')
#         stored_code = request.session.get('verification_code')
#         user_data = request.session.get('user_data')
#
#         if entered_code == stored_code:
#             del request.session['verification_code']
#             del request.session['user_data']
#             user = User.objects.create_user(
#                 email=user_data['email'],
#                 password=user_data['password'],
#                 is_staff=user_data['is_staff'],
#                 is_superuser=user_data['is_superuser']
#             )
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             messages.add_message(request, messages.SUCCESS, 'Your Code has been verified')
#             return redirect('shops:index')
#         else:
#             messages.add_message(request, messages.ERROR, 'Invalid code')
#
#     return render(request, 'User/enter_number.html')