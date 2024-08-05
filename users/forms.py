from django import forms
from django.forms import ModelForm
from .models import *

class ProfileEditForm(ModelForm):
    class Meta:
        
        model = Profile
        #execlude field
        exclude = ['user']

        labels = {
            'realname' : 'Name',
            'image':'Avatar'
        }
        widgets = {
            'bio' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a bio here ...'}),
            'image':forms.FileInput(attrs={'id':'profile-img-input'}),
            'realname':forms.TextInput(attrs={'id':'profile-name-input'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})