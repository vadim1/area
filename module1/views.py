from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Module1 as Module, Module1Form as ModuleForm

from decisions.views import base_restart
from decisions.modules import load_json, load_module, parse_request_path

import datetime
import json

"""
Ordered list of URLs for this Module
"""
def navigation():
    urls = [
        'intro',
        'review',
        'map',
        'game1/instructions',
        'game1/game',
        'game1/end',
        'game2/instructions',
        'game2/game',
        'game2/end',
        'game_results',
        'area',
        'decisions/directions',
        'maps/self_awareness',
        'decisions/personal',
        'decisions/living',
        'decisions/sample',
        'maps/vision',
        'cc',
        'cc/nylah',
        'cc/cheetah',
        'cc/deriving',
        'cc/exploring',
        'maps/confidence',
        'decision',
        'success',
        'maps/conviction',
        'conviction',
        'building',
        'challenge',
        'buddy',
        'commitment',
        'summary'
    ]

    return urls

"""
Default Page Controller
"""
@login_required
def generic_page_controller(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        return save_form(request, module, parsed)

    return render_page(request, module, parsed, {})

"""
Default Render Page Handler
"""
def render_page(request, module, parsed, context={}):
    context['module'] = module
    context['nav'] = parsed
    context['mod_description'] = Module.get_description()

    return render(request, parsed['templatePath'], context)

"""
Default Form Save Handler
"""
def save_form(request, module, parsed):
    form = ModuleForm(request.POST, instance=module)
    if form.is_valid():
        form.save()
        return redirect(parsed['urlPrefix'] + parsed['nextUrl'])
    else:
        print("Form on step: {0} did not validate".format(parsed['currentStep']))
        print(form.errors)

"""
Module Specific Controllers
"""
@login_required
def area(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    context = {
        'answers': module.answers_json,
        'questions': module.game1_questions,
    }
    return render_page(request, module, parsed, context)

@login_required
def cc_exploring(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.cc1_list = json.dumps(request.POST.getlist('cc1[]'))
        module.cc2_list = json.dumps(request.POST.getlist('cc2[]'))
        save_form(request, module, parsed)

    context = {
        'cc1_list': load_json(module.cc1_list),
        'cc2_list': load_json(module.cc2_list),
    }
    return render_page(request, module, parsed, context)

@login_required
def challenge(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.cc = json.dumps(request.POST.getlist('cc[]'))
        module.cc_not = json.dumps(request.POST.getlist('cc_not[]'))
        save_form(request, module, parsed)

    context = {
        'cc': load_json(module.cc),
        'cc_not': load_json(module.cc_not),
    }
    return render_page(request, module, parsed, context)

@login_required
def commitment(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        return redirect(parsed['urlPrefix'] + parsed['nextUrl'])

    # Build out mailto link
    mail_body = module.decision_buddy + ',' + '%0D%0D' + \
                'Please help me with a big decision: ' + module.decision + '%0D%0D'
    for concept in load_json(module.cc):
        mail_body += concept + '%0D'

    mail_body += '%0D' + \
                'Would you help me get started?  Here are a few questions I need to answer:' + '%0D%0D' + \
                'What are the organizations involved in your decision?' + '%0D' + \
                'Who are the people who could help you make your decision?' + '%0D' + \
                'What do you need to find out?' + '%0D' + \
                'How will getting information help you make your decision?' + '%0D%0D' + \
                'Thank you!'
    to = module.decision_buddy_email + ',' + request.user.email

    return render(request, parsed['templatePath'], {
        'module': module,
        'nav': parsed,
        'cc': load_json(module.cc),
        'mail_body': mail_body,
        'to': to,
    })

@login_required
def game(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        attr = request.POST.get('attr')
        attrs = []
        answers = {}
        if module.answers:
            answers = load_json(module.answers)
        for i in range(0, len(module.game1_questions().values())):
            index = str(i)
            question_i = module.game1_questions().values()[i]
            attr_i = request.POST.get('answer[' + index + ']')
            attrs.append(attr_i)
            if question_i not in answers:
                answers[question_i] = {
                    'title': module.game1_questions().keys()[i]
                }
            answers[question_i][attr] = attr_i

        module.answers = json.dumps(answers)
        module.save()
        return redirect(parsed['urlPrefix'] + parsed['nextUrl'])
    else:
        if parsed['section'] == 'game1':
            clear_game_answers(module)  # TODO - save old answers
            attr = 'easy'
        else:
            attr = 'confident'

    return render(request, parsed['prefix']+'game.html', {
        'module': module,
        'nav': parsed,
        'attr': attr,
        'labels': module.game_labels()[attr],
        'num_questions': len(module.game1_questions()),
        'answers': module.answers_json,
        'questions': module.game1_questions().values(),
    })

@login_required
def map(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    context = {
        'display_mode': 'all',
    }
    return render_page(request, module, parsed, context)

@login_required
def restart(request):
    parsed = parse_request_path(request, navigation())
    return base_restart(request, Module, parsed['prefix'])

@login_required
def success(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.cc = json.dumps(request.POST.getlist('cc[]'))
        save_form(request, module, parsed)

    context = {
        'cc': load_json(module.cc),
    }
    return render_page(request, module, parsed, context)

@login_required
def summary(request):
    parsed = parse_request_path(request, navigation())
    module = load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.completed_on = datetime.datetime.now()
        module.save()
        return redirect('/decisions')

    return render_page(request, module, parsed, context)

"""
Module Specific Utilities
"""
def clear_game_answers(module):
    if module.answers:
        module.answers = json.dumps({})
        module.save()