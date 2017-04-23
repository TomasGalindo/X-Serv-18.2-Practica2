from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from acorta.models import URL
# Create your views here.


@csrf_exempt
def barra(request):
    if request.method == "GET":
        # Imprimir la base de datos
        respuesta = "Listado de las URL guardadas"  # URL e ID
        lista_URL = URL.objects.all()
        for url in lista_URL:
            respuesta += "<br>" + url.name + " --> Id = " + str(url.id)

        # formulario para introducir en la base de datos
        respuesta += "<br>¿Añadir una pagina?<br>"
        respuesta += "<form action='/' method='post'>"
        respuesta += "Name: <input type= 'text' name='name'>"
        respuesta += "<input type= 'submit' value='enviar'>"
        respuesta += "</form>"
        sts = 200
    elif request.method == "POST":
        name = request.POST['name']  # URL que intenta guardar
        if name.startswith('http://') or name.startswith('https://'):
            url_Guard = name
            respuesta = "PAGINA = " + url_Guard
        else:
            url_Guard = "http://" + name
            respuesta = "PAGINA = " + url_Guard
        # url ha sido tratada; tengo que ver a ver si esta guardada en la lista
        try:
            url_busq = URL.objects.get(name=url_Guard)
            # si existe
            respuesta += "<br>Ya existe la pagina que querias guardar: "
            respuesta += ("<a href=" + url_busq.name + ">localhost:1234/" +
                          str(url_busq.id) + "</a>")
        except URL.DoesNotExist:
            respuesta += "<br> No existe; guardando en la base de datos"
            url_def = URL(name=url_Guard)
            url_def.save()

        sts = 200
    else:
        respuesta = "Method Not Allowed"
        sts = 405
    return HttpResponse(respuesta, status=sts)


def busqURL(request, identificador):
    if request.method == "GET":
        try:
            url_busq = URL.objects.get(id=identificador)
            # si existe
            respuesta = "Existe la pagina que querias guardar: "
            return redirect(url_busq.name)
        except URL.DoesNotExist:
            respuesta = "<br> No existe"
            sts = 404
    else:
        repuesta = "Method Not Allowed"
        sts = 405

    return HttpResponse(respuesta, status=sts)
