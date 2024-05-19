from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from puppet_theatre.account import views

app_name = 'account'

urlpatterns = [    
    path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
]

htmx_urlpatterns = [
    path('check-username/', views.check_username, name='check_username'),
    path('check-subject/', views.check_subject, name='check_subject'),
]

urlpatterns += htmx_urlpatterns