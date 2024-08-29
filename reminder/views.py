from django.shortcuts import render
from django.views import generic

from . import backend # برای این که کارها انجام بشن. استفاده ای ازش نمیکنیم اینجا.

class HomePage(generic.TemplateView):
    template_name = 'index.html'
    template_name = 'enter_number.html'
