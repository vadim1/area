from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module0 as Module
from decisions.views import load_module, load_json, base_intro, base_instructions, base_map, base_restart,\
    base_review, base_summary
from area_app.views.view import get_randomized_questions, compute_archetype

import datetime
import json

# template location
prefix = "module" + str(Module.num()) + "/"
# url location
url_prefix = "/" + str(Module.num()) + "/"

def load_this_module(request, step=None):
    return load_module(request, Module, step)

# Page order
# intro
# map
# instructions
# psp_profiles
# game (quiz)
# archetype
# pro_con
# right
# archetypes
# cheetah
# eval (cheetah sheet 1)
# review

@login_required
def intro(request):
    return base_intro(request, Module, prefix)

@login_required
def map(request):
    return base_map(request, Module, prefix)

@login_required
def instructions(request):
    return base_instructions(request, Module, prefix)

@login_required
def psp_profiles(request):
    module0 = load_this_module(request, 'psp_profiles')
    return render(request, prefix + 'psp_profiles.html', {
        'module': module0,
        'archetype': module0.archetype,
    })

@login_required
def game(request):
    module0 = load_this_module(request, 'game')
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
        return redirect(url_prefix + 'archetype')
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

    return render(request, prefix + 'game.html', {
        'questions': get_randomized_questions(),
        'questions_yes': questions_yes,
        'module': module0,
    })

@login_required
def archetype(request):
    module0 = load_this_module(request, 'archetype')
    return render(request, prefix + 'decisions_archetype.html', {
        'archetype': module0.archetype,
    })

@login_required
def pro_con(request):
    module0 = load_this_module(request, 'pro_con')
    return render(request, prefix + 'pro_con.html', {
        'archetype': module0.archetype,
        'module': module0
    })

@login_required
def right(request):
    module0 = load_this_module(request, 'right')
    if request.method == 'POST':
        psp_correct = request.POST.get('agree')
        module0.psp_correct = psp_correct
        module0.save()
        return redirect(url_prefix + 'archetypes')
    return render(request, prefix + 'right.html', {
        'archetype': module0.archetype,
        'module': module0
    })

@login_required
def archetypes(request):
    module0 = load_this_module(request, 'archetypes')
    return render(request, prefix + 'decisions_archetypes.html', {
        'archetype': module0.archetype,
        'module': module0
    })

@login_required
def cheetah(request):
    module0 = load_this_module(request, 'cheetah')
    return render(request, prefix + 'cheetah.html', {
        'archetype': module0.archetype,
        'module': module0
    })

@login_required
def eval(request):
    module0 = load_this_module(request, 'eval')

    if request.method == 'POST':
        # Save any questions that were answered 'Yes'
        cheetah_answers = json.dumps(request.POST.getlist('ca[]'))
        module0.cheetah_answers = cheetah_answers
        module0.save()

        return redirect(url_prefix + 'review')
    else:
        cheetah_answers = load_json(module0.cheetah_answers)

    return render(request, prefix + 'eval.html', {
        'archetype': module0.archetype,
        'module': module0,
        'ca': cheetah_answers,
    })

@login_required
def review(request):
    module0 = load_this_module(request, 'review')
    if request.method == 'POST':
        module0.completed_on = datetime.datetime.now()
        module0.save()
        return redirect('/decisions')

    return base_review(request, Module, None, {}, prefix)

@login_required
def restart(request):
    return base_restart(request, Module, prefix)
