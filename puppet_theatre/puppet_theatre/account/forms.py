# account/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.contrib.auth.forms import AuthenticationForm


from .models import AccountUser


class AccountRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'register-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.layout = Layout(
            Field('email', placeholder='Email'),
            Field('first_name', placeholder='First Name'),
            Field('last_name', placeholder='Last Name'),
            Field('password', placeholder='Password'),
            ButtonHolder(
                Submit('submit', 'Register', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = AccountUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CrispyAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'login-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))
        self.helper.layout = Layout(
            Field('username', placeholder='Username'),
            Field('password', placeholder='Password'),
            ButtonHolder(
                Submit('submit', 'Login', css_class='btn btn-primary')
            )
        )


# from django import forms
# from django.urls import reverse_lazy
# from django.utils import timezone
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

# from .models import AccountUser


# class AccountUserForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'accountuser-form'
#         self.helper.attrs = {
#             'hx-post': reverse_lazy('index'),
#             'hx-target': '#accountuser-form',
#             'hx-swap': 'outerHTML'
#         }
#         self.helper.add_input(Submit('submit', 'Submit'))

#     date_joined = forms.DateTimeField(
#         widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'max': timezone.now().strftime('%Y-%m-%dT%H:%M')})
#     )

#     class Meta:
#         model = AccountUser
#         fields = ('email', 'first_name', 'last_name',)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#         return user
