from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import HttpResponse
from BookSearch.book_search import search as book_search


class search(TemplateView):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q'):
            req = request.GET.get('q')
            print(req)
            search_book = book_search(req)
            print(search_book)
            return render(request, 'search/search.html')
        else:
            print('else')
            return render(request, 'search/search.html')


class about(TemplateView):
    template_name = 'search/about.html'
