import logging

from django import template
from django.utils.html import escape

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag(takes_context=False)
def formz_value(form, field_name, *_args, **_kwargs):
    if field_name in form.fields:
        return escape(form.cleaned_data[field_name])
    return f"No field named `{escape(field_name)}`"


class FormzFieldValueNode(template.Node):
    def __init__(self, tokens):
        # Consider assuming form_variable_name == form
        # if len(tokens) == 1
        self.form_variable_name = tokens[0]
        self.form_variable = template.Variable(self.form_variable_name)
        self.field_name = tokens[1]
        if (
            self.field_name[0] in ["'", '"']
            and self.field_name[0] == self.field_name[-1]
        ):
            # Strip quotes
            self.field_name = self.field_name[1:-1]

    def render(self, context):
        try:
            form = self.form_variable.resolve(context)
            if self.field_name in form.fields:
                return escape(form.cleaned_data[self.field_name])
        except template.VariableDoesNotExist:
            return f"Missing variable `{self.form_variable_name}`"
        return f"No field named `{escape(self.field_name)}`"


class FormzErrorNode(template.Node):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def render(self, _context):
        return escape(self.error_msg)


def do_formz(_parser, token):
    # split_contents() knows not to split quoted strings.
    # first argument is tag name
    _, sub_tag, *tokens = token.split_contents()
    logging.debug(sub_tag)
    logging.debug(tokens)
    if sub_tag.strip() == "value":
        return FormzFieldValueNode(tokens)
    return FormzErrorNode(f"formz: Invalid sub tag `{sub_tag}`")


register.tag("formz", do_formz)

"""
@register.simple_tag(takes_context=True)
def url_replace_parameter(context, **kwargs):
    query = context["request"].GET.copy()
    for kwarg in kwargs:
        with contextlib.suppress(KeyError):
            query.pop(kwarg)
    query.update(kwargs)
    return mark_safe(query.urlencode())  # noqa: S308


@register.filter
def repeat(string: str, times: int):
    return mark_safe(string * times)  # noqa: S308


@register.simple_tag
def repeat_multi(string: str, times: int, times2: int):
    return mark_safe(string * times * times2)  # noqa: S308
"""
