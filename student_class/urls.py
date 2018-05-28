from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$', views.home, name='Student Class'),
    url(r'^show/(\d+)$', views.show, name='Student Class'),
    url(r'^(\d+)$', views.show, name='Student Class'),
    url(r'^create$', views.create, name='Create Student Class'),
    url(r'^(\d+)/join', views.join, name='Join Student Class'),
    url(r'^(\d+)/leave', views.leave, name='Leave Student Class'),
    url(r'^(\d)/delete$', views.delete, name='Delete Student Class'),
    url(r'^(\d+)/close$', views.close, name='Close Student Class'),
    url(r'^(\d+)/reopen$', views.reopen, name='Reopen Student Class'),
    url(r'^student/(\d+)$', views.student, name='Student'),
]
