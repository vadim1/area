from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from area_app.forms import MobileAuthenticationForm, MobileSignUpForm, \
    OtpForm, MobilePasswordResetForm

from area_app.models import User
from area_app.utils import generate_otp, send_otp


# Some of the code is taken from django.contrib.auth.views.py
@sensitive_post_parameters()
@csrf_protect
@never_cache
def mobile_login(request):
    """
    Displays the mobile login form and handles the login action.
    """
    template_name = "account/login.html"
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = MobileAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            login_url = resolve_url(settings.LOGIN_URL)
            return HttpResponseRedirect(login_url)
    else:
        form = MobileAuthenticationForm()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'mobile': True
    }
    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def mobile_signup(request):
    """
    Displays the mobile signup form and handles the signup action.
    """
    template_name = "account/signup.html"
    redirect_field_name = REDIRECT_FIELD_NAME
    authentication_form = MobileSignUpForm
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    step = request.session.get('auth_step', 1)
    if request.method == "POST":
        if step == 1:
            form = authentication_form(data=request.POST)
            if form.is_valid():
                request.session['auth_step'] = 2
                request.session['otp'] = generate_otp()
                request.session['username'] = form.cleaned_data['username']
                request.session['password'] = form.cleaned_data['password1']
                send_otp(request.session['username'], request.session['otp'])
        else:
            form = OtpForm(request=request, data=request.POST)
            if form.is_valid():
                user = User.objects.create(username=request.session['username'])
                user.set_password(request.session['password'])
                user.is_active = True
                user.save()
                user = authenticate(phone_number=user.phone_number, password=request.session['password'])
                login(request, user)
                del request.session['otp']
                del request.session['username']
                del request.session['auth_step']
                return redirect(reverse('mobile_login'))
    else:
        if step == 1:
            form = authentication_form()
        else:
            form = OtpForm()
    if step != 1:
        template_name = "account/confirm_otp.html"

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'mobile': True,
    }
    return TemplateResponse(request, template_name, context)


def resend_otp(request):
    mobile_number = request.session.get('username', None)
    if mobile_number is None:
        return redirect('/')
    send_otp(mobile_number, request.session['otp'])
    return JsonResponse(data={'result': 'Sent OTP to your number!'})


def mobile_forget_password(request):
    template_name = "account/password_reset.html"
    redirect_field_name = REDIRECT_FIELD_NAME
    authentication_form = MobilePasswordResetForm
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    step = request.session.get('auth_step', 1)
    if request.method == "POST":
        if step == 1:
            form = authentication_form(data=request.POST)
            if form.is_valid():
                request.session['auth_step'] = 2
                request.session['otp'] = generate_otp()
                request.session['username'] = form.cleaned_data.get('phone_number')
                request.session['password'] = form.cleaned_data.get('password1')
                send_otp(request.session['username'], request.session['otp'])
                return redirect(reverse('mobile_forget_password'))
        else:
            form = OtpForm(request=request, data=request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.session['username'])
                user.set_password(request.session['password'])
                user.save()
                del request.session['auth_step']
                del request.session['otp']
                del request.session['username']
                del request.session['password']
                return redirect(reverse('mobile_login'))
    else:
        if step == 1:
            form = authentication_form()
        else:
            form = OtpForm()
    if step != 1:
        template_name = "account/confirm_otp.html"
    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'mobile': True
    }
    return TemplateResponse(request, template_name, context)
