from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main/main.html'


def some_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/main.html')
