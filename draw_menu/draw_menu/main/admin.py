from django.contrib import admin
from .models import MenuItem, Menu


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = MenuItemInline,


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = 'title', 'parent', 'menu_name'
    list_filter = ('title', 'menu_name')
    ordering = ('menu_name', )
    search_fields = ('title', )
