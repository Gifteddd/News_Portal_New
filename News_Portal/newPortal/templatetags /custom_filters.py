from django import template

register = template.Library()


@register.filter()
def censor(value):
    value = str(value).replace("редиска", "*******")
    return f'{value}'
