from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic as views

from puppet_theatre.account import forms

class RegisterAccountView(views.CreateView):
    form_class = forms.AccountRegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')
    

class CustomLoginView(LoginView):
    form_class = forms.CrispyAuthenticationForm
    template_name = 'account/login.html'
    