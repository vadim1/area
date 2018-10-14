from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Module1 as Module, Module1Form as ModuleForm

from decisions.views import base_restart
from decisions.utils import CheetahSheet, Nylah, ViewHelper

import datetime
import json

cheetah_sheet2 = CheetahSheet()
cheetah_sheet2.num = 2
cheetah_sheet2.title = "Let's Practice Critical Concepts"

cheetah_sheet3 = CheetahSheet()
cheetah_sheet3.num = 3
cheetah_sheet3.title = "Define Success and Critical Concepts"

nylah = Nylah()

"""
Ordered list of URLs for this Module
"""
def navigation():
    urls = [
        reverse('module1_intro'),
        reverse('module1_review'),
        reverse('module1_map'),
        reverse('module1_game1_instructions'),
        reverse('module1_game1_game'),
        reverse('module1_game1_end'),
        reverse('module1_game2_game'),
        reverse('module1_game2_end'),
        reverse('module1_game2_results'),
        reverse('module1_decisions_personal'),
        reverse('module1_decisions_living'),
        reverse('module1_decisions_sample'),
        reverse('module1_cc_intro'),
        reverse('module1_cc_nylah'),
        reverse('module1_cc_nylah2'),
        reverse('module1_cc_nylah3'),
        reverse('module1_cheetah2_intro'),
        reverse('module1_cheetah2_sheet'),
        reverse('module1_maps_confidence'),
        reverse('module1_cheetah3_sheet'),
        reverse('module1_cheetah3_buddy'),
        reverse('module1_cheetah3_apply'),
        reverse('module1_summary'),
    ]

    return urls

"""
Default Page Controller
"""
@login_required
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
    context['sample_student'] = nylah
    context['mod_description'] = Module.get_description()

    return render(request, parsed['templatePath'], context)

"""
Default Form Save Handler
"""
def save_form(request, module, parsed):
    form = ModuleForm(request.POST, instance=module)
    if form.is_valid():
        form.save()
        return redirect(parsed['nextUrl'])
    else:
        print("Form on step: {0} did not validate".format(parsed['currentStep']))
        print(form.errors)

"""
Module Specific Controllers
"""
@login_required
def area(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    context = {
        'answers': ViewHelper.load_json(module.answers),
        'questions': module.game1_questions,
    }
    return render_page(request, module, parsed, context)

@login_required
def cc_deriving(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.practice_cc1 = json.dumps(request.POST.getlist('practice_cc1[]'))
        return save_form(request, module, parsed)

    context = {
        'practice_cc1': ViewHelper.load_json(module.practice_cc1),
    }
    return render_page(request, module, parsed, context)

@login_required
def cc_exploring(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.practice_cc2 = json.dumps(request.POST.getlist('practice_cc2[]'))
        return save_form(request, module, parsed)

    context = {
        'practice_cc2': ViewHelper.load_json(module.practice_cc2),
    }
    return render_page(request, module, parsed, context)

@login_required
def cheetah2_sheet(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.practice_cc1 = json.dumps(request.POST.getlist('practice_cc1[]'))
        module.practice_cc2 = json.dumps(request.POST.getlist('practice_cc2[]'))
        return save_form(request, module, parsed)

    context = {
        'practice_cc1': ViewHelper.load_json(module.practice_cc1),
        'practice_cc2': ViewHelper.load_json(module.practice_cc2),
        'cheetah_sheet': cheetah_sheet2,
    }
    return render_page(request, module, parsed, context)

@login_required
def cheetah3_report(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, 'cheetah3_apply', Module)

    context = {
        'answers': ViewHelper.load_json(module.answers),
        'cc': ViewHelper.load_json(module.cc),
        'cc_occurred': ViewHelper.load_json(module.cc_occurred),
        'cheetah_sheet': cheetah_sheet3,
        'module': module,
        'nav': parsed,
        'questions': module.game1_questions,
    }

    if parsed['currentStep'] == 'cheetah3_email':
        data = {}
        if request.user.is_authenticated():
            emails = [request.user.email]
            subject = "AREA Module {0}: Own it: Apply to real life!".format(module.display_num())
            template = 'module1/cheetah3/email.html'

            try:
                results = ViewHelper.send_html_email(emails, subject, template, context)
                msg = "Email sent to {}. [Code {}]".format(request.user.email, results)
            except Exception as e:
                if hasattr(e, 'message'):
                    print("Exception: " + e.message)
                else:
                    print("Exception: " + e)

                msg = "Unable to send email. There was an internal server error. Try again later."
        else:
            msg = "User is not authenticated. Cannot send email."

        data['message'] = msg
        print("Email: {0} to {1}".format(data['message'], request.user.email))
        return JsonResponse(data)

    return render_page(request, module, parsed, context)

@login_required
def cheetah3_sheet(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.cc = json.dumps(request.POST.getlist('cc[]'))
        module.cc_occurred = json.dumps(request.POST.getlist('cc_occurred[]'))
        return save_form(request, module, parsed)

    context = {
        'cc': ViewHelper.load_json(module.cc),
        'cc_occurred': ViewHelper.load_json(module.cc_occurred),
        'cheetah_sheet': cheetah_sheet3,
    }
    return render_page(request, module, parsed, context)

@login_required
def decisions_personal(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.why = json.dumps(request.POST.getlist('why[]'))
        return save_form(request, module, parsed)

    context = {
        'why': ViewHelper.load_json(module.why),
    }
    return render_page(request, module, parsed, context)

@login_required
def decisions_sample(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.sample_cc = json.dumps(request.POST.getlist('sample_cc[]'))
        return save_form(request, module, parsed)

    context = {
        'sample_cc': ViewHelper.load_json(module.sample_cc),
    }
    return render_page(request, module, parsed, context)

@login_required
def challenge(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.cc = json.dumps(request.POST.getlist('cc[]'))
        module.cc_not = json.dumps(request.POST.getlist('cc_not[]'))
        return save_form(request, module, parsed)

    context = {
        'cc': ViewHelper.load_json(module.cc),
        'cc_not': ViewHelper.load_json(module.cc_not),
    }
    return render_page(request, module, parsed, context)

@login_required
def game(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        attr = request.POST.get('attr')
        attrs = []
        answers = {}
        if module.answers:
            answers = ViewHelper.load_json(module.answers)
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
        return redirect(parsed['nextUrl'])
    else:
        print(parsed['section'])
        if parsed['section'] == 'game1':
            clear_game_answers(module)  # TODO - save old answers
            attr = 'easy'
            pageTitle = 'Is this decision EASY or HARD?'
        else:
            attr = 'confident'
            pageTitle = 'Are you CONFIDENT or UNSURE about this decision?'

    return render(request, parsed['prefix']+'game.html', {
        'module': module,
        'nav': parsed,
        'attr': attr,
        'labels': module.game_labels()[attr],
        'num_questions': len(module.game1_questions()),
        'pageTitle': pageTitle,
        'questions': module.game1_questions().values(),
    })

@login_required
def map(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    context = {
        'display_mode': 'all',
        'btn_label': 'Shall We Play A Game?',
    }
    return render_page(request, module, parsed, context)

@login_required
def restart(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    return base_restart(request, Module, parsed['prefix'])

@login_required
def summary(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.completed_on = datetime.datetime.now()
        module.save()
        return redirect(reverse('decisions_home'))

    context = {}

    return render_page(request, module, parsed, context)

"""
Module Specific Utilities
"""
def clear_game_answers(module):
    if module.answers:
        module.answers = json.dumps({})
        module.save()