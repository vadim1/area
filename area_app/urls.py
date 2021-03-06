from django.conf.urls import url
import views.view as views
import views.mobile_auth as mobile

urlpatterns = [
    url(r'toc/?$', views.toc, name='Table of Contents'),

    url(r'^$', views.home, name='Home'),
    url(r'^1$', views.home, name='Home'),
    url(r'^decision$', views.decision, name='Decision'),
    url(r'^2$', views.decision, name='Decision'),
    url(r'^rank', views.rank, name='Rank What Matters'),
    url(r'^3$', views.rank, name='Rank What Matters'),
    url(r'^questions', views.questions, name='Questions'),
    url(r'^4$', views.questions, name='Questions'),
    url(r'^critical_concepts', views.critical_concepts, name='Critical Concepts'),
    url(r'^ccex', views.critical_concepts_example, name='Critical Concepts Example'),
    url(r'^archetype$', views.archetype, name='Archetype'),
    url(r'^psp$', views.psp, name='Problem_Solver_Profile'),
    url(r'^psp/(?P<profile>[\w-]+)$', views.psp, name='Problem_Solver_Profile'),
    url(r'^archetype_info$', views.archetype_info, name='Archetype_Info'),
    url(r'^5$', views.archetype, name='Archetype'),
    url(r'^archetypes$', views.archetypes_list, name='Archetypes'),
    url(r'^cheetah_sheets$', views.cheetah_sheets, name='Cheetah_Sheets'),
    url(r'^cheetah_master$', views.cheetah_master, name='Cheetah_Master'),
    url(r'^action_map$', views.action_map, name='Action_Map'),
    url(r'^summary$', views.summary, name='Summary'),
    url(r'^restart$', views.restart_session, name='Restart'),
    url(r'^accounts/login/mobile', mobile.mobile_login, name="mobile_login"),
    url(r'^accounts/signup/mobile', mobile.mobile_signup, name='mobile_signup'),
    url(r'^accounts/forget-password/mobile', mobile.mobile_forget_password, name='mobile_forget_password'),
    url(r'^accounts/resend/otp', mobile.resend_otp, name='resend_otp'),
]
