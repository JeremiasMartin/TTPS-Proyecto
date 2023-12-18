from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command


def ejecutar_etl(request):
    if request.method == "POST":
        # Ejecutar el comando personalizado
        call_command("etl")

        return HttpResponse("ETL ejecutado correctamente.")

    return render(request, "ejecutar_etl.html")
