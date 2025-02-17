import io
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import LoginForm, CafeInfoForm, ProductCreateForm, MenuCreateForm, \
    OrderForm, ReserveForm, CostCreateForm, ReportCreateForm, SocialPageForm
from django.views.generic import UpdateView, DeleteView, View, CreateView
from .models import Cafe, Products, Menu, Templates, Order, OrderProd,\
    TableReserve, Cost, Payments, Report, SocialNetworkPage
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, FileResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.conf import settings
from django.templatetags.static import static
from django.core import serializers
import datetime
import qrcode
import xlsxwriter
import requests
import json
from easy_thumbnails.files import get_thumbnailer
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO

MERCHANT = 'f93a89ae-a0ed-4f94-b963-f9e2ef285a51'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
AMOUNT = 11000
description = "D"
email = 'email@example.com'
mobile = '09123456789'
CallbackURL = 'https://barisca.ir/pay/verify/subscription/'


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        # if not request.is_ajax():
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("Bad Request")
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def sub_check(u):
    def check(request, *args, **kwargs):
        if not request.user.cafe.first().premium_exp > datetime.datetime.now():
            return redirect('/dashboard/upgrade')
        return u(request, *args, **kwargs)

    return check


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated successfully')
                    return redirect('cafes:DashB')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'SignIn.html', {'form': form})


def configure_cafe(request):
    if Cafe.objects.filter(owner=request.user).count() == 0:
        if request.method == 'POST':
            form = CafeInfoForm(data=request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                cafe = form.save(commit=False)
                cafe.owner = request.user
                # cafe.premium_exp = datetime.datetime.now() + datetime.timedelta(days=7)
                cafe.save()

                return JsonResponse({'status': 'ok'}, status=200)
            else:
                return JsonResponse({'status': 'error'}, status=400)
        else:
            form = CafeInfoForm(data=request.GET)

            return render(request, 'dashboard/cafeConfigure.html',
                          {'form': form})
    else:
        return redirect('cafes:DashB')


@login_required
def upgrade_account(request):
    status = True
    sub_exp = request.user.cafe.first().premium_exp.strftime("%y/%b/%d - %H:%M")
    payments = request.user.cafe.first().cafe_payments.all()
    for p in payments:
        p.price = "{:,}".format(int(p.price/10))
    if request.user.cafe.first().premium_exp > datetime.datetime.now():
        status = True
    else:
        status = False

    paginator = Paginator(payments, 5)

    page = request.GET.get("page")
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        payments = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/paymentsAJAX.html',
                      {'payments': payments})

    return render(request, 'dashboard/subscription.html',
                  {'title': 'حساب پریمیوم',
                   'subStatus': status,
                   'subExp': sub_exp,
                   'payments': payments,
                   'section': 'upgrade'})


