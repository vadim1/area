from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import biases
import archetypes
import random
import os
import json


def restart_session(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/decision')


def logged_in(request):
    return redirect('/')


def check_partner(request):
    partner = ''
    if 'partner' in request.GET:
        partner = request.GET['partner']
    request.session['partner'] = partner


def home(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/home')
        return redirect('/decision')
    check_partner(request)
    return render(request, 'home.html', {
    })


def decision(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/')
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
        return redirect('/critical_concepts')
    decision_types_comma_delimited = ''
    if 'decision_types' in request.session:
        for decision_type in request.session['decision_types']:
            decision_types_comma_delimited += decision_type + ','
    return render(request, 'decision.html', {
        'decision_types': decision_types_comma_delimited
    })


success = {
    "new": "I created a new solution that I hadn't considered when I started.",
    "gut": "I trusted my gut instinct and followed my heart.",
    "evidence": "I acted on a strong plan based in evidence.",
    "options": "I considered all my options and took my time to decide.",
    "guidance": "I relied on the guidance of the friends and people I trust.",
}


def critical_concepts(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/decision')
        request.session['success'] = request.POST['success']
        return redirect('/edges_pitfalls')
    success_keys = success.keys()
    random.shuffle(success_keys)
    success_shuffled = []
    for success_key in success_keys:
        success_shuffled.append([success_key, success[success_key]])
    return render(request, 'critical_concepts.html', {
        'success': success_shuffled,
    })


def edges_pitfalls(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/critical_concepts')
        questions_yes = request.POST.getlist('question[]')
        request.session['questions_yes'] = questions_yes
        top_archetypes = archetypes.get_top_archetypes(questions_yes)
        request.session['archetype'] = top_archetypes
        top_archetype = top_archetypes[0]
        request.session['top_archetype'] = top_archetype[0]
        return redirect('/cognitive_biases')
    # Randomize the order of questions
    random_order_questions = []
    for question, weights in archetypes.edges_pitfalls.items():
        random_order_questions.append(question)
    random.shuffle(random_order_questions)
    questions_yes = ''
    if 'questions_yes' in request.session:
        questions_yes = request.session['questions_yes']
    return render(request, 'edges_pitfalls.html', {
        'questions': random_order_questions,
        'questions_yes': questions_yes,
    })


def cognitive_biases(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/edges_pitfalls')
        return redirect('/action_map')
    if 'archetype' not in request.session:
        return render(request, 'cognitive_biases.html', {
        })
    top_archetypes = request.session['archetype']
    top_archetype = top_archetypes[0]
    return render(request, 'cognitive_biases.html', {
        'archetype': top_archetype[0],
        'strength': top_archetype[1]
    })


def cheetah_sheets(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/cognitive_biases')
        return redirect('/summary')
    attributes = request.session['attributes']
    attribute_cheetahs = biases.get_top(attributes, biases.attribute_cheetahs)
    request.session['cheetah_sheets'] = attribute_cheetahs
    return render(request, 'cheetah_sheets.html', {
        'attribute_cheetahs': attribute_cheetahs,
    })


def action_map(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/cognitive_biases')
        request.session['commitment'] = request.POST['commitment']
        request.session['commitment_days'] = request.POST['days']
        return redirect('/summary')
    if 'top_archetype' not in request.session:
        return render(request, 'action_map.html', {});
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
    })


def summary(request):
    request.session['summary'] = 1
    if 'decision' not in request.session:
        return render(request, 'summary.html', {});
    return render(request, 'summary.html', {
        'type': request.session['decision_type'],
        'decision': request.session['decision'],
        'options': request.session['options'],
        'timeframe': request.session['timeframe'],
        'archetype': request.session['top_archetype'],
        'cheetahs': request.session['cheetah_sheets'],
        'commitment': request.session['commitment'],
        'commitment_days': request.session['commitment_days'],
    })


def cheetah_master(request):
    cheetahs = os.listdir('../area/views/cheetah')
    return render(request, 'cheetah_master.html', {
        'cheetahs': cheetahs,
    })


dream_directors = [
    'Bob, New York',
    'Jill, California',
]


def autocomplete_dd(request):
    return json.dumps({'results': dream_directors})
