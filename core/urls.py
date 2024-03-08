from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('embarque/generar', views.generarEmbarqueView, name='generar-embarque'),
    path('embarque/gen', views.generarEmbarque, name='gen-embarque'),
    path('embarque/listar', views.ListEmbarqueView, name='listar-embarque'),
    path('persona', views.ListarPersonaView.as_view(), name='persona-listar'),
    path('persona/crear', views.CrearPersonaView.as_view(), name='persona-crear'),
    path('persona/<int:pk>/editar', views.EditarPersonaView.as_view(), name='persona-editar'),
    path('cargo', views.ListarCargoView.as_view(), name='cargo-listar'),
    path('cargo/crear', views.CrearCargoView.as_view(), name='cargo-crear'),
    path('cargo/<int:pk>/editar', views.EditarCargoView.as_view(), name='cargo-editar'),
    path('categoria', views.ListarCategoriaView.as_view(), name='categoria-listar'),
    path('categoria/crear', views.CrearCategoriaView.as_view(), name='categoria-crear'),
    path('categoria/<int:pk>/editar', views.EditarCategoriaView.as_view(), name='categoria-editar'),
    path('posicion', views.ListarPosicionView.as_view(), name='posicion-listar'),
    path('posicion/crear', views.CrearPosicionView.as_view(), name='posicion-crear'),
    path('posicion/<int:pk>/editar', views.EditarPosicionView.as_view(), name='posicion-editar'),
    path('afectacion', views.ListarAfectacionView.as_view(), name='afectacion-listar'),
    path('afectacion/crear', views.CrearAfectacionView.as_view(), name='afectacion-crear'),
    path('afectacion/<int:pk>/editar', views.EditarAfectacionView.as_view(), name='afectacion-editar'),
    path('turno', views.ListarTurnoView.as_view(), name='turno-listar'),
    path('turno/crear', views.CrearTurnoView.as_view(), name='turno-crear'),
    path('turno/<int:pk>/editar', views.EditarTurnoView.as_view(), name='turno-editar'),
    path('descansoplanificado', views.ListarDescansoPlanificadoView.as_view(), name='descansoplanificado-listar'),
    path('descansoplanificado/crear', views.CrearDescansoPlanificadoView.as_view(), name='descansoplanificado-crear'),
    path('descansoplanificado/<int:pk>/editar', views.EditarDescansoPlanificadoView.as_view(), name='descansoplanificado-editar'),
    path('afect_personas', views.ListarAfectacionPersonaView.as_view(), name='afect_persona-listar'),
    path('afect_personas/crear', views.CrearAfectacionPersonaView.as_view(), name='afect_persona-crear'),
    path('afect_personas/<int:pk>/editar', views.EditarAfectacionPersonaView.as_view(), name='afect_persona-editar'),
    path('cat_personas', views.ListarCategoriaPersonaView.as_view(), name='cat_persona-listar'),
    path('cat_personas/crear', views.CrearCategoriaPersonaView.as_view(), name='cat_persona-crear'),
    path('cat_personas/<int:pk>/editar', views.EditarCategoriaPersonaView.as_view(), name='cat_persona-editar'),
    path('rotacion', views.ListarRotacionView.as_view(), name='rotacion-listar'),
    path('rotacion/crear', views.CrearRotacionView.as_view(), name='rotacion-crear'),
    path('rotacion/<int:pk>/editar', views.EditarRotacionView.as_view(), name='rotacion-editar'),
    path('brigada', views.ListarBrigadaView.as_view(), name='brigada-listar'),
    path('brigada/crear', views.CrearBrigadaView.as_view(), name='brigada-crear'),
    path('brigada/<int:pk>/editar', views.EditarBrigadaView.as_view(), name='brigada-editar'),
]