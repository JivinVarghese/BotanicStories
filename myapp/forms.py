# forms.py
from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Add a public comment...', 'rows': 3})
        }


class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False, help_text='Enter tags separated by commas.')

    class Meta:
        model = Post
        fields = ['post_title', 'image', 'content', 'tags']
        widgets = {
            'post_title': forms.TextInput(attrs={'class': 'title-input', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'content-textarea', 'placeholder': 'Tell your story...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'image-input'}),
            'tags': forms.TextInput(attrs={'class': 'tags-input', 'placeholder': 'Add tags...'}),
        }
