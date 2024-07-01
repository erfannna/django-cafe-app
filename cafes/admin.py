from django.contrib import admin
from .models import Categories, Products, Cafe, Templates, Menu, Order, TableReserve, Report, Payments


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'premium_exp']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'cate', 'price']


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'template', 'id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'price', 'created', 'table']


@admin.register(TableReserve)
class TableReserveAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'tNumber', 'reservedBy', 'date']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'created', 'type']


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'created', 'type', 'price']
