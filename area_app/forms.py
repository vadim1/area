from django.forms import CharField, Form
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


# TODO - create custom fields for Future Project
class FutureProjectSignupForm(SignupWithNameForm):
    dream_director = CharField(max_length=60, label='Dream Director')

    def signup(self, request, user):
        user.dream_director = self.cleaned_data['dream_director']
        user.save()
        Question.fill_in_user(user, request.session.session_key)
        return user
