from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from .forms import UploadFileForm, handle_uploaded_file,chuncks
from .models import synctable
import logging
import sys,json,ast,time
from apiAccess import openAPI,Main
from wineClass import handleNegoceFile,handleDictionary
import pandas as pd
import ast
# Create your views here. apiAccess


logging.basicConfig(filename="logfile.txt")
stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)

def home(request):
    return render(request,'home.html')

@login_required
def logged_in(request):
    #results = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'])
            #__init__(self,path,production_env,location='/home/ubuntu/app/data/',negoces=negoces_dictionary)
            try:
                msg_obj = handleNegoceFile(path,True)
                msg = msg_obj.getContent()
            except Exception as e:
                print e
                msg = {}
                msg["error"] = "The file doesn't have the correct format: {0}".format(e)
 
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
                Vendors = msg["vendors"]
                Types = msg["types"]
                error = None
            else:
                Wines = None
                Prices = None
                Years = None
                Regions = None
                error = msg["error"]
            if Wines and Prices and Years:
                results = zip(Wines,Prices,Years,Regions,Formats,PricesMarkup,Percentiles,Negoces,Quantities,Vendors,Types)
            else:
                results = None
            return render(request,'upload.html', {"Results":results,"error":error})
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
    return render(request, 'logged_in.html', {'form': form})

@login_required
def upload_dictionary(request):
    #results = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'])
            results = None
            error = None
            try:
                msg_obj = handleDictionary(path,False)
                msg = msg_obj.getDictionaryData()
                WinesID = [msg['Item ID'][item] for item in msg['Item ID'].keys()]
                Ratings = [msg['Ratings'][item] for item in msg['Ratings'].keys()]
                TypeEnglish = [msg['Type (English)'][item] for item in msg['Type (English)'].keys()]
                WineEnglish = [msg['Wine (English)'][item] for item in msg['Wine (English)'].keys()]
                Vintage = [msg['Vintage'][item] for item in msg['Vintage'].keys()]
                CountryEnglish = [msg['Country (English)'][item] for item in msg['Country (English)'].keys()]
                WineChinese = [msg['Wine (Chinese)'][item] for item in msg['Wine (Chinese)'].keys()]
                RegionEnglish = [msg['Region (English)'][item] for item in msg['Region (English)'].keys()]
                Growth = [msg['Growth'][item] for item in msg['Growth'].keys()]
                TypeChinese = [msg['Type (Chinese)'][item] for item in msg['Type (Chinese)'].keys()]
                RegionChinese = [msg['Region (Chinese)'][item] for item in msg['Region (Chinese)'].keys()]
                VendorChinese = [msg['Vendor (Chinese)'][item] for item in msg['Vendor (Chinese)'].keys()]
                CountryChinese = [msg['Country (Chinese)'][item] for item in msg['Country (Chinese)'].keys()]
                VendorEnglish = [msg['Vendor (English)'][item] for item in msg['Vendor (English)'].keys()]

                results = zip(WinesID,Ratings,TypeEnglish,WineEnglish,Vintage,CountryEnglish,WineChinese,RegionEnglish,Growth,
                              TypeChinese,RegionChinese,VendorChinese,CountryChinese,VendorEnglish)
            except Exception as e:
                print e
                string = msg.keys()
                string = " ".join(string)
                error = "The file doesn't have the correct format: {0}. The file has following fields: {1}".format(e,string)
                
            return render(request,'uploaded_dictionary.html', {"Results":results,"error":error})
        else:
            form = UploadFileForm()
            form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    else:
        form = UploadFileForm()
        form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    print "logged"
    form = UploadFileForm()
    form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    return render(request, 'page_to_upload_dictionary.html', {'form': form})

