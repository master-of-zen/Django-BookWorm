from django.shortcuts import render
from django.views.generic import View
#from .models import
# Create your views here.


class MainView(View):
    template_name = 'search/base.html'
