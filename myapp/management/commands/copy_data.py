from django.core.management.base import BaseCommand
from myapp.models import Subject, Project, Material

class Command(BaseCommand):
    help = 'Copies existing data to Armenian translation fields'

    def handle(self, *args, **kwargs):
        # 1. Subject-ի պատճենում
        for item in Subject.objects.all():
            # Եթե հայերեն դաշտը դատարկ է, պատճենիր
            if not item.name_hy:
                item.name_hy = item.name
                item.description_hy = item.description
                item.save()
        self.stdout.write(self.style.SUCCESS('Subject data copied!'))

        # 2. Project-ի պատճենում
        for item in Project.objects.all():
            if not item.title_hy:
                item.title_hy = item.title
                item.description_hy = item.description
                item.save()
        self.stdout.write(self.style.SUCCESS('Project data copied!'))

        # 3. Material-ի պատճենում
        for item in Material.objects.all():
            if not item.title_hy:
                item.title_hy = item.title
                item.content_hy = item.content
                item.save()
        self.stdout.write(self.style.SUCCESS('Material data copied!'))

        self.stdout.write(self.style.SUCCESS('All data successfully synced!'))