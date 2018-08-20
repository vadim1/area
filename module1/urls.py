from django.conf.urls import url, include
from django.views.generic import RedirectView
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='module2_intro', permanent=True)),

    url(r'^intro/?$', views.generic_page_controller, name='module2_intro'),
    url(r'^previous_review/?$', views.generic_page_controller, name='module2_previous_review'),
    url(r'^map/?$', views.generic_page_controller, name='module2_map'),

    url(r'^game1/instructions/?$', views.game_controller, name='module2_game1_instructions'),
    url(r'^game1/game/?$', views.game_controller, name='module2_game1_instructions'),
    url(r'^game1/end/?$', views.game_controller, name='module2_game1_end'),
    url(r'^game2/instructions/?$', views.game_controller, name='module2_game2_instructions'),
    url(r'^game2/game/?$', views.game_controller, name='module2_game2_game'),
    url(r'^game2/end/?$', views.game_controller, name='module2_game2_end'),

    url(r'^game_results/?$', views.game_results, name='module2_game_results'),

    url(r'^area/?$', views.area, name='module2_area'),
    url(r'^decisions/directions/?$', views.decisions_controller, name='module2_decisions_directions'),
    url(r'^decisions/details/?$', views.decisions_controller, name='module2_decisions_details'),
    url(r'^decisions/living/?$', views.decisions_controller, name='module2_decisions_living'),
    url(r'^decisions/sample/?$', views.decisions_controller, name='module2_decisions_sample'),

    url(r'^cc/?$', views.generic_page_controller, name='module2_cc'),
    url(r'^cc/nylah/?$', views.generic_page_controller, name='module2_cc_nylah'),
    url(r'^cc/deriving/?$', views.cc_controller, name='module2_cc_deriving'),
    url(r'^cc/exploring/?$', views.cc_controller, name='module2_cc_exploring'),

    url(r'^decision/?$', views.generic_page_controller, name='module2_decision'),
    url(r'^cheetah/?$', views.generic_page_controller, name='module2_cheetah'),
    url(r'^challenge/?$', views.generic_page_controller, name='module2_challenge'),
    url(r'^buddy/?$', views.generic_page_controller, name='module2_buddy'),

    url(r'^commitment/?$', views.commitment, name='module2_commitment'),
    url(r'^summary/?$', views.summary, name='module2_summary'),

    url(r'^restart/?', views.restart, name='module2_restart'),
]
