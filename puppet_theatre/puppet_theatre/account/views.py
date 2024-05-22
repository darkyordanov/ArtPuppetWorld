from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView

from django.http import JsonResponse
from django.views import View

from puppet_theatre.account import forms
from puppet_theatre.account.models import AccountUser

UserModel = get_user_model()


class RegisterAccountView(views.CreateView):
    form_class = forms.AccountRegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')
    

class CustomLoginView(auth_views.LoginView):
    form_class = forms.CrispyAuthenticationForm
    template_name = 'account/login.html'
    

class CustomPasswordChangeView(auth_mixins.LoginRequiredMixin, PasswordChangeView):
    pass
    

class ProfileView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = 'account/details_account.html'
    queryset = UserModel.objects.all()
    
    
class CheckUsernameView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if AccountUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        return JsonResponse({'success': 'Username is available'})

class CheckSubjectView(View):
    def get(self, request, *args, **kwargs):
        subject = request.GET.get('subject')
        if AccountUser.objects.filter(subject=subject).count() > 3:
            return JsonResponse({'error': 'No spaces available in this subject'}, status=400)
        return JsonResponse({'success': 'Spaces available'})


class EditAccountView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'account/edit_account.html'


class DeleteAccountView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'account/delete_account.html'