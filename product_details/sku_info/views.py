import json
import datetime
from django.shortcuts import render
from django.db import models
from datetime import date
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.db.models import Avg, Sum, Max
from .models import *
import logging


# Create your views here.
def home(request):
    return render(request, 'home.html', {'name': 'Prajwal'})


def table_view(request):
    filter_list = {"L1": [item for item in ProductHeirarchyData.objects.all().values('category').distinct()]}
    context = {"filters": filter_list}
    return render(request, "base.html", context)


def show_table_data(request):
    l1 = request.GET.get("L1") or None
    l2 = request.GET.get("L2") or None
    l3 = request.GET.get("L3") or None
    start = request.GET.get("from") or None
    end = request.GET.get('to') or None
    print("*********", l1, l2, l3, "*********")

    hier_data = ProductHeirarchyData.objects.all()
    table_data = []

    if start is not None:
        table_data1 = hier_data.filter(category=l1, product_line=l2, brick=l3)
        sku_objects = table_data1.values("sku_id", "sku", "brand_name")
        for index, sku_objects in enumerate(sku_objects):
            comp_data = CompetitionData.objects.filter(sku_id=sku_objects["sku_id"], dt__range=[start, end])
            sales_data = SalesData.objects.filter(sku_id=sku_objects["sku_id"], sales_date__range=[start, end])
            table_data1 = {}
            table_data1["sku_id"] = sku_objects["sku_id"]
            table_data1["sku"] = sku_objects["sku"]
            table_data1["brand_name"] = sku_objects["brand_name"]
            table_data1["Croma"] = comp_data.filter(comp_name='Croma').aggregate(Avg("price"))["price__avg"] or 0
            table_data1["Amazon"] = comp_data.filter(comp_name='Amazon').aggregate(Avg("price"))["price__avg"] or 0
            table_data1["FlipKart"] = comp_data.filter(comp_name='FlipKart').aggregate(Avg("price"))["price__avg"] or 0
            table_data1["Vijay_Sales"] = comp_data.filter(comp_name='Vijay_Sales').aggregate(Avg("price"))[
                                             "price__avg"] or 0
            table_data1["RelianceDigital"] = comp_data.filter(comp_name='RelianceDigital').aggregate(Avg("price"))[
                                                 "price__avg"] or 0
            table_data1["units_sold"] = sales_data.aggregate(Sum("units_sold"))["units_sold__sum"] or 0
            table_data1["sale_price"] = sales_data.aggregate(Avg("sale_price"))["sale_price__avg"] or 0
            table_data.append(table_data1)

    else:
        date = SalesData.objects.aggregate(Max("sales_date"))["sales_date__max"]  # get the max date
        sku_ids = SalesData.objects.all().values('sku_id').distinct()  # get the max date
        print(type(date))
        sku_list =[]
        for i in sku_ids:
            sku_list.append(i["sku_id"])

        empty_input = hier_data.filter(sku_id__in=sku_list)
            #print("****",empty_input,"****")


        sku_objects = empty_input.values("sku_id", "sku", "brand_name")
        print("***********",sku_objects)
        for index, sku_objects in enumerate(sku_objects):
            comp_data = CompetitionData.objects.filter(sku_id=sku_objects["sku_id"], dt=date)
            sales_data = SalesData.objects.filter(sku_id=sku_objects["sku_id"], sales_date=date)
            table_data1 = {}

            table_data1["sku_id"] = sku_objects["sku_id"]
            table_data1["sku"] = sku_objects["sku"]
            table_data1["brand_name"] = sku_objects["brand_name"]
            table_data1["Croma"] = comp_data.filter(comp_name='Croma').aggregate(Avg("price"))["price__avg"] or 0
            table_data1["Amazon"] = comp_data.filter(comp_name='Amazon').aggregate(Avg("price"))["price__avg"] or 0
            table_data1["FlipKart"] = comp_data.filter(comp_name='FlipKart').aggregate(Avg("price"))["price__avg"] or 0
            table_data1["Vijay_Sales"] = comp_data.filter(comp_name='Vijay_Sales').aggregate(Avg("price"))[
                                             "price__avg"] or 0
            table_data1["RelianceDigital"] = comp_data.filter(comp_name='RelianceDigital').aggregate(Avg("price"))[
                                                 "price__avg"] or 0
            table_data1["units_sold"] = sales_data.aggregate(Sum("units_sold"))["units_sold__sum"] or 0
            table_data1["sale_price"] = sales_data.aggregate(Avg("sale_price"))["sale_price__avg"] or 0

            table_data.append(table_data1)

    context = {"data": table_data}

    return HttpResponse(json.dumps(context), content_type="application/json")