def pay_send_request(request, plan):
    amount = 0
    if plan == 1:
        amount = 1_200_000
    elif plan == 2:
        amount = 3_450_000
    elif plan == 3:
        amount = 6_600_000
    elif plan == 4:
        amount = 12_000_000
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": f'{CallbackURL}{plan}',
        "description": f'حساب پریمیوم باریسکا پلن : {plan}',
        "metadata": {"mobile": mobile, "email": request.user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def pay_verify(request, plan):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if t_status == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        amount = 0
        if plan == 1:
            amount = 1_200_000
        elif plan == 2:
            amount = 3_450_000
        elif plan == 3:
            amount = 6_600_000
        elif plan == 4:
            amount = 12_000_000
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                # return HttpResponse('Transaction success.\nRefID: ' + str(
                    # req.json()['data']['ref_id']
                # ))
                cafe = request.user.cafe.first()
                if cafe.premium_exp > datetime.datetime.now():
                    if plan == 1:
                        cafe.premium_exp += datetime.timedelta(days=30)
                    elif plan == 2:
                        cafe.premium_exp += datetime.timedelta(days=90)
                    elif plan == 3:
                        cafe.premium_exp += datetime.timedelta(days=180)
                    elif plan == 4:
                        cafe.premium_exp += datetime.timedelta(days=365)
                else:
                    if plan == 1:
                        cafe.premium_exp = datetime.datetime.now() + datetime.timedelta(days=30)
                    elif plan == 2:
                        cafe.premium_exp = datetime.datetime.now() + datetime.timedelta(days=90)
                    elif plan == 3:
                        cafe.premium_exp = datetime.datetime.now() + datetime.timedelta(days=180)
                    elif plan == 4:
                        cafe.premium_exp = datetime.datetime.now() + datetime.timedelta(days=365)
                cafe.save()
                new_pay = Payments.objects.create(cafe=request.user.cafe.first(),
                                                  type="شارژ پنل",
                                                  price=amount,
                                                  status="موفق")

                return render(request, 'dashboard/paymentSuccess.html',
                              {'title': 'حساب پریمیوم',
                               'pStatus': 'موفق',
                               'status': 1})
            elif t_status == 101:
                # return HttpResponse('Transaction submitted : ' + str(
                    # req.json()['data']['message']
                # ))
                return render(request, 'dashboard/paymentSuccess.html',
                              {'title': 'حساب پریمیوم',
                               'pStatus': 'ثبت شده',
                               'status': 2})
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                    # req.json()['data']['message']
                # ))
                new_pay = Payments.objects.create(cafe=request.user.cafe.first(),
                                                  type="شارژ پنل",
                                                  price=amount,
                                                  status="ناموفق")
                return render(request, 'dashboard/paymentSuccess.html',
                              {'title': 'حساب پریمیوم',
                               'pStatus': 'ناموفق',
                               'status': 3})
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            new_pay = Payments.objects.create(cafe=request.user.cafe.first(),
                                              type="شارژ پنل",
                                              price=amount,
                                              status="خطا")
            return render(request, 'dashboard/paymentSuccess.html',
                          {'title': 'حساب پریمیوم',
                           'pStatus': 'خطا',
                           'message': e_message,
                           'status': 4})
    else:
        # return HttpResponse('Transaction failed or canceled by user')
        return render(request, 'dashboard/paymentSuccess.html',
                      {'title': 'حساب پریمیوم',
                       'pStatus': 'لغو شده',
                       'status': 5})


def home(request):
    return render(request, 'dashboard/landing/Main.html')


def cafe_profile(request, pk):
    cafe = Cafe.objects.get(slug=pk)
    try:
        menu = Menu.objects.get(cafe=cafe, isDefault=True)
    except:
        menu = Menu.objects.filter(cafe=cafe).last()
    return render(request, 'themes/cafeProfile.html',
                  {'cafe': cafe, 'menu': menu})


@login_required()
def dashboard(request):
    try:
        cafe = Cafe.objects.get(owner=request.user)
    except:
        return redirect('cafes:cafeConfigure')

    cafe_orders = cafe.cafe_orders.all().order_by("-created")
    today = datetime.date.today()
    daily_income, orders_num, reserved_num = 0, 0, 0
    chart_days = []
    chart_o_income, chart_r_income = [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]
    ch_days = [today]
    for x in range(1, 7):
        da = ch_days[0] - datetime.timedelta(days=x)
        ch_days.append(da)

    for o in cafe_orders:
        if o.created.year == today.year \
                and o.created.month == today.month \
                and o.created.day == today.day:
            daily_income += o.price
            orders_num += 1
        i = 0
        for ch in ch_days:
            if o.created.year == ch.year \
                    and o.created.month == ch.month \
                    and o.created.day == ch.day:
                chart_o_income[i] += o.price
            i += 1

    reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-date")
    for r in reservations:
        if r.date.year == today.year \
                and r.date.month == today.month \
                and r.date.day == today.day:
            daily_income += r.cost
            reserved_num += 1
        i = 0
        for ch in ch_days:
            if r.date.year == ch.year \
                    and r.date.month == ch.month \
                    and r.date.day == ch.day:
                chart_r_income[i] += r.cost
            i += 1

    chart_o_income.reverse()
    chart_r_income.reverse()
    for d in ch_days:
        chart_days.append(d.strftime("%b/%d"))
    chart_days.reverse()
    daily_income = "{:,}".format(daily_income)

    if cafe.premium_exp > datetime.datetime.now():
        if cafe.premium_exp <= datetime.datetime.now() + datetime.timedelta(days=7):
            sub_exp = 1
        else:
            sub_exp = 0
    else:
        sub_exp = 2

    return render(request, 'dashboard/Dashboard.html',
                  {'title': 'داشبورد', 'section': 'DashB',
                   'ordersNUM': orders_num,
                   'reservedNUM': reserved_num,
                   'daily_income': daily_income,
                   'chart_income': chart_o_income,
                   'chart_r_income': chart_r_income,
                   'chart_days': chart_days,
                   'sub_exp': sub_exp})


@login_required
def cafe_edit(request):
    cafe = request.user.cafe.first()
    sn = cafe.social.first()
    if request.method == 'POST':
        form = CafeInfoForm(data=request.POST, instance=cafe, files=request.FILES)
        if sn:
            sn_form = SocialPageForm(data=request.POST, instance=sn)
        else:
            sn_form = SocialPageForm(data=request.POST)
        if form.is_valid() and sn_form.is_valid():
            cd = form.cleaned_data
            cafe = form.save(commit=False)
            nsn = sn_form.save()
            if nsn not in cafe.social.all():
                cafe.social.add(nsn)
            if form.data["photoKeepStatus"] == '0':
                cafe.pPhoto.delete()
            if form.data["backgroundKeepStatus"] == '0':
                cafe.pBackground.delete()

            # if cd["slug"] != cafe.slug:
            qr_t = f'https://barisca.ir/{cafe.slug}'
            qr_n = f'{cafe.name}.png'
            qr_image = qrcode.make(qr_t)
            qr_offset = Image.new('RGB', (330, 330), 'white')
            draw_img = ImageDraw.Draw(qr_offset)
            qr_offset.paste(qr_image)
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            cafe.qr.save(qr_n, File(stream), save=False)
            qr_offset.close()

            cafe.save()

            # messages.success(request, '!محصول جدید با موفقیت ساخته شد')
            return render(request, 'dashboard/cafeEdit.html',
                          {'title': 'ویرایش مشخصات', 'section': 'cEdit',
                           'form': form, 'cafe': cafe, 'sn_form': sn_form, 'confirmAlert': 'Y'})
    else:
        form = CafeInfoForm(instance=cafe)
        if sn:
            sn_form = SocialPageForm(instance=sn)
        else:
            sn_form = SocialPageForm(data=request.GET)
        return render(request, 'dashboard/cafeEdit.html',
                      {'title': 'ویرایش مشخصات', 'section': 'cEdit',
                       'form': form, 'cafe': cafe, 'confirmAlert': 'N', 'sn_form': sn_form})


@login_required
def cafe_location_edit(request):
    cafe = request.user.cafe.first()
    if request.method == 'POST':
        form = CafeInfoForm(data=request.POST, instance=cafe, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            cafe = form.save(commit=False)

            cafe.save()

            return render(request, 'dashboard/cafeLocation.html',
                          {'title': 'لوکیشن کافه', 'section': 'cLocation', 'form': form, 'confirmAlert': 'Y'})
    else:
        form = CafeInfoForm(instance=cafe)
        return render(request, 'dashboard/cafeLocation.html',
                      {'title': 'لوکیشن کافه', 'section': 'cLocation', 'form': form, 'confirmAlert': 'N'})


@login_required
@sub_check
def product_create(request):
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_pro = form.save(commit=False)
            new_pro.cafe = Cafe.objects.get(owner=request.user)
            new_pro.save()

            form = ProductCreateForm(data=request.GET)
            pro_img = f'/download/product_icon/{new_pro.id}' if new_pro.photo else ''
            # messages.success(request, '!محصول جدید با موفقیت ساخته شد')
            return JsonResponse({'name': new_pro.name, 'id': new_pro.id, 'price': new_pro.price,
                                 'cat': new_pro.cate.name, 'img': pro_img}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)
            # return render(request, 'dashboard/productCreate.html',
            # {'title': 'محصول جدید', 'section': 'nProduct', 'form': form, 'confirmAlert': 'Y'})
    else:
        form = ProductCreateForm(data=request.GET)
        return render(request, 'dashboard/productCreate.html',
                      {'title': 'محصول جدید', 'section': 'nProduct', 'form': form, 'confirmAlert': 'N'})


@login_required
def products_list(request):
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_pro = form.save(commit=False)
            new_pro.cafe = Cafe.objects.get(owner=request.user)
            new_pro.save()

            form = ProductCreateForm(data=request.GET)
            products = Products.objects.filter(cafe=request.user.cafe.first()).order_by("cate")
            for p in products:
                p.price = "{:,}".format(p.price)

            # messages.success(request, '!محصول جدید با موفقیت ساخته شد')
            return render(request, 'dashboard/productsList.html',
                          {'title': 'محصولات کافه', 'section': 'lProducts',
                           'products': products, 'form': form, 'confirmAlert': 'Y'})
    else:
        form = ProductCreateForm(data=request.GET)
        products = Products.objects.filter(cafe=request.user.cafe.first()).order_by("cate")
        for p in products:
            p.price = "{:,}".format(p.price)

        return render(request, 'dashboard/productsList.html',
                      {'title': 'محصولات کافه', 'section': 'lProducts',
                       'products': products, 'form': form, 'confirmAlert': 'N'})


@login_required
def product_update(request, pk):
    if request.method == 'POST':
        pro = Products.objects.get(id=pk)
        form = ProductCreateForm(data=request.POST, files=request.FILES, instance=pro)
        if form.is_valid():
            cd = form.cleaned_data
            new_pro = form.save(commit=False)
            if form.data["photoKeepStatus"] == '0':
                new_pro.photo.delete()
            new_pro.save()
            return redirect('cafes:lProducts')

    else:
        pro = Products.objects.get(id=pk)
        form = ProductCreateForm(instance=pro)
        return render(request, 'dashboard/productCreate.html',
                      {'title': 'ویرایش محصول', 'section': 'lProducts', 'form': form})


@login_required
@ajax_required
def product_delete(request):
    try:
        p_id = request.POST.get('id')
        Products.objects.get(id=p_id).delete()
        return JsonResponse({'status': 'ok'})

    except:
        return JsonResponse({'status': 'error'})


@login_required()
@sub_check
def menu_create(request):
    if request.method == 'POST':

        t_id = request.POST.get('templateId')
        template = Templates.objects.get(id=t_id)

        p_ids = request.POST.getlist('prosList[]')
        products = []
        for p in p_ids:
            pro = Products.objects.get(id=p)
            if pro.cate in template.pTypes.all() or template.pTypes.count() == 0:
                products.append(pro)

        if template and products:
            try:
                new_menu = Menu.objects.create(cafe=request.user.cafe.first(),
                                               template=template)
                for prod in products:
                    new_menu.products.add(prod)
                qr_t = f'https://barisca.ir/m/{new_menu.id}'
                qr_n = f'{new_menu.cafe.name}-{new_menu.id}.png'
                qr_image = qrcode.make(qr_t)
                qr_offset = Image.new('RGB', (330, 330), 'white')
                draw_img = ImageDraw.Draw(qr_offset)
                qr_offset.paste(qr_image)
                stream = BytesIO()
                qr_offset.save(stream, 'PNG')
                new_menu.qr.save(qr_n, File(stream), save=False)
                qr_offset.close()
                new_menu.save()
                return JsonResponse({'status': 'ok', 'qr': f'/download/menu/{new_menu.id}',
                                     'url': new_menu.get_absolute_url()})

            except:
                pass

        return JsonResponse({'status': 'error'})

    else:
        form = MenuCreateForm(data=request.GET)
        products = request.user.cafe.first().cafe_products.all().order_by("cate")
        templates = Templates.objects.all()
        return render(request, 'dashboard/menuCreate.html',
                      {'title': 'منوی جدید', 'section': 'nMenu', 'form': form,
                       'products': products, 'templates': templates})


def menu_show(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    if menu.cafe.premium_exp > datetime.datetime.now():
        products = menu.products.all().order_by("cate")
        cats = []
        for p in products:
            p.price = "{:,}".format(p.price)
            if p.cate.name not in cats:
                cats.append(p.cate.name)

        return render(request, f'themes/{menu.template.name}.html',
                      {'title': menu.cafe.name, 'menu': menu, 'products': products, 'cats': cats})
    else:
        return render(request, f'themes/notActive.html',
                      {'menu': menu})


def default_menu_show(request, pk):
    cafe = get_object_or_404(Cafe, slug=pk)
    try:
        menu = Menu.objects.get(cafe=cafe, isDefault=True)
    except:
        menu = Menu.objects.filter(cafe=cafe).last()

    if cafe.premium_exp > datetime.datetime.now():
        products = menu.products.all().order_by("cate")
        cats = []
        for p in products:
            p.price = "{:,}".format(p.price)
            if p.cate.name not in cats:
                cats.append(p.cate.name)

        return render(request, f'themes/{menu.template.name}.html',
                      {'title': menu.cafe.name, 'menu': menu, 'products': products, 'cats': cats})
    else:
        return render(request, f'themes/notActive.html',
                      {'menu': menu})


@login_required()
def menus_list(request):
    menus = Menu.objects.filter(cafe=request.user.cafe.first())

    return render(request, 'dashboard/menusList.html',
                  {'title': 'منوهای کافه', 'section': 'lMenus', 'menus': menus})


@login_required
@ajax_required
def menu_default(request):
    try:
        m_id = request.POST.get('id')
        try:
            default = request.user.cafe.first().cafe_menus.filter(isDefault=True)
            for d in default:
                d.isDefault = False
                d.save()
        except:
            pass

        menu = request.user.cafe.first().cafe_menus.get(id=m_id)
        menu.isDefault = True
        menu.save()
        return JsonResponse({'status': 'ok'})

    except:
        return JsonResponse({'status': 'error'})


@login_required
@ajax_required
def menu_delete(request):
    try:
        m_id = request.POST.get('id')
        Menu.objects.get(id=m_id).delete()
        return JsonResponse({'status': 'ok'})

    except:
        return JsonResponse({'status': 'error'})


@login_required()
@sub_check
def orders(request):
    if request.method == 'POST':
        table_id = request.POST.get('tableID')
        p_ids = request.POST.getlist('prosList[]')
        products = []
        for p in p_ids:
            pro = Products.objects.get(id=p)
            products.append(pro)

        if products:
            new_order = Order.objects.create(cafe=request.user.cafe.first(), table=table_id)
            for prod in products:
                status = False
                for pr in new_order.prods.all():
                    if pr.prod.id == prod.id:
                        status = True
                if status == 0:
                    n_order_p = OrderProd.objects.create(prod=prod, number=1)
                    new_order.prods.add(n_order_p)
                else:
                    for p in new_order.prods.all():
                        if prod.id == p.prod.id:
                            p.number += 1
                            p.save()

                new_order.price += prod.price

            new_order.save()
            price = "{:,}".format(new_order.price)

            return JsonResponse({'status': 'ok', 'oId': new_order.id,
                                 'time': f'{new_order.created.time().strftime("%H:%M %p.")}',
                                 'price': price})

        return JsonResponse({'status': 'error'})
    else:
        form = OrderForm(data=request.GET)
        products = request.user.cafe.first().cafe_products.all().order_by("cate")
        orders_list = request.user.cafe.first().cafe_orders.all().order_by("-created")
        for o in orders_list:
            o.price = "{:,}".format(o.price)

        paginator = Paginator(orders_list, 5)
        page = request.GET.get("page")
        try:
            orders_list = paginator.page(page)
        except PageNotAnInteger:
            orders_list = paginator.page(1)
        except EmptyPage:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse('')
            orders_list = paginator.page(paginator.num_pages)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/ordersAJAX.html',
                          {'orders': orders_list})

        carts = Order.objects.filter(cafe=request.user.cafe.first(), closed=False)

        return render(request, 'dashboard/orderManager.html',
                      {'title': 'مدیریت سفارشات', 'section': 'lOrders', 'form': form,
                       'products': products, 'orders': orders_list, 'cafeId': request.user.cafe.first().id,
                       'today': datetime.date.today(),
                       'carts': carts})


@login_required()
def orders_screen(request):
    return render(request, 'dashboard/ordersBarista.html',
                  {'title': 'مانیتور باریستا', 'section': 'lOrders',
                   'cafeId': request.user.cafe.first().id,
                   'today': datetime.date.today()})


@login_required()
@sub_check
def table_order(request, table):
    form = OrderForm(data=request.GET)
    menu = Menu.objects.get(cafe=request.user.cafe.first(), isDefault=True)
    products = menu.products.all().order_by("cate")

    for p in products:
        p.price = "{:,}".format(p.price)

    return render(request, 'dashboard/tableOrderSubmit.html',
                  {'title': 'سفارش میز', 'form': form,
                   'tableID': table,
                   'products': products, 'cafeId': request.user.cafe.first().id,
                   'today': datetime.date.today()})


@login_required
@sub_check
def table_reserve(request):

    reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-date")
    reserved = []
    reserved_other_days = []
    for re in reservations:
        re.cost = "{:,}".format(re.cost)
        if re.date.year == datetime.date.today().year\
                and re.date.month == datetime.date.today().month\
                and re.date.day == datetime.date.today().day:
            reserved.append(re)
        else:
            reserved_other_days.append(re)

    if request.method == 'POST':
        form = ReserveForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_pro = form.save(commit=False)
            new_pro.cafe = Cafe.objects.get(owner=request.user)
            new_pro.save()

            # messages.success(request, '!محصول جدید با موفقیت ساخته شد')
            return redirect('/reservations')
    else:
        form = ReserveForm(data=request.GET)

        paginator = Paginator(reserved_other_days, 5)
        page = request.GET.get("page")
        try:
            reserved_other_days = paginator.page(page)
        except PageNotAnInteger:
            reserved_other_days = paginator.page(1)
        except EmptyPage:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse('')
            reserved_other_days = paginator.page(paginator.num_pages)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/reservedAJAX.html',
                          {'reserved': reserved,
                           'reserved_other_days': reserved_other_days,
                           'first_page': False})

        return render(request, 'dashboard/reservation.html',
                      {'title': 'مدیریت رزرو میزها',
                       'section': 'lReservations', 'form': form,
                       'reserved': reserved,
                       'reserved_other_days': reserved_other_days,
                       'confirmAlert': 'N',
                       'first_page': True})


@login_required
@ajax_required
def reserved_delete(request):
    try:
        r_id = request.POST.get('id')
        TableReserve.objects.get(id=r_id).delete()
        return JsonResponse({'status': 'ok'})

    except:
        return JsonResponse({'status': 'error'})


@login_required
@sub_check
def cost_create(request):
    if request.method == 'POST':
        form = CostCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_pro = form.save(commit=False)
            new_pro.cafe = Cafe.objects.get(owner=request.user)
            new_pro.save()

            form = CostCreateForm(data=request.GET)
            costs = request.user.cafe.first().cafe_costs.all().order_by("-date")
            for c in costs:
                c.price = "{:,}".format(c.price)
            paginator = Paginator(costs, 10)
            costs = paginator.page(1)

            return render(request, 'dashboard/costCreate.html',
                          {'title': 'هزینه ها', 'section': 'nCost', 'form': form,
                           'confirmAlert': 'Y', 'costs': costs,
                           'today': datetime.date.today()})
    else:
        form = CostCreateForm(data=request.GET)
        costs = request.user.cafe.first().cafe_costs.all().order_by("-date")
        for c in costs:
            c.price = "{:,}".format(c.price)
        paginator = Paginator(costs, 10)

        page = request.GET.get("page")
        try:
            costs = paginator.page(page)
        except PageNotAnInteger:
            costs = paginator.page(1)
        except EmptyPage:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse('')
            costs = paginator.page(paginator.num_pages)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/costsAJAX.html',
                          {'costs': costs,
                           'today': datetime.date.today()})

        return render(request, 'dashboard/costCreate.html',
                      {'title': 'هزینه ها', 'section': 'nCost', 'form': form,
                       'confirmAlert': 'N', 'costs': costs,
                       'today': datetime.date.today()})


