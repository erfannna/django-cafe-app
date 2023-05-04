from django import forms
from .models import Cafe, Products, Menu, Order, TableReserve, Cost, Report
from django.forms import TextInput, Textarea, NumberInput, FileInput, Select, SelectMultiple,\
    DateTimeInput, DateInput, TimeInput, ChoiceField
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'نام کاربری',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور',
        }),
        label="",
    )


class CafeInfoForm(forms.ModelForm):

    class Meta:
        model = Cafe
        fields = ('name', 'bio', 'pPhoto', 'pBackground', 'map_link')
        widgets = {
            'name': TextInput(attrs={
                'class': "nForm fText",
                'id': "cafeName",
                'placeholder': "نام کافه",
                'maxlength': "50",
            }),
            'bio': Textarea(attrs={
                'class': "nForm fText",
                'id': "cafeBio",
                'placeholder': "کافه خود را توصیف کنید...",
                'maxlength': "150",
            }),
            'pPhoto': FileInput(attrs={
                'class': "nForm",
                'id': "cafePhoto",
                'accept': "image/*",
                'title': "عکسی انتخاب نشده",
                'value': "انتخاب",
                'hidden': 'true'
            }),
            'pBackground': FileInput(attrs={
                'class': "nForm",
                'id': "cBackPhoto",
                'accept': "image/*",
                'title': "عکسی انتخاب نشده",
                'value': "انتخاب",
                'hidden': 'true'
            }),
            'map_link': TextInput(attrs={
                'class': "nForm fText",
                'id': "cafeLocation",
                'placeholder': "مختصات جغرافیایی کافه",
                'maxlength': "50",
            })
        }


# Product Forms
class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('cate', 'name', 'price')
        widgets = {
            'name': TextInput(attrs={
                'class': "nForm fText",
                'id': "nProductName",
                'placeholder': "نام محصول جدید کافه",
                'maxlength': "50",
            }),
            'price': NumberInput(attrs={
                'class': "nForm fText",
                'id': "nProductPrice",
                'placeholder': "قیمت محصول جدید کافه",
                'maxlength': "50",
            }),
            'cate': Select(attrs={
                'class': "nForm fSelect",
                'id': "nProductCat",
                'placeholder': "دسته بندی",
            }),
        }


class ProductEditForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('name', 'price',)
        widgets = {
            'name': TextInput(attrs={
                'class': "nForm fText",
                'id': "nProductName",
                'placeholder': "نام محصول جدید کافه",
                'maxlength': "50",
            }),
            'price': NumberInput(attrs={
                'class': "nForm fText",
                'id': "nProductPrice",
                'placeholder': "قیمت محصول جدید کافه",
                'maxlength': "50",
            }),
        }


# Menu Forms
class MenuCreateForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('template', 'products',)
        widgets = {
            'template': Select(attrs={
                'class': "nForm fSelect",
                'id': "nProductPrice",
                'placeholder': "قالب",
                'maxlength': "50",
                'hidden': "true"
            }),
            'products': SelectMultiple(attrs={
                'class': "nForm fSelect",
                'id': "nProductCat",
                'placeholder': "محصولات",
                'hidden': "true"
            }),
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('table',)
        widgets = {
            'table': NumberInput(attrs={
                'class': "nForm fText",
                'id': "nOrderTable",
                'placeholder': "شماره میز کافه",
                'maxlength': "50",
                'value': "0"
            }),
        }


class ReserveForm(forms.ModelForm):

    class Meta:
        model = TableReserve
        fields = ('tNumber', 'date', 'endTime', 'reservedBy', 'cost')
        widgets = {
            'tNumber': NumberInput(attrs={
                'class': "nForm fText",
                'id': "nReserveTable",
                'placeholder': "شماره میز کافه",
                'maxlength': "50",
            }),
            'reservedBy': TextInput(attrs={
                'class': "nForm fText",
                'id': "nReservedBy",
                'placeholder': "نام رزرو کننده",
                'maxlength': "25",
            }),
            'date': DateTimeInput(attrs={
                'class': "nForm fText",
                'id': "nReserveDate",
                'type': "datetime-local",
                'placeholder': "تاریخ رزرو میز",
            }),
            'endTime': TimeInput(attrs={
                'class': "nForm fText",
                'id': "nReserveTime",
                'type': "time",
                'placeholder': "ساعت پایان رزرو",
            }),
            'cost': NumberInput(attrs={
                'class': "nForm fText",
                'id': "nReserveCost",
                'placeholder': "هزینه رزرو میز",
            }),
        }


# Cost Forms
class CostCreateForm(forms.ModelForm):

    class Meta:
        model = Cost
        fields = ('caption', 'date', 'price')
        widgets = {
            'caption': TextInput(attrs={
                'class': "nForm fText",
                'id': "nCostName",
                'placeholder': "توضیحات",
                'maxlength': "50",
            }),
            'price': NumberInput(attrs={
                'class': "nForm fText",
                'id': "nCostPrice",
                'placeholder': "قیمت کل",
                'maxlength': "50",
            }),
            'date': DateInput(attrs={
                'class': "nForm fText",
                'id': "nCostDat",
                'type': "datetime-local",
                'placeholder': "تاریخ",
            }),
        }


# Report Forms
class ReportCreateForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('type', 'dateFrom', 'dateTo')
        widgets = {
            'type': Select(choices=(("1", "سفارشات"), ("2", "رزروی"), ("3", "هزینه")), attrs={
                'class': "nForm fText",
                'id': "rType",
                'placeholder': "type",
                'maxlength': "50",
                'required': 'true'
            }),
            'dateFrom': DateInput(attrs={
                'class': "nForm fText",
                'id': "dateFrom",
                'type': "date",
                'placeholder': "از تاریخ",
            }),
            'dateTo': DateInput(attrs={
                'class': "nForm fText",
                'id': "dateTo",
                'type': "date",
                'placeholder': "تا تاریخ",
            }),
        }
