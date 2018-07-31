from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^$', views.intro, name='Module 0'),
    url(r'^intro/?$', views.intro, name='Module 0'),
    url(r'^restart/?', views.restart, name='Module 0 Restart'),
    url(r'^review/?$', views.review, name='Module 0 Review'),
    url(r'^map/?$', views.map, name='Module 0 Map'),
    url(r'^instructions/?$', views.instructions, name='Module 0 Instructions'),

    url(r'^game/?$', views.game, name='Module 0 Game'),
    url(r'^archetype/?$', views.archetype, name='Module 0 Archetype'),
    url(r'^right/?$', views.right, name='Module 0 Right?'),
    url(r'^pro_con/?$', views.pro_con, name='Module 0 Pro Con'),
    url(r'^cheetah/?$', views.cheetah, name='Module 0 Cheetah Sheet'),
    url(r'^archetypes/?$', views.archetypes, name='Module 0 Archetypes'),
    url(r'^eval/?$', views.eval, name='Module 0 Evaluation'),

    url(r'^summary/?$', views.summary, name='Module 0 Summary'),
]
