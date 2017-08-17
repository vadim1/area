from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from area_app import forms
from .models import Course, Module1
from datetime import datetime
import json


def load_course(request):
    courses = Course.objects.filter(user=request.user)
    course = None
    if courses:
        course = courses.first()
    else:
        course = Course(user=request.user)
        course.save()
    return course


def home(request):
    request.session['start'] = '/decisions'
    request.session['partner'] = 'fp'
    # TODO - fix signup
    module1 = None
    if request.user.is_authenticated():
        course = load_course(request)
        module1 = load_module1(request)
        # If it's the first time, take them to the tour
        if not course.intro_on:
            return redirect('/decisions/tour')
    return render(request, 'decisions/intro.html', {
        'form': forms.FutureProjectSignupForm,
        'module1': module1,
    })


def tour(request):
    """
    Tour page to show only once when user first signs up
    """
    if request.method == 'POST':
        # Mark as seen, go on
        course = load_course(request)
        course.intro_on = datetime.now()
        course.save()
        return redirect('/decisions')
    return render(request, 'decisions/tour.html', {
    })


def load_module1(request, step=''):
    course = load_course(request)
    module1list = Module1.objects.filter(course=course)
    module1 = None
    if module1list:
        module1 = module1list.first()
        if step:
            module1.step = step
            module1.save()
    else:
        module1 = Module1(course=course, step=step)
        module1.save()
    module1.answers_json = json.loads(module1.answers)
    return module1


def module1(request):
    module1 = load_module1(request, '')
    return render(request, 'decisions/module1/intro.html', {
    })


def module1instructions(request):
    module1 = load_module1(request, 'instructions')
    return render(request, 'decisions/module1/instructions.html', {
    })


module1game_questions = [
    'What to eat for breakfast?',
    'To study for a test or just hope for the best?',
    'To get an internship or a summer job?',
    'To take care of your siblings or meet up with friends?',
    'To stay up watching Netflix or finish your homework?',
    'Make lunch to bring in or buy at the cafeteria?',
    'Eat meat or become a vegetarian?',
    'Sit and wait or take action?',
    'Complain or fix the problem?',
    'Watch someone get bullied or tell a teacher/take action?',
    'Be lied to or told the truth?',
    'Go to a 2-year college or a 4-year university?',
    'Stay home on a sick day or get work done at school?',
    'Wear a winter coat or just grab a sweatshirt?',
    'Sit next to a friend during a test or stay on my own?',
    'What to do with my hair?',
    'Share a problem with a friend',
    'Stay for help after school or try it on my own?',
    'Buy myself a new video game or save up for my sister\'s birthday?',
]


def module1game(request):
    module1 = load_module1(request, 'game')
    if request.method == 'POST':
        easy = []
        like = []
        answers = {}
        for i in range(0, len(module1game_questions)):
            index = str(i)
            question_i = module1game_questions[i]
            easy_i_str = request.POST.get('easy[' + index + ']')
            like_i_str = request.POST.get('like[' + index + ']')
            easy_i = int(easy_i_str) if easy_i_str else 5
            like_i = int(like_i_str) if like_i_str else 5
            easy.append(easy_i)
            like.append(like_i)
            answers[question_i] = {
                'difficulty': easy_i,
                'likeability': like_i,
            }
        module1.answers = json.dumps(answers)
        module1.save()
        return redirect('/decisions/1/game_results')
    return render(request, 'decisions/module1/game.html', {
        'questions': module1game_questions,
    })


def module1game_results(request):
    module1 = load_module1(request, 'game_results')
    return render(request, 'decisions/module1/game_results.html', {
        'answers': module1.answers_json,
    })


def module1explain(request):
    module1 = load_module1(request, 'explain')
    return render(request, 'decisions/module1/explain.html', {
    })


def module1area(request):
    module1 = load_module1(request, 'area')
    return render(request, 'decisions/module1/area.html', {
        'answers': module1.answers_json,
    })


def module1video(request):
    module1 = load_module1(request, 'video')
    return render(request, 'decisions/module1/video.html', {
    })


def module1directions(request):
    module1 = load_module1(request, 'directions')
    return render(request, 'decisions/module1/directions.html', {
    })


def module1sample(request):
    module1 = load_module1(request, 'sample')
    return render(request, 'decisions/module1/sample.html', {
        'answers': module1.answers_json,
    })


def module1deriving_cc(request):
    module1 = load_module1(request, 'deriving_cc')
    if request.method == 'POST':
        module1.cc0 = request.POST.getlist('cc[]')
        module1.save()
        return redirect('/decisions/1/exploring_cc')
    return render(request, 'decisions/module1/deriving_cc.html', {
    })


def module1exploring_cc(request):
    module1 = load_module1(request, 'exploring_cc')
    if request.method == 'POST':
        module1.cc1 = request.POST.getlist('cc1[]')
        module1.cc2 = request.POST.getlist('cc2[]')
        module1.save()
        return redirect('/decisions/1/decision')
    return render(request, 'decisions/module1/exploring_cc.html', {
    })


def module1decision(request):
    module1 = load_module1(request, 'decision')
    if request.method == 'POST':
        module1.decision = request.POST.get('decision')
        module1.save()
        return redirect('/decisions/1/cheetah')
    return render(request, 'decisions/module1/decision.html', {
    })


def module1cheetah(request):
    module1 = load_module1(request, 'cheetah')
    if request.method == 'POST':
        module1.cc = request.POST.getlist('cc[]')
        module1.save()
        return redirect('/decisions/1/challenge')
    return render(request, 'decisions/module1/cheetah.html', {
        'decision': module1.decision,
    })


def module1challenge(request):
    module1 = load_module1(request, 'challenge')
    if request.method == 'POST':
        module1.cc = request.POST.getlist('cc[]')
        module1.cc_not = request.POST.getlist('cc_not[]')
        module1.save()
        return redirect('/decisions/1/buddy')
    return render(request, 'decisions/module1/challenge.html', {
        'cc': module1.cc,
        'decision': module1.decision,
    })


def module1buddy(request):
    module1 = load_module1(request, 'buddy')
    if request.method == 'POST':
        module1.decision_buddy = request.POST.get('decision_buddy')
        module1.decision_buddy_email = request.POST.get('decision_buddy_email')
        module1.save()
        # TODO - *Send buddy name and email to the student entering it and dream director
        return redirect('/decisions/1/commitment')
    return render(request, 'decisions/module1/buddy.html', {
    })


def module1commitment(request):
    module1 = load_module1(request, 'commitment')
    if request.method == 'POST':
        return redirect('/decisions/1/summary')
    return render(request, 'decisions/module1/commitment.html', {
        'decision_buddy': module1.decision_buddy,
        'decision_buddy_email': module1.decision_buddy_email,
    })


def module1summary(request):
    module1 = load_module1(request, 'summary')
    module1.completed_on = datetime.now()
    module1.save()
    return render(request, 'decisions/module1/summary.html', {
    })


"""
Module 2
"""


def module2(request):
    return render(request, 'decisions/module2/intro.html', {
    })
