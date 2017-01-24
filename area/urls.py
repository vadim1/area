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
from django.conf.urls import url
from django.contrib import admin
from area_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='Home'),
    url(r'^decision$', views.decision, name='Decision'),
    url(r'^critical_concepts$', views.critical_concepts, name='Critical Concepts'),
    url(r'^edges_pitfalls$', views.edges_pitfalls, name='Edges and Pitfalls'),
    url(r'^cognitive_biases$', views.cognitive_biases, name='Cognitive Biases'),
    url(r'^cheetah_sheets$', views.cheetah_sheets, name='Cheetah Sheets'),
    url(r'^action_map$', views.action_map, name='Action Map'),
    url(r'^summary$', views.summary, name='Summary'),
    url(r'^restart$', views.restart_session, name='Restart'),
]
