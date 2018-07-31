from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Module2 as Module, Course
from module1.models import Module1 as PreviousModule
from module1.views import load_module as load_module1
from datetime import datetime
from decisions.views import load_course, load_json, load_module, base_intro, base_instructions, base_map, base_restart,\
    base_review, base_summary
import json


prefix = "module" + str(Module.num()) + "/"


def load_this_module(request, step=None):
    return load_module(request, Module, step)


def load_previous_module(request):
    return load_module(request, PreviousModule)


@login_required
def intro(request):
    return base_intro(request, Module, prefix)


@login_required
def review(request):
    module1 = load_previous_module(request)
    return base_review(request, Module, PreviousModule, {
        'decision_buddy': module1.decision_buddy,
        'decision': module1.decision,
        'cc': load_json(module1.cc),
    }, prefix)


@login_required
def map(request):
    return base_map(request, Module, prefix)


@login_required
def instructions(request):
    return base_instructions(request, Module, prefix)


@login_required
def summary(request):
    return base_summary(request, Module, prefix)


@login_required
def restart(request):
    return base_restart(request, Module, prefix)


game_questions = {
    'authority1': {
        'question': 'When your mom asks you to do something do you...',
        'answer0': 'Do it automatically',
        'answer1': 'Question it first',
        'bias': 'authority',
        'bias_answer': 0,
    },
    'authority2': {
        'question': 'Your aunt says you should just apply to safety schools. Do you...',
        'answer0': 'Follow her advice without questioning it',
        'answer1': 'You check with your guidance counselor',
        'bias': 'authority',
        'bias_answer': 1,
    },
    'liking1': {
        'question': 'When a friend asks you to get ice cream late in the evening, do you...',
        'answer0': 'Say yes, because she is your friend',
        'answer1': 'Say no, because of the time',
        'bias': 'liking',
        'bias_answer': 0,
    },
    'liking2': {
        'question': 'When you go down the cereal aisle do you...',
        'answer0': 'Automatically look for the cereal you want',
        'answer1': 'Look at all of the cereal boxes',
        'bias': 'liking',
        'bias_answer': 0,
    },
    'planning2': {
        'question': 'When you look at your homework list, do you...',
        'answer0': 'Start and it will take you until you are done or run out of time',
        'answer1': 'Go over the entire list and guess how long each will take so you can budget your time',
        'bias': 'planning',
        'bias_answer': 0,
    },
    'planning3': {
        'question': 'You have a big math test in two days. Do you...',
        'answer0': 'Start studying tonight so you have time to ask for help tomorrow',
        'answer1': 'Figure starting tomorrow will be enough time to prepare',
        'bias': 'planning',
        'bias_answer': 1,
    },
    'optimism1': {
        'question': 'If you just passed your driver\'s license test, do you...',
        'answer0': 'Believe you are an above average driver',
        'answer1': 'Think that\'s silly, how could you be?',
        'bias': 'optimism',
        'bias_answer': 0,
    },
    'optimism2': {
        'question': 'You need to pick up your little sister from school do you...',
        'answer0': 'Remind her that you\'re getting her and tell her where to meet you',
        'answer1': 'Figure you can show up and it will all work out',
        'bias': 'optimism',
        'bias_answer': 1,
    },
    'social1': {
        'question': 'At school all of your friends are wearing a popular new brand of sneakers. Do you...',
        'answer0': 'Save up for your own pair, too',
        'answer1': 'Stick with your regular shoes, they\'re fine',
        'bias': 'social',
        'bias_answer': 0,
    },
    'social2': {
        'question': 'You overheard some kids are sneaking alcohol into a party you\'re going to. Do you...',
        'answer0': 'Drink some, because it\'s easier to go along',
        'answer1': 'Going along with the crowd isn\'t a factor in your decision',
        'bias': 'social',
        'bias_answer': 0,
    },
    'projection1': {
        'question': 'You see tickets for your favorite band playing a show nearby. Do you...',
        'answer0': 'Buy two tickets, of course your friend will want to come',
        'answer1': 'You ask your friend first, they\'re pricey tickets',
        'bias': 'projection',
        'bias_answer': 0,
    },
    'projection2': {
        'question': 'You\'re assigned a group project. Do you...',
        'answer0': 'Wait for the girl who always leads to to tell you your role',
        'answer1': 'Look at the tasks and sign up for the one you want',
        'bias': 'projection',
        'bias_answer': 0,
    },
}

biases = [
    {'key': 'authority', 'label': 'Authority Bias'},
    {'key': 'liking', 'label': 'Liking Bias'},
    {'key': 'planning', 'label': 'Planning Bias'},
    {'key': 'optimism', 'label': 'Optimism Bias'},
    {'key': 'social', 'label': 'Social Proof'},
    {'key': 'projection', 'label': 'Projection Bias'},
]


