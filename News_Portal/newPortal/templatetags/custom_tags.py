from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Пользовательский тег шаблонов для замены или добавления параметров в URL-адресе текущей страницы.

    Принимает контекст запроса и произвольное количество именованных аргументов (`**kwargs`),
    которые представляют параметры, которые нужно заменить или добавить в URL-адресе.

    Возвращает закодированную строку параметров GET.

    Пример использования в шаблоне:
    <a href="?{% url_replace page=2 %}">Страница 2</a>
    """
    d = context['request'].GET.copy()  # Получаем словарь параметров GET из текущего запроса и создаем его копию
    for k, v in kwargs.items():
        d[k] = v  # Заменяем или добавляем параметр `k` со значением `v` в словаре `d`
    return d.urlencode()  # Возвращаем закодированную строку параметров GET
