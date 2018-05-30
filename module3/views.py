from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module3 as Module, Course
from decisions.models import Module2
from datetime import datetime
import json


prefix = "module" + str(Module.num()) + "/"


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


@login_required
def intro(request):
    module = load_module(request, 'intro')
    return render(request, prefix+'intro.html', {
        'module': module,
    })


@login_required
def review(request):
    module = load_module(request, 'review')
    module2 = Module2
    return render(request, prefix+'review.html', {
        'module': module,
        'previous_module': module2,
    })


@login_required
def map(request):
    module = load_module(request, 'map')
    return render(request, prefix+'map.html', {
        'module': module,
    })


@login_required
def instructions(request):
    module = load_module(request, 'instructions')
    return render(request, prefix+'instructions.html', {
        'module': module,
    })


@login_required
def summary(request):
    module = load_module(request, 'summary')
    module.completed_on = datetime.now()
    module.save()
    return render(request, prefix+'summary.html', {
        'module': module,
    })


@login_required
def restart(request):
    module = load_module(request, 'intro')
    module.completed_on = None
    module.save()
    return redirect('/' + str(Module.num()) + '/')
