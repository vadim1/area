import json
import os
import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
import area_app.archetypes
import area_app.biases
from area_app.utils import send_from_default_email

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


def get_randomized_questions():
    """
    Randomize the order of questions
    """
    question_and_details = area_app.archetypes.questions.items()
    random.shuffle(question_and_details)
    return question_and_details


def home(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/home')
        return redirect('/decision')
    check_partner(request)
    questions_yes = ''
    if 'questions_yes' in request.session:
        questions_yes = request.session['questions_yes']
    return render(request, 'home.html', {
        'questions': get_randomized_questions(),
        'questions_yes': questions_yes,
    })


@login_required
def decision(request):
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
        return redirect('/rank')
    decision_types_comma_delimited = ''
    if 'decision_types' in request.session:
        for decision_type in request.session['decision_types']:
            decision_types_comma_delimited += decision_type + ','
    return render(request, 'decision.html', {
        'decision_types': decision_types_comma_delimited,
        'step': 1,
    })


success = {
    "new": "I created a new solution that I hadn't considered when I started.",
    "gut": "I trusted my gut instinct and followed my heart.",
    "evidence": "I acted on a strong plan based in evidence.",
    "options": "I considered all my options and took my time to decide.",
    "guidance": "I relied on the guidance of the friends and people I trust.",
}


@login_required
def rank(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/decision')
        request.session['success'] = request.POST['success']
        return redirect('/questions')
    success_keys = success.keys()
    random.shuffle(success_keys)
    success_shuffled = []
    for success_key in success_keys:
        success_shuffled.append([success_key, success[success_key]])
    return render(request, 'rank.html', {
        'success': success_shuffled,
        'step': 2,
    })


@login_required
def questions(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/rank')
        questions_yes = request.POST.getlist('question[]')
        request.session['questions_yes'] = questions_yes
        top_archetypes = area_app.archetypes.get_top_archetypes(questions_yes)
        request.session['archetype'] = top_archetypes
        top_archetype = top_archetypes[0]
        request.session['top_archetype'] = top_archetype[0]
        return redirect('/archetype')
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


@login_required
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


@login_required
def archetype_info(request):
    archetype = request.GET['t']


@login_required
def cheetah_sheets(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/archetype')
        return redirect('/summary')
    attributes = request.session['attributes']
    attribute_cheetahs = area_app.biases.get_top(attributes, area_app.biases.attribute_cheetahs)
    request.session['cheetah_sheets'] = attribute_cheetahs
    return render(request, 'cheetah_sheets.html', {
        'attribute_cheetahs': attribute_cheetahs,
        'step': 5,
    })


@login_required
def archetypes_list(request):
    return render(request, 'archetypes.html', {
        'step': 4,
    })


@login_required
def action_map(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/archetype')
        request.session['commitment'] = request.POST['commitment']
        request.session['commitment_days'] = request.POST['days']
        request.session['email_sent'] = False

        return redirect('/summary')
    if 'top_archetype' not in request.session:
        return render(request, 'action_map.html', {})
    archetype = request.session['top_archetype']
    archetype_cheetahs = area_app.archetypes.archetype_cheetah_sheets[archetype]
    request.session['cheetah_sheets'] = archetype_cheetahs
    return render(request, 'action_map.html', {
        'type': request.session['decision_type'],
        'decision': request.session['decision'],
        'options': request.session['options'],
        'timeframe': request.session['timeframe'],
        'archetype': archetype,
        'cheetahs': archetype_cheetahs,
        'step': 5,
    })


@login_required
def summary(request):
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
        'step': 5,
    })


def cheetah_master(request):
    cheetahs = os.listdir('../area/templates/cheetah')
    return render(request, 'cheetah_master.html', {
        'cheetahs': cheetahs,
    })


@login_required
def autocomplete_dd(request):
    return json.dumps({'results': dream_directors})


@login_required
def restart_session(request):
    for key in request.session.keys():
        if not key.startswith('_'):
            del request.session[key]
    return redirect('/decision')