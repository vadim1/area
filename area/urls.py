"""area URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from area_app import urls as area_app_urls
from decisions import urls as decisions_urls
from django.conf import settings
from module0 import urls as module0_urls
from module1 import urls as module1_urls
from module2 import urls as module2_urls
from module3 import urls as module3_urls
from student_class import urls as student_class_urls
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(area_app_urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^decisions/', include(decisions_urls)),
    url(r'^class/', include(student_class_urls)),
    url(r'^0/', include(module0_urls)),
    url(r'^1/', include(module1_urls)),
    url(r'^2/', include(module2_urls)),
    url(r'^3/', include(module3_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
