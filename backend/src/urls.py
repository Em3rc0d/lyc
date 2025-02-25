from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from automata import views

def home(request):
    return HttpResponse("Bienvenido a la API.")

urlpatterns = [
    path('', home, name='home'),  # Ruta raíz
    path('admin/', admin.site.urls),
    path('api/validate/', views.validate, name='validate'),
    path('api/automata/convert/', views.convert_automata, name='convert_automata'),
]