@login_required
@ajax_required
def cost_delete(request):
    try:
        c_id = request.POST.get('id')
        Cost.objects.get(id=c_id).delete()
        return JsonResponse({'status': 'ok'})

    except:
        return JsonResponse({'status': 'error'})


@login_required
def financial_reports(request):
    monthly_income = 0
    total_income = 0
    total_orders = 0
    monthly_orders = 0
    cafe_orders = request.user.cafe.first().cafe_orders.all().order_by("-created")
    reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-id")
    costs = request.user.cafe.first().cafe_costs.all().order_by("-date")

    for o in cafe_orders:
        total_income += o.price
        if o.created.year == datetime.date.today().year and o.created.month == datetime.date.today().month:
            monthly_income += o.price
            monthly_orders += o.price
        total_orders += o.price
        o.price = "{:,}".format(o.price)

    for r in reservations:
        total_income += r.cost
        if r.date.year == datetime.date.today().year and r.date.month == datetime.date.today().month:
            monthly_income += r.cost
        r.cost = "{:,}".format(r.cost)

    monthly_net_in = monthly_income
    for c in costs:
        if c.date.year == datetime.date.today().year and c.date.month == datetime.date.today().month:
            monthly_net_in -= c.price
        c.price = "{:,}".format(c.price)

    monthly_net_in = "{:,}".format(monthly_net_in)
    total_income = "{:,}".format(total_income)
    monthly_income = "{:,}".format(monthly_income)
    total_orders = "{:,}".format(total_orders)
    monthly_orders = "{:,}".format(monthly_orders)
    orders_num = "{:,}".format(cafe_orders.count())

    paginator = Paginator(cafe_orders, 10)

    page = request.GET.get("page")
    try:
        orders_list = paginator.page(page)
    except PageNotAnInteger:
        orders_list = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        orders_list = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/reportsAJAX.html',
                      {'orders': orders_list,
                       'today': datetime.date.today()})

    form = ReportCreateForm(data=request.GET)
    return render(request, 'dashboard/FinancialReports.html',
                  {'title': 'گزارشات مالی|سفارش',
                   'section': 'fReports',
                   'income': total_income,
                   'monthly_income': monthly_income,
                   'mNetIncome': monthly_net_in,
                   'total_orders': total_orders,
                   'monthly_orders': monthly_orders,
                   'orders': orders_list,
                   'orders_num': orders_num,
                   'reportType': 'orders',
                   'form': form,
                   'today': datetime.date.today()})


