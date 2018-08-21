from django.http import request

from .models import Course

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
        parsed = {
            'parsed': [],
            'moduleNum': None,
            'section': None,
            'step': None,
            'currentStep': None,
            'templatePath': None,
            'requestPath': request.path,
            'previous': None,
            'next': None,
            'prefix': None,
            'urlPrefix': None,
        }

        parts = request.path.split("/")

        # Typical path is /<module_num>/<section>
        if len(parts) > 2:
            section = parts[2]
            step = None

            # Log the step we are on e.g. intro
            current = section
            currentStep = section
            # Path to the template
            templatePath = section + ".html"

            # There is a sub directory path
            if len(parts) == 4:
                step = parts[3]
                current = section + "/" + step
                currentStep = section + "_" + step
                templatePath = section + "/" + step + ".html"

            if len(module_urls) == 0:
                nextUrl = "/decisions"
                previousUrl = "/decisions"
                previousNdx = 0
                nextNdx = 0
            else:
                # Calculate the previous and next steps
                if current in module_urls:
                    currentNdx = module_urls.index(current)

                    previousNdx = currentNdx - 1
                    if previousNdx > 0:
                        previousUrl = module_urls[previousNdx]
                    else:
                        previousUrl = module_urls[0]

                    nextNdx = currentNdx + 1
                    if nextNdx < len(module_urls):
                        nextUrl = module_urls[nextNdx]
                    else:
                        nextUrl = "/decisions"
                else:
                    # URL not found in list
                    nextUrl = "/decisions"
                    previousUrl = "/decisions"
                    previousNdx = 0
                    nextNdx = 0

            print("previous[{0}]: {1}, next[{2}]: {3}".format(previousNdx, previousUrl, nextNdx, nextUrl))

            # template location
            prefix = "module" + str(parts[1]) + "/"
            # url location
            urlPrefix = "/" + str(parts[1]) + "/"

            parsed = {
                'parsed': parts,
                'moduleNum': parts[1],
                'section': section,
                'step': step,
                'currentStep': currentStep,
                'templatePath': prefix + templatePath,
                'current': current,
                'nextUrl': nextUrl,
                'previousUrl': previousUrl,
                'prefix': prefix,
                'urlPrefix': urlPrefix,
            }

        return parsed
