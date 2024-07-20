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

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['profile_pic', 'bio', 'location', 'interests', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 3}),
        }