def get_l1(request):
    l1 = request.GET.get('L1')
    return render(request, 'base.html', {'l1': l1})


def load_L2(request):
    l1 = request.GET.get('L1')
    query = "SELECT  distinct(product_line) from  product_heirarchy_data WHERE category = '%s'" % l1
    print("**********************", l1, "*********************")
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    # l2 = L2.objects.raw(query)
    return HttpResponse(json.dumps(results), content_type="application/json")



def load_L3(request):
    l2 = request.GET.get('L2')
    query = "SELECT  distinct(brick) from  product_heirarchy_data WHERE product_line = '%s'" % l2
    print("**********************", l2, "*********************")
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    print(json.dumps(results))
    cursor.close()
    # l2 = L2.objects.raw(query)
    return HttpResponse(json.dumps(results), content_type="application/json")



def get_chart_data(request):
    sku_id1 = request.GET.get('sku_id')
    sku_id1 = int(sku_id1)

    comp_data = CompetitionData.objects.filter(sku_id=sku_id1)
    sales_data = SalesData.objects.filter(sku_id=sku_id1)

    date_db = SalesData.objects.values("sales_date").distinct()
    date_list = []
    results = []
    for d in date_db:
        date_list.append(d["sales_date"].strftime('%Y-%m-%d'))

    Amazon_data = comp_data.filter(dt__in=date_list, sku_id=sku_id1, comp_name='Amazon').values('price')
    FlipKart_data = comp_data.filter(dt__in=date_list, sku_id=sku_id1, comp_name='FlipKart').values('price')
    Croma_data = comp_data.filter(dt__in=date_list, sku_id=sku_id1, comp_name='Croma').values('price')
    Vijay_Sales_data = comp_data.filter(dt__in=date_list, sku_id=sku_id1, comp_name='Vijay_Sales').values('price')
    RelianceDigital_data = comp_data.filter(dt__in=date_list, sku_id=sku_id1, comp_name='RelianceDigital').values('price')

    Croma_Sales_data = sales_data.filter(sales_date__in=date_list, sku_id=sku_id1).values('sale_price')

    Amazon_data_list = []
    FlipKart_data_list = []
    Croma_data_list = []
    Vijay_Sales_data_list = []
    RelianceDigital_data_list = []
    Croma_Sales_data_list = []

    for item in Amazon_data:
        if not item["price"] < 0:
            Amazon_data_list.append(item["price"])
        else:
            Amazon_data_list.append(0)

    for item in FlipKart_data:
        if not item["price"] < 0:
            FlipKart_data_list.append(item["price"])
        else:
            FlipKart_data_list.append(0)

    for item in Croma_data:
        if not item["price"] < 0:
            Croma_data_list.append(item["price"])
        else:
            Croma_data_list.append(0)

    for item in Vijay_Sales_data:
        if not item["price"] < 0:
            Vijay_Sales_data_list.append(item["price"])
        else:
            Vijay_Sales_data_list.append(0)

    for item in RelianceDigital_data:
        if not item["price"] < 0:
            RelianceDigital_data_list.append(item["price"])
        else:
            RelianceDigital_data_list.append(0)
    for item in Croma_Sales_data:
        if not item["sale_price"] < 0:
            Croma_Sales_data_list.append(item["sale_price"])
        else:
            Croma_Sales_data_list.append(0)

    result = {}
    result["Amazon"] = Amazon_data_list
    result["FlipKart"] = FlipKart_data_list
    result["Croma"] = Croma_data_list
    result["Vijay_Sales"] = Vijay_Sales_data_list
    result["RelianceDigital"] = RelianceDigital_data_list
    result['date_list'] = date_list
    result['Croma_Sales_data'] = Croma_Sales_data_list

    print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")
