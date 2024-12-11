from django import forms
from .models import Cliente

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

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_senha(self.cleaned_data['senha'])  # Criptografa a senha
        if commit:
            cliente.save()
        return cliente
    
class Login(forms.Form):
    email = forms.EmailField(max_length=255)
    senha = forms.CharField(widget=forms.PasswordInput)
