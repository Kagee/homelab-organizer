# Custom tag for diagnostics

from django import template
import pprint
from django.utils.html import mark_safe
register = template.Library()

@register.filter()
def json_dump_var(var):
    return pprint.pformat(vars(var), indent=4, width=30, compact=True)# json.dumps(var, indent=4)

# @register.simple_tag(takes_context=True)

@register.simple_tag(takes_context=True)
def url_replace_parameter(context, **kwargs):
    query = context['request'].GET.copy()
    for kwarg in kwargs:
        try:
            query.pop(kwarg)
        except KeyError:
            pass
    query.update(kwargs)
    return mark_safe(query.urlencode())

#register.simple_tag(url_replace, takes_context=True)