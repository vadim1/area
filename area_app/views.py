from django.shortcuts import render, redirect
import biases
import archetypes
import random


def restart_session(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/decision')


def home(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/home')
        return redirect('/decision')
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


def critical_concepts(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/decision')
        request.session['success'] = request.POST['success']
        return redirect('/edges_pitfalls')

    return render(request, 'critical_concepts.html', {
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
    archetype = request.session['top_archectype']
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
    return render(request, 'summary.html', {
        'type': request.session['decision_type'],
        'decision': request.session['decision'],
        'options': request.session['options'],
        'timeframe': request.session['timeframe'],
        'archetype': request.session['top_archectype'],
        'cheetahs': request.session['cheetah_sheets'],
        'commitment': request.session['commitment'],
        'commitment_days': request.session['commitment_days'],
    })

