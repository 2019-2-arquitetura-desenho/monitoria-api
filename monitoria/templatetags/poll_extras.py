from django import template
from monitoria.settings import DOMAIN, FRONT

register = template.Library()

@register.simple_tag
def get_Domain_link():
    return DOMAIN
@register.simple_tag
def get_Front_link():
    return FRONT
