from django.shortcuts import render
from django.views.generic import TemplateView

class search(TemplateView):
    template_name = 'search.html'
    

class about(TemplateView):
    template_name = 'about.html'
