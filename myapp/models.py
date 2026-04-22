from django.db import models
from ckeditor.fields import RichTextField


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)  # ՆՈՐ (Գլխավոր էջի նկարը)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    tech_stack = models.CharField(max_length=200)
    image = models.ImageField(upload_to='projects/')
    description = RichTextField()  # ՓՈԽՎԱԾ (Սովորական դաշտից դարձավ CKEditor)

    def __str__(self):
        return self.title


class Material(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='material_covers/', blank=True, null=True)  # ՆՈՐ (Նյութի կազմի նկարը)
    content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email