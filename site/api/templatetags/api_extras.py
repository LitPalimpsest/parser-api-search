from operator import itemgetter
import re

from django import template
from django.template.defaultfilters import stringfilter
from api.models import LocationMention, Location, Sentence

register = template.Library()


@register.filter
@stringfilter
def wrap_with_span(string, arg):
    """ Wraps all instances of a string with a span element"""
    words = arg.split(' ')

    for word in words:
        if word[-1].lower() == 's':
            word = word[:-1]
        pattern = re.compile(r'\b({0}[\w\d]*)\b'.format(word), flags=re.I)

        for (match) in re.findall(pattern, string):
            string = re.sub(r'{0}'.format(match),
                '<span>{0}</span>'.format(match), string)
            break;

    return string.replace('&amp;#x', '&#x')

@register.filter
@stringfilter
def add_locations(string, args):
    """ Adds location links to a snippet string """
    string = string.replace('  ', ' ')
    locs = args[0]
    text = args[1]
    for loc in locs:
        pattern = re.compile(r'(\b)({0})(\b)'.format(loc['location']), flags=re.I)
        for (start, match, end) in re.findall(pattern, string):
            string = re.sub(r'{0}'.format(match),
                '<a href="/search/?loc={0}&text={1}">{2}</a>'.format(loc['locid'], text, match), string)
            break;
    return string


@register.tag
def make_list(parser, token):
  bits = list(token.split_contents())
  if len(bits) >= 4 and bits[-2] == "as":
    varname = bits[-1]
    items = bits[1:-2]
    return MakeListNode(items, varname)
  else:
    raise template.TemplateSyntaxError("%r expected format is 'item [item ...] as varname'" % bits[0])

class MakeListNode(template.Node):
  def __init__(self, items, varname):
    self.items = map(template.Variable, items)
    self.varname = varname

  def render(self, context):
    context[self.varname] = [ i.resolve(context) for i in self.items ]
    return ""
