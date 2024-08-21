from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Field
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("E-mail"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('E-mail')})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', _('Sign In'), css_class='btn btn-primary btn-block'))


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('E-mail')})
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
    )
    repeat_password = forms.CharField(
        label=_("Confirm Password"),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm Password')}),
    )
    first_name = forms.CharField(
        label=_("First Name"),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First Name')})
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last Name')})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError({"password": _("Passwords do not match.")})

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError({"email": _("A user with this email already exists.")})

        if len(password) < 6:
            raise forms.ValidationError({"password": _("Password must be at least 6 characters long.")})

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError({"password": _("Password must contain at least one digit.")})

        if not any(char.isalpha() for char in password):
            raise forms.ValidationError({"password": _("Password must contain at least one letter.")})

        if not any(char in '!@#$%^&*()' for char in password):
            raise forms.ValidationError({"password": _("Password must contain at least one special character.")})

        return cleaned_data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
        return user
