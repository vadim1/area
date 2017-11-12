from django.conf import settings


def global_settings(request):
    base_template = 'base.html'
    if settings.SITE_NAME == 'fp':
        base_template = 'decisions/base.html'
    return {
        'SITE_NAME': settings.SITE_NAME,
        'base_template': base_template,
    }
