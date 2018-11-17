from django.conf.urls import url, include
from django.views.generic import RedirectView
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='module2_intro', permanent=True)),

    url(r'^intro/?$', views.generic_page_controller, name='module2_intro'),
    url(r'^review/?$', views.review, name='module2_review'),
    url(r'^map/?$', views.show_map, name='module2_map'),

    url(r'^game1/instructions/?$', views.generic_page_controller, name='module2_game1_instructions'),
    url(r'^game1/game/?$', views.game, name='module2_game1_game'),
    url(r'^explain/?$', views.generic_page_controller, name='module2_explain'),
    url(r'^bias/?$', views.generic_page_controller, name='module2_bias'),
    url(r'^game1/results/?$', views.game1_results, name='module2_game1_results'),

    url(r'^game2/instructions/?$', views.generic_page_controller, name='module2_game2_instructions'),
    url(r'^game2/game/$', views.game2_game, name='module2_game2_game'),

    # Cheetah Sheet 4
    url(r'^cheetah4/intro/$', views.generic_page_controller, name='module2_cheetah4_intro'),
    url(r'^cheetah4/sheet/?$', views.cheetah4_sheet, name='module2_cheetah4_sheet'),

    url(r'^bias/shortcuts/$', views.generic_page_controller, name='module2_bias_shortcuts'),
    url(r'^bias/pro_con/$', views.generic_page_controller, name='module2_bias_pro_con'),
    url(r'^bias/remedies/$', views.generic_page_controller, name='module2_bias_remedies'),
    url(r'^bias/practice/$', views.bias_remedies_practice, name='module2_bias_practice'),

    # Cheetah Sheet 5
    url(r'^cheetah5/sheet/?$', views.cheetah5_sheet, name='module2_cheetah5_sheet'),
    url(r'^cheetah5/apply/?$', views.cheetah5_report, name='module2_cheetah5_apply'),

    url(r'^summary/?$', views.summary, name='module2_summary'),

    # Other Module-specific URLs
    url(r'^cheetah5/email/?$', views.cheetah5_report, name='module2_cheetah5_email'),
    url(r'^cheetah5/print/?$', views.cheetah5_report, name='module2_cheetah5_print'),
    url(r'^restart/?$', views.restart, name='module2_restart'),
]
