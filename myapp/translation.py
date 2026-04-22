from modeltranslation.translator import register, TranslationOptions
from .models import Subject, Project, Material

@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'tech_stack', 'description')

@register(Material)
class MaterialTranslationOptions(TranslationOptions):
    fields = ('title', 'content')