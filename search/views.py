from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.http import HttpResponse


class search(TemplateView):

    template_name = 'search/search.html'
    """
    def get(self, request, *args, **kwargs):
        q_ = request.GET['usr_query']
        print(q_)
        return render(request, 'search.html')
    """

class about(TemplateView):
    template_name = 'search/about.html'