@login_required
def upload_smallerfile(request):
    msg = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'])
            results = None
            error = None
            try:
                msg_obj = handleDictionary(path,True)
                msg = msg_obj.getConvertedFileData()
                WinesID = [msg['item id'][item] for item in msg['item id'].keys()]
                Wines = [msg['wine'][item] for item in msg['wine'].keys()]
                Costs = [msg['price'][item] for item in msg['price'].keys()]
                Vintages = [msg['year'][item] for item in msg['year'].keys()]
                Ratings = [msg['rating'][item] for item in msg['rating'].keys()]
                TypeEnglish = [msg['type english'][item] for item in msg['type english'].keys()]
                TypeChinese = [msg['type chinese'][item] for item in msg['type chinese'].keys()]
                Formats = [msg['format'][item] for item in msg['format'].keys()]
                VendorEnglish = [msg['vendor english'][item] for item in msg['vendor english'].keys()]
                VendorChinese = [msg['vendor chinese'][item] for item in msg['vendor chinese'].keys()]
                RegionEnglish = [msg['region english'][item] for item in msg['region english'].keys()]
                RegionChinese = [msg['region chinese'][item] for item in msg['region chinese'].keys()]
                Quantities = [msg['qty'][item] for item in msg['qty'].keys()]
                Negoces = [msg['negoce'][item] for item in msg['negoce'].keys()]
                CountryEnglish = [msg['country english'][item] for item in msg['country english'].keys()]
                CountryChinese = [msg['country chinese'][item] for item in msg['country chinese'].keys()]
                Growth = [msg['growth'][item] for item in msg['growth'].keys()]

                results = zip(WinesID,Wines,Costs,Vintages,Ratings,TypeEnglish,TypeChinese,Formats,VendorEnglish,
                              VendorChinese,RegionEnglish,RegionChinese,Quantities,Negoces,CountryEnglish,
                              CountryChinese,Growth)
            except Exception as e:
                print e
                msg = {}
                results = []
                string = msg.keys()
                string = " ".join(string)
                error = "The file doesn't have the correct format: {0}. The file has following fields: {1}".format(e,string)
                
            return render(request,'uploaded_smaller_file.html', {"Results":results,"error":error,"msg":json.dumps(msg)})
        else:
            form = UploadFileForm()
            form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    else:
        form = UploadFileForm()
        form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    print "logged"
    form = UploadFileForm()
    form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    return render(request, 'page_to_upload_smaller_file.html', {'form': form})
def testingPage(request):
    return render(request,'testing_page.html')
def upload(request):
    return render(request,'upload.html')
def uploaded_dictionary(request):
    return render(request,'uploaded_dictionary.html')   
def uploaded_smallerfile(request):
    res = "nan"
    if request.method == 'POST':
        path = r"/home/ubuntu/app/data/export3.csv"
        data = request.POST.get('alldata')
        try:
            content = request.POST.get('alldata')
            content = json.loads(content.encode("utf-8"))
            df = pd.DataFrame.from_dict(content) 
           
            df.to_csv(path,encoding="utf-8")
            data = open(path,"r").read()
            response = HttpResponse(data,content_type='text/csv')
            res = "works"
            response['Content-Disposition'] = 'attachment; filename="export3.csv"'
            return response
        except Exception as e:
            failure = {}
            failure["error"] = e
            failure["type"] = type(content)
            failure["dict"] = content
            return render(request, 'page_to_upload_smaller_file.html', {"failure":failure})
    return render(request,'uploaded_smallerfile.html',{"nan":res}) 

@login_required
def wine(request):
    values = None
    wine = "wine"
    year = "year"
    msg = None
    if request.method == "POST":
        wine = request.POST.get('wine')
        year = request.POST.get('year')   
        obj_wine = openAPI(year,"A",wine)
        merchants, prices, bottles, links = obj_wine.apiData()
        if len(merchants) == 0:
            wine = "wine"
            year = "year"
        else:
            msg = "data"
            values = zip(merchants,prices,bottles,links)
        return render(request,'wine.html',{"values":values,"wine":wine,"year":year,"msg":msg})
    return render(request,'wine.html',{"values":values,"wine":wine,"year":year,"msg":msg})

