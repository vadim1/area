#!/usr/bin/env python
# -*- coding: latin-1 -*-

types = {

}
attributes = {
    'Structural': {
        'description': 'This frame is about paying attention and controlling for your biases so that they don\'t negatively influence your behavior.',
        'attributes':
            [
                'Time', 'Money', 'Location', 'Skill_Set', 'Experience'
            ],
    },
    'Analytical': {
        'description': 'This frame is about getting the right data.  To effectively make a good decision you need to have all of the pertinent facts in place.',
        'attributes':
            [
                'Insight', 'Understanding', 'Analysis'
            ],
    },
    'Informational': {
        'description': 'This frame is about distilling and synthesizing your data well to reach the right conclusions once you\'ve collected the right data.',
        'attributes':
            [
                'Availability', 'Access'
            ],
    },
    'Behavioral': {
        'description': 'This frame is about the limitations and opportunities of your environment. It gets at flexibility and timing. Some decisions are constrained by a short time horizon while others may be made under less pressure.',
        'attributes':
            [
                'Personal_Preference', 'Peer_Pressure', 'Empathy'
            ],
    },
}

attribute_biases = {
    'Time': ['Planning Fallacy', 'Planning Fallacy'],
    'Money': ['Optimism Bias', ['Loss Aversion', 'Scarcity']],
    'Location': ['Relativity Bias', 'Salience Bias'],
    'Skill_Set': ['Confirmation Bias', 'Social Proof'],
    'Experience': ['Confirmation Bias', 'Social Proof'],
    'Insight': ['Optimism Bias', 'Social Proof'],
    'Understanding': ['Optimism Bias', 'Authority Bias'],
    'Analysis': ['Projection Bias', 'Confirmation Bias'],
    'Availability': ['Planning Fallacy', 'Loss Aversion'],
    'Access': ['Optimism Bias', 'Narrative Bias'],
    'Personal_Preference': ['Authority Bias', 'Projection Bias'],
    'Peer_Pressure': ['Liking Bias', 'Social Proof'],
    'Empathy': ['Liking Bias', 'Confirmation Bias'],
}

biases = {
    'Planning Fallacy': 'The planning fallacy is our tendency to underestimate the time, costs, and risks of completing a task, even though we\'ve previously experienced similar tasks. Time management is a significant issue in research and decision-making. We may miss out on an opportunity because we\'ve underestimated how long it takes us to conduct our research.',
    'Confirmation Bias': 'The confirmation bias refers to a form of selective thinking in which we seek out and overvalue information that confirms our existing beliefs, while neglecting or undervaluing information that is contradictory to our existing beliefs. It is related to commitment and consistency bias where we behave in a way that validates our prior actions. It is also related to the incentive bias where we adapt our templates to what benefits us. A confirmation bias may lead us to interpret information falsely because it conflicts with our prior templates and beliefs. Confirmation biases can lead to overconfidence in personal beliefs, even in the face of contrary evidence. In business and in our personal lives, it can lead to extremely poor (and costly) decisions.',
    'Optimism Bias': 'This is a bias in which someone\'s subjective confidence in their judgments, or in the judgments of others, is reliably greater than their objective accuracy.  For example, we are only correct about 80% of the time when we are "99% sure."',
    'Projection Bias': 'Without meaning to, we tend to project our thoughts and beliefs onto others and assume that they are wired the same way we are.  This can lead to "false consensus bias," which not only assumes that other people think like we do, but that they reach the same conclusions that we have reached. In short, this bias creates a false consensus or sense of confidence. For example, if we like a product, we will assume other people like it as much as we do.',
    'Social Proof': 'We tend to think and believe what the people around us think and believe. We see ourselves as individuals but we actually run in herds - large or small, bullish or bearish.  For example research on obesity says that it tends to be socially "catching," through social connections/circles.',
    'Salience Bias': 'Salience bias refers to the tendency to overweight evidence that is recent or vivid. For example, people greatly overestimate murder as a cause of death. In fact, murder isn\'t even among the top 15 causes of death in the U.S. There are more than ten times as many deaths from heart disease (the leading cause of death) as from murder.',
    'Narrative Bias': 'We prefer stories - narratives - to data. Narratives are crucial to how we make sense of reality.  They help us to explain, understand and interpret the world around us.  They also give us a frame of reference we can use to remember the concepts we take them to represent.  However, our inherent preference of narrative over data often limits our understanding of complicated situations. For example, a good story can sell almost anything.',
    'Loss Aversion': 'Empirical estimates find that losses are felt almost two-and-a-half times as strongly as gains. An example is that if we have recently lost money in an investment, we might be unlikely to make similar investments in the future.',
    'Relativity Bias': 'The Relativity Bias inhibits our ability to objectively assess information based upon an over-dependence on comparisons. For example, when given a choice, we tend to pick the middle option, not too pricey, or too cheap.',
    'Authority Bias': 'This bias refers to our natural inclination to follow and to believe in authority figures. For example, Nike pays Roy Mcllroy millions of dollars to wear the company\'s logo betting that consumers will follow his lead.',
    'Liking Bias': 'If you like someone or something, you will interpret data in their favor. We tend to like people who are like us, or have qualities that we admire. For example, you might be inclined to favor a candidate who went to your Alma Mater. This bias is closely related to the reciprocity bias in which we tend to want to reciprocate a favor that someone has done for us.',
    'Scarcity': 'We tend to covet things we believe are scarce, sometimes irrationally. For example, during the real estate bubble, investors became concerned that only a limited amount of land was available to be developed with no real evidence that this was the case.',
}

