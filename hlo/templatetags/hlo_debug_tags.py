import pprint

from django import template

register = template.Library()


@register.filter()
def dump_var(var):
    return pprint.pformat(vars(var), indent=4, width=30, compact=True)


@register.filter()
def dump_var_type(var):
    return pprint.pformat(type(var), indent=4, width=30, compact=True)


@register.filter()
def dump_var_dir(var):
    return pprint.pformat(dir(var), indent=4, width=30, compact=True)
