
from django.contrib import admin
from django.urls import path
from . import views
from sku_info.views import *;
urlpatterns = [
    path('', views.table_view, name='table_view'),
    path('show-table-data', show_table_data, name='show_table_data'),
    path('load-L2', load_L2, name='load_L2'),
    path('load-L3', load_L3, name='load_L3'),
    path('get-chart-data', get_chart_data, name='get_chart_data')
]
