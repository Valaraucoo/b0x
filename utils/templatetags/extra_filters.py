from django import template

from users.forms import tailwind_form

register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg=None):
    return value.as_widget(attrs={'class': f'{tailwind_form} {arg}'})
