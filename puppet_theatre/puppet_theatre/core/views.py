from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def contacts(request):
    return render(request, 'core/contacts.html')