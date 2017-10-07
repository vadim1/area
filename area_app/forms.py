from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import CharField, Form, ChoiceField, EmailField, PasswordInput

from area_app.constants import GRADES, DREAM_DIRECTORS
from .models import Question


class SignupWithNameForm(Form):
    first_name = CharField(max_length=40, label='First Name')
    last_name = CharField(max_length=40, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        Question.fill_in_user(user, request.session.session_key)
        return user


class FutureProjectSignupForm(SignupWithNameForm):
    school = CharField(max_length=60, label='School', required=True)
    grade = ChoiceField(required=True, choices=GRADES)
    dream_director = ChoiceField(required=False, choices=DREAM_DIRECTORS)

    def clean_school(self):
        school = self.cleaned_data.get('school', None)
        if school is None or school == '':
            raise forms.ValidationError("School is required.")
        return school

    def clean_grade(self):
        grade = self.cleaned_data.get('grade', None)
        if grade is None or grade == '':
            raise forms.ValidationError("Grade is required.")
        return grade

    def signup(self, request, user):
        user.school = self.cleaned_data['school']
        user.grade = self.cleaned_data['grade']
        user.dream_director = self.cleaned_data['dream_director']
        user.save()
        Question.fill_in_user(user, request.session.session_key)
        return user


# Most of the code taken from django.contrib.auth.forms.py
class MobileAuthenticationForm(forms.Form):
    phone_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'autofocus': ''}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct mobile number and password. Note that password "
            "field may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(MobileAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')

        if phone_number and password:
            self.user_cache = authenticate(phone_number=phone_number, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class MobileSignUpForm(FutureProjectSignupForm):
    phone_number = forms.CharField(max_length=16)
    password = forms.CharField(widget=PasswordInput, validators=[])

    def __init__(self, *args, **kwargs):
        super(FutureProjectSignupForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # password2 = self.cleaned_data.get("password2")
        # if password1 and password2 and password1 != password2:
        #     raise forms.ValidationError(
        #         self.error_messages['password_mismatch'],
        #         code='password_mismatch',
        #     )
        self.instance.username = self.cleaned_data.get('phone_number')
        self.instance.is_active = False
        password_validation.validate_password(password, self.instance)
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # remove all '+' except 1st one
            i = 0
            while phone_number[i] == '+' and i < len(phone_number):
                i += 1
            if i != 0:
                phone_number = phone_number[i - 1:]
        try:
            _ = int(phone_number)
        except ValueError:
            phone_number = None
        if phone_number:
            return phone_number
        raise forms.ValidationError("Entered phone number number is invalid")


class MobilePasswordResetForm(forms.Form):
    phone_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'autofocus': ''}),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False)


class OtpForm(forms.Form):
    otp = forms.CharField(label="OTP")

    def __init__(self, request=None, *args, **kwargs):
        super(OtpForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if otp == self.request.session['otp']:
            return otp
        raise forms.ValidationError("Entered OTP is not valid")
