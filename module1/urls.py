from django.conf.urls import url, include
from django.views.generic import RedirectView
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='module1_intro', permanent=True)),

    url(r'^intro/?$', views.generic_page_controller, name='module1_intro'),
    url(r'^review/?$', views.generic_page_controller, name='module1_review'),
    url(r'^map/?$', views.map, name='module1_map'),

    # Self-Awareness
    url(r'^game1/instructions/?$', views.generic_page_controller, name='module1_game1_instructions'),
    url(r'^game1/game/?$', views.game, name='module1_game1_game'),
    url(r'^game1/end/?$', views.generic_page_controller, name='module1_game1_end'),
    url(r'^game2/game/?$', views.game, name='module1_game2_game'),
    url(r'^game2/end/?$', views.generic_page_controller, name='module1_game2_end'),
    url(r'^game2/results/?$', views.area, name='module1_game2_results'),
    url(r'^decisions/personal/?$', views.decisions_personal, name='module1_decisions_personal'),
    url(r'^decisions/living/?$', views.generic_page_controller, name='module1_decisions_living'),
    url(r'^decisions/sample/?$', views.decisions_sample, name='module1_decisions_sample'),

    # Vision of Success
    url(r'^cc/intro/?$', views.generic_page_controller, name='module1_cc_intro'),
    url(r'^cc/nylah/?$', views.generic_page_controller, name='module1_cc_nylah'),
    url(r'^cc/nylah2/?$', views.generic_page_controller, name='module1_cc_nylah2'),
    url(r'^cc/nylah3/?$', views.generic_page_controller, name='module1_cc_nylah3'),
    url(r'^cheetah2/intro/?$', views.generic_page_controller, name='module1_cheetah2_intro'),
    url(r'^cheetah2/sheet/?$', views.cheetah2_sheet, name='module1_cheetah2_sheet'),

    # Build Your Confidence
    url(r'^maps/confidence/?$', views.generic_page_controller, name='module1_maps_confidence'),
    url(r'^cheetah3/sheet/?$', views.cheetah3_sheet, name='module1_cheetah3_sheet'),
    url(r'^cheetah3/buddy/?$', views.generic_page_controller, name='module1_cheetah3_buddy'),
    url(r'^cheetah3/apply/?$', views.cheetah3_report, name='module1_cheetah3_apply'),

    url(r'^summary/?$', views.summary, name='module1_summary'),

    # Other Module-specific URLs
    url(r'^cheetah3/email/?$', views.cheetah3_report, name='module1_cheetah3_email'),
    url(r'^cheetah3/print/?$', views.cheetah3_report, name='module1_cheetah3_print'),
    url(r'^restart/?', views.restart, name='module1_restart'),
]
