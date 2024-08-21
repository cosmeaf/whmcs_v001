from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from user_manager.forms.auth_forms import UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account_login')

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'account/login.html'