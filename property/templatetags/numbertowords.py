from django import template
from num2words import num2words

register = template.Library()

@register.filter
def numbertowords(value):
    return num2words(value)

# register.filter("numbertowords", numbertowords)