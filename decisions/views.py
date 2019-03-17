from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from area_app import forms
from .models import Course
from module0.models import Module0
from module1.models import Module1
from module2.models import Module2
#from module3.models import Module3
from student_class.models import StudentClass

from decisions.utils import ViewHelper

from decisions.decorator import active_user_required

from datetime import datetime
import json

#import stripe
from django.urls import reverse

def load_json(json_data):
    json_object = {}
    try:
        json_object = json.loads(json_data)
    except ValueError, e:
        pass
        # TODO - log
    return json_object


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


@login_required
def load_module(request, module_class, step=''):
    module = None
    course = load_course(request)
    if course:
        module_list = module_class.objects.filter(course=course)
        if module_list:
            module = module_list.first()
            if step:
                module.step = step
                module.save()
        else:
            module = module_class(course=course, step=step)
            module.save()
        module.answers_json = ''
        if module.answers:
            module.answers_json = load_json(module.answers)
    if not module:
        module = module_class()
        module.answers_json = None
    return module

# @login_required
@active_user_required
def home(request):
    request.session['start'] = '/decisions'
    request.session['partner'] = 'fp'
    course = Course.load_course(request)

    module0 = ViewHelper.load_module(request, '', Module0)
    module1 = ViewHelper.load_module(request, '', Module1)
    module2 = ViewHelper.load_module(request, '', Module2)
    #module3 = ViewHelper.load_module(request, '', Module3)

    student_classes = None
    if request.user.is_staff:
        student_classes = StudentClass.objects.filter(instructor=request.user)
    # If it's the first time, take them to the tour
    if not course.intro_on:
        return redirect('/decisions/tour')

    if request.method == 'POST':
        request.user.has_tou = True
        request.user.save()
        print(request.user.email + " accepted terms of use")

        #token = request.POST.get('stripeToken')
        #print("token: " + token)
        #stripe.api_key = settings.STRIPE_SECRET_KEY

        #try:
        #    charge = stripe.Charge.create(
        #        amount = 999,
        #        currency = "usd",
        #        source = token,
        #        description = "Subscription for Module 2"
        #    )
        #    print("Stripe charge id: " + charge.id)
        #except stripe.error.CardError as ce:
        #    print("Exception")
        #    print(ce)

    return render(request, 'decisions/intro.html', {
        'form': forms.FutureProjectSignupForm,
        'module0': module0,
        'module1': module1,
        'module2': module2,
        #'module3': module3,
        'student_classes': student_classes,
        'my_classes': StudentClass.my_classes(course),
        'open_classes': StudentClass.open_classes(course),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })

def checkout(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            charge = stripe.Charge.create(
                amount = 999,
                currency = "usd",
                source = token,
                description = "Subscription for Module 2"
            )

            print("Stripe charge id: " + charge.id)
        except stripe.error.CardError as ce:
            print("Exception")
            print(ce)

        return redirect(reverse('decisions_home'))
    else:
        print("Redirecting back to /decisions")
        return redirect(reverse('decisions_home'))

def limit_reached(request):
    """
    Dislay the limit reached message when the user limit has been reached
    """
    return render(request, 'decisions/base/limit_reached.html', {})

def tour(request):
    """
    Tour page to show only once when user first signs up
    """
    if request.method == 'POST':
        # Mark as seen, go on
        course = Course.load_course(request)
        course.intro_on = datetime.now()
        course.save()
        return redirect('/decisions')
    return render(request, 'decisions/tour.html', {
    })


@login_required
def journal(request):
    """
    Journal to keep track of old decisions
    """
    module1 = ViewHelper.load_module(request, '', Module1)
    return render(request, 'decisions/journal.html', {
    })


def terms_conditions(request):
    return render(request, 'decisions/terms_conditions.html', {
    })


"""

Common Methods

"""


def base_intro(request, module_class, prefix):
    module = load_module(request, module_class, 'intro')
    return render(request, prefix+'intro.html', {
        'module': module,
    })


def base_review(request, module_class, previous_module_class, extra_map, prefix):
    module = load_module(request, module_class, 'review')
    return render(request, prefix+'review.html', {
        'module': module,
        'previous_module': previous_module_class,
    })


def base_map(request, module_class, prefix):
    module = load_module(request, module_class, 'map')
    return render(request, prefix+'map.html', {
        'module': module,
    })


def base_instructions(request, module_class, prefix):
    module = load_module(request, module_class, 'instructions')
    if request.method == 'POST':
        return redirect('/' + str(module_class.num()) + '/game')
    return render(request, prefix+'instructions.html', {
        'module': module,
    })


def base_summary(request, module_class, prefix):
    module = load_module(request, module_class, 'summary')
    module.completed_on = datetime.now()
    module.save()
    return render(request, prefix+'summary.html', {
        'module': module,
    })


def base_restart(request, module_class, prefix):
    module = load_module(request, module_class, 'intro')
    module.completed_on = None
    module.save()
    return redirect('/' + str(module_class.num()) + '/')