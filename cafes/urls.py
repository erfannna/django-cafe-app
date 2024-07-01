from django.urls import path
from . import views


app_name = 'cafes'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('configure', views.configure_cafe, name='cafeConfigure'),
    path('<str:pk>/profile', views.cafe_profile, name='cProfile'),
    path('dashboard', views.dashboard, name='DashB'),
    path('dashboard/edit', views.cafe_edit, name='cEdit'),
    path('dashboard/location/edit', views.cafe_location_edit, name='cLocation'),
    path('product/new', views.product_create, name='pCreate'),
    path('menu/new', views.menu_create, name='mCreate'),
    path('m/<int:pk>', views.menu_show, name='mShow'),
    path('product/list', views.products_list, name='lProducts'),
    path('menu/list', views.menus_list, name='lMenus'),
    path('menu/default', views.menu_default, name='mDefault'),
    path('product/<int:pk>/update', views.product_update, name='pUpdate'),
    path('product/delete', views.product_delete, name='pDelete'),
    path('menu/delete', views.menu_delete, name='mDelete'),
    path('orders', views.orders, name='orders'),
    path('orders/barista', views.orders_screen, name='ordersBarista'),
    path('orders/<int:table>', views.table_order, name='tOrder'),
    path('reservations', views.table_reserve, name='reservations'),
    path('reservations/delete', views.reserved_delete, name='rDelete'),
    path('costs', views.cost_create, name='cost'),
    path('cost/delete', views.cost_delete, name='cDelete'),
    path('reports', views.financial_reports, name='fReports'),
    path('reports/new', views.xlsx_reports, name='nReport'),
    path('reports/reservations', views.financial_reports_reserved, name='fReportsRes'),
    path('reports/costs', views.financial_reports_costs, name='fReportsCost'),
    path('reports/xlsx', views.financial_reports_xlsx, name='fReportsXlsx'),
    path('dashboard/upgrade', views.upgrade_account, name='upgrade'),
    path('pay/request/subscription/<int:plan>', views.pay_send_request, name='pay_request'),
    path('pay/verify/subscription/<int:plan>', views.pay_verify, name='pay_verify'),
    path('download/<str:f_type>/<int:pk>', views.download, name='download'),
    path('<str:pk>', views.default_menu_show, name='defaultMenu'),
]
