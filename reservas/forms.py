from django import forms
from django.contrib.auth.forms import AuthenticationForm

class FormEmail(AuthenticationForm):
    #Aqui eu estou alterando o 'username' nativo do python para ter a formataçaõ de um email
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
