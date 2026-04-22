import csv
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core import signing
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

# Քո մոդելները և ֆորմաները
from .models import Subject, Project, Material, NewsletterSubscriber
from .forms import NewsletterForm, ContactForm

from django.contrib.auth.models import User
from django.http import HttpResponse


def home(request):
    subjects = Subject.objects.all()
    latest_projects = Project.objects.all().order_by('-id')[:3]
    return render(request, 'index.html', {
        'subjects': subjects,
        'projects': latest_projects,
        'contact_form': ContactForm(),
        'newsletter_form': NewsletterForm()
    })


def all_projects(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'all_projects.html', {'projects': projects})


def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'subject_detail.html', {'subject': subject})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.exclude(pk=project.pk).order_by('-id')[:3]
    return render(request, 'project_detail.html', {
        'project': project,
        'related_items': related_projects
    })


def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    related_materials = Material.objects.filter(subject=material.subject).exclude(pk=material.pk).order_by(
        '-created_at')[:3]
    return render(request, 'material_detail.html', {
        'material': material,
        'related_items': related_materials
    })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Ստեղծում ենք ապահով թոքեն ֆորմայի տվյալներով
            payload = {
                'action': 'contact',
                'name': data['name'],
                'email': data['email'],
                'subject': data['subject'],
                'message': data['message']
            }
            token = signing.dumps(payload)
            verify_link = request.build_absolute_uri(reverse('verify_email', args=[token]))

            # Պատրաստում ենք նամակը թարգմանված տեքստերով և HTML դիզայնով
            subject_text = _("Aram Code Lab: Please verify your email")
            context = {
                'title': _("Verify Your Message"),
                'greeting': _("Hello") + f" {data['name']},",
                'message_text': _("Please click the button below to confirm and send your message to us. The link is valid for 1 hour."),
                'button_text': _("Confirm Message"),
                'verify_link': verify_link,
            }
            html_message = render_to_string('emails/verification.html', context)
            plain_message = strip_tags(html_message)

            try:
                # Ուղարկում ենք ՀԱՍՏԱՏՄԱՆ նամակ ՕԳՏԱՏԻՐՈՋԸ
                send_mail(
                    subject=subject_text,
                    message=plain_message,
                    from_email='aram.poghosyan.2004@gmail.com',
                    recipient_list=[data['email']],
                    html_message=html_message
                )
                messages.success(request, _("We sent a verification link to your email. Please check your inbox."), extra_tags='contact')
                return redirect('/#get-in-touch')
            except Exception:
                messages.error(request, _("An error occurred while sending the email. Please try again."), extra_tags='contact')
        else:
            messages.error(request, _("Please check the entered data."), extra_tags='contact')

        return render(request, 'index.html', {
            'subjects': Subject.objects.all(),
            'projects': Project.objects.all().order_by('-id')[:3],
            'contact_form': form,
            'newsletter_form': NewsletterForm()
        })
    return redirect('/')


def subscribe_newsletter(request):
    if request.method == 'POST':
        if request.POST.get('honeypot'):
            return redirect('/')

        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Ստուգում ենք՝ արդյոք արդեն բաժանորդագրված է
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, _("This email is already subscribed."), extra_tags='newsletter')
                return redirect('/#newsletter')

            # Ստեղծում ենք ապահով թոքեն բաժանորդագրման համար
            payload = {'action': 'newsletter', 'email': email}
            token = signing.dumps(payload)
            verify_link = request.build_absolute_uri(reverse('verify_email', args=[token]))

            # Պատրաստում ենք նամակը թարգմանված տեքստերով և HTML դիզայնով
            subject_text = _("Aram Code Lab: Confirm your subscription")
            context = {
                'title': _("Confirm Subscription"),
                'greeting': _("Hello,"),
                'message_text': _("Please click the button below to confirm your subscription to our newsletter. The link is valid for 1 hour."),
                'button_text': _("Confirm Subscription"),
                'verify_link': verify_link,
            }
            html_message = render_to_string('emails/verification.html', context)
            plain_message = strip_tags(html_message)

            try:
                # Ուղարկում ենք ՀԱՍՏԱՏՄԱՆ նամակ ՕԳՏԱՏԻՐՈՋԸ
                send_mail(
                    subject=subject_text,
                    message=plain_message,
                    from_email='aram.poghosyan.2004@gmail.com',
                    recipient_list=[email],
                    html_message=html_message
                )
                messages.success(request, _("We sent a confirmation link to your email. Please check your inbox."), extra_tags='newsletter')
                return redirect('/#newsletter')
            except Exception:
                messages.error(request, _("An error occurred while sending the confirmation link."), extra_tags='newsletter')
        else:
            messages.error(request, _("Please enter a valid email address."), extra_tags='newsletter')

            return render(request, 'index.html', {
                'subjects': Subject.objects.all(),
                'projects': Project.objects.all().order_by('-id')[:3],
                'contact_form': ContactForm(),
                'newsletter_form': form
            })
    return redirect('/')


# --- ՆՈՐ ՖՈՒՆԿՑԻԱ՝ Հղումը հաստատելու համար ---
def verify_email_action(request, token):
    status_title = ""
    status_message = ""
    is_success = False

    try:
        # Ապակոդավորում ենք թոքենը: Այն վավեր է միայն 3600 վայրկյան (1 ժամ)
        payload = signing.loads(token, max_age=3600)

        if payload.get('action') == 'contact':
            # Հիմա արդեն ուղարկում ենք բուն նամակը ՔԵԶ (ադմինին)
            send_mail(
                subject=f"Aram Code Lab: {payload['subject']}",
                message=f"Նոր նամակ կայքից (ՀԱՍՏԱՏՎԱԾ էլ. հասցեով):\n\nՈւղարկող: {payload['name']} ({payload['email']})\n\n{payload['message']}",
                from_email=payload['email'],
                recipient_list=['aram.poghosyan.2004@gmail.com'],
            )
            status_title = _("Message Sent!")
            status_message = _("Thank you for confirming. Your message has been successfully sent to us.")
            is_success = True

        elif payload.get('action') == 'newsletter':
            # Գրանցում ենք բազայում
            obj, created = NewsletterSubscriber.objects.get_or_create(email=payload['email'])
            if created:
                status_title = _("Successfully Subscribed!")
                status_message = _("Thank you for confirming. You have successfully subscribed to our newsletter.")
            else:
                status_title = _("Already Subscribed")
                status_message = _("Your email address is already subscribed to our newsletter.")
            is_success = True

    except signing.SignatureExpired:
        status_title = _("Link Expired")
        status_message = _("The verification link has expired (it is valid for 1 hour). Please submit your form again.")
    except signing.BadSignature:
        status_title = _("Invalid Link")
        status_message = _("The verification link is invalid or corrupted.")

    # Ցույց ենք տալիս հատուկ դիզայնով էջը՝ սովորական redirect-ի փոխարեն
    return render(request, 'verification_result.html', {
        'status_title': status_title,
        'status_message': status_message,
        'is_success': is_success
    })


@staff_member_required
def export_subscribers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed At'])

    subscribers = NewsletterSubscriber.objects.all()
    for sub in subscribers:
        writer.writerow([sub.email, sub.subscribed_at])

    return response