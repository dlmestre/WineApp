from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from datadb.forms import UploadFileForm, handle_uploaded_file,chuncks
from datadb.wineClass import handleNegoceFile,check,getMarkup
from helper import read_path,remove_file,read_path2,remove_file2
from .models import negoces,negoces2,manual
from django.template import loader
import csv
import pandas as pd
import json
# Create your views here.

def round_price(price):
    if int(price) > 200:
        rest = int(price) % 10
        if rest >= 5 and rest < 8:
            last_digit = 5
        elif rest < 5 :
            last_digit = 0
        else:
            last_digit = 8
        str_price = str(int(price))
        str_price = str_price[:-1] + str(last_digit)
        price = int(str_price)
    return price

@login_required
def database(request):
    #results = {}
    #files = read_path()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #msg = handle_uploaded_file(request.FILES['file'],database=True)
            #msg = handle_uploaded_file(request.FILES['django_file'])
            path = handle_uploaded_file(request.FILES['file'],database=True)
            #__init__(self,path,production_env,location='/home/ubuntu/app/data/',negoces=negoces_dictionary)
            msg_obj = handleNegoceFile(path,True,location="/home/ubuntu/app/dbfiles/")
            msg = msg_obj.getContent()

            if "wines" in msg.keys() and "prices" in msg.keys() and "years" in msg.keys():
                Wines = msg["wines"]
                Prices = msg["prices"]
                Years = msg["years"]
                Regions = msg["regions"]
                Formats = msg["formats"]
                PricesMarkup = msg["markup prices"]
                Percentiles = msg["percentiles"]
                Negoces = msg["negoces"]
                Quantities = msg["quantities"]
                Types = msg["types"]
                Vendors = msg["vendors"]
                error = None
            else:
                Wines = None
                Prices = None
                Years = None
                Regions = None
                error = msg["error"]
            if Wines and Prices and Years:
                results = zip(Wines,Prices,Years,Regions,Formats,PricesMarkup,Percentiles,Negoces,Quantities,Types,Vendors)
            else:
                results = None
            return render(request,'upload2.html', {"Results":results,"error":error})
    #        return HttpResponse(json.dumps(results),content_type="application/json")
        else:
            form = UploadFileForm()
            form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    else:
        form = UploadFileForm()
        form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    print "logged"
    form = UploadFileForm()
    form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    return render(request, 'database.html', {'form': form})

@login_required
def remover(request):
    files = read_path2()

    files_list = []
    for a_file in files:
        files_dict = {}
        files_dict["name"] = str(a_file).split(".")[0].replace("_converted","")
        files_dict["file"] = a_file
        files_list.append(files_dict)
    error = None
    if request.method == 'POST':
        values = request.POST.getlist('checks')
        for value in values:
            name = str(value).split(".")[0]
            try:
                original_file = name.replace("_converted","") + ".csv"
                remove_file2(original_file)
            except Exception as e:
                print e
                error = e
            try:
                remove_file2(str(value))
            except Exception as e:
                print e
                error = e
        return render(request,'remover.html', {"results":values,"error":error})
    return render(request, 'remover.html',{"files":files_list})

@login_required
def remover_copy(request):
    files = read_path2()

    files_list = []
    for a_file in files:
        files_dict = {}
        files_dict["name"] = str(a_file).split(".")[0].replace("_converted","")
        files_dict["file"] = a_file
        files_list.append(files_dict)
    error = None
    if request.method == 'POST':
        values = request.POST.getlist('checks')
        for value in values:
            name = str(value).split(".")[0]
            try:
                original_file = name.replace("_converted","") + ".csv"
                remove_file2(original_file)
            except Exception as e:
                print e
                error = e
            try:
                remove_file2(str(value))
            except Exception as e:
                print e
                error = e
        return render(request,'remover_copy.html', {"results":values,"error":error})
    return render(request, 'remover_copy.html',{"files":files_list})



