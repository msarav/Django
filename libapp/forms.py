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
        fields = ['title', 'pubyr', 'type', 'cost','comments']


class SearchlibForm(forms.Form):

    title=forms.CharField(label='Title', max_length=100,required=False)
    author = forms.CharField(label='Author', max_length=100,required=False)
