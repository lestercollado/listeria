from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, FormView, DeleteView, CreateView, RedirectView
from django.http import HttpResponse
from django.template import loader
from core.form import PersonaForm
from core.models import *
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta

def index(request):
  personas = Persona.objects.all()
  certificados = AfectacionPersona.objects.filter(afectacion__id = 2)
  vacaciones = AfectacionPersona.objects.filter(afectacion__id = 1,fecha_fin__gte = datetime.now())
  descansos = DescansoPlanificado.objects.filter(fecha__gte = datetime.now())
  
  for persona in personas:
    hoy = datetime.now()
    hoy_anterior = datetime.now() - timedelta(days=6)
    cant_turnos = Rotacion.objects.filter(persona = persona, fecha__lte = hoy, fecha__gte = hoy_anterior)
    if len(cant_turnos) == 7:
      dp_exits = DescansoPlanificado.objects.filter(fecha = datetime.now() + timedelta(days=1), persona = persona)
      if len(dp_exits) == 0:
        dp = DescansoPlanificado()
        dp.fecha = datetime.now() + timedelta(days=1)
        dp.persona = persona
        dp.save()  
    
  context = {}
  context["personas"] = personas
  context["certificados"] = certificados
  context["vacaciones"] = vacaciones
  context["descansos"] = descansos
  
  template = loader.get_template('base.html')
  return HttpResponse(template.render(context, request))

