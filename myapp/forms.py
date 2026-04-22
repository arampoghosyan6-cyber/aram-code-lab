from django import forms

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'txtb', 'placeholder': 'Enter Your Email', 'required': True})
    )

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'nameZone', 'placeholder': 'Your Full Name', 'required': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'emailZone', 'placeholder': 'Your Email', 'required': True}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'subjectZone', 'placeholder': 'Subject', 'required': True}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'messageZone', 'placeholder': 'Message', 'required': True}))