#!/usr/bin/env python
# -*- coding: latin-1 -*-

from models import QuestionModel, Question

questions = {
    'I tend to make gut decisions.': {
        'yes': {'adventurer': 1},
        'no': {'thinker': 1},
        'why': 'AREA checks your gut with data and evidence.',
    },
    'I like to collect all possible evidence before making a decision.': {
        'yes': {'detective': 1},
        'no': {'adventurer': 1},
        'why': 'Data collection is vital when making a high stakes decision. AREA gives you a structure for doing this. It makes your work more effective and efficient.',
    },
    'I have trouble making decisions because I see all the pros and cons.': {
        'yes': {'thinker': 1},
        'no': {'adventurer': 1, 'visionary': 1},
        'why': 'AREA inverts normal decision making so that you focus on what matters most to you. It also gives you exercises to weigh the pros and cons.',
    },
    'The best way for me to make a decision is to ask others for advice.': {
        'yes': {'listener': 1},
        'no': {'adventurer': 1, 'detective': 1},
        'why': 'Remember that everyone has incentives and motives. AREA makes these explicit.',
    },
    'I always think outside the box when making decisions.': {
        'yes': {'visionary': 1},
        'no': {'detective': 1},
        'why': 'AREA encourages creativity in decision making but makes sure that you have evidence to back your decision.',
    },
    'I always consider how much a decision will cost me before I make it.': {
        'yes': {'detective': 1},
        'no': {'adventurer': 1},
        'why': 'Cost is an important part of making a decision but it\'s not the only part. AREA guides you to look at the numbers but to look at other important data too.',
    },
    'I know where to look for good resources to solve my problems.': {
        'yes': {'thinker': 1, 'detective': 1},
        'no': {},
        'why': 'AREA gives you tools to evaluate the data you collect from the resource you use.',
    },
    'I am good at getting the information I need.': {
        'yes': {'thinker': 1, 'visionary': 1},
        'no': {'adventurer': 1, 'listener': 1},
        'why': 'AREA gives you tools to evaluate the information you collect.',
    },
    'I am good at drawing conclusions.': {
        'yes': {'thinker': 1, 'visionary': 1},
        'no': {'adventurer': 1, 'listener': 1},
        'why': 'It\'s good to analyze your options before making a decisions. AREA makes sure that you don\'t rush to the conclusion by building in space to allow for new information and insights.',
    },
    'I like learning from others.': {
        'yes': {'listener': 1},
        'no': {},
        'why': 'It is good to learn from others but we also want to develop confidence and conviction in our own decision making. AREA gives you a tool kit to do that.',
    },
    'I don\'t like to listen to the opinions of other people - I prefer to make my own decisions.': {
        'yes': {'adventurer': 1},
        'no': {'listener': 1},
        'why': 'Other people may have information that you don\'t have. With the AREA Method you maintain control of your decision making and you make the most of useful resources around you.',
    },
    'I feel overwhelmed when I have too many options.': {
        'yes': {'thinker': 1},
        'no': {'detective': 1},
        'why': 'Decision making can be overwhelming. AREA helps you reduce the options to focus on really matters to you.',
    },
    'I like to get input from my friends to make decisions.': {
        'yes': {'listener': 1},
        'no': {'detective': 1},
        'why': 'Friends can be a great help with decision making but remember that that they have their own perspective. The AREA Method encourages you to go beyond friends so you can arrive at the best solution for you.',
    },
    'I like to come up with creative solutions.': {
        'yes': {},
        'no': {'visionary': 1},
        'why': 'The AREA Method encourages creative decision making but makes sure that you have evidence to back your decision.',
    },
    'I feel the need to make decisions quickly.': {
        'yes': {'adventurer': 1},
        'no': {'thinker': 1},
        'why': 'It can be uncomfortable to have a decision hanging over your head. AREA gives you a step by step process so that you can decisions efficiently.',
    },
    'I don\'t like to pick the obvious decision.': {
        'yes': {'visionary': 1},
        'no': {},
        'why': 'Sometimes the obvious decision is the wrong one, but sometimes it\'s the right one. AREA helps you evaluate your evidence so you can make the best decision for you.',
    },
    'People tell me that I\'m careful and cautious.': {
        'yes': {'thinker': 1},
        'no': {},
        'why': 'The AREA Method allows you to make decisions carefully and cautiously but with data and a focus on what really matters to you.',
    },
    'I tend to be independent and go my own way.': {
        'yes': {'visionary': 1},
        'no': {'listener': 1},
        'why': 'If you rely on instinct beware that you are subject to mental shortcuts and biases. The AREA Method is structured so you can be independant without making a decision on instinct alone.',
    },
}


def get_top_archetypes(questions_yes):
    archetypes = {
        'adventurer': 0,
        'thinker': 0,
        'detective': 0,
        'listener': 0,
        'visionary': 0,
    }
    for question, yes_no in questions.items():
        if question in questions_yes:
            weights = yes_no['yes']
        else:
            weights = yes_no['no']
        for archetype, weight in weights.items():
            archetypes[archetype] = archetypes[archetype] + weight
    top = sorted(archetypes.iteritems(), key=lambda (k, v): (v, k), reverse=True)
    return top


archetype_cheetah_sheets = {
    'adventurer': ['Scenario Analysis', 'Pro Con'],
    'thinker': ['Thinking with Your Whole Brain', 'Great Questions Roadmap'],
    'detective': ['Pro Con', 'Scenario Analysis'],
    'listener': ['Great Questions Roadmap', 'Scenario Analysis'],
    'visionary': ['Pro Con', 'Scenario Analysis'],
}


def save_questions(questions_yes, request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    for question, details in questions.items():
        question_model = QuestionModel.get_by_question(question)
        q = Question(question=question_model, user=user, session_key=request.session.session_key)
        if question in questions_yes:
            q.answer = True
        else:
            q.answer = False
        q.save()


def load_questions(user):
    questions_yes = []
    for question in Question.get_yes_questions(user):
        questions_yes.append(question.text())
    return questions_yes


def populate_questions():
    for question, details in questions.items():
        question_model = QuestionModel.get_by_question(question)
        if not question_model:
            # New Question - add it
            yes = details['yes']
            no = details['no']
            why = details['why']
            question_model = QuestionModel(question=question, answer_yes=yes, answer_no=no, why=why)
            question_model.save()
