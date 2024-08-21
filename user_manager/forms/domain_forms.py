from django import forms
from user_manager.models import Domain
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['subdomain']

    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-sm btn-success'))
        self.helper.add_input(Submit('cancel', 'Cancelar', css_class='btn btn-sm btn-secondary', onclick="window.history.back()"))

    def clean_subdomain(self):
        subdomain = self.cleaned_data['subdomain']
        # Apenas letras minúsculas, números e hífens são permitidos
        if not re.match(r'^[a-z0-9-]+$', subdomain):
            raise forms.ValidationError("O subdomínio só pode conter letras minúsculas, números e hífens.")
        return subdomain

    def clean(self):
        cleaned_data = super().clean()
        subdomain = cleaned_data.get("subdomain")

        if subdomain:
            # Remove qualquer protocolo da URL
            cleaned_data['subdomain'] = re.sub(r'^https?://', '', subdomain)

        return cleaned_data
