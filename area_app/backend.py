from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class MobileAuthenticationBackend(ModelBackend):
    def authenticate(self, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
