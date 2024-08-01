from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    url = models.CharField(max_length=200, blank=True, verbose_name='URL')
    named_url = models.CharField(max_length=200, blank=True, verbose_name='Named URL')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child',
                               on_delete=models.CASCADE, verbose_name='Родитель')
    menu_name = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='Меню')

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        return f'{self.title}-{self.menu_name.name}'
