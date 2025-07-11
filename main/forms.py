from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'mobile', 'inquiry']

from django import forms
from .models import StudioContact

class StudioContactForm(forms.ModelForm):
    class Meta:
        model = StudioContact
        fields = ['address', 'email', 'phone', 'extra_phone', 'hours']
