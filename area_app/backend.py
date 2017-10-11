from django.contrib.auth.backends import ModelBackend
from .models import User


class MobileAuthenticationBackend(ModelBackend):
    def authenticate(self, phone_number=None, password=None, **kwargs):
        if phone_number and password:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                User().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
