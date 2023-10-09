from django.shortcuts import render


def home(request):
    return render(request, 'ProyectoApp/home.html')


def dash(request):
    return render(request, 'ProyectoApp/dashboard.html')
