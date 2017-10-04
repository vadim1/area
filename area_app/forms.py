from django.forms import CharField, Form, ChoiceField, EmailField, PasswordInput
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
    email = EmailField(required=True)
    password = CharField(max_length=32, widget=PasswordInput)
    school = CharField(max_length=60, label='School', required=True)
    grade = ChoiceField(required=True, choices=(('', '-'),
                                                ('9', '9'),
                                                ('10', '10'),
                                                ('11', '11'),
                                                ('12', '12'),
                                                ))
    dream_director = ChoiceField(required=False, choices=(('', '-'),
                                                ('ben.kimmerle', 'Ben'),
                                                ('carrie.sangiovanni', 'Carrie'),
                                                ('christian.shaboo', 'Christian'),
                                                ('jessica.valoris', 'Jess'),
                                                ('justin.zeigler', 'Justin'),
                                                ('lamarr.womble', 'Lamarr'),
                                                ('malia.west', 'Malia'),
                                                ('nikhita', 'Nikhita'),
                                                ('paula.ramirez', 'Paula'),
                                                ('scotty.crowe', 'Scotty'),
                                                ('william.jenkins', 'William'),
                                                ('zaki', 'Zaki'),
                                                ))

    def signup(self, request, user):
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password']
        user.school = self.cleaned_data['school']
        user.grade = self.cleaned_data['grade']
        user.dream_director = self.cleaned_data['dream_director']
        user.save()
        Question.fill_in_user(user, request.session.session_key)
        return user
