from django import template

from users.models import Channel

register = template.Library()

@register.simple_tag
def check_channel(user):
    return Channel.objects.filter(user = user).exists()