@login_required
def financial_reports_reserved(request):
    monthly_income = 0
    total_income = 0
    total_reserved = 0
    monthly_reserved = 0
    cafe_orders = request.user.cafe.first().cafe_orders.all().order_by("-created")
    reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-date")
    costs = request.user.cafe.first().cafe_costs.all().order_by("-date")

    for o in cafe_orders:
        total_income += o.price
        if o.created.year == datetime.date.today().year and o.created.month == datetime.date.today().month:
            monthly_income += o.price
        o.price = "{:,}".format(o.price)

    for r in reservations:
        total_income += r.cost
        if r.date.year == datetime.date.today().year and r.date.month == datetime.date.today().month:
            monthly_income += r.cost
            monthly_reserved += r.cost
        total_reserved += r.cost
        r.cost = "{:,}".format(r.cost)

    monthly_net_in = monthly_income
    for c in costs:
        if c.date.year == datetime.date.today().year and c.date.month == datetime.date.today().month:
            monthly_net_in -= c.price
        c.price = "{:,}".format(c.price)
    monthly_net_in = "{:,}".format(monthly_net_in)

    total_income = "{:,}".format(total_income)
    monthly_income = "{:,}".format(monthly_income)
    total_reserved = "{:,}".format(total_reserved)
    monthly_reserved = "{:,}".format(monthly_reserved)
    reserved_num = "{:,}".format(reservations.count())

    paginator = Paginator(reservations, 10)

    page = request.GET.get("page")
    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        reservations = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/reportsAJAX.html',
                      {'reservations': reservations,
                       'today': datetime.date.today()})

    form = ReportCreateForm(data=request.GET)
    return render(request, 'dashboard/FinancialReports.html',
                  {'title': 'گزارشات مالی|رزرو',
                   'section': 'fReports',
                   'income': total_income,
                   'monthly_income': monthly_income,
                   'mNetIncome': monthly_net_in,
                   'total_reserved': total_reserved,
                   'monthly_reserved': monthly_reserved,
                   'reservations': reservations,
                   'reserved_num': reserved_num,
                   'reportType': 'reservations',
                   'form': form,
                   'today': datetime.date.today()})


