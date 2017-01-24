#!/usr/bin/env python
# -*- coding: latin-1 -*-

edges_pitfalls = {
    'I tend to make gut decisions.': {
        'yes': {'intuitive': 1},
        'no': {'thinker': 1}
    },
    'I like to collect all possible evidence before making a decision.': {
        'yes': {'detective': 1},
        'no': {'intuitive': 1}
    },
    'I have trouble making decisions because I see all the pluses and minuses.': {
        'yes': {'thinker': 1},
        'no': {'intuitive': 1, 'architect': 1}
    },
    'The best way for me to make a decision is to ask others for advice.': {
        'yes': {'listener': 1},
        'no': {'intuitive': 1, 'detective': 1}
    },
    'I always think outside the box when making decisions.': {
        'yes': {'architect': 1},
        'no': {'detective': 1}
    },
    'I never consider how much a decision will cost me before I make it.': {
        'yes': {'intuitive': 1},
        'no': {'detective': 1}
    },
    'I know where to look for good resources to solve my problems.': {
        'yes': {'thinker': 1, 'detective': 1},
        'no': {}
    },
    'I am good at making sense of information and understanding the implications of it.': {
        'yes': {'thinker': 1, 'architect': 1},
        'no': {}
    },
    'I like learning from others.': {
        'yes': {'listener': 1},
        'no': {}
    },
    'I don\'t like to listen to the opinions of other people - I prefer to make my own decisions.': {
        'yes': {'intuitive': 1},
        'no': {'listener': 1}
    },
    'I feel overwhelmed when I have too much choice.': {
        'yes': {'thinker': 1},
        'no': {'detective': 1}
    },
    'I love to gather information from the people around me.': {
        'yes': {'listener': 1},
        'no': {}
    },
    'I let my friends influence my decisions.': {
        'yes': {'listener': 1},
        'no': {'detective': 1}
    },
    'I prefer to come up with creative solutions.': {
        'yes': {},
        'no': {'architect': 1}
    },
    'I don\'t feel the need to make decisions quickly.': {
        'yes': {'thinker': 1},
        'no': {'intuitive': 1}
    },
    'I don\'t like to pick the obvious decision.': {
        'yes': {'architect': 1},
        'no': {}
    },
    'I prefer to lean on my community of friends than to do my own thing.': {
        'yes': {'listener': 1},
        'no': {'architect': 1}
    },
    'People tell me that I\'m careful and cautious.': {
        'yes': {'thinker': 1},
        'no': {}
    },
    'I tend to be independent and go my own way.': {
        'yes': {'architect': 1},
        'no': {'listener': 1}
    },
}


def get_top_archetypes(questions_yes):
    archetypes = {
        'intuitive': 0,
        'thinker': 0,
        'detective': 0,
        'listener': 0,
        'architect': 0,
    }
    for question, yes_no in edges_pitfalls.items():
        if question in questions_yes:
            weights = yes_no['yes']
        else:
            weights = yes_no['no']
        for archetype, weight in weights.items():
            archetypes[archetype] = archetypes[archetype] + weight
    top = sorted(archetypes.iteritems(), key=lambda (k, v): (v, k), reverse=True)
    return top


archetype_cheetah_sheets = {
    'intuitive': ['Scenario Analysis', 'Pro Con'],
    'thinker': ['Getting Help with Your Search', 'Great Questions Roadmap'],
    'detective': ['Competing Alternative Hypothesis', 'Pre Mortem'],
    'listener': ['Scenario Analysis', 'Pre Mortem'],
    'architect': ['Great Questions Direct Broad and Theoretical', 'Scenario Analysis'],
}
