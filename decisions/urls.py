from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^$', views.home, name='decisions_home'),

    # TODO: clean up. Not sure if we're using
    url(r'^tour/?$', views.tour, name='Tour'),
    url(r'^journal/?$', views.journal, name='Journal'),
    url(r'^terms_conditions/?$', views.terms_conditions, name='Terms and Conditions'),
    url(r'^checkout/?$', views.checkout, name='Checkout'),
    url(r'^limit_reached/?$', views.limit_reached, name='decisions_limit_reached'),
    url(r'^take_survey/?$', views.take_survey, name='take_survey'),
]
