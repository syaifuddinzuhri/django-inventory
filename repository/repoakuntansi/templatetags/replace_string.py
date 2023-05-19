from django import template

register = template.Library()

@register.filter
def replace_string(value):
    if value is None: return ""
    return value.replace("\n",",")