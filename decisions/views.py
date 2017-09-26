from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from area_app import forms
from .models import Course, Module1
from datetime import datetime
import json


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


def journal(request):
    """
    Journal to keep track of old decisions
    """
    module1 = load_module1(request, '')
    return render(request, 'decisions/journal.html', {
    })


def terms_conditions(request):
    return render(request, 'decisions/terms_conditions.html', {
    })


def load_module1(request, step=''):
    module1 = None
    course = load_course(request)
    if course:
        module1list = Module1.objects.filter(course=course)
        if module1list:
            module1 = module1list.first()
            if step:
                module1.step = step
                module1.save()
        else:
            module1 = Module1(course=course, step=step)
            module1.save()
        module1.answers_json = ''
        if module1.answers:
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


def module1instructions2(request):
    module1 = load_module1(request, 'instructions')
    return render(request, 'decisions/module1/instructions2.html', {
    })


module1game_questions = {
    'Breakfast': 'What to eat for breakfast?',
    'Test': 'To study for a test or just hope for the best?',
    'Job': 'To get an internship or a summer job?',
    'Siblings': 'To take care of your siblings or meet up with friends?',
    'Netflix': 'To stay up watching Netflix or finish your homework?',
    'Lunch': 'Make lunch to bring in or buy at the cafeteria?',
    'Vegetarian': 'Eat meat or become a vegetarian?',
    'Action': 'Sit and wait or take action?',
    'Problem': 'Complain or fix the problem?',
    'Bullying': 'Watch someone get bullied or tell a teacher/take action?',
    'Honesty': 'Be lied to or told the truth?',
    'College': 'Go to a 2-year college or a 4-year university?',
    'Coat': 'Wear a winter coat or just grab a sweatshirt?',
    'Hair': 'What to do with my hair?',
    'Friend': 'Share a problem with a friend?',
}

game_labels = {
    'easy': ['Easy', 'Hard'],
    'confident': ['Confident', 'Unsure'],
}


def game(request, module1, attr, next):
    if request.method == 'POST':
        attrs = []
        answers = {}
        if module1.answers:
            answers = json.loads(module1.answers)
        for i in range(0, len(module1game_questions.values())):
            index = str(i)
            question_i = module1game_questions.values()[i]
            attr_i = request.POST.get('answer[' + index + ']')
            attrs.append(attr_i)
            if question_i not in answers:
                answers[question_i] = {
                    'title': module1game_questions.keys()[i]
                }
            answers[question_i][attr] = attr_i
        module1.answers = json.dumps(answers)
        module1.save()
        return redirect('/decisions/1/'+next)
    return render(request, 'decisions/module1/game.html', {
        'questions': module1game_questions.values(),
        'attr': attr,
        'labels': game_labels[attr],
        'num_questions': len(module1game_questions),
    })


def clear_game_answers(module1):
    if module1.answers:
        module1.answers = json.dumps({})
        module1.save()


def module1game(request):
    module1 = load_module1(request, 'game')
    clear_game_answers(module1)  # TODO - save old answers
    return game(request, module1, 'easy', 'instructions2')


def module1game2(request):
    module1 = load_module1(request, 'game2')
    return game(request, module1, 'confident', 'game_end')


def module1game_end(request):
    module1 = load_module1(request, 'game_end')
    return render(request, 'decisions/module1/game_end.html', {
    })


def module1game_results(request):
    module1 = load_module1(request, 'game_results')
    return render(request, 'decisions/module1/game_results.html', {
        'answers': module1.answers_json,
        'questions': module1game_questions,
    })


def module1explain(request):
    module1 = load_module1(request, 'explain')
    return render(request, 'decisions/module1/explain.html', {
    })


def module1area(request):
    module1 = load_module1(request, 'area')
    return render(request, 'decisions/module1/area.html', {
        'answers': module1.answers_json,
        'questions': module1game_questions,
    })


def module1video(request):
    module1 = load_module1(request, 'video')
    return render(request, 'decisions/module1/video.html', {
    })


def module1details(request):
    module1 = load_module1(request, 'details')
    return render(request, 'decisions/module1/details.html', {
    })


def module1directions(request):
    module1 = load_module1(request, 'directions')
    if request.method == 'POST':
        why_list = Exception(request.POST.getlist('why[]'))
        # TODO: save why_list
        return redirect('/decisions/1/details')
    return render(request, 'decisions/module1/directions.html', {
        'answers': module1.answers_json,
        'questions': module1game_questions,
        'why_options': [
            'Not sure how to solve my problem',
            'Not sure what I want from my decision outcome',
            'Worried I will make a poor decision',
            'Worried about what other people will think of my decision',
            'Not sure that I need to make the decision now',
        ],
    })


def module1sample(request):
    module1 = load_module1(request, 'sample')
    return render(request, 'decisions/module1/sample.html', {
        'answers': module1.answers_json,
    })


def module1defining_cc(request):
    module1 = load_module1(request, 'defining_cc')
    return render(request, 'decisions/module1/defining_cc.html', {
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
        'decision': module1.decision,
    })


def module1cheetah(request):
    module1 = load_module1(request, 'cheetah')
    if request.method == 'POST':
        module1.cc = json.dumps(request.POST.getlist('cc[]'))
        module1.save()
        return redirect('/decisions/1/challenge')
    return render(request, 'decisions/module1/cheetah.html', {
        'decision': module1.decision,
    })


def module1challenge(request):
    module1 = load_module1(request, 'challenge')
    if request.method == 'POST':
        module1.cc = json.dumps(request.POST.getlist('cc[]'))
        module1.cc_not = json.dumps(request.POST.getlist('cc_not[]'))
        module1.save()
        return redirect('/decisions/1/buddy')
    return render(request, 'decisions/module1/challenge.html', {
        'cc': json.loads(module1.cc),
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
        'decision': module1.decision,
        'cc': json.loads(module1.cc),
    })


def module1summary(request):
    module1 = load_module1(request, 'summary')
    module1.completed_on = datetime.now()
    module1.save()
    return render(request, 'decisions/module1/summary.html', {
    })


def module1restart(request):
    module1 = load_module1(request, 'summary')
    module1.completed_on = None
    module1.save()
    return redirect('/decisions/1')


"""
Module 2
"""


def module2(request):
    return render(request, 'decisions/module2/intro.html', {
    })
