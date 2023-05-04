import datetime

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Categories(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return str(self.name)


class Cafe(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='cafe',
                              on_delete=models.CASCADE)
    bio = models.TextField(max_length=150,
                           blank=True)
    pPhoto = models.ImageField(upload_to='profiles/pic/%Y/%m/%d/',
                               blank=True)
    pBackground = models.ImageField(upload_to='profiles/bg/%Y/%m/%d/',
                                    blank=True)
    rate = models.PositiveIntegerField(default=0)
    premium = models.BooleanField(default=False)
    premium_exp = models.DateTimeField(default=timezone.now)
    map_link = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.name)


class Products(models.Model):
    cate = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products')
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_products',
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Templates(models.Model):
    name = models.CharField(max_length=25)
    pTypes = models.ManyToManyField(Categories,
                                    related_name='template_products',
                                    blank=True)
    htmlFile = models.FileField(upload_to='templates/html',
                                blank=True)
    thumbnail = models.ImageField(upload_to='templates/thumbnails/',
                                  blank=True)

    def __str__(self):
        return str(self.name)


class Menu(models.Model):
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_menus',
                             on_delete=models.CASCADE)
    template = models.ForeignKey(Templates,
                                 related_name='template_menus',
                                 on_delete=models.CASCADE)
    products = models.ManyToManyField(Products,
                                      related_name='menu_products',
                                      blank=True)
    qr = models.ImageField(upload_to='qrcode/%Y/%m/%d/',
                           blank=True)
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cafe.name)

    def get_absolute_url(self):
        return reverse('cafes:mShow', kwargs={'pk': self.pk})


class OrderProd(models.Model):
    prod = models.ForeignKey(Products,
                             on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)


class Order(models.Model):
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_orders',
                             on_delete=models.CASCADE)
    prods = models.ManyToManyField(OrderProd,
                                   related_name='order_products',
                                   blank=True)
    price = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    table = models.PositiveSmallIntegerField(blank=False, default=00)


class TableReserve(models.Model):
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_tables_reserved',
                             on_delete=models.CASCADE)
    tNumber = models.PositiveSmallIntegerField(blank=False, default=00)
    date = models.DateTimeField(blank=False)
    endTime = models.TimeField(blank=False)
    reservedBy = models.CharField(max_length=25, blank=False, default="مشتری")
    cost = models.PositiveIntegerField(default=0)


class Cost(models.Model):
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_costs',
                             on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, blank=False, default="هزینه جاری")
    price = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)


class Report(models.Model):
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_reports',
                             on_delete=models.CASCADE)
    type = models.CharField(default="orders", max_length=15, blank=False)
    dateFrom = models.DateField(default=timezone.datetime.today)
    dateTo = models.DateField(default=timezone.datetime.today)
    file = models.FileField(upload_to='reports/%Y/%m/%d/',
                            blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Payments(models.Model):
    cafe = models.ForeignKey(Cafe,
                             related_name='cafe_payments',
                             on_delete=models.CASCADE)
    type = models.CharField(default="panel_charge", max_length=20, blank=False)
    status = models.CharField(default="success", max_length=15, blank=False)
    price = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
