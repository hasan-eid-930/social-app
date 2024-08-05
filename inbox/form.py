from django.forms import ModelForm
from django import forms
from .models import *

class MessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = [ 'body']
        labels = {
            'body' : '',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a message ...','class':'form-control'}),
        }
          