@login_required
def financial_reports_costs(request):
    monthly_income = 0
    total_income = 0
    total_costs = 0
    monthly_costs = 0
    cafe_orders = request.user.cafe.first().cafe_orders.all().order_by("-created")
    reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-id")
    costs = request.user.cafe.first().cafe_costs.all().order_by("-date")

    for o in cafe_orders:
        total_income += o.price
        if o.created.year == datetime.date.today().year and o.created.month == datetime.date.today().month:
            monthly_income += o.price
        o.price = "{:,}".format(o.price)

    for r in reservations:
        total_income += r.cost
        if r.date.year == datetime.date.today().year and r.date.month == datetime.date.today().month:
            monthly_income += r.cost
        r.cost = "{:,}".format(r.cost)

    monthly_net_in = monthly_income
    for c in costs:
        if c.date.year == datetime.date.today().year and c.date.month == datetime.date.today().month:
            monthly_net_in -= c.price
            monthly_costs += c.price
        total_costs += c.price
        c.price = "{:,}".format(c.price)
    monthly_net_in = "{:,}".format(monthly_net_in)

    total_income = "{:,}".format(total_income)
    monthly_income = "{:,}".format(monthly_income)
    total_costs = "{:,}".format(total_costs)
    monthly_costs = "{:,}".format(monthly_costs)
    costs_num = "{:,}".format(costs.count())

    paginator = Paginator(costs, 10)

    page = request.GET.get("page")
    try:
        costs = paginator.page(page)
    except PageNotAnInteger:
        costs = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        costs = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/reportsAJAX.html',
                      {'costs': costs,
                       'today': datetime.date.today()})

    form = ReportCreateForm(data=request.GET)
    return render(request, 'dashboard/FinancialReports.html',
                  {'title': 'گزارشات مالی|هزینه',
                   'section': 'fReports',
                   'income': total_income,
                   'monthly_income': monthly_income,
                   'mNetIncome': monthly_net_in,
                   'total_costs': total_costs,
                   'monthly_costs': monthly_costs,
                   'costs': costs,
                   'costs_num': costs_num,
                   'reportType': 'costs',
                   'form': form,
                   'today': datetime.date.today()})


