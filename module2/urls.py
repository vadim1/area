from django.conf.urls import url, include
from django.views.generic import RedirectView
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='module2_intro', permanent=True)),

    url(r'^intro/?$', views.generic_page_controller, name='module2_intro'),
    url(r'^review/?$', views.review, name='module2_review'),
    url(r'^map/?$', views.map, name='module2_map'),

    url(r'^game1/instructions/?$', views.generic_page_controller, name='module2_game1_instructions'),
    url(r'^game1/game/?$', views.game, name='module2_game1_game'),
    url(r'^explain/?$', views.generic_page_controller, name='module2_explain'),
    url(r'^bias/?$', views.generic_page_controller, name='module2_bias'),
    url(r'^game1/results/?$', views.game1_results, name='module2_game1_results'),

    url(r'^game2/instructions/?$', views.generic_page_controller, name='module2_game2_instructions'),
    url(r'^game2/game/$', views.game2_game, name='module2_game2_game'),

    url(r'^nylah/1/$', views.generic_page_controller, name='module2_nylah_1'),
    url(r'^nylah/2/$', views.generic_page_controller, name='module2_nylah_2'),
    url(r'^nylah/3/$', views.nylah_3, name='module2_nylah_3'),
    url(r'^nylah/4/$', views.generic_page_controller, name='module2_nylah_4'),

    url(r'^pin2/instructions/$', views.generic_page_controller, name='module2_pin2_instructions'),
    url(r'^pin2/2/$', views.generic_page_controller, name='module2_pin2_2'),

    url(r'^pin3/instructions/$', views.generic_page_controller, name='module2_pin3_instructions'),
    url(r'^pin3/2/$', views.generic_page_controller, name='module2_pin3_2'),
    url(r'^pin3/3/$', views.pin3_3, name='module2_pin3_3'),

    # Perspective-taking
    url(r'^pin4$', RedirectView.as_view(pattern_name='module3_pin4_instructions', permanent=True)),
    url(r'^pin4/instructions/$', views.generic_page_controller, name='module3_pin4_instructions'),
    url(r'^pin4/2/$', views.pin4_2, name='module3_pin4_2'),
    url(r'^pin4/3/$', views.generic_page_controller, name='module3_pin4_3'),
    url(r'^pin4/4/$', views.pin4_4, name='module3_pin4_4'),

    # Cheetah Sheet
    url(r'^cheetah$', RedirectView.as_view(pattern_name='module3_cheetah_introduction', permanent=True)),
    url(r'^cheetah/introduction/$', views.generic_page_controller, name='module3_cheetah_introduction'),
    url(r'^cheetah/2/$', views.cheetah_2, name='module3_cheetah_2'),
    url(r'^cheetah/cc_edit/$', views.cc_edit, name='module3_cheetah_cc_edit'),
    # Takes in query string params ?num=X
    url(r'^cheetah/3/?$', views.cheetah_3, name='module3_cheetah_3'),
    url(r'^cheetah/4/$', views.cheetah_4, name='module3_cheetah_4'),

    url(r'^eval/?$', views.eval, name='module3_eval'),
    url(r'^summary/?$', views.summary, name='module3_summary'),

    url(r'^restart/?$', views.restart, name='module3_restart'),
]