attribute_cheetahs = {
    'Time': ['Competing Alternative Hypothesis', 'Scenario Analysis'],
    'Money': [['Finding Good Prospects', 'Finding Good Prospects Deep Dive'], 'Pro Con'],
    'Location': ['Pre Mortem', 'Pro Con'],
    'Skill_Set': ['Competing Alternative Hypothesis', 'Great Questions Direct Broad and Theoretical'],
    'Experience': ['Competing Alternative Hypothesis', 'Great Questions Roadmap'],
    'Insight': ['Pre Mortem', 'Great Questions Roadmap'],
    'Understanding': ['Pre Mortem', ['Finding Good Prospects', 'Getting Help with Your Search']],
    'Analysis': ['Scenario Analysis', 'Pre Mortem'],
    'Availability': ['Great Questions Direct Broad and Theoretical', ['Finding Good Prospects', 'Getting Help with Your Search']],
    'Access': ['Great Questions Direct Broad and Theoretical', ['Finding Good Prospects', 'Getting Help with Your Search']],
    'Personal_Preference': ['Pre Mortem', 'Scenario Analysis'],
    'Peer_Pressure': ['Competing Alternative Hypothesis', 'Scenario Analysis'],
    'Empathy': ['Types of Great Questions', 'Types of Great Questions'],
}


def get_top(weights, matrix):
    top = {}
    for attribute, weight in weights.items():
        weight = int(weight)
        if weight == 0:
            continue
        attribute_positives_negatives = matrix[attribute]
        attrs = None
        if weight > 0:
            attrs = attribute_positives_negatives[0]
        else:
            attrs = attribute_positives_negatives[1]
        if isinstance(attrs, basestring):
            attrs = [attrs]
        for attr in attrs:
            if attr in top:
                top[attr] += abs(weight)
            else:
                top[attr] = abs(weight)
    top = sorted(top.iteritems(), key=lambda (k, v): (v, k), reverse=True)
    return top


def test():
    weights = {
        'Access': 5,
        'Understanding': 4,
        'Time': -3,
    }
    biases = get_top(weights, attribute_biases)
    print "Biases: "
    print biases
    cheetahs = get_top(weights, attribute_cheetahs)
    print "Cheetahs: "
    print cheetahs


# test()
