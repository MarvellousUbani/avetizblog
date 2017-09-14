from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from models import Profile


class LoginForm(forms.Form):
	username=forms.CharField(label='Username',
	help_text='Please enter you username', 
	widget=forms.TextInput(attrs={'class':'form-control', 'required': True}))
	
	password=forms.CharField(label='Password',
	help_text='Please Enter Your Password',
	widget=forms.PasswordInput(attrs={'class':'form-control', 'required':True}))



class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('first_name',"username", "email", "password")
        model = get_user_model()
        widgets={
        'first_name' : forms.TextInput(attrs={'class':'form-control'}),
        'username' : forms.TextInput(attrs={'class':'form-control'}),
        'email' :forms.EmailInput(attrs={'class':'form-control'}),
        'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        fields=('role',)
        model=Profile

        widgets={
        'role':forms.Select(attrs={'class':'form-control'}),
        }

    