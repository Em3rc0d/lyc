from django.urls import path
from . import views

urlpatterns = [
    path('validate/', views.validate, name='validate'),
    path('convert/', views.convert_automata, name='convert_automata'),
]