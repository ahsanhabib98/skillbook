from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'source_link', 'content', 'category', 'image', 'file')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. 5 ways to be a better developer',
                'required': True
            }),
            'source_link': forms.URLInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. google.com',
                'required': True
            }),
            'content': forms.TextInput(attrs={
                'class': 'text-field w-input',
                'placeholder': 'eg. Why this source is important?',
                'required': True
            }),
            'category': forms.RadioSelect(attrs={
                'required': True
            }),
        }
