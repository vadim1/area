from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Module0 as Module, Module0Form as ModuleForm

from decisions.views import base_restart, base_review
from decisions.utils import CheetahSheet, ViewHelper
from area_app.views.view import get_randomized_questions, compute_archetype

from decisions.decorator import active_user_required

import datetime
import json

"""
Ordered list of URLs for this Module
"""
def navigation():
    urls = [
        reverse('module0_intro'),
        reverse('module0_map'),
        reverse('module0_game1_instructions'),
        reverse('module0_game1_profiles'),
        reverse('module0_game1_game'),
        reverse('module0_your_psp_intro'),
        reverse('module0_your_psp_strengths'),
        reverse('module0_your_psp_blind_spots'),
        reverse('module0_your_psp_right'),
        reverse('module0_your_psp_archetypes'),
        reverse('module0_cheetah1_intro'),
        reverse('module0_cheetah1_sheet'),
        reverse('module0_cheetah1_apply'),
        reverse('module0_summary'),
    ]

    return urls

"""
Default Page Controller
"""
@active_user_required
def generic_page_controller(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        return save_form(request, module, parsed)

    return render_page(request, module, parsed, {})

"""
Default Render Page Handler
"""
def render_page(request, module, parsed, context={}):
    context['is_mobile'] = ViewHelper.is_mobile(request)
    context['module'] = module
    context['nav'] = parsed

    return render(request, parsed['templatePath'], context)

"""
Default Form Save Handler
"""
def save_form(request, module, parsed):
    form = ModuleForm(request.POST, instance=module)
    if form.is_valid():
        form.save()
        print("Form saved. Redirecting to {0}".format(parsed['nextUrl']))
        return redirect(parsed['nextUrl'])
    else:
        print("Form on step: {0} did not validate".format(parsed['currentStep']))
        print(form.errors)

"""
Module Specific Controllers
"""
@active_user_required
def cheetah1_report(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    cheetah_sheet = CheetahSheet()

    context = {
        'ca': ViewHelper.load_json(module.cheetah_answers),
        'cheetah_sheet': cheetah_sheet,
        'module': module,
        'nav': parsed,
    }

    if parsed['currentStep'] == 'cheetah1_email':
        data = {}
        if request.user.is_authenticated():
            emails = [request.user.email]
            subject = "AREA Module {0}: Own it: Apply to real life!".format(module.display_num())
            template = 'module0/cheetah1/email.html'

            try:
                results = ViewHelper.send_html_email(emails, subject, template, context)
                msg = "Email sent to {}. [Code {}]".format(request.user.email, results)
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)

                msg = "Unable to send email. There was a server error."
        else:
            msg = "User is not authenticated. Cannot send email."

        data['message'] = msg
        return JsonResponse(data)

    return render_page(request, module, parsed, context)

@active_user_required
def cheetah1_sheet(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    cheetah_sheet = CheetahSheet()

    if request.method == 'POST':
        module.cheetah_answers = json.dumps(request.POST.getlist('ca[]'))
        return save_form(request, module, parsed)

    context = {
        'ca': ViewHelper.load_json(module.cheetah_answers),
        'cheetah_sheet': cheetah_sheet,
    }
    return render_page(request, module, parsed, context)

@active_user_required
def game1_game(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module0 = ViewHelper.load_module(request, parsed['currentStep'], Module)
    questions_yes = None

    if request.method == 'POST':
        # Save any questions that were answered 'Yes'
        questions_yes = request.POST.getlist('question[]')
        request.session['questions_yes'] = questions_yes
        module0.answers = questions_yes
        top_archetype = compute_archetype(request)
        request.session['arch'] = top_archetype
        module0.archetype = top_archetype

        # compute_archetype calculates all of the scores but only returns the first one
        # the rest are stored in a session var called 'archetypes'
        if 'archetypes' in request.session:
            # extract everything but the first element
            archetypes = request.session['archetypes']
            print(archetypes)
            module0.other_archetypes = archetypes[1:]

        module0.save()
        return redirect(parsed['nextUrl'])
    else:
        # Retrieve any previously stored questions for this user
        # However, this is stored as a unicode array e.g.
        # [u'Ans1', u'Ans2'], so convert it first to a list
        # before passing it to the view
        if questions_yes is None:
            questions_yes = []

        asciidata = Module.to_ascii(module0.answers)
        questions_yes = asciidata.split(",")
        questions_yes = [x.strip() for x in questions_yes]
        request.session['questions_yes'] = questions_yes

    return render(request, parsed['templatePath'], {
        'questions': get_randomized_questions(),
        'questions_yes': questions_yes,
        'module': module0,
        'nav': parsed,
    })

@active_user_required
def map(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    context = {
        'display_mode': 'all',
        'btn_label': 'Shall We Play A Game?',
    }
    return render_page(request, module, parsed, context)

@active_user_required
def summary(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.completed_on = datetime.datetime.now()
        module.save()
        # Increment the access counter
        ViewHelper.update_view_counter(request.user)
        return redirect(reverse('decisions_home'))

    context = {}
    return render_page(request, module, parsed, context)

@active_user_required
def restart(request):
    parsed = ViewHelper.parse_request_path(request, navigation())

    return base_restart(request, Module, parsed['prefix'])