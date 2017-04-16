import json
import os
import random

import archetypes
import biases
import forms

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from utils import send_from_default_email
from .models import Problem

dream_directors = [
    'Bob, New York',
    'Jill, California',
]


def check_partner(request):
    partner = ''
    if 'partner' in request.GET:
        partner = request.GET['partner']
    else:
        partner = settings.DEFAULT_PARTNER
    request.session['partner'] = partner
    return partner


def get_randomized_questions():
    """
    Randomize the order of questions
    """
    question_and_details = archetypes.questions.items()
    random.shuffle(question_and_details)
    return question_and_details


def home(request):
    if request.user.is_authenticated():
        return home_logged_in(request)
    if request.method == 'POST':
        return handle_answers(request)
        return redirect('/accounts/signup/?next=/archetype')
    partner = check_partner(request)
    login_form = None
    if partner == 'fp':
        login_form = forms.FutureProjectSignupForm
    questions_yes = ''
    if 'questions_yes' in request.session:
        questions_yes = request.session['questions_yes']
    return render(request, 'home.html', {
        'questions': get_randomized_questions(),
        'questions_yes': questions_yes,
        'form': login_form,
    })


def get_from_session(request, param):
    if param in request.session:
        return request.session[param]
    else:
        return None


def home_logged_in(request):
    request.session['questions_yes'] = archetypes.load_questions(request.user)
    compute_archetype(request)
    problems = Problem.objects.filter(user=request.user).all()
    return render(request, 'home_logged_in.html', {
        'type': get_from_session(request, 'decision_type'),
        'decision': get_from_session(request, 'decision'),
        'options': get_from_session(request, 'options'),
        'timeframe': get_from_session(request, 'timeframe'),
        'archetype': get_from_session(request, 'top_archetype'),
        'cheetahs': get_from_session(request, 'cheetah_sheets'),
        'commitment': get_from_session(request, 'commitment'),
        'commitment_days': get_from_session(request, 'commitment_days'),
        'questions_yes': request.session['questions_yes'],
        'problems': problems,
        'step': 1,
    })


def load_problem(request):
    pid = None  # Problem id
    if request.method == 'POST':
        if 'pid' in request.POST:
            pid = request.POST['pid']
        else:
            raise Exception('POST without pid')
    else:
        if 'pid' in request.GET:
            pid = request.GET['pid']
    problem = Problem()
    if pid:
        problem = Problem.objects.filter(id=pid).first()
    request.session['pid'] = pid
    request.session['decision_type'] = problem.decision_type
    request.session['decision'] = problem.decision
    request.session['options'] = problem.options
    request.session['timeframe'] = problem.time_frame
    request.session['decision_type_other'] = problem.decision_type_other
    request.session['success'] = problem.success
    request.session['commitment_days'] = problem.commitment_days
    request.session['commitment'] = problem.commitment
    return problem


def decision(request):
    problem = load_problem(request)
    if request.method == 'POST':
        if request.POST['submit'] == 'Back':
            return redirect('/')
        decision_types = request.POST.getlist('decision_type[]')
        request.session['decision_types'] = decision_types
        decision_type_text = ''
        for decision_type in decision_types:
            if decision_type_text:
                decision_type_text += ' and '
            if decision_type == 'other':
                decision_type = request.POST['decision_type_other']
            decision_type_text += decision_type
        request.session['decision_type'] = decision_type_text
        request.session['decision'] = request.POST['decision']
        request.session['options'] = request.POST['options']
        request.session['timeframe'] = request.POST['timeframe']
        request.session['decision_type_other'] = request.POST['decision_type_other']
        if request.user.is_authenticated():
            problem.user = request.user
        else:
            problem.user = None
        problem.decision_type = decision_type_text
        problem.decision = request.session['decision']
        problem.options = request.session['options']
        problem.time_frame = request.session['timeframe']
        problem.decision_type_other = request.session['decision_type_other']
        problem.save()
        return redirect('/rank?pid='+str(problem.id))
    decision_types_comma_delimited = ''
    if 'decision_types' in request.session:
        for decision_type in request.session['decision_types']:
            decision_types_comma_delimited += decision_type + ','
    return render(request, 'decision.html', {
        'decision_types': decision_types_comma_delimited,
        'pid': problem.id,
        'step': 1,
    })


success = {
    "new": "I created a new solution that I hadn't considered when I started.",
    "gut": "I trusted my gut instinct and followed my heart.",
    "evidence": "I acted on a strong plan based in evidence.",
    "options": "I considered all my options and took my time to decide.",
    "guidance": "I relied on the guidance of the friends and people I trust.",
}


@login_required(login_url='/accounts/signup/')
def rank(request):
    problem = load_problem(request)
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/decision')
        success_shuffled = request.POST['success']
        request.session['success'] = success_shuffled
        problem.success = success_shuffled
        problem.save()
        if 'questions_yes' in request.session:
            return redirect('/action_map?pid='+str(problem.id))
        else:
            return redirect('/questions?pid='+str(problem.id))
    success_keys = None
    if problem:
        success_keys = problem.success.split(',')
    if not success_keys:
        success_keys = success.keys()
        random.shuffle(success_keys)
    success_shuffled = []
    for success_key in success_keys:
        success_shuffled.append([success_key, success[success_key]])
    return render(request, 'rank.html', {
        'success': success_shuffled,
        'step': 2,
        'pid': problem.id,
    })


