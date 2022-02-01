from dataclasses import field
from django import forms
from .models import NewsletterUser, Newsletter

#Informacion del modelo NewsletterUser
class NewsletterUserSignUpForm(forms.modelForm):
    class Meta:
        model = NewsletterUser
        fields = ['email']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['name','subject','body','email']

