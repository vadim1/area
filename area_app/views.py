from django.shortcuts import render, redirect
import biases


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
        # request.session['personal'] = request.POST['personal']
        decision = request.POST['decision']
        request.session['decision'] = decision
        return redirect('/critical_concepts')
    return render(request, 'decision.html', {
    })


def critical_concepts(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/decision')
        request.session['good_outcome'] = request.POST['good_outcome']
        request.session['issues'] = request.POST['issues']
        #request.session['how_to_know'] = request.POST['how_to_know']
        #request.session['matters_less'] = request.POST['matters_less']
        request.session['critical_concept_1'] = request.POST['critical_concept_1']
        request.session['critical_concept_2'] = request.POST['critical_concept_2']
        request.session['critical_concept_3'] = request.POST['critical_concept_3']

        summary = request.session['critical_concept_1']
        if request.session['critical_concept_2']:
            if summary:
                summary += ', '
            summary += request.session['critical_concept_2']
        if request.session['critical_concept_3']:
            if summary:
                summary += ', '
            summary += request.session['critical_concept_3']
        request.session['critical_concepts'] = summary

        return redirect('/edges_pitfalls')

    return render(request, 'critical_concepts.html', {
    })


def edges_pitfalls(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/critical_concepts')
        attributes = {}
        for attribute in request.POST:
            if attribute == 'csrfmiddlewaretoken' or attribute == 'submit':
                continue
            if attribute.endswith('_explain'):
                value = request.POST[attribute]
                if value and value != '':
                    if 'explains' in request.session:
                        explains = request.session['explains']
                    else:
                        explains = {}
                    explains[attribute] = request.POST[attribute]
                    request.session['explains'] = explains
                continue
            weight = request.POST[attribute]
            if int(weight) > 0 or int(weight) < 0:
                attributes[attribute] = weight
        request.session['attributes'] = attributes
        attributes_sorted = sorted(attributes.iteritems(), key=lambda (k, v): (v, k), reverse=True)
        request.session['attributes_sorted'] = attributes_sorted
        edges = []
        pitfalls = []
        for attribute, weight in attributes_sorted:
            if int(weight) > 0:
                edges.append(attribute + " (" + weight + ")")
            else:
                pitfalls.append(attribute + " (" + unicode(abs(int(weight))) + ")")
        request.session['edges'] = edges
        request.session['pitfalls'] = pitfalls
        return redirect('/cognitive_biases')
    return render(request, 'edges_pitfalls.html', {
        'attributes': biases.attributes.items(),
    })


def cognitive_biases(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'Back': return redirect('/edges_pitfalls')
        return redirect('/cheetah_sheets')
    attributes = request.session['attributes']
    attribute_biases = biases.get_top(attributes, biases.attribute_biases)
    top_biases = []
    for bias, weight in attribute_biases:
        description = biases.biases[bias]
        top_biases.append(
            {'bias': bias, 'weight': weight, 'description': description}
        )
    request.session['cognitive_biases'] = top_biases
    return render(request, 'cognitive_biases.html', {
        'biases': top_biases,
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


def summary(request):
    request.session['summary'] = 1
    attributes_sorted = request.session['attributes_sorted']
    edges = []
    pitfalls = []
    explains = {}
    if 'explains' in request.session:
        explains = request.session['explains']
    for attribute, weight in attributes_sorted:
        explain = ''
        if attribute+'_explain' in explains:
            explain = ' - ' + explains[attribute+'_explain']
        if int(weight) > 0:
            desc = attribute + ": " + weight + explain
            edges.append(desc)
        else:
            desc = attribute + ": " + unicode(abs(int(weight))) + explain
            pitfalls.append(desc)

    return render(request, 'summary.html', {
        'edges': edges,
        'pitfalls': pitfalls,
    })

