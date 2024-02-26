from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, FormView, DeleteView, CreateView, RedirectView
from django.http import HttpResponse
from django.template import loader
from core.personas.form import PersonaForm

def index(request):
  template = loader.get_template('personas/form.html')
  return HttpResponse(template.render())

class PersonaView(TemplateView):
    template_name = "personas/persona_form.html"

    def get_context_data(self, **kwargs):
        context = super(PersonaView, self).get_context_data(**kwargs)
        context["titulo_page"] = "Personas"   
        context["persona_form"] = PersonaForm()
        return context