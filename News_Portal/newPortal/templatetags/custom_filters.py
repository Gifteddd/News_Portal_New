from django import template

register = template.Library()

censored_words = ['редиска', 'нож', 'клей']  # Здесь перечисли все нежелательные слова


@register.filter
def censor(value):
    for word in censored_words:
        value = str(value).replace(word, '*' * len(word))
    return value
