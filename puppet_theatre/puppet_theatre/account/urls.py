from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView

from puppet_theatre.account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterAccountView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
]

htmx_urlpatterns = [
    path('check-username/', views.CheckUsernameView.as_view(), name='check_username'),
    path('check-subject/', views.CheckSubjectView.as_view(), name='check_subject'),
]

urlpatterns += htmx_urlpatterns


# from django.urls import path
# from django.contrib.auth.views import LogoutView, PasswordChangeView

# from puppet_theatre.account import views

# app_name = 'account'

# urlpatterns = [    
#     path('register/', views.RegisterAccountView.as_view(), name='register'),
#     path('login/', views.CustomLoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('profile/', views.ProfileView.as_view(), name='profile'),
#     path('password-change/', PasswordChangeView.as_view(), name='password_change'),
# ]

# htmx_urlpatterns = [
#     path('check-username/', views.CheckUsernameView.as_view(), name='check_username'),
#     path('check-subject/', views.CheckSubjectView.as_view(), name='check_subject'),
# ]

# urlpatterns += htmx_urlpatterns
