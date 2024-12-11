from django import forms
from .models import Cliente

class Cadastro(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, max_length=255)

    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'senha']

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_senha(self.cleaned_data['senha'])  # Criptografa a senha
        if commit:
            cliente.save()
        return cliente
    
    from django import forms

class Login(forms.Form):
    email = forms.EmailField(max_length=255)
    senha = forms.CharField(widget=forms.PasswordInput)
