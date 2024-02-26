from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('persona/crear', views.PersonaView.as_view(), name='persona'),
]