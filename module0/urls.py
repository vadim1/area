from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^$', views.intro, name='Module 1'),
    url(r'^intro/?$', views.intro, name='Module 1'),
    url(r'^restart/?', views.restart, name='Module 1 Restart'),
    url(r'^review/?$', views.review, name='Module 1 Review'),
    url(r'^map/?$', views.map, name='Module 1 Map'),
    url(r'^instructions/?$', views.instructions, name='Module 1 Instructions'),
    url(r'^psp_profiles/?$', views.psp_profiles, name='Module 1 Problem Solver Profiles'),

    url(r'^game/?$', views.game, name='Module 1 Game'),
    url(r'^archetype/?$', views.archetype, name='Module 1 Archetype'),
    url(r'^right/?$', views.right, name='Module 1 Right?'),
    url(r'^pro_con/?$', views.pro_con, name='Module 1 Pro Con'),
    url(r'^cheetah/?$', views.cheetah, name='Module 1 Cheetah Sheet'),
    url(r'^archetypes/?$', views.archetypes, name='Module 1 Archetypes'),
    url(r'^eval/?$', views.eval, name='Module 1 Evaluation'),

]
