from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name="penalty")
def penalty_duration(td):
    total_seconds = int(td.total_seconds())
    return '{}'.format(total_seconds)

@register.filter(name="run")
def run_duration(td):
    total_time = str(td)
    return '{}'.format(total_time[3:10])
