from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

from puppet_theatre.account import forms

UserModel = get_user_model()

class RegisterAccountView(views.CreateView):
    form_class = forms.AccountRegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')
    
class CustomLoginView(auth_views.LoginView):
    form_class = forms.CrispyAuthenticationForm
    template_name = 'account/login.html'
    
class CustomPasswordChangeView(auth_mixins.LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('account:password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)  # Keep the user logged in
        return response
    
class ProfileView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = 'account/details_account.html'
    queryset = UserModel.objects.all()
    
class CheckUsernameView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if UserModel.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        return JsonResponse({'success': 'Username is available'})

class CheckSubjectView(View):
    def get(self, request, *args, **kwargs):
        subject = request.GET.get('subject')
        if UserModel.objects.filter(subject=subject).count() > 3:
            return JsonResponse({'error': 'No spaces available in this subject'}, status=400)
        return JsonResponse({'success': 'Spaces available'})

class EditAccountView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'account/edit_account.html'
    queryset = UserModel.objects.all()
    form_class = forms.AccountEditForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('account:details_account', kwargs={'pk': self.object.pk})
    
    
class DeactivateAccountView(auth_mixins.LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, 'Your profile has been deactivated.')
        return redirect('account:login')


class DeleteAccountView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'account/delete_account.html'
