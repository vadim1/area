from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from area_app import forms
from .models import Course, Module1, Module2
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


def load_json(json_data):
    json_object = {}
    try:
        json_object = json.loads(json_data)
    except ValueError, e:
        pass
        # TODO - log
    return json_object


@login_required
def home(request):
    request.session['start'] = '/decisions'
    request.session['partner'] = 'fp'
    course = load_course(request)
    module1 = load_module1(request)
    module2 = load_module2(request)
    # If it's the first time, take them to the tour
    if not course.intro_on:
        return redirect('/decisions/tour')
    return render(request, 'decisions/intro.html', {
        'form': forms.FutureProjectSignupForm,
        'module1': module1,
        'module2': module2,
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
            module1.answers_json = load_json(module1.answers)
    if not module1:
        module1 = Module1()
        module1.answers_json = None
    return module1


def module1(request):
    module1 = load_module1(request, '')
    return render(request, 'decisions/module1/intro.html', {
    })


def load_module2(request, step=''):
    module2 = None
    course = load_course(request)
    if course:
        module2list = Module2.objects.filter(course=course)
        if module2list:
            module2 = module2list.first()
            if step:
                module2.step = step
                module2.save()
        else:
            module2 = Module2(course=course, step=step)
            module2.save()
        module2.answers_json = ''
        if module2.answers:
            module2.answers_json = load_json(module2.answers)
    if not module2:
        module2 = Module2()
        module2.answers_json = None
    return module2


def module2(request):
    module2 = load_module2(request, '')
    return render(request, 'decisions/module2/intro.html', {
    })


def module1instructions(request):
    module1 = load_module1(request, 'instructions')
    return render(request, 'decisions/module1/instructions.html', {
    })


def module1game1_end(request):
    module1 = load_module1(request, 'game1_end')
    return render(request, 'decisions/module1/game1_end.html', {
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
    'Bullying': 'Watch someone get bullied or take action?',
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
            answers = load_json(module1.answers)
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
        return redirect('/decisions/1/' + next)
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
    return game(request, module1, 'easy', 'game1_end')


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


def module1game_explained(request):
    module1 = load_module1(request, 'game_explained')
    return render(request, 'decisions/module1/game_explained.html', {
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


def module1details2(request):
    module1 = load_module1(request, 'details2')
    return render(request, 'decisions/module1/details2.html', {
    })


def module1details3(request):
    module1 = load_module1(request, 'details3')
    if request.method == 'POST':
        living = request.POST.get('living')
        # TODO: save living
        return redirect('/decisions/1/sample')
    return render(request, 'decisions/module1/details3.html', {
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
            'Worried I will make a poor decision',
            'Worried about what other people will think of my decision',
            'Not sure that I need to make the decision now',
        ],
    })


def module1sample(request):
    module1 = load_module1(request, 'sample')
    if request.method == 'POST':
        module1.cc0 = request.POST.get('cc0')
        module1.cc1 = request.POST.get('cc1')
        module1.cc2 = request.POST.get('cc2')
        module1.save()
        return redirect('/decisions/1/cc')
    return render(request, 'decisions/module1/sample.html', {
        'answers': module1.answers_json,
        'cc0': module1.cc0,
        'cc1': module1.cc1,
        'cc2': module1.cc2,
    })


def module1nylah_decision(request):
    module1 = load_module1(request, 'nylah_decision')
    return render(request, 'decisions/module1/nylah_decision.html', {
        'answers': module1.answers_json,
    })


def module1cc(request):
    module1 = load_module1(request, 'cc')
    return render(request, 'decisions/module1/cc.html', {
    })


def module1defining_cc(request):
    module1 = load_module1(request, 'defining_cc')
    return render(request, 'decisions/module1/defining_cc.html', {
    })


def module1deriving_cc(request):
    module1 = load_module1(request, 'deriving_cc')
    if request.method == 'POST':
        module1.cc0 = request.POST.get('cc0')
        module1.cc1 = request.POST.get('cc1')
        module1.cc2 = request.POST.get('cc2')
        module1.save()
        return redirect('/decisions/1/exploring_cc')
    return render(request, 'decisions/module1/deriving_cc.html', {
        'cc0': module1.cc0,
        'cc1': module1.cc1,
        'cc2': module1.cc2,
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
        'cc': load_json(module1.cc),
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
    return render(request, 'decisions/module1/commitment.html', {
        'decision_buddy': module1.decision_buddy,
        'decision_buddy_email': module1.decision_buddy_email,
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'mail_body': mail_body,
        'to': to,
    })


def module1summary(request):
    module1 = load_module1(request, 'summary')
    module1.completed_on = datetime.now()
    module1.save()
    return render(request, 'decisions/module1/summary.html', {
        'decision_buddy': module1.decision_buddy,
        'decision': module1.decision,
        'cc': load_json(module1.cc),
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


def module2review(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'review')
    return render(request, 'decisions/module2/review.html', {
        'decision_buddy': module1.decision_buddy,
        'decision': module1.decision,
        'cc': load_json(module1.cc),
    })


def module2map(request):
    module2 = load_module2(request, 'map')
    return render(request, 'decisions/module2/map.html', {
    })


def module2instructions(request):
    module2 = load_module2(request, 'instructions')
    return render(request, 'decisions/module2/instructions.html', {
    })


module2game_questions = {
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
    for i in range(0, len(module2game_questions.values())):
        question_i = module2game_questions.values()[i]
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


def module2game(request):
    module2 = load_module2(request, 'game')
    attr = 'easy'  # For count-down timer

    # Add title to each question
    for title in module2game_questions.keys():
        module2game_questions[title]['title'] = title

    if request.method == 'POST':
        answers = {}
        if module2.answers:
            answers = load_json(module2.answers)
        for i in range(0, len(module2game_questions.values())):
            index = str(i)
            question_i = module2game_questions.values()[i]
            attr_i = request.POST.get('answer[' + index + ']')
            answers[question_i['title']] = attr_i
        module2.answers = json.dumps(answers)
        module2.biases = json.dumps(calculate_biases(answers))
        module2.save()
        return redirect('/decisions/2/game_end')
    else:
        clear_game_answers(module2)  # TODO - save old answers
    return render(request, 'decisions/module2/game.html', {
        'questions': module2game_questions.values(),
        'attr': attr,
        'num_questions': len(module2game_questions),
    })


def module2game_end(request):
    module2 = load_module2(request, 'game_end')
    return render(request, 'decisions/module2/game_end.html', {
    })


def module2explain(request):
    module2 = load_module2(request, 'explain')
    return render(request, 'decisions/module2/explain.html', {
    })


def module2bias(request):
    module2 = load_module2(request, 'bias')
    return render(request, 'decisions/module2/bias.html', {
    })


def module2game_results(request):
    module2 = load_module2(request, 'game_results')
    return render(request, 'decisions/module2/game_results.html', {
        'biases': load_json(module2.biases),
        'answers': module2.answers_json,
        'questions': module2game_questions,
    })


def module2game2_intro(request):
    module2 = load_module2(request, 'game2_intro')
    return render(request, 'decisions/module2/game2_intro.html', {
    })


def module2game2(request):
    module2 = load_module2(request, 'game2')
    return render(request, 'decisions/module2/game2.html', {
        'questions': module2game_questions.values(),
        'biases': biases,
        'num_questions': len(module2game_questions),
    })


def module2nylah1(request):
    module2 = load_module2(request, 'nylah1')
    return render(request, 'decisions/module2/nylah1.html', {
    })


def module2nylah2(request):
    module2 = load_module2(request, 'nylah2')
    return render(request, 'decisions/module2/nylah2.html', {
    })


def module2nylah3(request):
    module2 = load_module2(request, 'nylah3')
    if request.method == 'POST':
        module2.nylah_bias = request.POST['nylah_bias']
        module2.save()
        return redirect('/decisions/2/nylah4')
    return render(request, 'decisions/module2/nylah3.html', {
        'biases': load_json(module2.biases).keys(),
    })


def module2nylah4(request):
    module2 = load_module2(request, 'nylah4')
    return render(request, 'decisions/module2/nylah4.html', {
        'nylah_bias': module2.nylah_bias,
    })


def module2nylah5(request):
    module2 = load_module2(request, 'nylah5')
    return render(request, 'decisions/module2/nylah5.html', {
    })


def module2nylah50(request):
    module2 = load_module2(request, 'nylah50')
    return render(request, 'decisions/module2/nylah50.html', {
    })


def module2nylah51(request):
    module2 = load_module2(request, 'nylah51')
    return render(request, 'decisions/module2/nylah51.html', {
    })


def module2nylahotherfacts(request):
    module2 = load_module2(request, 'nylahotherfacts')
    return render(request, 'decisions/module2/nylahotherfacts.html', {
    })


def module2nylah52(request):
    module2 = load_module2(request, 'nylah52')
    return render(request, 'decisions/module2/nylah52.html', {
    })


def module2nylah6(request):
    module2 = load_module2(request, 'nylah6')
    if request.method == 'POST':
        facts = request.POST.getlist('facts[]')
        # TODO: save facts
        return redirect('/decisions/2/nylah61')
    return render(request, 'decisions/module2/nylah6.html', {
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


def module2nylah61(request):
    module2 = load_module2(request, 'nylah61')
    if request.method == 'POST':
        opinions_reality = request.POST.get('opinions_reality')
        opinions_importance = request.POST.get('opinions_importance')
        # TODO: save
        return redirect('/decisions/2/nylah7')
    return render(request, 'decisions/module2/nylah61.html', {
    })


def module2nylah7(request):
    module2 = load_module2(request, 'nylah7')
    if request.method == 'POST':
        opinions = Exception(request.POST.getlist('opinions[]'))
        # TODO: save opinions
        return redirect('/decisions/2/nylah8')
    return render(request, 'decisions/module2/nylah7.html', {
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


def module2nylah8(request):
    module2 = load_module2(request, 'nylah8')
    return render(request, 'decisions/module2/nylah8.html', {
    })


def module2nylah_cc(request):
    module2 = load_module2(request, 'nylah_cc')
    return render(request, 'decisions/module2/nylah_cc.html', {
    })


def module2nylah_cc_facts(request):
    module2 = load_module2(request, 'nylah_cc_facts')
    return render(request, 'decisions/module2/nylah_cc_facts.html', {
    })


def module2nylah_cc_assumptions(request):
    module2 = load_module2(request, 'nylah_cc_assumptions')
    return render(request, 'decisions/module2/nylah_cc_assumptions.html', {
        'biases': biases,
    })


def module2nylah_cc_evidence(request):
    module2 = load_module2(request, 'nylah_cc_evidence')
    return render(request, 'decisions/module2/nylah_cc_evidence.html', {
    })


def module2cc(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'cc')
    if request.method == 'POST':
        # TODO: save Critical Concepts
        return redirect('/decisions/2/summary')
    return render(request, 'decisions/module2/cc.html', {
        'cc': load_json(module1.cc),
        'decision': module1.decision,
        'biases': biases,
    })


def module2cc_edit(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'cc_edit')
    if request.method == 'POST':
        # Save Critical Concepts
        module1.cc = json.dumps(request.POST.getlist('cc[]'))
        module1.save()
        return redirect('/decisions/2/steps2')
    return render(request, 'decisions/module2/cc_edit.html', {
        'cc': load_json(module1.cc),
        'decision': module1.decision,
        'biases': biases,
    })


def module2steps(request):
    module2 = load_module2(request, 'steps')
    return render(request, 'decisions/module2/steps.html', {
    })


def module2steps2(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'steps2')
    return render(request, 'decisions/module2/steps2.html', {
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


def module2steps3(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'steps3')
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
            module2.fact0 = fact
            module2.source0 = source
            module2.bias0 = bias
        elif cc_num == 1:
            module2.fact1 = fact
            module2.source1 = source
            module2.bias1 = bias
        elif cc_num == 2:
            module2.fact2 = fact
            module2.source2 = source
            module2.bias2 = bias
        else:
            raise Exception("Unexpected index: " + str(cc_num))
        module2.save()
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
        fact = module2.fact0
        source = module2.source0
        bias = module2.bias0
    elif cc_num == 1:
        fact = module2.fact1
        source = module2.source1
        bias = module2.bias1
    elif cc_num == 2:
        fact = module2.fact2
        source = module2.source2
        bias = module2.bias2
    return render(request, 'decisions/module2/steps3.html', {
        'num': cc_num,
        'n': cc_num + 1,
        'cc': load_json(module1.cc),
        'cc_current': load_json(module1.cc)[cc_num],
        'decision': module1.decision,
        'nylah_cc': nylah_ccs[cc_num],
        'nylah_facts': nylah_facts[cc_num],
        'biases': biases,
        'back': back,
        'fact': fact,
        'source': source,
        'bias': bias,
    })


def module2steps4(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'steps4')
    if request.method == 'POST':
        return redirect('/decisions/2/summary')
    mail_body = module1.decision_buddy + ',' + '%0D%0D' + \
                'Please help me validate facts for a big decision: ' + module1.decision + '%0D%0D'
    ccs = load_json(module1.cc)
    mail_body += 'I have identified 3 Critical Concepts. For each one I need to collect facts and make sure that I am not falling prey to biases. Please help me work through verifying the facts for each Critical Concept.' + '%0D%0D' + \
                 'Critical Concept: ' + ccs[0] + '%0D' + \
                 'Fact: ' + module2.fact0 + '%0D' + \
                 'Source: ' + module2.source0 + '%0D' + \
                 'Bias: ' + module2.bias0 + '%0D%0D' + \
                 'Critical Concept: ' + ccs[1] + '%0D' + \
                 'Fact: ' + module2.fact1 + '%0D' + \
                 'Source: ' + module2.source1 + '%0D' + \
                 'Bias: ' + module2.bias1 + '%0D%0D' + \
                 'Critical Concept: ' + ccs[2] + '%0D' + \
                 'Fact: ' + module2.fact2 + '%0D' + \
                 'Source: ' + module2.source2 + '%0D' + \
                 'Bias: ' + module2.bias2 + '%0D%0D' + \
                 'Thank you!'
    to = module1.decision_buddy_email + ',' + request.user.email
    return render(request, 'decisions/module2/steps4.html', {
        'subject': 'Decision Buddy - Help with fact finding',
        'decision_buddy': module1.decision_buddy,
        'decision_buddy_email': module1.decision_buddy_email,
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'mail_body': mail_body,
        'to': to,
        'fact0': module2.fact0,
        'source0': module2.source0,
        'bias0': module2.bias0,
        'fact1': module2.fact1,
        'source1': module2.source1,
        'bias1': module2.bias1,
        'fact2': module2.fact2,
        'source2': module2.source2,
        'bias2': module2.bias2,
    })


def module2cheetah(request):
    module1 = load_module1(request)
    module2 = load_module2(request, 'cheetah')
    if request.method == 'POST':
        # TODO: save cheetah
        # module1.cc = json.dumps(request.POST.getlist('cc[]'))
        # module1.save()
        return redirect('/decisions/2/summary')
    return render(request, 'decisions/module2/cheetah.html', {
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'evidence0': load_json(module2.evidence0),
        'evidence1': load_json(module2.evidence1),
        'evidence2': load_json(module2.evidence2),
    })


def module2summary(request):
    module2 = load_module2(request, 'summary')
    module1 = load_module1(request)
    module2.completed_on = datetime.now()
    module2.save()
    return render(request, 'decisions/module2/summary.html', {
        'decision': module1.decision,
        'cc': load_json(module1.cc),
        'evidence0': load_json(module2.evidence0),
        'evidence1': load_json(module2.evidence1),
        'evidence2': load_json(module2.evidence2),
    })


def module2restart(request):
    module2 = load_module2(request, 'intro')
    module2.completed_on = None
    module2.save()
    return redirect('/decisions/2')
