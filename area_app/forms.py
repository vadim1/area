from allauth.account.forms import SignupForm
from django.forms import TextInput


# TODO - create custom fields for Future Project
class FutureProjectSignupForm(SignupForm):
    dream_director = TextInput()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignupForm, self).__init__(*args, **kwargs)
