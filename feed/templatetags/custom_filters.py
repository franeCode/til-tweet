from django import template
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def custom_timesince(value):
    now = timezone.now()
    difference = now - value
    days, seconds = divmod(difference.seconds, 86400)

    if difference.days >= 7:
        weeks, days = divmod(difference.days, 7)
        result = f'{weeks}w {days}d '
    elif difference.days >= 1:
        hours, remainder = divmod(seconds, 3600)
        result = f'{difference.days}d {hours}h '
    elif seconds >= 3600:
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        result = f'{hours}h {minutes}m '
    elif seconds >= 60:
        minutes, seconds = divmod(seconds, 60)
        result = f'{minutes}m {seconds}s '
    else:
        result = f'{seconds}s '

    return result + ' ago'