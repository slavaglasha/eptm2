from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='see_dict_group')
def see_dict_group(user):
    if Group.objects.filter(pk=1).exists():
        group = Group.objects.get(pk=1)
        return True if group in user.groups.all() else False
    return False
