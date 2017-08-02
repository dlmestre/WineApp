from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from .forms import UploadFileForm, handle_uploaded_file,chuncks
from .models import synctable,dictionary
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

@login_required
def upload_dictionary_copy(request):
    #results = {}
    
    try:
        filenames = dictionary.objects.order_by().values_list("filename",flat=True)
        uploadingdates = dictionary.objects.order_by().values_list("uploadingdate",flat=True)
        wineids = dictionary.objects.order_by().values_list("wineid",flat=True)
        ratings = dictionary.objects.order_by().values_list("rating",flat=True)
        vintages = dictionary.objects.order_by().values_list("vintage",flat=True)
        growth = dictionary.objects.order_by().values_list("growth",flat=True)
        typeenglishs = dictionary.objects.order_by().values_list("typeenglish",flat=True)
        wineenglishs = dictionary.objects.order_by().values_list("wineenglish",flat=True)
        countryenglishs = dictionary.objects.order_by().values_list("countryenglish",flat=True)
        regionenglishs = dictionary.objects.order_by().values_list("regionenglish",flat=True)
        vendorenglishs = dictionary.objects.order_by().values_list("vendorenglish",flat=True)
        typechineses = dictionary.objects.order_by().values_list("typechinese",flat=True)
        winechineses = dictionary.objects.order_by().values_list("winechinese",flat=True)
        countrychineses = dictionary.objects.order_by().values_list("countrychinese",flat=True)
        regionchineses = dictionary.objects.order_by().values_list("regionchinese",flat=True)
        vendorchineses = dictionary.objects.order_by().values_list("vendorchinese",flat=True)

        values = zip(filenames,uploadingdates,wineids,ratings,vintages,growth,typeenglishs,wineenglishs,countryenglishs,
                     regionenglishs,vendorenglishs,typechineses,winechineses,countrychineses,regionchineses,vendorchineses)
    except Exception:
        values = None
    if request.method == 'POST':
        requested_file = request.FILES['dictionaryfile']
        try:
            filename = requested_file.name
        except Exception:
            filename = "N/A"
        path = handle_uploaded_file(requested_file)
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
            try:
                dictionary.objects.all().delete()
            except Exception:
                pass
            for wineid,rating,typeenglish,wineenglish,vintage,countryenglish,winechinese,regionenglish,growth, \
                typechinese,regionchinese,vendorchinese,countrychinese,vendorenglish in results:
                dictionary_record = dictionary(filename=filename,wineid=wineid,rating=rating,vintage=vintage,
                                               growth=growth,typeenglish=typeenglish,wineenglish=wineenglish,
                                               countryenglish=countryenglish,regionenglish=regionenglish,
                                               vendorenglish=vendorenglish,typechinese=typechinese,
                                               winechinese=winechinese,countrychinese=countrychinese,
                                               regionchinese=regionchinese,vendorchinese=vendorchinese)
                dictionary_record.save()
        except Exception as e:
            print e
            string = msg.keys()
            string = " ".join(string)
            error = "The file doesn't have the correct format: {0}. The file has following fields: {1}".format(e,string)
                
        return render(request,'uploaded_dictionary_copy.html', {"Results":results,"error":error})
    else:
        return render(request, 'page_to_upload_dictionary_copy.html',{"values":values})

@login_required
def upload_smallerfile_copy(request):
    msg = {}
    if request.method == 'POST':
        
        path = handle_uploaded_file(request.FILES['negocefile'])
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
                
        return render(request,'uploaded_smaller_file_copy.html', {"Results":results,"error":error,"msg":json.dumps(msg)})
    print "logged"
    return render(request, 'page_to_upload_smaller_file_copy.html')

def uploaded_dictionary_copy(request):
    return render(request,'uploaded_dictionary_copy.html')   
def uploaded_smallerfile_copy(request):
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
            return render(request, 'page_to_upload_smaller_file_copy.html', {"failure":failure})
    return render(request,'uploaded_smallerfile_copy.html',{"nan":res}) 


