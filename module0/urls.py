from django.conf.urls import url, include
from django.views.generic import RedirectView
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='module1_intro', permanent=True)),

    url(r'^intro/?$', views.module0_controller, name='module1_intro'),
    url(r'^map/?$', views.module0_controller, name='module1_map'),
    url(r'^instructions/?$', views.module0_controller, name='module1_instructions'),
    url(r'^psp_profiles/?$', views.module0_controller, name='module1_psp_profiles'),
    url(r'^game/?$', views.game, name='module1_game'),
    url(r'^archetype/?$', views.module0_controller, name='module1_archetype'),
    url(r'^pro_con/?$', views.module0_controller, name='module1_pro_con'),
    url(r'^right/?$', views.module0_controller, name='module1_right'),
    url(r'^archetypes/?$', views.module0_controller, name='module1_archetypes'),
    url(r'^cheetah/?$', views.module0_controller, name='module1_cheetah'),
    url(r'^eval/?$', views.module0_controller, name='module1_eval'),
    url(r'^review/?$', views.module0_controller, name='module1_review'),

    url(r'^restart/?', views.restart, name='module1_restart'),
]
