from django import template
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def custom_timesince(value):
    now = timezone.now()
    difference = now - value
    weeks, days = divmod(difference.days, 7)
    hours, remainder = divmod(difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    result = ''
    if weeks:
        result += f'{weeks}w '
    if days:
        result += f'{days}d '
    if hours:
        result += f'{hours}h '
    if minutes:
        result += f'{minutes}m '

    return result + 'ago'