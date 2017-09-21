from django import forms
from haystack.forms import FacetedSearchForm
from .models import Post, Comment,  ContactMessage


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
            'text': forms.Textarea(attrs={'class': 'form-control'}),

        }


class FacetedPostSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.text = data.get('text', [])
        self.title = data.get('title', [])
        super(FacetedPostSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedPostSearchForm, self).search()
        if self.text:
            query = None
            for item in self.text:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(item)
            sqs = sqs.narrow(u'category_exact:%s' % query)
        if self.title:
            query = None
            for item in self.title:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(item)
            sqs = sqs.narrow(u'brand_exact:%s' % query)
        return sqs

class SubscribeForm(forms.Form):
    email=forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control ' }))

class ContactForm(forms.ModelForm):

    class Meta:
        model=ContactMessage
        fields=('name','email','phone','message')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass form-control', 'placeholder':'Name', 'required':True}),
            'email': forms.EmailInput(attrs={'class': 'textinputclass form-control', 'placeholder':'Email', 'required':True}),
            'phone': forms.TextInput(attrs={'class': 'textinputclass form-control', 'placeholder':'Phone', 'required':True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Message', 'required':True}),

        }


