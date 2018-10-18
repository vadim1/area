from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

from .models import Module2 as Module, Module2Form as ModuleForm
from module1.models import Module1 as PreviousModule
from decisions.views import load_json, load_module, base_restart, base_review, base_summary
from decisions.utils import ViewHelper, ExampleStudent

import datetime
import json

"""
Ordered list of URLs for this Module
"""
def navigation():
    urls = [
        reverse('module2_intro'),
        reverse('module2_review'),
        reverse('module2_map'),
        reverse('module2_game1_instructions'),
        reverse('module2_game1_game'),
        reverse('module2_explain'),
        reverse('module2_bias'),
        reverse('module2_game1_results'),
        reverse('module2_game2_instructions'),
        reverse('module2_game2_game'),
        reverse('module2_bias_shortcuts'),
        reverse('module2_bias_action'),
        reverse('module2_nylah_1'),
        reverse('module2_nylah_2'),
        reverse('module2_nylah_3'),
        reverse('module2_nylah_4'),
        reverse('module2_pin2_instructions'),
        'pin2/2',
        'pin3/instructions',
        'pin3/2',
        'pin3/3',
        'pin4/instructions',
        'pin4/2',
        'pin4/3',
        'pin4/4',
        'cheetah/introduction',
        'cheetah/2',
        'cheetah/3',
        'cheetah/4',
        'eval',
        'summary',
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
    context['module'] = module
    context['nav'] = parsed
    context['sample_student'] = ExampleStudent()
    context['biases'] = module.get_biases()

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
def cc_edit(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    # TODO: move to ViewHelper
    module1 = load_previous_module(request)

    if request.method == 'POST':
        # Save Critical Concepts in the previous module
        module1.decision = request.POST.get('decision')
        module1.cc = json.dumps(request.POST.getlist('cc[]'))
        module1.save()
        return redirect(reverse('module3_cheetah_2'))

    context = {
        'cc': ViewHelper.load_json(module1.cc),
        'module1': module1,
    }

    return render_page(request, module, parsed, context)

@login_required
def cheetah_2(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    # TODO: move to ViewHelper
    module1 = load_previous_module(request)

    context = {
        'cc': ViewHelper.load_json(module1.cc),
        'decision': module1.decision,
    }

    return render_page(request, module, parsed, context)

@login_required
def cheetah_3(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    # TODO: move to ViewHelper
    module1 = load_previous_module(request)

    back = parsed['previousUrl']
    cc_num = int(request.GET.get('num', 0))
    fact = ''
    source = ''
    bias = ''

    sample_student_cheetah_data = Module.get_sample_student_cheetah_data()

    if request.method == 'POST':
        cc_num = int(request.POST.get('num'))
        fact = request.POST['fact']
        source = request.POST['source']
        bias = request.POST['bias']
        if cc_num == 0:
            module.fact0 = fact
            module.source0 = source
            module.bias0 = bias
        elif cc_num == 1:
            module.fact1 = fact
            module.source1 = source
            module.bias1 = bias
        elif cc_num == 2:
            module.fact2 = fact
            module.source2 = source
            module.bias2 = bias
        else:
            raise Exception("Unexpected index: " + str(cc_num))

        cc_num = cc_num + 1
        if cc_num < len(sample_student_cheetah_data):
            save_form(request, module, parsed)
            return redirect(reverse('module3_cheetah_3') + '?num=' + str(cc_num))
        else:
            return save_form(request, module, parsed)

    # GET
    if cc_num > 0:
        back = parsed['current'] + '?num=' + str(cc_num - 1)

    if cc_num == 0:
        fact = module.fact0
        source = module.source0
        bias = module.bias0
    elif cc_num == 1:
        fact = module.fact1
        source = module.source1
        bias = module.bias1
    elif cc_num == 2:
        fact = module.fact2
        source = module.source2
        bias = module.bias2

    cc_json = ViewHelper.load_json(module1.cc)
    # Your Critical Concept (from Module 1)
    cc_current = cc_json[cc_num]
    #print(cc_current)

    context = {
        'biases': module.get_biases(),
        'back': back,
        'bias': bias,
        'cc': cc_json,
        'cc_current': cc_current,
        'decision': module1.decision,
        'fact': fact,
        'n': cc_num + 1,
        'num': cc_num,
        'sample_student_cheetah_data': sample_student_cheetah_data[cc_num],
        'source': source,
    }

    return render_page(request, module, parsed, context)

@login_required
def cheetah_4(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    # TODO: move to ViewHelper
    module1 = load_previous_module(request)

    if request.method == 'POST':
        return save_form(request, module, parsed)

    mail_body = module1.decision_buddy + ',' + '%0D%0D' + \
                'Please help me validate facts for a big decision: ' + module1.decision + '%0D%0D'
    ccs = load_json(module1.cc)
    mail_body += 'I have identified 3 Critical Concepts. For each one I need to collect facts and make sure that I am not falling prey to biases. Please help me work through verifying the facts for each Critical Concept.' + '%0D%0D' + \
                 'Critical Concept: ' + ccs[0] + '%0D' + \
                 'Fact: ' + module.fact0 + '%0D' + \
                 'Source: ' + module.source0 + '%0D' + \
                 'Bias: ' + module.bias0 + '%0D%0D' + \
                 'Critical Concept: ' + ccs[1] + '%0D' + \
                 'Fact: ' + module.fact1 + '%0D' + \
                 'Source: ' + module.source1 + '%0D' + \
                 'Bias: ' + module.bias1 + '%0D%0D' + \
                 'Critical Concept: ' + ccs[2] + '%0D' + \
                 'Fact: ' + module.fact2 + '%0D' + \
                 'Source: ' + module.source2 + '%0D' + \
                 'Bias: ' + module.bias2 + '%0D%0D' + \
                 'Thank you!'
    to = module1.decision_buddy_email + ',' + request.user.email

    context = {
        'subject': 'Decision Buddy - Help with fact finding',
        'decision_buddy': module1.decision_buddy,
        'decision_buddy_email': module1.decision_buddy_email,
        'decision': module1.decision,
        'cc': ViewHelper.load_json(module1.cc),
        'mail_body': mail_body,
        'to': to,
    }

    return render_page(request, module, parsed, context)

@login_required
def eval(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        return save_form(request, module, parsed)

    context = {

    }

    return render_page(request, module, parsed, context)

@login_required
def game(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    attr = 'easy'  # For count-down timer

    # Add title to each question
    game_questions = Module.get_game_questions()
    for title in game_questions.keys():
        game_questions[title]['title'] = title

    if request.method == 'POST':
        answers = {}
        if module.answers:
            answers = load_json(module.answers)
        for i in range(0, len(game_questions.values())):
            index = str(i)
            question_i = game_questions.values()[i]
            attr_i = request.POST.get('answer[' + index + ']')
            answers[question_i['title']] = attr_i
        module.answers = json.dumps(answers)
        module.biases = json.dumps(calculate_biases(game_questions, answers))
        module.save()
        return redirect(parsed['nextUrl'])
    else:
        ViewHelper.clear_game_answers(module)

    context = {
        'attr': attr,
        'num_questions': len(game_questions),
        'questions': game_questions.values(),
    }

    return render_page(request, module, parsed, context)

@login_required
def game1_results(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    context = {
        'answers': module.answers_json,
        'biases': load_json(module.biases),
        'questions': module.get_game_questions(),
    }

    return render_page(request, module, parsed, context)

@login_required
def game2_game(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    context = {
        'biases': Module.get_biases(),
        'num_questions': len(Module.get_game_questions()),
        'questions': Module.get_game_questions().values(),
    }

    return render_page(request, module, parsed, context)


@login_required
def map(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    context = {
        'display_mode': 'all',
        'btn_label': 'Ready to make better decisions?',
    }
    return render_page(request, module, parsed, context)

@login_required
def nylah_3(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        return save_form(request, module, parsed)

    context = {
        'biases': ViewHelper.load_json(module.biases).keys(),
    }
    return render_page(request, module, parsed, context)

@login_required
def pin3_3(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.more_facts = json.dumps(request.POST.getlist('more_facts[]'))
        return save_form(request, module, parsed)

    context = {
        'selected_facts': ViewHelper.load_json(module.more_facts)
    }

    return render_page(request, module, parsed, context)

@login_required
def pin4_2(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.perspective = json.dumps(request.POST.getlist('perspective[]'))
        return save_form(request, module, parsed)

    context = {
        'selected_perspective': ViewHelper.load_json(module.perspective)
    }

    return render_page(request, module, parsed, context)

@login_required
def pin4_4(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)

    if request.method == 'POST':
        module.opinions = json.dumps(request.POST.getlist('opinions[]'))
        return save_form(request, module, parsed)

    context = {
        'selected_opinions': ViewHelper.load_json(module.opinions)
    }

    return render_page(request, module, parsed, context)

@login_required
def restart(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    return base_restart(request, Module, parsed['prefix'])

@login_required
def review(request):
    parsed = ViewHelper.parse_request_path(request, navigation())
    module = ViewHelper.load_module(request, parsed['currentStep'], Module)
    # TODO: move to ViewHelper
    module1 = load_previous_module(request)

    context = {
        'decision_buddy': module1.decision_buddy,
    }

    return render_page(request, module, parsed, context)

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
def calculate_biases(game_questions, answers):
    biases = {}
    for i in range(0, len(game_questions.values())):
        question_i = game_questions.values()[i]
        bias = question_i['bias']
        if bias not in Module.get_biases():
            biases[bias] = {
                'total': 1,
                'biased': 0,
                'ratio': 0,
            }
        else:
            biases[bias]['total'] += 1
        if answers[question_i['title']] == '':
            answers[question_i['title']] = 0  # TODO - shouldn't need it
        if int(answers[question_i['title']]) == int(question_i['bias_answer']):
            biases[bias]['biased'] += 1
        biases[bias]['ratio'] = int(float(biases[bias]['biased']) / float(biases[bias]['total']) * 100)
    return biases

def load_previous_module(request):
    return load_module(request, PreviousModule)