import json
from django import template
register = template.Library()


@register.filter(name='to_json')
def to_json(obj):
    return json.dumps(obj)
