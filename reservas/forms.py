from django import forms
from .models import Cliente
import re

class Cadastro(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, max_length=255)

    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'senha']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado. Por favor, use outro.")
        return email

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')

        # Verifica se tem pelo menos 6 números
        if len(re.findall(r'\d', senha)) < 6:
            raise forms.ValidationError('A senha deve conter pelo menos 6 números.')

        # Verifica se tem pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', senha):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra maiúscula.')

        return senha

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        # Verifica se o telefone tem exatamente 10 dígitos
        if len(telefone) != 10 or not telefone.isdigit():
            raise forms.ValidationError('O telefone deve ter 10 dígitos numéricos.')

        return telefone

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_senha(self.cleaned_data['senha'])  # Criptografa a senha
        if commit:
            cliente.save()
        return cliente

class Login(forms.Form):
    email = forms.EmailField(max_length=255)
    senha = forms.CharField(widget=forms.PasswordInput, max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            cliente = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            raise forms.ValidationError('Email não encontrado.')

        # Armazenar o cliente para usar na validação da senha
        self.cliente = cliente

        return email
    
    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        cliente = self.cleaned_data.get('cliente')  # Obter o cliente de cleaned_data
        
        if cliente and not cliente.verificar_senha(senha):
            raise forms.ValidationError('Senha incorreta.')
        
        return senha