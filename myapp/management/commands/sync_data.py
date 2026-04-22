from django.core.management.base import BaseCommand
from myapp.models import Subject, Project, Material


class Command(BaseCommand):
    help = 'Copies existing data to translation fields'

    def handle(self, *args, **kwargs):
        # Subject-ի համար
        for item in Subject.objects.all():
            if not item.name_hy:
                item.name_hy = item.name
                item.description_hy = item.description
                item.save()

        # Project-ի համար
        for item in Project.objects.all():
            if not item.title_hy:
                item.title_hy = item.title
                item.description_hy = item.description
                item.save()

        # Material-ի համար
        for item in Material.objects.all():
            if not item.title_hy:
                item.title_hy = item.title
                item.content_hy = item.content
                item.save()

        self.stdout.write(self.style.SUCCESS('Data sync complete!'))