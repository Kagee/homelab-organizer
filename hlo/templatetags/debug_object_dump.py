import pprint
from django import template

register = template.Library()

@register.filter()
def dump_var(var):
    return pprint.pformat(vars(var), indent=4, width=30, compact=True)
