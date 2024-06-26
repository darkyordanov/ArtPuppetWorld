from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.contrib.auth.forms import AuthenticationForm

from puppet_theatre.account.models import AccountUser, Profile


class AccountRegisterForm(forms.ModelForm):
    grade = forms.ChoiceField(choices=Profile.Subjects.choices, label='Grade')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'register-form'
        self.helper.form_method = 'post'
        self.create_layout()

    def create_layout(self):
        self.helper.layout = Layout(
            Field('email', placeholder='Email'),
            Field('first_name', placeholder='First Name'),
            Field('last_name', placeholder='Last Name'),
            Field('grade', placeholder='Grade'),
            Field('password', placeholder='Password'),
            Field('password2', placeholder='Confirm Password'),
            ButtonHolder(
                Submit('submit', 'Register', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = AccountUser
        fields = ('email', 'first_name', 'last_name', 'grade', 'password', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, grade=self.cleaned_data['grade'])
        return user


class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, label='Email')
    grade = forms.ChoiceField(choices=Profile.Subjects.choices, label='Grade')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'edit-form'
        self.helper.form_method = 'post'
        self.create_layout()
        
        # Retrieve the grade from the Profile model
        if self.instance and self.instance.pk:
            try:
                profile = self.instance.profile
                self.fields['grade'].initial = profile.grade
            except Profile.DoesNotExist:
                self.fields['grade'].initial = None

    def create_layout(self):
        self.helper.layout = Layout(
            Field('email', placeholder='Email'),
            Field('first_name', placeholder='First Name'),
            Field('last_name', placeholder='Last Name'),
            Field('grade', placeholder='Grade'),
            ButtonHolder(
                Submit('submit', 'Save Changes', css_class='btn btn-dark btn-lg btn-block')
            )
        )

    class Meta:
        model = AccountUser
        fields = ('email', 'first_name', 'last_name', 'grade')  # Include the grade field

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile.grade = self.cleaned_data['grade']
        if commit:
            profile.save()
        return user


class CrispyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'login-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', placeholder='Username'),
            Field('password', placeholder='Password')
        )