@login_required
def showtable(request):
    wines = negoces.objects.order_by().values_list("wine",flat=True)
    prices = negoces.objects.order_by().values_list("price",flat=True)
    dates = negoces.objects.order_by().values_list("date",flat=True)
    years = negoces.objects.order_by().values_list("year",flat=True)
    regions = negoces.objects.order_by().values_list("region",flat=True)
    formats = negoces.objects.order_by().values_list("format",flat=True)
    markup_prices = negoces.objects.order_by().values_list("markup_price",flat=True)
    markup_percentiles = negoces.objects.order_by().values_list("markup_percentile",flat=True)
    ws_merchants = negoces.objects.order_by().values_list("ws_merchants",flat=True)
    ws_prices = negoces.objects.order_by().values_list("ws_price",flat=True)
    negoce_names = negoces.objects.order_by().values_list("negoce_name",flat=True)
    recommended_prices = negoces.objects.order_by().values_list("recommended_price",flat=True)
    sells = negoces.objects.order_by().values_list("sell",flat=True)
    margins = negoces.objects.order_by().values_list("margin",flat=True)
    quantities = negoces.objects.order_by().values_list("quantity",flat=True)
    types = negoces.objects.order_by().values_list("a_type",flat=True) 
    vendors = negoces.objects.order_by().values_list("vendor",flat=True)

    values = zip(wines,prices,dates,years,regions,formats,markup_prices,markup_percentiles,
                 ws_merchants,ws_prices,negoce_names,recommended_prices,sells,margins,
                 quantities,types,vendors)
    return render(request,'table.html',{"values":values})


@login_required
def wine(request):
    wines_data = None
    values = None
    wine = None
    year = None
    msg = None
    if request.method == "POST":
        wine = request.POST.get('wine')
        year = request.POST.get('year')
        if wine and year:
            wines_data = negoces2.objects.all().filter(wine__iexact=wine,year=year)
        elif wine and not year:
            wines_data = negoces2.objects.all().filter(wine__iexact=wine)
        if wines_data:
            wines = wines_data.values_list("wine",flat=True)
            prices = wines_data.values_list("price",flat=True)
            dates = wines_data.values_list("date",flat=True)
            years = wines_data.values_list("year",flat=True)
            regions_english = wines_data.values_list("region_english",flat=True)
            regions_chinese = wines_data.values_list("region_chinese",flat=True)
            formats = wines_data.values_list("a_format",flat=True)
            markup_prices = wines_data.values_list("markup_price",flat=True)
            markup_percentiles = wines_data.values_list("markup_percentile",flat=True)
            vendors_english = wines_data.values_list("vendor_english",flat=True)
            vendors_chinese = wines_data.values_list("vendor_chinese",flat=True)
            countries_english = wines_data.values_list("country_english",flat=True)
            countries_chinese = wines_data.values_list("country_chinese",flat=True)
            ws_merchants = wines_data.values_list("ws_merchants",flat=True)
            ws_prices = wines_data.values_list("ws_price",flat=True)
            negoce_names = wines_data.values_list("negoce_name",flat=True)
            recommended_prices = wines_data.values_list("recommended_price",flat=True)
            sells = wines_data.values_list("sell",flat=True)
            ratings = wines_data.values_list("rating",flat=True)
            growths = wines_data.values_list("growth",flat=True)
            margins = wines_data.values_list("margin",flat=True)
            quantities = wines_data.values_list("quantity",flat=True)
            types_english = wines_data.values_list("a_type_english",flat=True)
            types_chinese = wines_data.values_list("a_type_chinese",flat=True)
            cheapest_percents = wines_data.values_list("cheapest_percent",flat=True)

            values = zip(wines,prices,dates,years,regions_english,regions_chinese,formats,markup_prices,
                         markup_percentiles,vendors_english,vendors_chinese,countries_english,countries_chinese,
                         ws_merchants,ws_prices,negoce_names,recommended_prices,sells,ratings,growths,margins,
                         quantities,types_english,types_chinese, cheapest_percents)
    if not wine and not year:
        wine = "Wine"
        year = "Year"
    return render(request,'selectedwines.html',{"values":values,"wine":wine,"year":year,"msg":msg})