@login_required
def getWine(request):
    values = None
    wine = "wine"
    year = "year"
    msg = None
    if request.method == "POST":
        wine = request.POST.get('wine')
        year = request.POST.get('year')
        obj_wine = openAPI(year,"A",wine)
        merchants, prices, bottles, links = obj_wine.apiData()
        if len(merchants) == 0:
            wine = "wine"
            year = "year"
        else:
            msg = "data"
            values = zip(merchants,prices,bottles,links)
        return render(request,'getwine.html',{"values":values,"wine":wine,"year":year,"msg":msg})
    return render(request,'getwine.html',{"values":values,"wine":wine,"year":year,"msg":msg})


def results(request):
    if request.method == 'POST':
        query_var = request.POST.get("django_file")
        results = ast.literal_eval(query_var)
        mode = "A"
        sender = {}
        dictionary_wines = {}
        wines = []
        prices = []
        years = []
        regions = []        
        formats = []
        markups = []
        percentiles = []
        negoces = []
        quantities = []
        vendors = []
        types = []

        bigList = []

        for wine,price,year,region,format,markup,percentile,negoce,quantity,vendor,a_type in results:
            wines.append(wine)
            prices.append(price)
            years.append(year)
            regions.append(region)
            formats.append(format)
            markups.append(markup)
            percentiles.append(percentile)
            negoces.append(negoce)
            quantities.append(quantity)
            vendors.append(vendor)
            types.append(a_type)

        sender["wines"] = wines
        sender["years"] = years
        sender["prices"] = prices
        sender["regions"] = regions
        sender["formats"] = formats
        sender["markups"] = markups     
        sender["percentiles"] = percentiles
        sender["negoces"] = negoces
        sender["quantities"] = quantities
        sender["vendors"] = vendors
        sender["types"] = types

        dictionary = Main(sender)
 
        print dictionary
        try:
            synctable.objects.all().delete()
        except Exception as e:
            print e

        for each_result in dictionary:
            dic = {}
            dic["Wines"] = dictionary[each_result]["wine"]
            dic["Prices"] = dictionary[each_result]["price"]
            dic["Years"] = dictionary[each_result]["year"]
            dic["Regions"] = dictionary[each_result]["region"]
            dic["Formats"] = dictionary[each_result]["format"]
            dic["Merchants"] = dictionary[each_result]["merchants"]
            dic["PricesMin"] = dictionary[each_result]["pricesmin"]
            dic["Bottles"] = dictionary[each_result]["bottles"]
            dic["Links"] = dictionary[each_result]["links"] 
            dic["Markups"] = dictionary[each_result]["markup"]
            dic["Percentiles"] = dictionary[each_result]["percentile"] 
            dic["Recommended"] = dictionary[each_result]["recommended"] #["recommended"]
            dic["Sell"] = dictionary[each_result]["sell"]
            dic["Margin"] = dictionary[each_result]["margin"]
            dic["Quantity"] = dictionary[each_result]["quantity"]
            dic["Type"] = dictionary[each_result]["type"]
            dic["Vendor"] = dictionary[each_result]["vendor"]
            bigList.append(dic) 

            SyncMerchants = ", ".join(dic["Merchants"])
            Negoce = dictionary[each_result]["negoce"]
            uploaded_wine = synctable(wine=dic["Wines"],price=dic["Prices"],year=dic["Years"],region=dic["Regions"],
                                      format=dic["Formats"],markup_price=dic["Markups"],markup_percentile=dic["Percentiles"],
                                      ws_merchants=SyncMerchants,ws_price=dic["PricesMin"][0],recommended_price=dic["Recommended"],
                                      margin=dic["Margin"],sell=dic["Sell"],negoce=Negoce,quantity=dic["Quantity"],
                                      a_type=dic["Type"],vendor=dic["Vendor"])
            uploaded_wine.save()
        FinalDictionary = {}
        FinalDictionary["Raw"] = results
        FinalDictionary["Result"] = bigList
        FinalDictionary["Wines"] = wines
        FinalDictionary["Prices"] = prices
        FinalDictionary["Years"] = years
        FinalDictionary["Regions"] = regions
        FinalDictionary["Formats"] = formats
        FinalDictionary["Markups"] = markups
        FinalDictionary["Percentiles"] = percentiles
        FinalDictionary["Negoces"] = negoces       
        FinalDictionary["Dict"] = dictionary
    return HttpResponse(json.dumps(FinalDictionary),content_type="application/json")

