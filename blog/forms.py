from django import forms

from .models import Post, User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('title', 'text',)