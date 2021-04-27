from django import forms
from django.forms import ModelForm

from .models import User,Merchant
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class MerchantChangeForm(forms.ModelForm):
    invoice_id=forms.CharField(disabled=True,widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    class Meta:
        model=Merchant
        exclude=('user',)




class MerchantRegForm(UserCreationForm):
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':"Enter Your Email Address",'class':'form-control mb-3'}))
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':"Enter Your Username",'class':'form-control mb-3'}))
    password1=forms.CharField(required=True,label='Enter Your Password',widget=forms.PasswordInput(attrs={'placeholder':"Enter Your Password",'class':'form-control mb-3'}))
    password2=forms.CharField(required=True,label='Confirm Your Password',widget=forms.PasswordInput(attrs={'placeholder':"Confirm Your Password",'class':'form-control mb-3'}))
    class Meta:
        model=User
        fields=('email','username','password1','password2')
