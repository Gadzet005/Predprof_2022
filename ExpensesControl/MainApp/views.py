from django.contrib import messages
from django.views.generic import *

class Home(TemplateView):
    template_name = "MainApp/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Главная'
        return context
