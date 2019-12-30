from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import HttpResponse
from BookSearch.book_search import search

class search(TemplateView):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q'):
            print(request.GET.get('q'))
            print(search(request.GET.get('q')))
            return render(request, 'search/search.html')
        else:
            return render(request, 'search/search.html')


class about(TemplateView):
    template_name = 'search/about.html'
