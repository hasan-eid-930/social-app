from django.forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','image', 'tags']
        labels = {
            'body' : 'Caption',
            'tags' : 'Category'
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...', 'class': 'form-control','textarea':True}),
            'title' : forms.TextInput(attrs={ 'class': 'form-control'}),
            'image' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags' : forms.CheckboxSelectMultiple(),
        }
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = [ 'body']
        labels = {
            'body' : 'Caption',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...', 'class': 'form-control','textarea':True}),
        }
        
        
