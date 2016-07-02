from django import forms
from django.db import models
from libapp.models import Suggestion,Libuser

class LoginForm(forms.ModelForm):
    class Meta:
        model=Libuser
        fields=['username','password']

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title','author','edition','publication','pubyr', 'type', 'cost','comments']

        widgets= { 'type':forms.RadioSelect,'pubyr':forms.TextInput,'cost':forms.TextInput, }

class RegisterForm(forms.ModelForm):
    class Meta:
        # password = forms.CharField(widget=forms.PasswordInput())
        model = Libuser
        fields = ['username', 'first_name', 'last_name', 'password','user_image']

        widgets = {
            'password': forms.PasswordInput(),
        }




class SearchlibForm(forms.Form):

    title=forms.CharField(label='Title', max_length=100,required=False)
    author = forms.CharField(label='Author', max_length=100,required=False)
