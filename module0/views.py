from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module0 as Module, Course, Module0Form
from decisions.views import load_module, load_json, base_intro, base_instructions, base_map, base_restart,\
    base_review, base_summary
from area_app.views.view import get_randomized_questions, compute_archetype

import datetime
import json

# template location
prefix = "module" + str(Module.num()) + "/"
# url location
url_prefix = "/" + str(Module.num()) + "/"

"""
Module Controllers
"""
@login_required
def module0_controller(request):
    parsed = parse_request_path(request)
    module = load_module(request, parsed['currentStep'])

    if request.method == 'POST':
        if parsed['section'] == 'game':
            return (game(request))
        elif parsed['section'] == 'right':
            module.psp_correct = request.POST.get('agree')
        elif parsed['section'] == 'eval':
            module.cheetah_answers = json.dumps(request.POST.getlist('ca[]'))

        form = Module0Form(request.POST, instance=module)
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
            'archetype': module.archetype,
        }

        if parsed['section'] == 'map':
            context['display_mode'] = 'all'
        elif parsed['section'] == 'game':
            return (game(request))
        elif parsed['section'] == 'eval':
            context['ca'] = load_json(module.cheetah_answers)

        return render(request, prefix + parsed['templatePath'], context)

@login_required
def game(request):
    parsed = parse_request_path(request)
    module0 = load_module(request, parsed['currentStep'])
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
        'nav': parsed,
    })

@login_required
def review(request):
    module0 = load_module(request, 'review')
    if request.method == 'POST':
        module0.completed_on = datetime.datetime.now()
        module0.save()
        return redirect('/decisions')

    return base_review(request, Module, None, {}, prefix)

@login_required
def restart(request):
    return base_restart(request, Module, prefix)


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
        'review',
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
            if nextNdx < len(module_urls):
                next = module_urls[nextNdx]
            else:
                next = "/decisions"


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
