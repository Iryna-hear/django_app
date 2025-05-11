from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def data_today():
    return datetime.now().strftime("%Y-%m-%d")


@register.filter(name='cut_sentence')
def cut_sentence(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value


@register.inclusion_tag('adress_list.html')
def show_adress_list(adress_list):
    return {'adress_list': adress_list}


