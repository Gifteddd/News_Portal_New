from django.core.management.base import BaseCommand, CommandError
from newPortal.models import Post, Category


class Command(BaseCommand):
    help = 'Удалить все новости/статьи из данной категории'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Название категории из которой нужно удалить новость/статью')

    def handle(self, *args, **options):
        name = options['name']

        try:
            category = Category.objects.get(name=name)
        except Category.DoesNotExist:
            raise CommandError(f'Категории "{name}" не существует. ')

        confirm = input(f'Вы уверенны, что хотите удалить все новости/статьи из "{name}"? (yes/no): ')

        if confirm.lower() == 'yes':
            news_to_delete = Post.objects.filter(postCategory=category)
            news_count = news_to_delete.count()
            news_to_delete.delete()
            self.stderr.write(self.style.SUCCESS(f'успешно удаленно новостей/статей {news_count} из категории "{name}". '))
        else:
            self.stderr.write(self.style.SUCCESS('Удаление отменено. Ни одна новость/статья не была удалена'))