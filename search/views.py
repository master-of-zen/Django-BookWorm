from django.shortcuts import render
from django.views.generic import TemplateView
from search_engine.book_search import search as book_search


class search(TemplateView):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q'):
            req = request.GET.get('q')
            print(req)
            print(type(req))
            search_book = book_search(str(req))
            print(search_book)
            return render(request, 'search/search.html')
        else:
            print('else')
            return render(request, 'search/search.html')


class about(TemplateView):
    template_name = 'search/about.html'
