from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        label='Дата публикации после:',
        field_name='created_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    postCategory = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='----'
    )

    Author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='----'
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'post_type',
            'postCategory',
        ]