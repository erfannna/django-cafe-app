from django.contrib import admin
from .models import Categories, Products, Cafe, Templates, Menu, Order, TableReserve, Report, Payments


@admin.register(Cafe)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'pPhoto', 'pBackground']


@admin.register(Categories)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Products)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'cate', 'price']


@admin.register(Templates)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'htmlFile', 'thumbnail']


@admin.register(Menu)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'template', 'id']


@admin.register(Order)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'price', 'created', 'table']


@admin.register(TableReserve)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'tNumber', 'reservedBy', 'date']


@admin.register(Report)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'created', 'type']


@admin.register(Payments)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'created', 'type', 'price']