class CrearPersonaView(TemplateView):
    template_name = "personas/persona_form.html"
    
    @transaction.atomic()
    def post(self, request):
      persona = Persona.objects.create(
          nombre = self.request.POST.get("nombre"),
          apellidos = self.request.POST.get("apellidos"),
          carnet = self.request.POST.get("carnet"),
          expediente = self.request.POST.get("expediente"),
          usuario = self.request.POST.get("usuario"),
          direccion = self.request.POST.get("direccion"),
          telefono = self.request.POST.get("telefono"),
          movil = self.request.POST.get("movil"),
          observacion = self.request.POST.get("observacion"),
          instructor = True if self.request.POST.get("instructor") == "on" else False,
          disponible = True if self.request.POST.get("disponible") == "on" else False,
          cargo_id = self.request.POST.get("cargo"),
      )
      return HttpResponseRedirect(reverse("core:persona-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearPersonaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Personas"   
      context["persona_form"] = PersonaForm()
      context["cargos"] = Cargo.objects.all() 
      return context
    
class EditarPersonaView(TemplateView):
    template_name = "personas/persona_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      persona = Persona.objects.filter(pk=pk).first()
      persona.nombre = self.request.POST.get("nombre")
      persona.apellidos = self.request.POST.get("apellidos")
      persona.carnet = self.request.POST.get("carnet")
      persona.expediente = self.request.POST.get("expediente")
      persona.usuario = self.request.POST.get("usuario")
      persona.direccion = self.request.POST.get("direccion")
      persona.telefono = self.request.POST.get("telefono")
      persona.movil = self.request.POST.get("movil")
      persona.observacion = self.request.POST.get("observacion")
      persona.instructor = True if self.request.POST.get("instructor") == "on" else False
      persona.disponible = True if self.request.POST.get("disponible") == "on" else False
      persona.cargo_id = self.request.POST.get("cargo")
      persona.save()      
      return HttpResponseRedirect(reverse("core:persona-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarPersonaView, self).get_context_data(**kwargs)
      persona = Persona.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Personas"   
      context["persona_form"] = PersonaForm()
      context["persona"] = persona
      context["cargos"] = Cargo.objects.all() 
      return context
    
class ListarPersonaView(TemplateView):
    template_name = "personas/persona_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarPersonaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Personas"   
      context["personas"] = Persona.objects.all()
      return context
    
class CrearCargoView(TemplateView):
    template_name = "cargos/cargo_form.html"
    
    @transaction.atomic()
    def post(self, request):
      cargo = Cargo.objects.create(
          nombre = self.request.POST.get("nombre"),
          codigo = self.request.POST.get("codigo"),
          activo = True if self.request.POST.get("activo") == "on" else False
      )
      return HttpResponseRedirect(reverse("core:cargo-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearCargoView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Cargos"   
      return context
    
class EditarCargoView(TemplateView):
    template_name = "cargos/cargo_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      cargo = Cargo.objects.filter(pk=pk).first()
      cargo.nombre = self.request.POST.get("nombre")
      cargo.codigo = self.request.POST.get("codigo")
      cargo.activo = True if self.request.POST.get("activo") == "on" else False
      cargo.save()      
      return HttpResponseRedirect(reverse("core:cargo-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarCargoView, self).get_context_data(**kwargs)
      cargo = Cargo.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Cargos"   
      context["cargo"] = cargo
      return context
    
class ListarCargoView(TemplateView):
    template_name = "cargos/cargo_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarCargoView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Cargos"   
      context["cargos"] = Cargo.objects.all()
      return context
    
class CrearCategoriaView(TemplateView):
    template_name = "categorias/categoria_form.html"
    
    @transaction.atomic()
    def post(self, request):
      categoria = Categoria.objects.create(
          nombre = self.request.POST.get("nombre"),
          codigo = self.request.POST.get("codigo"),
          activo = True if self.request.POST.get("activo") == "on" else False
      )
      return HttpResponseRedirect(reverse("core:categoria-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearCategoriaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Categorias"   
      return context
    
class EditarCategoriaView(TemplateView):
    template_name = "categorias/categoria_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      categoria = Categoria.objects.filter(pk=pk).first()
      categoria.nombre = self.request.POST.get("nombre")
      categoria.codigo = self.request.POST.get("codigo")
      categoria.activo = True if self.request.POST.get("activo") == "on" else False
      categoria.save()      
      return HttpResponseRedirect(reverse("core:categoria-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarCategoriaView, self).get_context_data(**kwargs)
      categoria = Categoria.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Categorias"   
      context["categoria"] = categoria
      return context
    
class ListarCategoriaView(TemplateView):
    template_name = "categorias/categoria_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarCategoriaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Categorias"   
      context["categorias"] = Categoria.objects.all()
      return context
    
class CrearPosicionView(TemplateView):
    template_name = "posiciones/posicion_form.html"
    
    @transaction.atomic()
    def post(self, request):
      posicion = Posicion.objects.create(
          nombre = self.request.POST.get("nombre"),
          codigo = self.request.POST.get("codigo"),
          activo = True if self.request.POST.get("activo") == "on" else False
      )
      return HttpResponseRedirect(reverse("core:posicion-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearPosicionView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Posiciones"   
      return context
    
class EditarPosicionView(TemplateView):
    template_name = "posiciones/posicion_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      posicion = Posicion.objects.filter(pk=pk).first()
      posicion.nombre = self.request.POST.get("nombre")
      posicion.codigo = self.request.POST.get("codigo")
      posicion.activo = True if self.request.POST.get("activo") == "on" else False
      posicion.save()      
      return HttpResponseRedirect(reverse("core:posicion-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarPosicionView, self).get_context_data(**kwargs)
      posicion = Posicion.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Posiciones"   
      context["posicion"] = posicion
      return context
    
class ListarPosicionView(TemplateView):
    template_name = "posiciones/posicion_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarPosicionView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Posiciones"   
      context["posiciones"] = Posicion.objects.all()
      return context
    
class CrearAfectacionView(TemplateView):
    template_name = "afectaciones/afectacion_form.html"
    
    @transaction.atomic()
    def post(self, request):
      afectacion = Afectacion.objects.create(
          nombre = self.request.POST.get("nombre"),
          codigo = self.request.POST.get("codigo"),
          activo = True if self.request.POST.get("activo") == "on" else False
      )
      return HttpResponseRedirect(reverse("core:afectacion-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearAfectacionView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Afectaciones"   
      return context
    
class EditarAfectacionView(TemplateView):
    template_name = "afectaciones/afectacion_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      afectacion = Afectacion.objects.filter(pk=pk).first()
      afectacion.nombre = self.request.POST.get("nombre")
      afectacion.codigo = self.request.POST.get("codigo")
      afectacion.activo = True if self.request.POST.get("activo") == "on" else False
      afectacion.save()      
      return HttpResponseRedirect(reverse("core:afectacion-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarAfectacionView, self).get_context_data(**kwargs)
      afectacion = Afectacion.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Afectaciones"   
      context["afectacion"] = afectacion
      return context
    
class ListarAfectacionView(TemplateView):
    template_name = "afectaciones/afectacion_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarAfectacionView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Afectaciones"   
      context["afectaciones"] = Afectacion.objects.all()
      return context
    
class CrearTurnoView(TemplateView):
    template_name = "turnos/turno_form.html"
    
    @transaction.atomic()
    def post(self, request):      
      turno = Turno.objects.create(
          nombre = self.request.POST.get("nombre"),
          codigo = self.request.POST.get("codigo"),
          tipo = self.request.POST.get("tipo"),
          activo = True if self.request.POST.get("activo") == "on" else False
      )
      return HttpResponseRedirect(reverse("core:turno-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearTurnoView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Turnos"   
      return context
    
class EditarTurnoView(TemplateView):
    template_name = "turnos/turno_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      turno = Turno.objects.filter(pk=pk).first()
      turno.nombre = self.request.POST.get("nombre")
      turno.codigo = self.request.POST.get("codigo")
      turno.tipo = self.request.POST.get("tipo_turno"),
      turno.activo = True if self.request.POST.get("activo") == "on" else False
      turno.save()      
      return HttpResponseRedirect(reverse("core:turno-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarTurnoView, self).get_context_data(**kwargs)
      turno = Turno.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Turnos"   
      context["turno"] = turno
      return context
    
class ListarTurnoView(TemplateView):
    template_name = "turnos/turno_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarTurnoView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Turnos"   
      context["turnos"] = Turno.objects.all()
      return context
    
class CrearDescansoPlanificadoView(TemplateView):
    template_name = "descansoplanificado/descansoplanificado_form.html"
    
    @transaction.atomic()
    def post(self, request):      
      DescansoPlanificado.objects.create(
          persona_id = self.request.POST.get("persona"),
          fecha = self.request.POST.get("fecha"),
      )
      return HttpResponseRedirect(reverse("core:descansoplanificado-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearDescansoPlanificadoView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Descanso Planificado"   
      context["personas"] = Persona.objects.all() 
      return context
    
class EditarDescansoPlanificadoView(TemplateView):
    template_name = "descansoplanificado/descansoplanificadoform.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      turno = DescansoPlanificado.objects.filter(pk=pk).first()
      turno.persona_id = self.request.POST.get("persona")
      turno.fecha = datetime.strptime(self.request.POST.get("fecha"), '%Y-%m-%d')
      turno.save()      
      return HttpResponseRedirect(reverse("core:descansoplanificado-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarDescansoPlanificadoView, self).get_context_data(**kwargs)
      descansoplanificados = DescansoPlanificado.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Descanso Planificado"   
      context["descansoplanificados"] = descansoplanificados
      context["personas"] = Persona.objects.all()
      return context
    
class ListarDescansoPlanificadoView(TemplateView):
    template_name = "descansoplanificado/descansoplanificado_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarDescansoPlanificadoView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Descanso Planificado"   
      context["descansoplanificados"] = DescansoPlanificado.objects.all()
      return context
    
class CrearAfectacionPersonaView(TemplateView):
    template_name = "afect_persona/afect_persona_form.html"
    
    @transaction.atomic()
    def post(self, request):
      AfectacionPersona.objects.create(
          persona_id = self.request.POST.get("persona"),
          afectacion_id = self.request.POST.get("afectacion"),
          fecha_inicio = self.request.POST.get("fecha_inicio"),
          fecha_fin = self.request.POST.get("fecha_fin"),
      )
      return HttpResponseRedirect(reverse("core:afect_persona-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearAfectacionPersonaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Afectacion Persona"   
      context["personas"] = Persona.objects.all() 
      context["afectaciones"] = Afectacion.objects.all() 
      return context
    
class EditarAfectacionPersonaView(TemplateView):
    template_name = "afect_persona/afect_persona_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      ap = AfectacionPersona.objects.filter(pk=pk).first()
      ap.persona_id = self.request.POST.get("persona")
      ap.afectacion_id = self.request.POST.get("afectacion")
      ap.fecha_inicio = datetime.strptime(self.request.POST.get("fecha_inicio"), '%Y-%m-%d')
      ap.fecha_fin = datetime.strptime(self.request.POST.get("fecha_fin"), '%Y-%m-%d')
      ap.save()      
      return HttpResponseRedirect(reverse("core:afect_persona-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarAfectacionPersonaView, self).get_context_data(**kwargs)
      afect_personas = AfectacionPersona.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Afectacion Persona"   
      context["afect_personas"] = afect_personas
      context["personas"] = Persona.objects.all() 
      context["afectaciones"] = Afectacion.objects.all() 
      return context
    
class ListarAfectacionPersonaView(TemplateView):
    template_name = "afect_persona/afect_persona_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarAfectacionPersonaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Afectacion Persona"   
      context["afect_personas"] = AfectacionPersona.objects.all()
      return context

class CrearCategoriaPersonaView(TemplateView):
    template_name = "cat_persona/cat_persona_form.html"
    
    @transaction.atomic()
    def post(self, request):
      CategoriaPersona.objects.create(
          persona_id = self.request.POST.get("persona"),
          categoria_id = self.request.POST.get("categoria"),
          principal = True if self.request.POST.get("activo") == "on" else False,
      )
      return HttpResponseRedirect(reverse("core:cat_persona-crear"))      

    def get_context_data(self, **kwargs):
      context = super(CrearCategoriaPersonaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Categoría Persona"   
      context["personas"] = Persona.objects.all() 
      context["categorias"] = Categoria.objects.all() 
      return context
    
class EditarCategoriaPersonaView(TemplateView):
    template_name = "cat_persona/cat_persona_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      ap = CategoriaPersona.objects.filter(pk=pk).first()
      ap.persona_id = self.request.POST.get("persona")
      ap.categoria_id = self.request.POST.get("categoria")
      ap.principal = True if self.request.POST.get("activo") == "on" else False
      ap.save()      
      return HttpResponseRedirect(reverse("core:cat_persona-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarCategoriaPersonaView, self).get_context_data(**kwargs)
      cat_personas = CategoriaPersona.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Categoría Persona"   
      context["cat_personas"] = cat_personas
      context["personas"] = Persona.objects.all() 
      context["categorias"] = Categoria.objects.all() 
      return context
    
class ListarCategoriaPersonaView(TemplateView):
    template_name = "cat_persona/cat_persona_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarCategoriaPersonaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Categoría Persona"   
      context["cat_personas"] = CategoriaPersona.objects.all()
      return context
    
class CrearRotacionView(TemplateView):
    template_name = "rotaciones/rotacion_form.html"
    
    @transaction.atomic()
    def post(self, request):
      Rotacion.objects.create(
          persona_id = self.request.POST.get("persona"),
          turno_id = self.request.POST.get("turno"),
          posicion_id = self.request.POST.get("posicion"),
          fecha = self.request.POST.get("fecha"),
      )
      return HttpResponseRedirect(reverse("core:rotacion-listar"))      

    def get_context_data(self, **kwargs):
      context = super(CrearRotacionView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Rotación"   
      context["personas"] = Persona.objects.all() 
      context["turnos"] = Turno.objects.all() 
      context["posiciones"] = Posicion.objects.all() 
      return context
    
class EditarRotacionView(TemplateView):
    template_name = "rotaciones/rotacion_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      ap = Rotacion.objects.filter(pk=pk).first()
      ap.persona_id = self.request.POST.get("persona")
      ap.turno_id = self.request.POST.get("turno")
      ap.posicion_id = self.request.POST.get("posicion")
      ap.fecha = datetime.strptime(self.request.POST.get("fecha"), '%Y-%m-%d')
      ap.save()      
      return HttpResponseRedirect(reverse("core:rotacion-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarRotacionView, self).get_context_data(**kwargs)
      rotaciones = Rotacion.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Rotación"   
      context["rotaciones"] = rotaciones
      context["personas"] = Persona.objects.all() 
      context["turnos"] = Turno.objects.all() 
      context["posiciones"] = Posicion.objects.all() 
      return context
    
class ListarRotacionView(TemplateView):
    template_name = "rotaciones/rotacion_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarRotacionView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Rotación"   
      context["rotaciones"] = Rotacion.objects.all()
      return context
    
class CrearBrigadaView(TemplateView):
    template_name = "brigadas/brigada_form.html"
    
    @transaction.atomic()
    def post(self, request):
      Brigada.objects.create(
          persona_id = self.request.POST.get("persona"),
          turno_id = self.request.POST.get("turno"),
          orden = self.request.POST.get("orden"),
      )
      return HttpResponseRedirect(reverse("core:brigada-crear"))      

    def get_context_data(self, **kwargs):
      context = super(CrearBrigadaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Brigadas"   
      context["personas"] = Persona.objects.all() 
      context["turnos"] = Turno.objects.all()
      return context
    
class EditarBrigadaView(TemplateView):
    template_name = "brigadas/brigada_form.html"
    
    @transaction.atomic()
    def post(self, request, pk):
      brigada = Brigada.objects.filter(pk=pk).first()
      brigada.persona_id = self.request.POST.get("persona")
      brigada.turno_id = self.request.POST.get("turno")
      brigada.orden = self.request.POST.get("orden")
      brigada.save()      
      return HttpResponseRedirect(reverse("core:brigada-listar"))      

    def get_context_data(self, **kwargs):
      context = super(EditarBrigadaView, self).get_context_data(**kwargs)
      brigadas = Brigada.objects.get(id=kwargs["pk"])
      context["titulo_page"] = "Brigadas"   
      context["brigadas"] = brigadas
      context["personas"] = Persona.objects.all() 
      context["turnos"] = Turno.objects.all()
      return context
    
class ListarBrigadaView(TemplateView):
    template_name = "brigadas/brigada_list.html"

    def get_context_data(self, **kwargs):
      context = super(ListarBrigadaView, self).get_context_data(**kwargs)
      context["titulo_page"] = "Brigadas"   
      context["brigadas"] = Brigada.objects.all()
      return context
    
def generarEmbarqueView(request):
  template = loader.get_template('embarque/embarque_form.html')
  turnos = Turno.objects.filter(activo = True, tipo = 1)
  return HttpResponse(template.render({'turnos': turnos,'titulo_page': "Generar embarque"}, request))

def generarEmbarque(request):
  turno = request.POST.get('turno')
  
  # Barco
  sts = int(request.POST.get('sts') if request.POST.get('sts') else 0)
  manos = int(request.POST.get('manos') if request.POST.get('manos') else 0)
  rtg_barco = int(request.POST.get('rtg_barco') if request.POST.get('rtg_barco') else 0)
  ech_barco = int(request.POST.get('ech_barco') if request.POST.get('ech_barco') else 0)
  ct_barco = int(request.POST.get('ct_barco') if request.POST.get('ct_barco') else 0)
  est_barco = int(request.POST.get('est_barco') if request.POST.get('est_barco') else 0)
  tar_barco = int(request.POST.get('tar_barco') if request.POST.get('tar_barco') else 0)
  
  # Tren
  rmg_tren = int(request.POST.get('rmg_tren') if request.POST.get('rmg_tren') else 0)
  rtg_tren = int(request.POST.get('rtg_tren') if request.POST.get('rtg_tren') else 0)
  ct_tren = int(request.POST.get('ct_tren') if request.POST.get('ct_tren') else 0)
  ech_tren = int(request.POST.get('ech_tren') if request.POST.get('ech_tren') else 0)
  est_tren = int(request.POST.get('est_tren') if request.POST.get('est_tren') else 0)
  tar_tren = int(request.POST.get('tar_tren') if request.POST.get('tar_tren') else 0)
  
  # Monta
  rtg_monta = int(request.POST.get('rtg_monta') if request.POST.get('rtg_monta') else 0)
  ech_monta = int(request.POST.get('ech_monta') if request.POST.get('ech_monta') else 0)
  est_monta = int(request.POST.get('est_monta') if request.POST.get('est_monta') else 0)
  tar_monta = int(request.POST.get('tar_monta') if request.POST.get('tar_monta') else 0)
  
  # ZAL
  rtg_zal = int(request.POST.get('rtg_zal') if request.POST.get('rtg_zal') else 0)
  ct_zal = int(request.POST.get('ct_zal') if request.POST.get('ct_zal') else 0)
  
  # Romociones
  rtg_remocion = int(request.POST.get('rtg_remocion') if request.POST.get('rtg_remocion') else 0)
  ech_remocion = int(request.POST.get('ech_remocion') if request.POST.get('ech_remocion') else 0)
  ct_remocion = int(request.POST.get('ct_remocion') if request.POST.get('ct_remocion') else 0)
  
  # Fregado
  rtg_fregado = int(request.POST.get('rtg_fregado') if request.POST.get('rtg_fregado') else 0)
  ech_fregado = int(request.POST.get('ech_fregado') if request.POST.get('ech_fregado') else 0)
  ct_fregado = int(request.POST.get('ct_fregado') if request.POST.get('ct_fregado') else 0)
  
  # Servicios
  rmg_servicios = int(request.POST.get('rmg_servicios') if request.POST.get('rmg_servicios') else 0)
  ct_servicios = int(request.POST.get('ct_servicios') if request.POST.get('ct_servicios') else 0)
  est_servicios = int(request.POST.get('est_servicios') if request.POST.get('est_servicios') else 0)
  mc_servicios = int(request.POST.get('mc_servicios') if request.POST.get('mc_servicios') else 0)
  
  # Obtener STS
  if sts > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 1)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < sts:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 4
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 1
            rotacion.save()
            count_need +=1
            
  # Obtener RTG
  if rtg_barco > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 2)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < rtg_barco:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 4
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 2
            rotacion.save()
            count_need +=1
            
  # Obtener ECH
  if ech_barco > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 3)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < ech_barco:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 4
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 3
            rotacion.save()
            count_need +=1
            
  # Obtener CT
  if ct_barco > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 6)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < ct_barco:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 4
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 6
            rotacion.save()
            count_need +=1
            
  # Obtener EST
  if est_barco > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 7)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < est_barco:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 4
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 7
            rotacion.save()
            count_need +=1
  
  # Obtener T
  if tar_barco > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 10)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < tar_barco:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 4
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 10
            rotacion.save()
            count_need +=1
            
  # Obtener RMG
  if rmg_tren > 0:
    perso_categoria = CategoriaPersona.objects.filter(categoria__id = 5)
    perso_brigada = Brigada.objects.filter(persona__id__in = perso_categoria.values('persona_id'), turno__id = int(turno))
    
    count_need = 0
    for perso in perso_brigada:
        if count_need < rmg_tren:
          afectacion = AfectacionPersona.objects.filter(persona__id = perso.id,fecha_fin__gt=datetime.now())
          descansoplanificado = DescansoPlanificado.objects.filter(persona__id = perso.id,fecha=datetime.now())
          if len(afectacion) == 0 and len(descansoplanificado) == 0:
            rotacion = Rotacion()
            rotacion.fecha = datetime.now()
            rotacion.persona_id = perso.id
            rotacion.posicion_id = 5
            rotacion.turno_id = int(turno)
            rotacion.categoria_id = 5
            rotacion.save()
            count_need +=1
  
  rotaciones_sts = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 1)
  rotaciones_rtg = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 2)
  rotaciones_rmg = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 5)
  rotaciones_ech = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 3)
  rotaciones_ct = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 6)
  rotaciones_est = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 7)
  rotaciones_t = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 10)
  all_rotaciones = Rotacion.objects.filter(fecha = datetime.now())
  
  context = {}
  context["rotaciones_sts"] = rotaciones_sts
  context["rotaciones_rtg"] = rotaciones_rtg
  context["rotaciones_rmg"] = rotaciones_rmg
  context["rotaciones_ech"] = rotaciones_ech
  context["rotaciones_ct"] = rotaciones_ct
  context["rotaciones_est"] = rotaciones_est
  context["rotaciones_t"] = rotaciones_t
  context["all_rotaciones"] = len(all_rotaciones)
  context["fecha"] = datetime.now()
  context["titulo_page"] = "Generar embarque"
  
  template = loader.get_template('embarque/embarque_list.html')
  return HttpResponse(template.render(context, request))

def ListEmbarqueView(request):
  rotaciones_sts = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 1)
  rotaciones_rtg = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 2)
  rotaciones_rmg = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 5)
  rotaciones_ech = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 3)
  rotaciones_ct = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 6)
  rotaciones_est = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 7)
  rotaciones_t = Rotacion.objects.filter(fecha = datetime.now(), categoria__id = 10)
  all_rotaciones = Rotacion.objects.filter(fecha = datetime.now())
  
  context = {}
  context["rotaciones_sts"] = rotaciones_sts
  context["rotaciones_rtg"] = rotaciones_rtg
  context["rotaciones_rmg"] = rotaciones_rmg
  context["rotaciones_ech"] = rotaciones_ech
  context["rotaciones_ct"] = rotaciones_ct
  context["rotaciones_est"] = rotaciones_est
  context["rotaciones_t"] = rotaciones_t
  context["all_rotaciones"] = len(all_rotaciones)
  context["fecha"] = datetime.now()
  context["titulo_page"] = "Listar embarque"
  
  template = loader.get_template('embarque/embarque_list.html')
  return HttpResponse(template.render(context, request))