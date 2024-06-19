from django.urls import path

from puppet_theatre.core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts')
]
