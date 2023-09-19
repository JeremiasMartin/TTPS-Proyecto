from django.shortcuts import render


def home(request):
    return render(request, 'ProyectoApp/home.html')
