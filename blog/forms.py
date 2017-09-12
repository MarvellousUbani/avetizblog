from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','post_pic')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control borderprob' }),
            'text': forms.Textarea(attrs={'class': ' form-control'}),

        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass form-control'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),

        }
