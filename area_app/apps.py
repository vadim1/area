from __future__ import unicode_literals

from django.apps import AppConfig


class AreaAppConfig(AppConfig):
    name = 'area_app'

    def ready(self):
        from .signals import create_user_profile
