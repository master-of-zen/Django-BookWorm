from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import HttpResponse


class search(TemplateView):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q'):
            print(request.GET)
            return render(request, 'search/search.html')
        else:
            return render(request, 'search/search.html')


class about(TemplateView):
    template_name = 'search/about.html'
