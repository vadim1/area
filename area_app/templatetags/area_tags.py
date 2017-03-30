from django import template

register = template.Library()


@register.filter(name='get_entry')
def get_entry(data_dictionary, key):
    """Return the value of an attribute from a data_dictionary or 0 if not there"""
    if key in data_dictionary:
        return data_dictionary[key]
    else:
        return 0


@register.filter(is_safe=False)
def add_str(a, b):
    try:
        return str(a) + str(b)
    except (ValueError, TypeError):
        return ""


@register.filter(name='get_explain')
def get_explain(data_dictionary, key):
    """Return the key_explain entry of an attribute from a data_dictionary or None if not there"""
    key += '_explain'
    # raise Exception(data_dictionary)
    if key in data_dictionary:
        return data_dictionary[key]
    else:
        return ''
