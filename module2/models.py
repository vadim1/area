from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

from decisions.models import Course, BaseModule

class Module2(BaseModule):
    answers = models.TextField(default='')
    biases = models.TextField(default='')
    more_facts = models.TextField(default='')
    nylah_bias = models.CharField(max_length=40, default='')
    opinions = models.TextField(default='')
    opinions_important = models.CharField(max_length=10, default='')
    opinions_reality = models.CharField(max_length=10, default='')
    perspective = models.TextField(default='')

    evidence0 = models.CharField(max_length=255, default='')
    evidence1 = models.CharField(max_length=255, default='')
    evidence2 = models.CharField(max_length=255, default='')
    fact0 = models.CharField(max_length=255, default='')
    source0 = models.CharField(max_length=255, default='')
    bias0 = models.CharField(max_length=255, default='')
    fact1 = models.CharField(max_length=255, default='')
    source1 = models.CharField(max_length=255, default='')
    bias1 = models.CharField(max_length=255, default='')
    fact2 = models.CharField(max_length=255, default='')
    source2 = models.CharField(max_length=255, default='')
    bias2 = models.CharField(max_length=255, default='')

    @staticmethod
    def num():
        return 2

    def save_without_historical_record(self, *args, **kwargs):
        #self.skip_history_when_saving = True
        #try:
        ret = self.save(*args, **kwargs)
        #finally:
            #del self.skip_history_when_saving
        return ret

    # Used to display the number to the user
    # internally it's still module 0
    @staticmethod
    def display_num():
        return 3

    @staticmethod
    def name():
        return 'Introduction to Mental Shortcuts'

    @staticmethod
    def get_eval_questions():
        eval_questions = [
            {
                'question': 'Do you feel confident that you know how to solve complex problems?',
                'min': 'Low Confidence',
                'max': 'Very Confident',
            },
            {
                'question': 'How often do you regret or second guess your decisions?',
                'min': 'Rarely',
                'max': 'Always',
            },
            {
                'question': 'Do you feel that you can stop yourself from rushing to judgement or jumping to conclusions?',
                'min': 'No',
                'max': 'Yes, all the time',
            },
            {
                'question': 'How often do you check your assumptions with data?',
                'min': 'Never',
                'max': 'All of the time',
            },
            {
                'question': 'Do you feel well-equipped to gather facts and evidence to help you make your decisions?',
                'min': 'Not Equipped',
                'max': 'Equipped',
            },
            {
                'question': 'How often do you check your assumptions with data?',
                'min': 'Never',
                'max': 'Always',
            },
            {
                'question': 'Do you feel well equipped to try to see the decisions through the eyes of other people impacted by the decision?',
                'min': 'Not Equipped',
                'max': 'Well Equipped',
            },
            {
                'question': 'Overall how would you rate yourself a decision maker?',
                'min': 'Below Average',
                'max': 'Above Average',
            },
        ]

        return eval_questions

    @staticmethod
    def get_biases():
        biases = [
            {
                'key': 'authority',
                'label': 'Authority Bias',
                'action': 'This bias is less likely but might be at work if an authority figure in your life is favorable towards Ohio State.',
            },
            {
                'key': 'liking',
                'label': 'Liking Bias',
                'action': 'This bias might be at work if you know someone who also likes it.',
            },
            {
                'key': 'planning',
                'label': 'Planning Bias',
                'action': 'This bias is not relevant because it is about underestimating how long a task will take even if we have done it before.',
            },
            {
                'key': 'optimism',
                'label': 'Optimism Bias',
                'action': "This bias about being overly optimistic isn't at work here.",
            },
            {
                'key': 'social',
                'label': 'Social Proof',
                'action': 'This bias is most relevant, because it is about being influenced by popularity.',
            },
            {
                'key': 'projection',
                'label': 'Projection Bias',
                'action': 'This bias is not relevant because it is about projecting your own thoughts and feelings onto others.',
            },
        ]

        return biases

    @staticmethod
    def get_mental_shortcuts(self):
        shortcuts = {
            'liking2': {
               'question': 'When you go down the cereal aisle, do you...',
               'answer0': 'Automatically look for the cereal you want',
               'answer1': 'Look at all of the cereal boxes',
               'bias': 'liking',
               'bias_answer': 0,
            },
            'planning1': {
                'question': 'You have a lab report due in two days. You\'ve done them before so you...',
                'answer0': 'Look at the directions when you start to do it',
                'answer1': 'Read the directions now because each lab is a different experiment',
                'bias': 'planning',
                'bias_answer': 0,
            },
            'optimism1': {
                'question': 'If you just passed your driver\'s license test, do you...',
                'answer0': 'Believe you are an above average driver',
                'answer1': 'Think that\'s silly, how could you be?',
                'bias': 'optimism',
                'bias_answer': 0,
            },
        }

        return shortcuts

    @staticmethod
    def get_sample_student_cheetah_data():
        cheetah_data = [
            {
                'cc': "It has a good graphic design program.",
                'facts': "I gathered facts from the colleges' websites about their graphic design programs. Ohio State has a major and Bates doesn't.",
                'source': "I got the data I needed directly from searching for graphic design on the colleges' websites.",
                'bias': "I checked my assumptions and am glad I did. Bates doesn't have a program so I won't apply there.",
            },
            {
                'cc': "I'm able to afford it.",
                'facts': "I don't have facts. My parents say I can choose the college I want to attend.",
                'source': "I could find facts by searching for tuition facts from all of my college choices. I could also download financial aid forms from the college websites and discuss the facts and forms with my parents.",
                'bias': "The Authority Bias might be at work because my parents are authority figures.",
            },
            {
                'cc': "My family supports my decision.",
                'facts': "My facts come from my observation that my family is helping me with my college search.",
                'source': "I don't think I need more facts.",
                'bias': "I am assuming their support is genuine (even though they will miss me). Social Proof could be at work. They might be doing what they think is best for me. ",
            }
        ]

        return cheetah_data

    @staticmethod
    def get_game_questions():
        game_questions = {
            'authority1': {
                'question': 'When your mom asks you to do something do you...',
                'answer0': 'Do it automatically',
                'answer1': 'Question it first',
                'bias': 'authority',
                'bias_answer': 0,
            },
            'liking1': {
                'question': 'When a friend asks you to get ice cream late in the evening, do you...',
                'answer0': 'Say yes, because she is your friend',
                'answer1': 'Say no, because of the time',
                'bias': 'liking',
                'bias_answer': 0,
            },
            'liking2': {
                'question': 'When you go down the cereal aisle, do you...',
                'answer0': 'Automatically look for the cereal you want',
                'answer1': 'Look at all of the cereal boxes',
                'bias': 'liking',
                'bias_answer': 0,
            },
            'planning1': {
                'question': 'You have a lab report due in two days. You\'ve done them before so you...',
                'answer0': 'Look at the directions when you start to do it',
                'answer1': 'Read the directions now because each lab is a different experiment',
                'bias': 'planning',
                'bias_answer': 0,
            },
            'planning2': {
                'question': 'When you look at your homework list, do you...',
                'answer0': 'Start at the top and work on assignments until they are complete or you run out of time',
                'answer1': 'Go over the entire list and plan your time',
                'bias': 'planning',
                'bias_answer': 0,
            },
            'optimism1': {
                'question': 'If you just passed your driver\'s license test, do you...',
                'answer0': 'Believe you are an above average driver',
                'answer1': 'Think that\'s silly, how could you be?',
                'bias': 'optimism',
                'bias_answer': 0,
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
                'answer1': 'Ask your friend before commiting her to buying them',
                'bias': 'projection',
                'bias_answer': 0,
            },
            'planning3': {
                'question': 'You have a big math test in two days. Do you...',
                'answer0': 'Start studying tonight so you have time to ask for help tomorrow',
                'answer1': 'Figure starting tomorrow will be enough time to prepare',
                'bias': 'planning',
                'bias_answer': 0,
            },
            'authority2': {
                'question': 'Your aunt says you should just apply to safety schools. Do you...',
                'answer0': 'Follow her advice without questioning it',
                'answer1': 'Check with your guidance counselor',
                'bias': 'authority',
                'bias_answer': 0,
            },
            'projection2': {
                'question': 'You\'re school changes the dress code without warning. Do you...',
                'answer0': 'You think it\'s unfair and assume your friends do too',
                'answer1': 'You ask around to see how other people feel about the new rule',
                'bias': 'projection',
                'bias_answer': 1,
            },
            'optimism2': {
                'question': 'The weather forecast says rain but the sky is blue so you...',
                'answer0': 'Bring an umbrella',
                'answer1': 'Ignore the forecast',
                'bias': 'optimism',
                'bias_answer': 1,
            },
        }

        return game_questions

    def get_more_facts(self):
        more_facts = [
            'The student to teacher ratio',
            'Graduation rates',
            'Tuition',
            'Housing',
            'Average SAT/ACT Scores',
            'Financial Aid',
        ]

        return more_facts

    def get_opinions(self):
        opinions = [
            'The weather is in Ohio and Maine',
            'How interesting the classes are',
            'Whether the professors are good',
            'How hard it is to get into classes',
            'How nice the dorms are',
            'How the food is',
            'How much homework there is',
            'Is there a Greek life',
        ]

        return opinions

    def get_perspective(self):
        perspective = [
            'Allows you to learn someone/something\'s story in their own words',
            'Promotes empathy',
            'Promotes understanding',
            'Builds your Self Awareness',
            'Focuses on what motivates the person/organization',
        ]

        return perspective

    @staticmethod
    def pins():
        pins = [
            'Mental Shortcuts and Bias',
            'Facts vs Opinions',
            'Perspective-taking',
            'How Facts Beats Bias',
        ]

        return pins

    def __str__(self):
        to_return = "Module 2 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 2 Data'
        verbose_name_plural = 'Module 2 Data'

class Module2Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Module2Form, self).__init__(*args, **kwargs)
        # Not all fields are available all at once so set these to false for now
        self.fields['answers'].required = False
        self.fields['biases'].required = False
        self.fields['more_facts'].required = False
        self.fields['nylah_bias'].required = False
        self.fields['opinions'].required = False
        self.fields['opinions_important'].required = False
        self.fields['opinions_reality'].required = False
        self.fields['perspective'].required = False


    class Meta:
        model = Module2
        fields = ['answers',
                  'biases',
                  'more_facts',
                  'nylah_bias',
                  'opinions',
                  'opinions_important',
                  'opinions_reality',
                  'perspective',
                  ]