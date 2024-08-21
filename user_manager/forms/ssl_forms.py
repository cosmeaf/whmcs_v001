from django import forms
from web.models.ssl_models import SSLConfiguration

class SSLForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email para o Certificado SSL'})
    )
    agree_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Eu concordo com os termos de uso do SSL"
    )

    class Meta:
        model = SSLConfiguration
        fields = ['ssl_certificate', 'ssl_certificate_key']
        widgets = {
            'ssl_certificate': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter SSL Certificate'}),
            'ssl_certificate_key': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter SSL Certificate Key'}),
        }