def calculate_biases(answers):
    biases = {}
    for i in range(0, len(game_questions.values())):
        question_i = game_questions.values()[i]
        bias = question_i['bias']
        if bias not in biases:
            biases[bias] = {
                'total': 1,
                'biased': 0,
                'ratio': 0,
            }
        else:
            biases[bias]['total'] += 1
        if answers[question_i['title']] == '':
            answers[question_i['title']] = 0  # TODO - shouldn't need it
        if int(answers[question_i['title']]) == int(question_i['bias_answer']):
            biases[bias]['biased'] += 1
        biases[bias]['ratio'] = int(float(biases[bias]['biased']) / float(biases[bias]['total']) * 100)
    return biases


@login_required
def clear_game_answers(module):
    if module.answers:
        module.answers = json.dumps({})
        module.save()


@login_required
def game(request):
    module = load_this_module(request, 'game')
    attr = 'easy'  # For count-down timer

    # Add title to each question
    for title in game_questions.keys():
        game_questions[title]['title'] = title

    if request.method == 'POST':
        answers = {}
        if module.answers:
            answers = load_json(module.answers)
        for i in range(0, len(game_questions.values())):
            index = str(i)
            question_i = game_questions.values()[i]
            attr_i = request.POST.get('answer[' + index + ']')
            answers[question_i['title']] = attr_i
        module.answers = json.dumps(answers)
        module.biases = json.dumps(calculate_biases(answers))
        module.save()
        return redirect('/decisions/2/game_end')
    else:
        clear_game_answers(module)  # TODO - save old answers
    return render(request, prefix+'game.html', {
        'questions': game_questions.values(),
        'attr': attr,
        'num_questions': len(game_questions),
    })


@login_required
def game_end(request):
    module = load_this_module(request, 'game_end')
    return render(request, prefix+'game_end.html', {
    })


@login_required
def explain(request):
    module = load_this_module(request, 'explain')
    return render(request, prefix+'explain.html', {
    })


@login_required
def bias(request):
    module = load_this_module(request, 'bias')
    return render(request, prefix+'bias.html', {
    })


@login_required
def game_results(request):
    module = load_this_module(request, 'game_results')
    return render(request, prefix+'game_results.html', {
        'biases': load_json(module.biases),
        'answers': module.answers_json,
        'questions': game_questions,
    })


@login_required
def game2_intro(request):
    module = load_this_module(request, 'game2_intro')
    return render(request, prefix+'game2_intro.html', {
    })


@login_required
def game2(request):
    module = load_this_module(request, 'game2')
    return render(request, prefix+'game2.html', {
        'questions': game_questions.values(),
        'biases': biases,
        'num_questions': len(game_questions),
    })


@login_required
def nylah1(request):
    module = load_this_module(request, 'nylah1')
    return render(request, prefix+'nylah1.html', {
    })


@login_required
def nylah2(request):
    module = load_this_module(request, 'nylah2')
    return render(request, prefix+'nylah2.html', {
    })


@login_required
def nylah3(request):
    module = load_this_module(request, 'nylah3')
    if request.method == 'POST':
        module.nylah_bias = request.POST['nylah_bias']
        module.save()
        return redirect('/decisions/2/nylah4')
    return render(request, prefix+'nylah3.html', {
        'biases': load_json(module.biases).keys(),
    })


@login_required
def nylah4(request):
    module = load_this_module(request, 'nylah4')
    return render(request, prefix+'nylah4.html', {
        'nylah_bias': module.nylah_bias,
    })


@login_required
def nylah5(request):
    module = load_this_module(request, 'nylah5')
    return render(request, prefix+'nylah5.html', {
    })


@login_required
def nylah50(request):
    module = load_this_module(request, 'nylah50')
    return render(request, prefix+'nylah50.html', {
    })


@login_required
def nylah51(request):
    module = load_this_module(request, 'nylah51')
    return render(request, prefix+'nylah51.html', {
    })


@login_required
def nylahotherfacts(request):
    module = load_this_module(request, 'nylahotherfacts')
    return render(request, prefix+'nylahotherfacts.html', {
    })


@login_required
def nylah52(request):
    module = load_this_module(request, 'nylah52')
    return render(request, prefix+'nylah52.html', {
    })


@login_required
def nylah6(request):
    module = load_this_module(request, 'nylah6')
    if request.method == 'POST':
        facts = request.POST.getlist('facts[]')
        # TODO: save facts
        return redirect('/decisions/2/nylah61')
    return render(request, prefix+'nylah6.html', {
        'facts': [
            [
                'Tuition',
                'Housing',
            ],
            [
                'Required Courses',
                'Average SAT/ACT Scores',
            ],
            [
                'Graduation Rates',
                'Financial Aid',
            ],
        ],
    })


