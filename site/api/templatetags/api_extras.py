import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def wrap_with_span(string, arg):
    """ Wraps all instances of a string with a span element"""

    words = arg.split(' ')

    for word in words:
        pattern = re.compile(r'(\b{0}[\w\d]*\b)'.format(word), flags=re.I)

        for (match) in re.findall(pattern, string):
            string = re.sub(r'{0}'.format(match),
                '<span>{0}</span>'.format(match), string)

    return string.replace('&amp;#x', '&#x')

