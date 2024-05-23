from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeDoneView
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterAccountView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('<int:pk>/', include([
        path('', views.ProfileView.as_view(), name='details_account'),
        path('edit/', views.EditAccountView.as_view(), name='edit_account'),
        path('delete/', views.DeleteAccountView.as_view(), name='delete_account'),
    ])),
    
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
]

htmx_urlpatterns = [
    path('check-username/', views.CheckUsernameView.as_view(), name='check_username'),
    path('check-subject/', views.CheckSubjectView.as_view(), name='check_subject'),
]

urlpatterns += htmx_urlpatterns
