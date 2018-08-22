from django.http import request

from .models import Course
from .parser import get_nav, parse_request_path, split_path

import json

class ViewHelper:
    @staticmethod
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

    @staticmethod
    def load_json(json_data):
        json_object = {}
        try:
            json_object = json.loads(json_data)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
        return json_object

    @staticmethod
    def load_module(request, step='', Module=None):
        module = None
        course = ViewHelper.load_course(request)
        if course:
            module_list = Module.objects.filter(course=course)
            if module_list:
                module = module_list.first()
                if step:
                    module.step = step
                    module.save()
            else:
                module = Module(course=course, step=step)
                module.save()
            module.answers_json = ''
            if module.answers:
                module.answers_json = ViewHelper.load_json(module.answers)
        if not module:
            module = Module()
            module.answers_json = None
        return module

    @staticmethod
    def parse_request_path(request, module_urls=[]):
        return parse_request_path(request, module_urls)