def compute_archetype(request):
    questions_yes = request.session['questions_yes']
    top_archetypes = archetypes.get_top_archetypes(questions_yes)
    request.session['archetype'] = top_archetypes
    top_archetype = top_archetypes[0]
    request.session['top_archetype'] = top_archetype[0]


def handle_answers(request):
    if request.POST['submit'] == 'Back':
        return redirect('/rank')
    questions_yes = request.POST.getlist('question[]')
    user = None
    if request.user.is_authenticated():
        user = request.user
    archetypes.save_questions(questions_yes=questions_yes, user=user)
    compute_archetype(request)
    return redirect('/archetype')


def questions(request):
    if request.method == 'POST':
        return handle_answers(request)
    questions_yes = ''
    if 'questions_yes' in request.session:
        questions_yes = request.session['questions_yes']
    return render(request, 'questions.html', {
        'questions': get_randomized_questions(),
        'questions_yes': questions_yes,
        'step': 3,
    })


def answer(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        if 'questions_yes' not in request.session:
            request.session['questions_yes'] = {}
        if answer == 'yes':
            request.session['questions_yes']


@login_required(login_url='/accounts/signup/')
def archetype(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/questions')
        return redirect('/action_map')
    if 'archetype' not in request.session:
        return render(request, 'archetype.html', {
        })
    top_archetypes = request.session['archetype']
    top_archetype = top_archetypes[0]
    return render(request, 'archetype.html', {
        'archetype': top_archetype[0],
        'strength': top_archetype[1],
        'step': 4,
    })


def archetype_info(request):
    archetype = request.GET['t']
    return archetype


@login_required(login_url='/accounts/signup/')
def cheetah_sheets(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/archetype')
        return redirect('/summary')
    attributes = request.session['attributes']
    attribute_cheetahs = biases.get_top(attributes, biases.attribute_cheetahs)
    request.session['cheetah_sheets'] = attribute_cheetahs
    return render(request, 'cheetah_sheets.html', {
        'attribute_cheetahs': attribute_cheetahs,
        'step': 5,
    })


def archetypes_list(request):
    return render(request, 'archetypes.html', {
        'step': 4,
    })


@login_required(login_url='/accounts/signup/')
def action_map(request):
    problem = load_problem(request)
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/archetype')
        request.session['commitment'] = request.POST['commitment']
        request.session['commitment_days'] = request.POST['days']
        problem.commitment = request.session['commitment']
        problem.commitment_days = request.session['commitment_days']
        problem.save()

        request.session['email_sent'] = False

        return redirect('/summary?pid='+str(problem.id))
    if 'top_archetype' not in request.session:
        return render(request, 'action_map.html', {})
    archetype = request.session['top_archetype']
    archetype_cheetahs = archetypes.archetype_cheetah_sheets[archetype]
    request.session['cheetah_sheets'] = archetype_cheetahs
    return render(request, 'action_map.html', {
        'type': request.session['decision_type'],
        'decision': request.session['decision'],
        'options': request.session['options'],
        'timeframe': request.session['timeframe'],
        'archetype': archetype,
        'cheetahs': archetype_cheetahs,
        'pid': problem.id,
        'step': 5,
    })


@login_required(login_url='/accounts/signup/')
def summary(request):
    problem = load_problem(request)
    request.session['summary'] = 1
    if 'decision' not in request.session:
        return render(request, 'summary.html', {})

    if not request.session['email_sent']:
        subject = "Your Commitment Details"
        message = list()
        message.append("You have taken commitments to do")
        message.append(request.session['commitment'])
        message.append("in")
        message.append(request.session['commitment_days'])
        message.append("Days.\n")
        message.append("Thank you.\n")
        message.append("Team App Areamethod\n")
        message.append("https://app.areamethod.com\n\n")

        send_from_default_email(subject, " ".join(message), [request.user.email])
        request.session['email_sent'] = True

    return render(request, 'summary.html', {
        'type': request.session['decision_type'],
        'decision': request.session['decision'],
        'options': request.session['options'],
        'timeframe': request.session['timeframe'],
        'archetype': request.session['top_archetype'],
        'cheetahs': request.session['cheetah_sheets'],
        'commitment': request.session['commitment'],
        'commitment_days': request.session['commitment_days'],
        'pid': problem.id,
        'step': 5,
    })


def cheetah_master(request):
    cheetahs = os.listdir('../area/templates/cheetah')
    return render(request, 'cheetah_master.html', {
        'cheetahs': cheetahs,
    })


def autocomplete_dd(request):
    return json.dumps({'results': dream_directors})


def restart_session(request):
    for key in request.session.keys():
        if not key.startswith('_'):
            del request.session[key]
    return redirect('/decision')