@login_required
def download2(request):
    path = r"/home/ubuntu/app/data/export2.csv"
    df = pd.DataFrame()

    wines = synctable.objects.order_by().values_list("wine",flat=True)
    prices = synctable.objects.order_by().values_list("price",flat=True)
    years = synctable.objects.order_by().values_list("year",flat=True)
    regions = synctable.objects.order_by().values_list("region",flat=True)
    formats = synctable.objects.order_by().values_list("format",flat=True)
    markup_prices = synctable.objects.order_by().values_list("markup_price",flat=True)
    markup_percentiles = synctable.objects.order_by().values_list("markup_percentile",flat=True)
    ws_merchants = synctable.objects.order_by().values_list("ws_merchants",flat=True)
    ws_prices = synctable.objects.order_by().values_list("ws_price",flat=True)
    negoce_names = synctable.objects.order_by().values_list("negoce",flat=True)
    recommended_prices = synctable.objects.order_by().values_list("recommended_price",flat=True)
    sells = synctable.objects.order_by().values_list("sell",flat=True)
    margins = synctable.objects.order_by().values_list("margin",flat=True)
    quantities = negoces.objects.order_by().values_list("quantity",flat=True)
    types = negoces.objects.order_by().values_list("a_type",flat=True)
    vendors = negoces.objects.order_by().values_list("vendor",flat=True)

    df["Wine"] = wines
    df["Price"] = prices
    
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
    response['Content-Disposition'] = 'attachment; filename="export2.csv"'
    
    return response



@login_required
def upload_dictionary_copy(request):
    #results = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'])
            results = None
            error = None
            try:
                msg_obj = handleDictionary(path,False)
                msg = msg_obj.getDictionaryData()
                WinesID = [msg['Item ID'][item] for item in msg['Item ID'].keys()]
                Ratings = [msg['Ratings'][item] for item in msg['Ratings'].keys()]
                TypeEnglish = [msg['Type (English)'][item] for item in msg['Type (English)'].keys()]
                WineEnglish = [msg['Wine (English)'][item] for item in msg['Wine (English)'].keys()]
                Vintage = [msg['Vintage'][item] for item in msg['Vintage'].keys()]
                CountryEnglish = [msg['Country (English)'][item] for item in msg['Country (English)'].keys()]
                WineChinese = [msg['Wine (Chinese)'][item] for item in msg['Wine (Chinese)'].keys()]
                RegionEnglish = [msg['Region (English)'][item] for item in msg['Region (English)'].keys()]
                Growth = [msg['Growth'][item] for item in msg['Growth'].keys()]
                TypeChinese = [msg['Type (Chinese)'][item] for item in msg['Type (Chinese)'].keys()]
                RegionChinese = [msg['Region (Chinese)'][item] for item in msg['Region (Chinese)'].keys()]
                VendorChinese = [msg['Vendor (Chinese)'][item] for item in msg['Vendor (Chinese)'].keys()]
                CountryChinese = [msg['Country (Chinese)'][item] for item in msg['Country (Chinese)'].keys()]
                VendorEnglish = [msg['Vendor (English)'][item] for item in msg['Vendor (English)'].keys()]

                results = zip(WinesID,Ratings,TypeEnglish,WineEnglish,Vintage,CountryEnglish,WineChinese,RegionEnglish,Growth,
                              TypeChinese,RegionChinese,VendorChinese,CountryChinese,VendorEnglish)
            except Exception as e:
                print e
                string = msg.keys()
                string = " ".join(string)
                error = "The file doesn't have the correct format: {0}. The file has following fields: {1}".format(e,string)
                
            return render(request,'uploaded_dictionary.html', {"Results":results,"error":error})
        else:
            form = UploadFileForm()
            form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    else:
        form = UploadFileForm()
        form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    print "logged"
    form = UploadFileForm()
    form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    return render(request, 'page_to_upload_dictionary_copy.html', {'form': form})

