#!/usr/bin/env python
# -*- coding: latin-1 -*-

questions = {
    'I tend to make gut decisions.': {
        'yes': {'adventurer': 1},
        'no': {'thinker': 1}
    },
    'I like to collect all possible evidence before making a decision.': {
        'yes': {'detective': 1},
        'no': {'adventurer': 1}
    },
    'I have trouble making decisions because I see all the pros and cons.': {
        'yes': {'thinker': 1},
        'no': {'adventurer': 1, 'creative': 1}
    },
    'The best way for me to make a decision is to ask others for advice.': {
        'yes': {'listener': 1},
        'no': {'adventurer': 1, 'detective': 1}
    },
    'I always think outside the box when making decisions.': {
        'yes': {'creative': 1},
        'no': {'detective': 1}
    },
    'I never consider how much a decision will cost me before I make it.': {
        'yes': {'adventurer': 1},
        'no': {'detective': 1}
    },
    'I know where to look for good resources to solve my problems.': {
        'yes': {'thinker': 1, 'detective': 1},
        'no': {}
    },
    'I am good at getting the information I need.': {
        'yes': {'thinker': 1, 'creative': 1},
        'no': {'adventurer': 1, 'listener': 1}
    },
    'I am good at drawing conclusions.': {
        'yes': {'thinker': 1, 'creative': 1},
        'no': {'adventurer': 1, 'listener': 1}
    },
    'I like learning from others.': {
        'yes': {'listener': 1},
        'no': {}
    },
    'I don\'t like to listen to the opinions of other people - I prefer to make my own decisions.': {
        'yes': {'adventurer': 1},
        'no': {'listener': 1}
    },
    'I feel overwhelmed when I have too many options.': {
        'yes': {'thinker': 1},
        'no': {'detective': 1}
    },
    'I love to gather information from the people around me.': {
        'yes': {'listener': 1},
        'no': {}
    },
    'I  lean on my friends to make my decisions for me.': {
        'yes': {'listener': 1},
        'no': {'detective': 1}
    },
    'I prefer to come up with creative solutions.': {
        'yes': {},
        'no': {'creative': 1}
    },
    'I don\'t feel the need to make decisions quickly.': {
        'yes': {'thinker': 1},
        'no': {'adventurer': 1}
    },
    'I don\'t like to pick the obvious decision.': {
        'yes': {'creative': 1},
        'no': {}
    },
    'I prefer to lean on my friends than to do my own thing.': {
        'yes': {'listener': 1},
        'no': {'creative': 1}
    },
    'People tell me that I\'m careful and cautious.': {
        'yes': {'thinker': 1},
        'no': {}
    },
    'I tend to be independent and go my own way.': {
        'yes': {'creative': 1},
        'no': {'listener': 1}
    },
}


def get_top_archetypes(questions_yes):
    archetypes = {
        'adventurer': 0,
        'thinker': 0,
        'detective': 0,
        'listener': 0,
        'creative': 0,
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
    'thinker': ['What Is The Story', 'Great Questions Roadmap'],
    'detective': ['Pro Con', 'Scenario Analysis'],
    'listener': ['What Is The Story', 'Scenario Analysis'],
    'creative': ['Great Questions Roadmap', 'Scenario Analysis'],
}
