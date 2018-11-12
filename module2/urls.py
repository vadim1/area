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

    url(r'^bias/shortcuts/$', views.generic_page_controller, name='module2_bias_shortcuts'),
    url(r'^bias/pro_con/$', views.generic_page_controller, name='module2_bias_pro_con'),
    url(r'^bias/remedies/$', views.generic_page_controller, name='module2_bias_remedies'),

    # Cheetah Sheet
    url(r'^cheetah4/intro/$', views.generic_page_controller, name='module3_cheetah4_intro'),
    #url(r'^cheetah4/sheet/?$', views.cheetah4_sheet, name='module3_cheetah4_sheet'),
    url(r'^cheetah4/apply/?$', views.cheetah4_report, name='module3_cheetah4_apply'),

    url(r'^summary/?$', views.summary, name='module3_summary'),

    # Other Module-specific URLs
    url(r'^cheetah4/email/?$', views.cheetah4_report, name='module3_cheetah4_email'),
    url(r'^cheetah4/print/?$', views.cheetah4_report, name='module3_cheetah4_print'),
    url(r'^restart/?$', views.restart, name='module3_restart'),
]