@login_required
def nylah61(request):
    module = load_this_module(request, 'nylah61')
    if request.method == 'POST':
        opinions_reality = request.POST.get('opinions_reality')
        opinions_importance = request.POST.get('opinions_importance')
        # TODO: save
        return redirect('/decisions/2/nylah7')
    return render(request, prefix+'nylah61.html', {
    })


@login_required
def nylah7(request):
    module = load_this_module(request, 'nylah7')
    if request.method == 'POST':
        opinions = Exception(request.POST.getlist('opinions[]'))
        # TODO: save opinions
        return redirect('/decisions/2/nylah8')
    return render(request, prefix+'nylah7.html', {
        'opinions': [
            'The weather is in Ohio and Maine',
            'How interesting the classes are',
            'Whether the professors are good',
            'How hard it is to get into classes',
            'How nice the dorms are',
            'How the food is',
            'How much homework there is',
            'Greek life',
        ],
    })


@login_required
def nylah8(request):
    module = load_this_module(request, 'nylah8')
    return render(request, prefix+'nylah8.html', {
    })


@login_required
def nylah_cc(request):
    module = load_this_module(request, 'nylah_cc')
    return render(request, prefix+'nylah_cc.html', {
    })


@login_required
def nylah_cc_facts(request):
    module = load_this_module(request, 'nylah_cc_facts')
    return render(request, prefix+'nylah_cc_facts.html', {
    })


@login_required
def nylah_cc_assumptions(request):
    module = load_this_module(request, 'nylah_cc_assumptions')
    return render(request, prefix+'nylah_cc_assumptions.html', {
        'biases': biases,
    })


@login_required
def nylah_cc_evidence(request):
    module = load_this_module(request, 'nylah_cc_evidence')
    return render(request, prefix+'nylah_cc_evidence.html', {
    })


@login_required
def cc(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'cc')
    if request.method == 'POST':
        # TODO: save Critical Concepts
        return redirect('/decisions/2/summary')
    return render(request, prefix+'cc.html', {
        'cc': load_json(module1.cc),
        'decision': module1.decision,
        'biases': biases,
    })


@login_required
def cc_edit(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'cc_edit')
    if request.method == 'POST':
        # Save Critical Concepts
        module1.cc = json.dumps(request.POST.getlist('cc[]'))
        module1.save()
        return redirect('/decisions/2/steps2')
    return render(request, prefix+'cc_edit.html', {
        'cc': load_json(module1.cc),
        'decision': module1.decision,
        'biases': biases,
    })


@login_required
def steps(request):
    module = load_this_module(request, 'steps')
    return render(request, prefix+'steps.html', {
    })


@login_required
def steps2(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'steps2')
    return render(request, prefix+'steps2.html', {
        'cc': load_json(module1.cc),
        'decision': module1.decision,
    })


nylah_ccs = [
    "It has a good graphic design program.",
    "I'm able to afford it.",
    "My family supports my decision.",
]

nylah_facts = [
    [
        "I gathered facts from the colleges' websites about their graphic design programs. Ohio State has a major and Bates doesn't.",
        "I got the data I needed directly from searching for graphic design on the colleges' websites.",
        "I checked my assumptions and am glad I did. Bates doesn't have a program so I won't apply there.",
    ],
    [
        "I don't have facts. My parents say I can choose the college I want to attend.",
        "I could find facts by searching for tuition facts from all of my college choices. I could also download financial aid forms from the college websites and discuss the facts and forms with my parents.",
        "The Authority Bias might be at work because my parents are authority figures.",
    ],
    [
        "My facts come from my observation that my family is helping me with my college search.",
        "I don't think I need more facts.",
        "I am assuming their support is genuine (even though they will miss me). Social Proof could be at work. They might be doing what they think is best for me. ",
    ],
]


