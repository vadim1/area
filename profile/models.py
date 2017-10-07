from django.db import models
from area_app.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
