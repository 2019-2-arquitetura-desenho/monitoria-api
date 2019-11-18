from django import template
from monitoria.settings import DOMAIN

register = template.Library()

@register.simple_tag
def get_Domain_link():
    return DOMAIN