@login_required
def financial_reports_xlsx(request):
    monthly_income = 0
    total_income = 0
    total_orders = 0
    monthly_orders = 0
    cafe_orders = request.user.cafe.first().cafe_orders.all().order_by("-created")
    reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-id")
    costs = request.user.cafe.first().cafe_costs.all().order_by("-date")
    reports = request.user.cafe.first().cafe_reports.all().order_by("-created")

    for o in cafe_orders:
        total_income += o.price
        if o.created.year == datetime.date.today().year and o.created.month == datetime.date.today().month:
            monthly_income += o.price
            monthly_orders += o.price
        total_orders += o.price
        o.price = "{:,}".format(o.price)

    for r in reservations:
        total_income += r.cost
        if r.date.year == datetime.date.today().year and r.date.month == datetime.date.today().month:
            monthly_income += r.cost
        r.cost = "{:,}".format(r.cost)

    monthly_net_in = monthly_income
    for c in costs:
        if c.date.year == datetime.date.today().year and c.date.month == datetime.date.today().month:
            monthly_net_in -= c.price
        c.price = "{:,}".format(c.price)

    monthly_net_in = "{:,}".format(monthly_net_in)
    total_income = "{:,}".format(total_income)
    monthly_income = "{:,}".format(monthly_income)
    total_orders = "{:,}".format(total_orders)
    monthly_orders = "{:,}".format(monthly_orders)
    orders_num = "{:,}".format(cafe_orders.count())

    paginator = Paginator(reports, 5)

    page = request.GET.get("page")
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        reports = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/reportsAJAX.html',
                      {'reports': reports})

    form = ReportCreateForm(data=request.GET)
    return render(request, 'dashboard/FinancialReports.html',
                  {'title': 'گزارشات مالی',
                   'section': 'fReports',
                   'income': total_income,
                   'monthly_income': monthly_income,
                   'mNetIncome': monthly_net_in,
                   'total_orders': total_orders,
                   'monthly_orders': monthly_orders,
                   'reports': reports,
                   'orders_num': orders_num,
                   'reportType': 'xlsx',
                   'form': form})


