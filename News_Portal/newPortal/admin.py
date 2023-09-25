from django.contrib import admin
from .models import *


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating.short_description = 'обнулить рэйтинг'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'rating')
    actions = [nullfy_rating]


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'title', 'text', 'rating', 'category_names')
    list_filter = ('author', 'post_type', 'title', 'text')
    search_fields = ('title',)
    actions = [nullfy_rating]

    def category_names(self, obj):
        return ", ".join([category.name for category in obj.postCategory.all()])
    # выводит поле со связью  ManyToManyField


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

