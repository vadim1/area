from django.conf.urls import url, include
from django.views.generic import RedirectView

import views

# If you modify the order of the URLs on this file, please update the list in
# views.navigation as well
urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='module0_intro', permanent=True)),

    # Module URLs in order
    url(r'^intro/?$', views.generic_page_controller, name='module0_intro'),
    url(r'^map/?$', views.map, name='module0_map'),
    url(r'^game1/instructions/?$', views.generic_page_controller, name='module0_game1_instructions'),
    url(r'^game1/profiles/?$', views.generic_page_controller, name='module0_game1_profiles'),
    url(r'^game1/game/?$', views.game1_game, name='module0_game1_game'),
    url(r'^your_psp/intro/?$', views.generic_page_controller, name='module0_your_psp_intro'),
    url(r'^your_psp/strengths/?$', views.generic_page_controller, name='module0_your_psp_strengths'),
    url(r'^your_psp/blind_spots/?$', views.generic_page_controller, name='module0_your_psp_blind_spots'),
    url(r'^your_psp/right/?$', views.generic_page_controller, name='module0_your_psp_right'),
    url(r'^your_psp/archetypes/?$', views.generic_page_controller, name='module0_your_psp_archetypes'),
    url(r'^cheetah1/intro/?$', views.generic_page_controller, name='module0_cheetah1_intro'),
    url(r'^cheetah1/sheet/?$', views.cheetah1_sheet, name='module0_cheetah1_sheet'),
    url(r'^cheetah1/apply/?$', views.generic_page_controller, name='module0_cheetah1_apply'),
    url(r'^summary/?$', views.summary, name='module0_summary'),

    # Other Module-specific URLs
    url(r'^cheetah1/email/?$', views.cheetah1_report, name='module0_cheetah1_email'),
    url(r'^cheetah1/print/?$', views.cheetah1_report, name='module0_cheetah1_print'),
    url(r'^restart/?', views.restart, name='module0_restart'),
]
