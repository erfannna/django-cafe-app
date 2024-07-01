from django import forms
from .models import BlogPost
from django.forms import TextInput, Textarea, FileInput


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'short', 'content', 'image', 'duration')
        widgets = {
            'title': TextInput(attrs={
                'class': "post-input",
                'id': "post-title",
                'placeholder': "عنوان مطلب",
                'maxlength': "100"
            }),
            'short': Textarea(attrs={
                'class': "post-input",
                'id': "post-short",
                'placeholder': "چکیده مطلب",
                'maxlength': "250"
            }),
            'content': Textarea(attrs={
                'class': "post-input",
                'id': "post-content",
                'placeholder': "محتوای مطلب"
            }),
            'image': FileInput(attrs={
                'class': "post-input",
                'id': "post-image",
                'accept': "image/*"
            }),
            'duration': TextInput(attrs={
                'class': "post-input",
                'id': "post-duration",
                'placeholder': "زمان مطالعه",
                'maxlength': "3"
            }),
        }

