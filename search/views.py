from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from search_engine.book_search import search as book_search
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class search(ListView):

    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q'):
            req = request.GET.get('q')
            search_book = book_search(str(req))
            return render(request, 'search/search.html', {'books': search_book})
        else:
            print('else')
            return render(request, 'search/search.html')


class about(TemplateView):
    template_name = 'search/about.html'

