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
            'body' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...'}),
            'image' : forms.FileInput(),
            'tags' : forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name=='tags':
                self.fields[field_name].widget.attrs.update({'class': 'btn-check'})
            else:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = [ 'body','tags']
        labels = {
            'body' : 'Caption',
            'tags':'Categories'
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...',}),
            'tags' : forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name=='tags':
                self.fields[field_name].widget.attrs.update({'class': 'btn-check'})
            else:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        
class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = [ 'body']
        labels = {
            'body' : '',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows': 1, 'placeholder': 'Add a comment ...', 'class':'form-control p-2'}),
        }