@login_required
def upload_smallerfile_copy(request):
    msg = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'])
            results = None
            error = None
            try:
                msg_obj = handleDictionary(path,True)
                msg = msg_obj.getConvertedFileData()
                WinesID = [msg['item id'][item] for item in msg['item id'].keys()]
                Wines = [msg['wine'][item] for item in msg['wine'].keys()]
                Costs = [msg['price'][item] for item in msg['price'].keys()]
                Vintages = [msg['year'][item] for item in msg['year'].keys()]
                Ratings = [msg['rating'][item] for item in msg['rating'].keys()]
                TypeEnglish = [msg['type english'][item] for item in msg['type english'].keys()]
                TypeChinese = [msg['type chinese'][item] for item in msg['type chinese'].keys()]
                Formats = [msg['format'][item] for item in msg['format'].keys()]
                VendorEnglish = [msg['vendor english'][item] for item in msg['vendor english'].keys()]
                VendorChinese = [msg['vendor chinese'][item] for item in msg['vendor chinese'].keys()]
                RegionEnglish = [msg['region english'][item] for item in msg['region english'].keys()]
                RegionChinese = [msg['region chinese'][item] for item in msg['region chinese'].keys()]
                Quantities = [msg['qty'][item] for item in msg['qty'].keys()]
                Negoces = [msg['negoce'][item] for item in msg['negoce'].keys()]
                CountryEnglish = [msg['country english'][item] for item in msg['country english'].keys()]
                CountryChinese = [msg['country chinese'][item] for item in msg['country chinese'].keys()]
                Growth = [msg['growth'][item] for item in msg['growth'].keys()]

                results = zip(WinesID,Wines,Costs,Vintages,Ratings,TypeEnglish,TypeChinese,Formats,VendorEnglish,
                              VendorChinese,RegionEnglish,RegionChinese,Quantities,Negoces,CountryEnglish,
                              CountryChinese,Growth)
            except Exception as e:
                print e
                msg = {}
                results = []
                string = msg.keys()
                string = " ".join(string)
                error = "The file doesn't have the correct format: {0}. The file has following fields: {1}".format(e,string)
                
            return render(request,'uploaded_smaller_file.html', {"Results":results,"error":error,"msg":json.dumps(msg)})
        else:
            form = UploadFileForm()
            form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    else:
        form = UploadFileForm()
        form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    print "logged"
    form = UploadFileForm()
    form.fields["file"].widget.attrs = {"class":"custom-file-input"}
    return render(request, 'page_to_upload_smaller_file_copy.html', {'form': form})

def error404(request):
    if request.user.is_authenticated():
        return render(request,'404.html')
    else:
        return HttpResponseRedirect('/login')

@login_required
def sync(request):
    values = None
    wine = "wine"
    year = "year"
    msg = None
    if request.method == "POST":
        wine = request.POST.get('wine')
        year = request.POST.get('year')
        obj_wine = openAPI(year,"A",wine)
        merchants, prices, bottles, links = obj_wine.apiData()
        if len(merchants) == 0:
            wine = "wine"
            year = "year"
        else:
            msg = "data"
            values = zip(merchants,prices,bottles,links)
        return render(request,'syncdb.html',{"values":values,"wine":wine,"year":year,"msg":msg})
    return render(request,'syncdb.html',{"values":values,"wine":wine,"year":year,"msg":msg})
