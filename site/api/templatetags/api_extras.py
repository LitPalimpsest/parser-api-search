import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def wrap_with_span(string, arg):
    """ Wraps all instances of a string with a span element"""
    return re.sub(r'\b{0}\b'.format(re.escape(arg)),
                  '<span>{0}</span>'.format(arg), string).replace(
                          '&amp;#x', '&#x')
