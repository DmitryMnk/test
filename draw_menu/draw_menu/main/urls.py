from django.urls import path
from .views import *
from .models import MenuItem
urls = [[item.url, item.named_url] for item in MenuItem.objects.all()]

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]

for url in urls:
    if url[1]:
        new_path: path = path(url[0], some_view, name=url[1])
    else:
        new_path: path = path(url[0], some_view)
    urlpatterns.append(new_path)