@login_required
def steps3(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'steps3')
    back = '/decisions/2/steps2'
    cc_num = int(request.GET.get('num', 0))
    fact = ''
    source = ''
    bias = ''
    if request.method == 'POST':
        cc_num = int(request.POST.get('num'))
        fact = request.POST['fact']
        source = request.POST['source']
        bias = request.POST['bias']
        if cc_num == 0:
            module.fact0 = fact
            module.source0 = source
            module.bias0 = bias
        elif cc_num == 1:
            module.fact1 = fact
            module.source1 = source
            module.bias1 = bias
        elif cc_num == 2:
            module.fact2 = fact
            module.source2 = source
            module.bias2 = bias
        else:
            raise Exception("Unexpected index: " + str(cc_num))
        module.save()
        cc_num = cc_num + 1
        if cc_num > 2:
            # Send email
            mail_body = module1.decision_buddy + ',' + '%0D%0D' + \
                        'Please help me with a big decision: ' + module1.decision + '%0D%0D'
            for concept in load_json(module1.cc):
                mail_body += concept + '%0D'
            mail_body += '%0D' + \
                         'Would you help me get started?  Here are a few questions I need to answer:' + '%0D%0D' + \
                         'What are the organizations involved in your decision?' + '%0D' + \
                         'Who are the people who could help you make your decision?' + '%0D' + \
                         'What do you need to find out?' + '%0D' + \
                         'How will getting information help you make your decision?' + '%0D%0D' + \
                         'Thank you!'
            to = module1.decision_buddy_email + ',' + request.user.email
            return redirect('/decisions/2/steps4')
        else:
            return redirect('/decisions/2/steps3?num=' + str(cc_num))
    if cc_num > 0:
        back = '/decisions/2/steps3?num=' + str(cc_num - 1)
    if cc_num == 0:
        fact = module.fact0
        source = module.source0
        bias = module.bias0
    elif cc_num == 1:
        fact = module.fact1
        source = module.source1
        bias = module.bias1
    elif cc_num == 2:
        fact = module.fact2
        source = module.source2
        bias = module.bias2
    cc_json = load_json(module1.cc)
    cc_current = cc_num
    if 'cc_num' in cc_json:
        cc_current = cc_json['cc_num']
    return render(request, prefix+'steps3.html', {
        'num': cc_num,
        'n': cc_num + 1,
        'cc': cc_json,
        'cc_current': cc_current,
        'decision': module1.decision,
        'nylah_cc': nylah_ccs[cc_num],
        'nylah_facts': nylah_facts[cc_num],
        'biases': biases,
        'back': back,
        'fact': fact,
        'source': source,
        'bias': bias,
    })


@login_required
def steps4(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'steps4')
    if request.method == 'POST':
        return redirect('/decisions/2/summary')
    mail_body = module1.decision_buddy + ',' + '%0D%0D' + \
                'Please help me validate facts for a big decision: ' + module1.decision + '%0D%0D'
    ccs = load_json(module1.cc)
    mail_body += 'I have identified 3 Critical Concepts. For each one I need to collect facts and make sure that I am not falling prey to biases. Please help me work through verifying the facts for each Critical Concept.' + '%0D%0D' + \
                 'Critical Concept: ' + ccs[0] + '%0D' + \
                 'Fact: ' + module.fact0 + '%0D' + \
                 'Source: ' + module.source0 + '%0D' + \
                 'Bias: ' + module.bias0 + '%0D%0D' + \
                 'Critical Concept: ' + ccs[1] + '%0D' + \
                 'Fact: ' + module.fact1 + '%0D' + \
                 'Source: ' + module.source1 + '%0D' + \
                 'Bias: ' + module.bias1 + '%0D%0D' + \
                 'Critical Concept: ' + ccs[2] + '%0D' + \
                 'Fact: ' + module.fact2 + '%0D' + \
                 'Source: ' + module.source2 + '%0D' + \
                 'Bias: ' + module.bias2 + '%0D%0D' + \
                 'Thank you!'
    to = module1.decision_buddy_email + ',' + request.user.email
    return render(request, prefix+'steps4.html', {
        'subject': 'Decision Buddy - Help with fact finding',
        'decision_buddy': module1.decision_buddy,
        'decision_buddy_email': module1.decision_buddy_email,
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'mail_body': mail_body,
        'to': to,
        'fact0': module.fact0,
        'source0': module.source0,
        'bias0': module.bias0,
        'fact1': module.fact1,
        'source1': module.source1,
        'bias1': module.bias1,
        'fact2': module.fact2,
        'source2': module.source2,
        'bias2': module.bias2,
    })


@login_required
def cheetah(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'cheetah')
    if request.method == 'POST':
        # TODO: save cheetah
        # module1.cc = json.dumps(request.POST.getlist('cc[]'))
        # module1.save()
        return redirect('/decisions/2/summary')
    return render(request, prefix+'cheetah.html', {
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'evidence0': load_json(module.evidence0),
        'evidence1': load_json(module.evidence1),
        'evidence2': load_json(module.evidence2),
    })


@login_required
def summary(request):
    module1 = load_previous_module(request)
    module = load_this_module(request, 'summary')
    module.completed_on = datetime.now()
    module.save()
    return render(request, prefix+'summary.html', {
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'evidence0': load_json(module.evidence0),
        'evidence1': load_json(module.evidence1),
        'evidence2': load_json(module.evidence2),
    })