@login_required
def download2(request):
    path = r"/home/ubuntu/app/data2/export2.csv"
    df = pd.DataFrame()

    wineids = negoces2.objects.order_by().values_list("wineid",flat=True)
    wines = negoces2.objects.order_by().values_list("wine",flat=True)
    years = negoces2.objects.order_by().values_list("year",flat=True)
    regions_english = negoces2.objects.order_by().values_list("region_english",flat=True)
    regions_chinese = negoces2.objects.order_by().values_list("region_chinese",flat=True)
    formats = negoces2.objects.order_by().values_list("a_format",flat=True)
    negoces = negoces2.objects.order_by().values_list("negoce_name",flat=True)
    prices = negoces2.objects.order_by().values_list("price",flat=True)
    markup_percentiles = negoces2.objects.order_by().values_list("markup_percentile",flat=True)
    markup_prices = negoces2.objects.order_by().values_list("markup_price",flat=True)
    ws_merchants = negoces2.objects.order_by().values_list("ws_merchants",flat=True)
    ws_prices = negoces2.objects.order_by().values_list("ws_price",flat=True)
    recommended_prices = negoces2.objects.order_by().values_list("recommended_price",flat=True)
    margins = negoces2.objects.order_by().values_list("margin",flat=True)
    sells = negoces2.objects.order_by().values_list("sell",flat=True)
    dates = negoces2.objects.order_by().values_list("date",flat=True)
    qtys = negoces2.objects.order_by().values_list("quantity",flat=True)
    english_types = negoces2.objects.order_by().values_list("a_type_english",flat=True)
    chinese_types = negoces2.objects.order_by().values_list("a_type_chinese",flat=True)
    english_vendors = negoces2.objects.order_by().values_list("vendor_english",flat=True)
    chinese_vendors = negoces2.objects.order_by().values_list("vendor_chinese",flat=True)
    ratings = negoces2.objects.order_by().values_list("rating",flat=True)

    df["ID"] = wineids
    df["Wine"] = wines
    df["Year"] = years
    df["Region English"] = regions_english
    df["Region Chinese"] = regions_chinese
    df["Formats"] = formats
    df["Negoces"] = negoces
    df["Price"] = prices
    df["Markup Percentile"] = markup_percentiles
    df["Markup Price"] = markup_prices
    df["WS Merchants"] = ws_merchants
    df["WS Prices"] = ws_prices
    df["Recommended Prices"] = recommended_prices
    df["Margin"] = margins
    df["Sell"] = sells
    df["Date"] = dates
    df["Qty"] = qtys
    df["English Type"] = english_types
    df["Chinese Type"] = chinese_types
    df["English Vendor"] = english_vendors
    df["Chinese Vendor"] = chinese_vendors
    df["Rating"] = ratings

    df.to_csv(path,encoding="utf-8")
    data = open(path,"r").read()
    response = HttpResponse(data,content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response


@login_required
def showtable2(request):
    wines = negoces2.objects.order_by().values_list("wine",flat=True)
    prices = negoces2.objects.order_by().values_list("price",flat=True)
    dates = negoces2.objects.order_by().values_list("date",flat=True)
    years = negoces2.objects.order_by().values_list("year",flat=True)
    regions_english = negoces2.objects.order_by().values_list("region_english",flat=True)
    regions_chinese = negoces2.objects.order_by().values_list("region_chinese",flat=True)
    formats = negoces2.objects.order_by().values_list("a_format",flat=True)
    markup_prices = negoces2.objects.order_by().values_list("markup_price",flat=True)
    markup_percentiles = negoces2.objects.order_by().values_list("markup_percentile",flat=True)
    vendors_english = negoces2.objects.order_by().values_list("vendor_english",flat=True)
    vendors_chinese = negoces2.objects.order_by().values_list("vendor_chinese",flat=True)
    countries_english = negoces2.objects.order_by().values_list("country_english",flat=True)
    countries_chinese = negoces2.objects.order_by().values_list("country_chinese",flat=True)
    ws_merchants = negoces2.objects.order_by().values_list("ws_merchants",flat=True)
    ws_prices = negoces2.objects.order_by().values_list("ws_price",flat=True)
    negoce_names = negoces2.objects.order_by().values_list("negoce_name",flat=True)
    recommended_prices = negoces2.objects.order_by().values_list("recommended_price",flat=True)
    sells = negoces2.objects.order_by().values_list("sell",flat=True)
    ratings = negoces2.objects.order_by().values_list("rating",flat=True)
    growths = negoces2.objects.order_by().values_list("growth",flat=True)
    margins = negoces2.objects.order_by().values_list("margin",flat=True)
    quantities = negoces2.objects.order_by().values_list("quantity",flat=True)
    types_english = negoces2.objects.order_by().values_list("a_type_english",flat=True)
    types_chinese = negoces2.objects.order_by().values_list("a_type_chinese",flat=True)
    cheapest_percents = negoces2.objects.order_by().values_list("cheapest_percent",flat=True) 

    percents = [str(i)+"%" for i in range(2,6) if str(i)+"%"!=str(cheapest_percents)]

    values = zip(wines,prices,dates,years,regions_english,regions_chinese,formats,markup_prices,
                 markup_percentiles,vendors_english,vendors_chinese,countries_english,countries_chinese,
                 ws_merchants,ws_prices,negoce_names,recommended_prices,sells,ratings,growths,margins,
                 quantities,types_english,types_chinese,cheapest_percents)
    return render(request,'table2.html',{"values":values,"percents":percents})

@login_required
def download(request):
    path = r"/home/ubuntu/app/data/export.csv"
    df = pd.DataFrame()

    wines = negoces.objects.order_by().values_list("wine",flat=True)
    prices = negoces.objects.order_by().values_list("price",flat=True)
    dates = negoces.objects.order_by().values_list("date",flat=True)
    years = negoces.objects.order_by().values_list("year",flat=True)
    regions = negoces.objects.order_by().values_list("region",flat=True)
    formats = negoces.objects.order_by().values_list("format",flat=True)
    markup_prices = negoces.objects.order_by().values_list("markup_price",flat=True)
    markup_percentiles = negoces.objects.order_by().values_list("markup_percentile",flat=True)
    ws_merchants = negoces.objects.order_by().values_list("ws_merchants",flat=True)
    ws_prices = negoces.objects.order_by().values_list("ws_price",flat=True)
    negoce_names = negoces.objects.order_by().values_list("negoce_name",flat=True)
    recommended_prices = negoces.objects.order_by().values_list("recommended_price",flat=True)
    sells = negoces.objects.order_by().values_list("sell",flat=True)
    margins = negoces.objects.order_by().values_list("margin",flat=True)
    quantities = negoces.objects.order_by().values_list("quantity",flat=True)
    types = negoces.objects.order_by().values_list("a_type",flat=True)
    vendors = negoces.objects.order_by().values_list("vendor",flat=True)

    df["Wine"] = wines
    df["Price"] = prices
    df["Date"] = dates
    df["Year"] = years
    df["Region"] = regions
    df["Format"] = formats
    df["Markup Price"] = markup_prices
    df["Markup %"] = markup_percentiles
    df["WS Merchant"] = ws_merchants
    df["WS Price"] = ws_prices
    df["Negoce"] = negoce_names
    df["Recommended Selling Price"] = recommended_prices
    df["Sell"] = sells
    df["Margin"] = margins
    df["Quantity"] = quantities
    df["Type"] = types
    df["Vendor"] = vendors

    df.to_csv(path,encoding="utf-8")
    data = open(path,"r").read()
    response = HttpResponse(data,content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    #writer = csv.writer(response)
 
    #writer.writerow({"wine":"wine 1","date": "date 1"})
    #writer.writerow({"wine":"wine 2","date": "date 2"})
    return response

@login_required
def manual_table(request):
    if request.method == 'POST':
        wine = request.POST.get('wine')
        price = request.POST.get('cost')
        year = request.POST.get('vintage')
        region = request.POST.get('region')
        quantity = request.POST.get('quantity')
        negoce = request.POST.get('negoce')

        markup_prices,markups = getMarkup()        
        rate,percentile = check(price,markup_prices,markups)
        price_after_markup = float(price) * (1 + rate)
        price_after_markup = "{0:.2f}".format(price_after_markup)

        uploaded_wine = manual(wine=wine,price=price,year=year,region=region,format="75cl",markup_price=price_after_markup,
                               markup_percentile=percentile,quantity=quantity,negoce=negoce)
        uploaded_wine.save()
    return render(request,'manual.html')

def percents(request):
    data = {}
    if request.method == "POST":
        data["wine"] = request.POST.get('winedjango')
        data["year"] = request.POST.get('yeardjango')
        data["percent"] = request.POST.get('percentdjango')
        percent = int(data["percent"].replace("%",""))
        ws_price = int(negoces2.objects.filter(wine=data["wine"],year=data["year"]).values("ws_price")[0]["ws_price"])
        recommended_price = ws_price * (100 - percent) / float(100)
        record_id = negoces2.objects.filter(wine=data["wine"],year=data["year"]).values("id")[0]["id"]
        data["id"] = record_id
        data["recommended"] = round_price(recommended_price)
        data["wine data"] = ws_price
        record = negoces2.objects.get(id=record_id)
        cost = record.price
        data["margin"] = round(float(data["recommended"]) - float(cost))
        record.recommended_price = data["recommended"]
        record.cheapest_percent = data["percent"]
        record.margin = data["margin"] 
        record.save()
    return HttpResponse(json.dumps(data),content_type="application/json")

@login_required
def getTable(request):
    wines = negoces2.objects.order_by().values_list("wine",flat=True)
    prices = negoces2.objects.order_by().values_list("price",flat=True)
    dates = negoces2.objects.order_by().values_list("date",flat=True)
    years = negoces2.objects.order_by().values_list("year",flat=True)
    regions_english = negoces2.objects.order_by().values_list("region_english",flat=True)
    regions_chinese = negoces2.objects.order_by().values_list("region_chinese",flat=True)
    formats = negoces2.objects.order_by().values_list("a_format",flat=True)
    markup_prices = negoces2.objects.order_by().values_list("markup_price",flat=True)
    markup_percentiles = negoces2.objects.order_by().values_list("markup_percentile",flat=True)
    vendors_english = negoces2.objects.order_by().values_list("vendor_english",flat=True)
    vendors_chinese = negoces2.objects.order_by().values_list("vendor_chinese",flat=True)
    countries_english = negoces2.objects.order_by().values_list("country_english",flat=True)
    countries_chinese = negoces2.objects.order_by().values_list("country_chinese",flat=True)
    ws_merchants = negoces2.objects.order_by().values_list("ws_merchants",flat=True)
    ws_prices = negoces2.objects.order_by().values_list("ws_price",flat=True)
    negoce_names = negoces2.objects.order_by().values_list("negoce_name",flat=True)
    recommended_prices = negoces2.objects.order_by().values_list("recommended_price",flat=True)
    sells = negoces2.objects.order_by().values_list("sell",flat=True)
    ratings = negoces2.objects.order_by().values_list("rating",flat=True)
    growths = negoces2.objects.order_by().values_list("growth",flat=True)
    margins = negoces2.objects.order_by().values_list("margin",flat=True)
    quantities = negoces2.objects.order_by().values_list("quantity",flat=True)
    types_english = negoces2.objects.order_by().values_list("a_type_english",flat=True)
    types_chinese = negoces2.objects.order_by().values_list("a_type_chinese",flat=True)
    cheapest_percents = negoces2.objects.order_by().values_list("cheapest_percent",flat=True) 

    percents = [str(i)+"%" for i in range(2,6) if str(i)+"%"!=str(cheapest_percents)]

    values = zip(wines,prices,dates,years,regions_english,regions_chinese,formats,markup_prices,
                 markup_percentiles,vendors_english,vendors_chinese,countries_english,countries_chinese,
                 ws_merchants,ws_prices,negoce_names,recommended_prices,sells,ratings,growths,margins,
                 quantities,types_english,types_chinese,cheapest_percents)
    return render(request,'negocestable.html',{"values":values,"percents":percents})

