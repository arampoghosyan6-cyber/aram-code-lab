# Register your models here.
from django.contrib import admin
from .models import Subject, Project, Material,NewsletterSubscriber
from modeltranslation.admin import TranslationAdmin
from django.http import HttpResponse  # Այ սա էր պակասում
import csv


@admin.register(Subject)
class SubjectAdmin(TranslationAdmin):
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ('title', 'tech_stack')

@admin.register(Material)
class MaterialAdmin(TranslationAdmin):
    list_display = ('title', 'subject', 'created_at')


# 1. Ֆունկցիան, որը CSV է պատրաստում
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

    writer = csv.writer(response)
    # Ավելացնում ենք վերնագիրը
    writer.writerow(['Email', 'Subscribed At'])

    # Գրում ենք տվյալները
    for obj in queryset:
        writer.writerow([obj.email, obj.subscribed_at])

    return response


# Տալիս ենք կոճակին անուն, որ երևա ադմին պանելում
export_as_csv.short_description = "Export Selected to CSV"


# 2. Գրանցում ենք մոդելը ադմին պանելում
@admin.register(NewsletterSubscriber)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    actions = [export_as_csv]

#admin.site.register(Subject)
#admin.site.register(Project)
#admin.site.register(Material)