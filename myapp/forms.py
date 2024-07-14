from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Add a public comment...', 'rows': 3})
        }
