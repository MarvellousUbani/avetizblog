from django import forms

from .models import Advert, Transaction
from blog.models import Post
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth import get_user_model

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','post_pic','category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control borderprob' }),
            'text': forms.Textarea(attrs={'class': ' form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=('amount', 'description')

        widgets={
            'amount':forms.NumberInput(attrs={'class':'form-control borderprob' , 'min':'0'}),
            'description': forms.TextInput(attrs={'class':'form-control borderprob'}),
        }


class advertForm(forms.ModelForm):
    class Meta:
        model=Advert
        exclude=('publisher','payt_status','advert_cost','status')

   

        widgets={
        'company':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'advert_desc':forms.Textarea(attrs={'class':'form-control'}),
        'frequency':forms.Select(attrs={'class':'form-control'}),
        'plan':forms.Select(attrs={'class':'form-control'}),
        'link':forms.TextInput(attrs={'class':'form-control borderprob'}),

        }





class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','first_name','last_name','email')

        widgets={
        'first_name':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'last_name':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'username':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'email':forms.EmailInput(attrs={'class':'form-control borderprob'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('user',)

        widgets={
        'phone':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'address':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'facebook_link':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'twitter_link':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'instagram_link':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'linkedin_link':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'short_description':forms.Textarea(attrs={'class':'form-control borderprob'}),
        }






