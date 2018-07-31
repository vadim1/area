from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^$', views.intro, name='Module 3'),
    url(r'^intro/?$', views.intro, name='Module 3'),
    url(r'^restart/?', views.restart, name='Module 3 Restart'),
    url(r'^review/?$', views.review, name='Module 3 Review'),
    url(r'^map/?$', views.map, name='Module 3 Map'),
    url(r'^instructions/?$', views.instructions, name='Module 3 Instructions'),

    url(r'^summary/?$', views.summary, name='Module 3 Summary'),
]
