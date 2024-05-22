from django.urls import include, path
from django.contrib.auth.views import LogoutView

from puppet_theatre.account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterAccountView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('<int:pk>/', include([
        path('', views.ProfileView.as_view(), name='details account'),
        path('edit/', views.EditAccountView.as_view(), name='edit account'),
        path('delete/', views.DeleteAccountView.as_view(), name='delete account'),
    ])),
    
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
]

htmx_urlpatterns = [
    path('check-username/', views.CheckUsernameView.as_view(), name='check_username'),
    path('check-subject/', views.CheckSubjectView.as_view(), name='check_subject'),
]

urlpatterns += htmx_urlpatterns