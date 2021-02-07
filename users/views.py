from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class AboutPage(TemplateView):
    template_name = 'about.html'


class TechPage(TemplateView):
    template_name = 'tech.html'