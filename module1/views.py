from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Module1 as Module, Course, Module1Form
from module0.models import Module0 as PreviousModule
from datetime import datetime

import json

# template location
prefix = "module" + str(Module.num()) + "/"
# url location
url_prefix = "/" + str(Module.num()) + "/"

"""
Module Controllers
"""
@login_required
def game_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

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
        return redirect(url_prefix + parsed['next'])
    else:
        if parsed['section'] == 'game1':
            clear_game_answers(module)  # TODO - save old answers
            attr = 'easy'
        else:
            attr = 'confident'

    return render(request, prefix+'game.html', {
        'module': module,
        'nav': parsed,
        'attr': attr,
        'labels': module.game_labels()[attr],
        'num_questions': len(module.game1_questions()),
        'questions': module.game1_questions().values(),
    })

@login_required
def generic_page_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

    if request.method == 'POST':
        if parsed['step'] == 'exploring':
            module.cc1_list = json.dumps(request.POST.getlist('cc1[]'))
            module.cc2_list = json.dumps(request.POST.getlist('cc2[]'))
        elif parsed['section'] == 'cheetah':
            module.cc = json.dumps(request.POST.getlist('cc[]'))
        elif parsed['section'] == 'challenge':
            module.cc = json.dumps(request.POST.getlist('cc[]'))
            module.cc_not = json.dumps(request.POST.getlist('cc_not[]'))

        form = Module1Form(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect(url_prefix + parsed['next'])
        else:
            print("Form did not validate")
            print(form.errors)
    else:
        # Add the module to the context by default
        context = {
            'module': module,
            'nav': parsed,
        }

        if parsed['section'] == 'map':
            context['display_mode'] = 'all'
        elif parsed['section'] == 'success':
            context['cc'] = load_json(module.cc)
        elif parsed['section'] == 'challenge':
            context['cc'] =  load_json(module.cc)
            context['cc_not'] = load_json(module.cc_not)
        elif parsed['section'] == 'area' or parsed['section'] == 'game_results':
            context['answers'] = module.answers_json
            context['questions'] = module.game1_questions
        elif parsed['step'] == 'exploring':
            context['cc1_list'] = load_json(module.cc1_list)
            context['cc2_list'] = load_json(module.cc2_list)

        return render(request, prefix + parsed['templatePath'], context)

@login_required
def commitment(request):
    parsed = parse_request_path(request)
    module = load_module(request, 'commitment')

    if request.method == 'POST':
        return redirect(url_prefix + 'summary')

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

    return render(request, prefix + 'commitment.html', {
        'module': module,
        'nav': parsed,
        'cc': load_json(module.cc),
        'mail_body': mail_body,
        'to': to,
    })

@login_required
def summary(request):
    module = load_module(request, 'intro')
    module.completed_on = datetime.now()
    module.save()
    return redirect('/decisions')

@login_required
def restart(request):
    module = load_module(request, 'intro')
    module.completed_on = None
    module.save()
    return redirect('/' + str(Module.num()) + '/')

"""
Helper Utilities
TODO: Move to its own file
"""
def clear_game_answers(module):
    if module.answers:
        module.answers = json.dumps({})
        module.save()

def load_course(request):
    course = None
    if request.user.is_authenticated():
        courses = Course.objects.filter(user=request.user)
        if courses:
            course = courses.first()
        else:
            course = Course(user=request.user)
            course.save()
    return course

def load_json(json_data):
    json_object = {}
    try:
        json_object = json.loads(json_data)
    except ValueError, e:
        pass
        # TODO - log
    return json_object

@login_required
def load_module(request, step=''):
    module = None
    course = load_course(request)
    if course:
        module_list = Module.objects.filter(course=course)
        if module_list:
            module = module_list.first()
            if step:
                module.step = step
                module.save()
        else:
            module = Module(course=course, step=step)
            module.save()
        module.answers_json = ''
        if module.answers:
            module.answers_json = load_json(module.answers)
    if not module:
        module = Module()
        module.answers_json = None
    return module

# Ordered list of URLs, used to calculate back and next
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

def parse_request_path(request):
    parsed = {
        'parsed': [],
        'moduleNum': None,
        'section': None,
        'step': None,
        'currentStep': None,
        'templatePath': None,
        'requestPath': request.path,
        'previous': None,
        'next': None
    }

    parts = request.path.split("/")

    # Typical path is /<module_num>/<section>
    if len(parts) > 2:
        section = parts[2]
        step = None

        # Log the step we are on e.g. intro
        current = section
        currentStep = section
        # Path to the template
        templatePath = section + ".html"

        # There is a sub directory path
        if len(parts) == 4:
            step = parts[3]
            current = section + "/" + step
            currentStep = section + "_" + step
            templatePath = section + "/" + step + ".html"

        module_urls = navigation()

        # Calculate the previous and next steps
        if current in module_urls:
            currentNdx = module_urls.index(current)

            previousNdx = currentNdx - 1
            print(module_urls[previousNdx])
            if previousNdx > 0:
                previous = module_urls[previousNdx]
            else:
                previous = module_urls[0]

            nextNdx = currentNdx + 1
            if nextNdx > len(module_urls):
                next = module_urls[len(module_urls)]
            else:
                next = module_urls[nextNdx]

        print("previous: " + previous + ", next: " + next)

        parsed = {
            'parsed': parts,
            'moduleNum': parts[1],
            'section': section,
            'step': step,
            'currentStep': currentStep,
            'templatePath': templatePath,
            'current': current,
            'next': next,
            'previous': previous,
        }

    return parsed
