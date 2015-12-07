from django import template

from ..base import EXPERIMENTS

register = template.Library()

@register.filter
def experiment(user, experiment, group='experiment'):
    return EXPERIMENTS[experiment].in_group(user, group)
