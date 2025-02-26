from django.urls import path
from . import views

urlpatterns = [
    path('validate/', views.validate, name='validate'),
    path('automata/', views.save_automata, name='save_automata'),  # Para POST
    path('automata/convert/', views.convert_automata, name='convert_automata'),
    path('automata/save/', views.save_automata, name='save_automata_alt'),
    path('automata/load/', views.load_automata, name='load_automata'),
]