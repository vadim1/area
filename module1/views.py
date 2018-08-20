from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Module1 as Module, Course
from module0.models import Module0 as PreviousModule
from datetime import datetime

import json

# template location
prefix = "module" + str(Module.num()) + "/"
# url location
url_prefix = "/" + str(Module.num()) + "/"

@login_required
def generic_page_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

    if request.method == 'POST':
        if parsed['section'] == 'decision':
            module.decision = request.POST.get('decision')
            next = 'cheetah'
        elif parsed['section'] == 'cheetah':
            module.cc = json.dumps(request.POST.getlist('cc[]'))
            next = 'challenge'
        elif parsed['section'] == 'challenge':
            module.cc = json.dumps(request.POST.getlist('cc[]'))
            module.cc_not = json.dumps(request.POST.getlist('cc_not[]'))
            next = 'buddy'
        elif parsed['section'] == 'buddy':
            # TODO - *Send buddy name and email to the student entering it and dream director
            module.decision_buddy = request.POST.get('decision_buddy')
            module.decision_buddy_email = request.POST.get('decision_buddy_email')
            next = 'commitment'
        else:
            next = ""

        module.save()
        return redirect(url_prefix + next)
    else:
        if parsed['section'] == 'cheetah':
            return render(request, prefix + parsed['templatePath'], {
                'module': module,
                'cc': load_json(module.cc),
            })
        elif parsed['section'] == 'challenge':
            return render(request, prefix + parsed['templatePath'], {
                'module': module,
                'cc': load_json(module.cc),
                'cc_not': load_json(module.cc_not),
            })
        else:
            return render(request, prefix + parsed['templatePath'], {
                'module': module
            })

@login_required
def game_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

    # Are we playing a game?
    if parsed['step'] == 'game':
        # For game1 we clear any previous answers but not for game2
        if parsed['section'] == 'game1':
            clear_game_answers(module)  # TODO - save old answers
            return game(request, module, 'easy', 'game1/instructions', 'game1/end')
        else:
            return game(request, module, 'confident', 'game2/instructions', 'game2/end')

    return generic_page_controller(request)


@login_required
def game_results(request):
    module = load_module(request, 'game_results')

    return render(request, prefix+'results.html', {
        'module': module,
        'answers': module.answers_json,
        'questions': module.game1_questions(),
    })

@login_required
def area(request):
    module = load_module(request, 'area')

    return render(request, prefix+'area.html', {
        'module': module,
        'answers': module.answers_json,
        'questions': module.game1_questions(),
    })

@login_required
def decisions_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

    if request.method == 'POST':
        if parsed['step'] == 'living':
            module.living = request.POST.get('living')
            next = 'decisions/sample'
        elif parsed['step'] == 'sample':
            module.cc0 = request.POST.get('cc0')
            module.cc1 = request.POST.get('cc1')
            module.cc2 = request.POST.get('cc2')
            next = 'cc'
        elif parsed['step'] == 'directions':
            module.why_list = request.POST.getlist('why[]')
            next = 'decisions/details'

        module.save()
        return redirect(url_prefix + next)
    else:
        return generic_page_controller(request)

@login_required
def cc_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

    if request.method == 'POST':
        if parsed['step'] == 'deriving':
            module.cc0 = request.POST.get('cc0')
            module.cc1 = request.POST.get('cc1')
            module.cc2 = request.POST.get('cc2')
            next = 'cc/exploring'
        elif parsed['step'] == 'exploring':
            module.cc1_list = json.dumps(request.POST.getlist('cc1[]'))
            module.cc2_list = json.dumps(request.POST.getlist('cc2[]'))
            next = 'decision'

        module.save()
        return redirect(url_prefix + next)
    else:
        if parsed['step'] == 'exploring':
            return render(request, prefix + parsed['templatePath'], {
                'module': module,
                'cc1_list': load_json(module.cc1_list),
                'cc2_list': load_json(module.cc2_list),
            })

        return generic_page_controller(request)

@login_required
def commitment(request):
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

def game(request, module, attr, back, next):
    if request.method == 'POST':
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
        return redirect(url_prefix + next)

    return render(request, prefix+'game.html', {
        'backUrlTarget': url_prefix + back,
        'module': module,
        'questions': module.game1_questions().values(),
        'attr': attr,
        'labels': module.game_labels()[attr],
        'num_questions': len(module.game1_questions()),
    })

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

def parse_request_path(request):
    parsed = {
        'parsed': [],
        'moduleNum': None,
        'section': None,
        'step': None,
        'currentStep': None,
        'templatePath': None,
        'requestPath': request.path,
    }

    parts = request.path.split("/")
    # Typical path is /<module_num>/<section>
    if len(parts) > 2:
        section = parts[2]
        step = None

        # Log the step we are on e.g. intro
        currentStep = section
        # Path to the template
        templatePath = section + ".html"

        # There is a sub directory path
        if len(parts) == 4:
            step = parts[3]
            currentStep = section + "_" + step
            templatePath = section + "/" + step + ".html"

        parsed = {
            'parsed': parts,
            'moduleNum': parts[1],
            'section': section,
            'step': step,
            'currentStep': currentStep,
            'templatePath': templatePath
        }

    return parsed
