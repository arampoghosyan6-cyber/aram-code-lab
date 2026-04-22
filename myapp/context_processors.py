from .models import Subject
from .forms import ContactForm, NewsletterForm

def subjects_processor(request):
    return {
        'all_subjects': Subject.objects.all()
    }

def global_forms(request):
    return {
        'contact_form': ContactForm(),
        'newsletter_form': NewsletterForm(),
        'all_subjects': Subject.objects.all() # Սա կաշխատի նաև քո նավբարի համար
    }