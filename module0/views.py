from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Module0 as Module, Module0Form

from decisions.views import base_restart, base_review
from decisions.utils import ViewHelper
from area_app.views.view import get_randomized_questions, compute_archetype

import datetime
import json

"""
Module Controllers
"""
@login_required
def module0_controller(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        if parsed['section'] == 'game':
            return game(request)
        elif parsed['section'] == 'eval':
            module.cheetah_answers = json.dumps(request.POST.getlist('ca[]'))

        form = Module0Form(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect(parsed['urlPrefix'] + parsed['nextUrl'])
        else:
            print("Form on step: {0} did not validate".format(parsed['currentStep']))
            print(form.errors)
    else:
        # Add the module to the context by default
        context = {
            'module': module,
            'nav': parsed,
        }

        if parsed['section'] == 'map':
            context['display_mode'] = 'all'
        elif parsed['section'] == 'game':
            return (game(request))
        elif parsed['section'] == 'eval':
            context['ca'] = ViewHelper.load_json(module.cheetah_answers)

        return render(request, parsed['templatePath'], context)

@login_required
def game(request):
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
            module0.other_archetypes = archetypes[1:]

        module0.save()
        return redirect(parsed['urlPrefix'] + parsed['nextUrl'])
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

@login_required
def review(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.completed_on = datetime.datetime.now()
        module.save()
        return redirect('/decisions')

    return base_review(request, Module, None, {}, parsed['prefix'])

@login_required
def restart(request):
    parsed = ViewHelper.parse_request_path(request, navigation())

    return base_restart(request, Module, parsed['prefix'])

"""
Helper Utilities
"""
# Ordered list of URLs, used to calculate back and next
def navigation():
    urls = [
        'intro',
        'map',
        'instructions',
        'psp_profiles',
        'game',
        'archetype',
        'pro_con',
        'right',
        'archetypes',
        'cheetah',
        'eval',
        'summary',
    ]

    return urls