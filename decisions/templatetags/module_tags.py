from django import template
from django.urls import reverse
from django.templatetags import static
from django.core.urlresolvers import NoReverseMatch

register = template.Library()

# https://stackoverflow.com/a/41579629
@register.simple_tag(takes_context=True)
def define(context, key, value):
    context.dicts[0][key] = value
    return ''

@register.simple_tag(takes_context=True)
def get_static_url(context):
    return "http://13.57.240.107"

@register.inclusion_tag('decisions/snippets/badge.html')
def get_module_badge(badge_label):
    return { 'badge_label': badge_label }

@register.inclusion_tag('decisions/snippets/module_link.html')
def get_module_link(moduleObj, userObj):
    #
    moduleObj.display_label = "Module {0} : {1}".format(moduleObj.display_num(), moduleObj.name())
    # Build out the url to reverse
    if moduleObj.step != "":
      to_reverse = "module{0}_{1}".format(moduleObj.num(), moduleObj.step)
      try:
        moduleObj.display_url = reverse(to_reverse)
      except NoReverseMatch:
        print("Unable to reverse: {0}".format(to_reverse))
        moduleObj.display_url = "/{0}/".format(moduleObj.num())
    else:
      # Default to module number
      print("Using default module link")
      moduleObj.display_url = "/{0}/".format(moduleObj.num())

    return { 'module': moduleObj, 'user': userObj }

@register.inclusion_tag('decisions/snippets/back_link.html')
def get_back_link(moduleObj, target):
    if not target.startswith("/"):
        target = "/" + str(moduleObj.num()) + "/" + target

    return { 'target': target }

@register.inclusion_tag('decisions/snippets/next_button.html')
def get_next_btn(moduleObj, btnLabel, target, btnType="button"):
    if not target.startswith("/"):
        target = "/" + str(moduleObj.num()) + "/" + target

    return {
        'btnLabel': btnLabel,
        'btnType': btnType,
        'target': target
    }
