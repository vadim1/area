from django.test import TestCase
from .parser import get_nav, parse_request_path, split_path

"""
Sample and simplified request object to test
parse_request_path
"""
class MockRequest():
    def __init__(self):
        self.path = "/3/section/step/"

class ParserTestCase(TestCase):
    def setUp(self):
        self.urls = [
            'home',
            'body1',
            'body2/step1',
            'body3/step2',
            'end'
        ]

    """
    get_nav()
    """
    def test_nav_current(self):
        nav = get_nav('home', self.urls)
        self.assertEquals(nav['current'], 'home')

        nav = get_nav('body1', self.urls)
        self.assertEquals(nav['current'], 'body1')

        nav = get_nav('end', self.urls)
        self.assertEquals(nav['current'], 'end')

    def test_nav_next(self):
        nav = get_nav('home', self.urls)
        self.assertEquals(nav['nextUrl'], 'body1')

        nav = get_nav('body2/step1', self.urls)
        self.assertEquals(nav['nextUrl'], 'body3/step2')

        nav = get_nav('end', self.urls)
        self.assertEquals(nav['nextUrl'], '')

    def test_nav_previous(self):
        nav = get_nav('home', self.urls)
        self.assertEquals(nav['previousUrl'], '')

        nav = get_nav('body3/step2', self.urls)
        self.assertEquals(nav['previousUrl'], 'body2/step1')

        nav = get_nav('end', self.urls)
        self.assertEquals(nav['previousUrl'], 'body3/step2')

    """
    parse_request_path()
    """
    def test_parse_request_path(self):
        r = MockRequest()
        urls = [
            'home',
            'section',
            'section/step',
            'end'
        ]

        parsed = parse_request_path(r, urls)
        self.assertEquals(parsed['moduleNum'], '3')
        self.assertEquals(parsed['section'], 'section')
        self.assertEquals(parsed['step'], 'step')
        self.assertEquals(parsed['current'], 'section/step')
        self.assertEquals(parsed['nextUrl'], 'end')
        self.assertEquals(parsed['previousUrl'], 'section')
        self.assertEquals(parsed['currentStep'], 'section_step')
        self.assertEquals(parsed['prefix'], 'module3/')
        self.assertEquals(parsed['templatePath'], 'module3/section/step.html')
        self.assertEquals(parsed['urlPrefix'], '/3/')

    """
    test when the list of urls is in unicode (as it will be if using reverse())
    """
    def test_parse_request_path_unicode(self):
        r = MockRequest()
        urls = [
            u'home',
            u'section',
            u'section/step',
            u'end'
        ]

        parsed = parse_request_path(r, urls)
        self.assertEquals(parsed['moduleNum'], '3')
        self.assertEquals(parsed['section'], 'section')
        self.assertEquals(parsed['step'], 'step')
        self.assertEquals(parsed['current'], 'section/step')
        self.assertEquals(parsed['nextUrl'], 'end')
        self.assertEquals(parsed['previousUrl'], 'section')
        self.assertEquals(parsed['currentStep'], 'section_step')
        self.assertEquals(parsed['prefix'], 'module3/')
        self.assertEquals(parsed['templatePath'], 'module3/section/step.html')
        self.assertEquals(parsed['urlPrefix'], '/3/')

    """
    split_path()
    """
    def test_split_path_modulenum(self):
        parts = split_path("/0")
        self.assertEquals(parts['moduleNum'], "0")

        parts = split_path("/1/test/step/1")
        self.assertEquals(parts['moduleNum'], "1")

    def test_split_path_section(self):
        parts = split_path("/0/")
        self.assertEquals(parts['section'], "")

        parts = split_path("/1/section1")
        self.assertEquals(parts['section'], "section1")

        parts = split_path("/2/section2/")
        self.assertEquals(parts['section'], "section2")

    def test_split_path_step(self):
        parts = split_path("/0/")
        self.assertEquals(parts['step'], "")

        parts = split_path("/1/section1")
        self.assertEquals(parts['step'], "")

        parts = split_path("/2/section2/")
        self.assertEquals(parts['step'], "")

        parts = split_path("/3/section2/step1")
        self.assertEquals(parts['step'], "step1")

        parts = split_path("/4/section2/step2/")
        self.assertEquals(parts['step'], "step2")

        parts = split_path("/5/section2/step3/junk1")
        self.assertEquals(parts['step'], "step3")