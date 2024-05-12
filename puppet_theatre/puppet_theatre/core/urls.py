from django.urls import path

from puppet_theatre.core.views import home

urlpatterns = [
    path('', home, name='home')
]
