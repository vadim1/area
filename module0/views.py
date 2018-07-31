from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module0 as Module, Course
from decisions.views import load_module, base_intro, base_instructions, base_map, base_restart,\
    base_review, base_summary
from area_app.views.view import get_randomized_questions, compute_archetype


prefix = "decisions/module" + str(Module.num()) + "/"


def load_this_module(request, step=None):
    return load_module(request, Module, step)


@login_required
def intro(request):
    return base_intro(request, Module, prefix)


@login_required
def review(request):
    return base_review(request, Module, None, {}, prefix)


@login_required
def map(request):
    return base_map(request, Module, prefix)


@login_required
def instructions(request):
    return base_instructions(request, Module, prefix)


@login_required
def summary(request):
    module0 = load_this_module(request, 'summary')
    return base_summary(request, Module, {
        'archetype': module0.archetype,
    }, prefix)


@login_required
def restart(request):
    return base_restart(request, Module, prefix)


"""

Module Specific Pages

"""


@login_required
def game(request):
    module0 = load_this_module(request, 'game')
    questions_yes = None
    if request.method == 'POST':
        questions_yes = request.POST.getlist('question[]')
        request.session['questions_yes'] = questions_yes
        module0.answers = questions_yes
        top_archetype = compute_archetype(request)
        request.session['arch'] = top_archetype
        module0.archetype = top_archetype
        module0.save()
        return redirect('/' + str(Module.num()) + 'archetype')
    return render(request, 'decisions/module0/game.html', {
        'questions': get_randomized_questions(),
        'questions_yes': questions_yes,
    })


@login_required
def archetype(request):
    module0 = load_this_module(request, 'archetype')
    return render(request, 'decisions/module0/decisions_archetype.html', {
        'archetype': module0.archetype,
    })


@login_required
def right(request):
    module0 = load_this_module(request, 'archetype')
    if request.method == 'POST':
        psp_correct = request.POST.get('agree')
        raise Exception(psp_correct)
        module0.psp_correct = psp_correct
        module0.save()
        return redirect('/' + str(Module.num()) + '/pro_con')
    return render(request, 'decisions/module0/right.html', {
        'archetype': module0.archetype,
    })


@login_required
def pro_con(request):
    module0 = load_this_module(request, 'archetype')
    return render(request, 'decisions/module0/pro_con.html', {
        'archetype': module0.archetype,
    })


@login_required
def cheetah(request):
    # TODO
    module0 = load_this_module(request, 'archetype')
    return render(request, 'decisions/module0/decisions_archetype.html', {
        'archetype': module0.archetype,
    })


@login_required
def archetypes(request):
    module0 = load_this_module(request, 'archetypes')
    return render(request, 'decisions/module0/decisions_archetypes.html', {
        'archetype': module0.archetype,
    })


@login_required
def eval(request):
    # TODO
    module0 = load_this_module(request, 'archetype')
    return render(request, 'decisions/module0/decisions_archetype.html', {
        'archetype': module0.archetype,
    })