@login_required
@ajax_required
def xlsx_reports(request):

    if request.method == 'POST':
        form = ReportCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            report = form.save(commit=False)
            report.cafe = Cafe.objects.get(owner=request.user)
            d_from = report.dateFrom
            d_to = report.dateTo
            r_type = report.type
            report.save()

            buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(buffer)
            worksheet = workbook.add_worksheet()
            r, c = 0, 0

            if r_type == '1':
                r_orders = []
                cafe_orders = request.user.cafe.first().cafe_orders.all().order_by("-created")
                for o in cafe_orders:
                    if d_from <= o.created.date() <= d_to:
                        r_orders.append(o)
                worksheet.write(r, c, "کدسفارش")
                worksheet.write(r, c+1, "تاریخ/ساعت")
                worksheet.write(r, c+2, "میز")
                worksheet.write(r, c+3, "قیمت")
                worksheet.write(r, c+4, "محصولات")
                r += 1
                for order in r_orders:
                    worksheet.write(r, c, order.id)
                    c += 1
                    worksheet.write(r, c, order.created.strftime("%y/%b/%d-%H:%M"))
                    c += 1
                    worksheet.write(r, c, order.table)
                    c += 1
                    worksheet.write(r, c, order.price)
                    c += 1
                    for pro in order.prods.all():
                        worksheet.write(r, c, f'{pro.prod.name}-{pro.number}')
                        c += 1
                    r += 1
                    c = 0
            elif r_type == '2':
                r_reserved = []
                reservations = TableReserve.objects.filter(cafe=request.user.cafe.first()).order_by("-id")
                for re in reservations:
                    if d_from <= re.date.date() <= d_to:
                        r_reserved.append(re)
                worksheet.write(r, c, "کدرزرو")
                worksheet.write(r, c+1, "میز")
                worksheet.write(r, c+2, "به نام")
                worksheet.write(r, c+3, "تاریخ/ساعت")
                worksheet.write(r, c+4, "پایان")
                worksheet.write(r, c+5, "قیمت")
                r += 1
                for res in r_reserved:
                    worksheet.write(r, c, res.id)
                    c += 1
                    worksheet.write(r, c, res.tNumber)
                    c += 1
                    worksheet.write(r, c, res.reservedBy)
                    c += 1
                    worksheet.write(r, c, res.date.strftime("%y/%b/%d-%H:%M"))
                    c += 1
                    worksheet.write(r, c, res.endTime.strftime("%H:%M"))
                    c += 1
                    worksheet.write(r, c, res.cost)
                    c += 1

                    r += 1
                    c = 0
            else:
                r_costs = []
                costs = request.user.cafe.first().cafe_costs.all().order_by("-date")
                for cost in costs:
                    if d_from <= cost.date.date() <= d_to:
                        r_costs.append(cost)
                worksheet.write(r, c, "توضیحات")
                worksheet.write(r, c+1, "تاریخ/ساعت")
                worksheet.write(r, c+2, "قیمت")
                r += 1
                for co in r_costs:
                    worksheet.write(r, c, co.caption)
                    c += 1
                    worksheet.write(r, c, co.date.strftime("%y/%b/%d-%H:%M"))
                    c += 1
                    worksheet.write(r, c, co.price)
                    c += 1

                    r += 1
                    c = 0

            workbook.close()
            buffer.seek(0)

            try:
                report.file.save(f'{request.user.cafe.first().name}-{report.id}.xlsx', buffer)
            except:
                return JsonResponse({'status': 'output_error'}, status=400)

            report.save()
            ser_report = serializers.serialize('json', [report])

            return JsonResponse({'reportFile': f'/download/report/{report.id}'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)


def download(request, f_type, pk):
    if f_type == 'default_menu':
        document = get_object_or_404(Cafe, pk=pk)
        response = HttpResponse(document.qr, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.qr.name}"'
    elif f_type == 'menu':
        document = get_object_or_404(Menu, pk=pk)
        response = HttpResponse(document.qr, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.qr.name}"'
    elif f_type == 'menu_thumb':
        document = get_object_or_404(Templates, pk=pk)
        response = HttpResponse(document.thumbnail, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.thumbnail.name}"'
    elif f_type == 'product':
        document = get_object_or_404(Products, pk=pk)
        thumb = get_thumbnailer(document.photo)['product']
        response = HttpResponse(thumb, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.name}"'
    elif f_type == 'product_icon':
        document = get_object_or_404(Products, pk=pk)
        thumb = get_thumbnailer(document.photo)['avatar']
        response = HttpResponse(thumb, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.name}"'
    elif f_type == 'report':
        document = get_object_or_404(Report, pk=pk)
        response = HttpResponse(document.file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
    elif f_type == 'profile':
        document = get_object_or_404(Cafe, pk=pk)
        thumb = get_thumbnailer(document.pPhoto)['profile']
        response = HttpResponse(thumb, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.name}"'
    else:
        document = get_object_or_404(Cafe, pk=pk)
        thumb = get_thumbnailer(document.pBackground)['wallpaper']
        response = HttpResponse(thumb, content_type='image/png+jpeg')
        response['Content-Disposition'] = f'attachment; filename="{document.name}"'

    return response
