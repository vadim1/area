from django import template

register = template.Library()

@register.inclusion_tag('decisions/snippets/module_link.html')
def get_module_link(moduleObj, userObj):
    return { 'module': moduleObj, 'user': userObj }

@register.inclusion_tag('decisions/snippets/back_link.html')
def get_back_link(moduleObj, target):
    if not target.startswith("/"):
        target = "/" + str(moduleObj.num()) + "/" + target

    return { 'target': target }

@register.inclusion_tag('decisions/snippets/next_button.html')
def get_next_btn(moduleObj, btnLabel, target):
    if not target.startswith("/"):
        target = "/" + str(moduleObj.num()) + "/" + target

    return { 'btnLabel': btnLabel, 'target': target }