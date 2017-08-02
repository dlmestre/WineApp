from django import forms
import pandas as pd
import re
from yahoo_finance import Currency
from .models import eurhkd, usdhkd, markup

def cleaner(region):
    if type(region) == str:
        region = region.replace("AOC","").replace("BLANC","").replace("ROUGE","").replace("RGE","").strip()
        return region.lower().title()
    else:
        return region

def check(value,prices_list,rates_list):
    prices_list = list(prices_list)
    rates_list = list(rates_list)
    for i in range(len(prices_list)):
        if float(value) < float(prices_list[i]):
            if i > 0:
                rate = rates_list[i-1].replace("%","").strip()
                return float(rate)/100.0,rates_list[i-1]
            else:
                rate = rates_list[0].replace("%","").strip()
                return float(rate)/100.0,rates_list[0]
            break
    rate = rates_list[-1].replace("%","").strip()
    return float(rate)/100.0,rates_list[-1]

def currencies(currency):
    if currency == "euro":
        return Currency('EURHKD')
    elif currency == "dollar":
        return Currency('USDHKD')
def parse_df(names,prices):
    years = []
    all_names = []
    all_prices = []

    for name,price in zip(names,prices):
        name = name.split("(")[0]
        try:
            match = re.search('\d{4}',name)
            year = match.group(0)
        except Exception as e:
            year = None
            pass
        if year:
            name = name.replace(year,"")
            all_names.append(name)
            all_prices.append(price)
            years.append(year)
    return years,all_names,all_prices

def handle_uploaded_file(f,database=False):
    named = f.name
    if database:
        pos = '/home/ubuntu/app/dbfiles/'
    else:
        pos = '/home/ubuntu/app/data/'
    path = pos+str(named)
    with open(path,'w') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    return path

def handle_uploaded_file2(f,database=False):
    named = f.name
    if database:
        pos = '/home/ubuntu/app/dbfiles/'
    else:
        pos = '/home/ubuntu/app/data/'
    path = pos+str(named)
    msg = {}
    msg["error"] = []
    wines_dictionary = {}
    wines_dictionary['1/2 bt.'] = "37,5cl"
    wines_dictionary['bt.'] = "75cl"
    wines_dictionary['d.mag.'] = "3,0L"
    wines_dictionary['imp\xc3\xa9.'] = "6,0L"
    wines_dictionary['j\xc3\xa9ro.'] = "5.0L"
    wines_dictionary['mag.'] = "1,5L"
    wines_dictionary['balt.'] = "12,0L"

    #rate = markup.objects.all()
    markup_prices = markup.objects.order_by().values_list("price",flat=True)
    markups = markup.objects.order_by().values_list("mark",flat=True)
    with open(path,'w') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    if path.endswith('csv'):
        try:
            df = pd.read_csv(path)
            Columns = df.columns
            if "Cost" in Columns and "Wine" in Columns and "Vintage" in Columns:
                msg["prices"] = df["Cost"].tolist()
                msg["wines"] = df["Wine"].tolist()
                msg["years"] = df["Vintage"].tolist()
                msg["regions"] = df["Region"].tolist()
                msg["formats"] = df["Format"].tolist()
            elif "Item Name" in Columns and "Trade" in Columns:
                names = df["Item Name"].tolist()
                prices = df["Trade"].tolist()
                years,all_names,all_prices = parse_df(names,prices)
                msg["prices"] = all_prices
                msg["wines"] = all_names
                msg["years"] = years
                msg["regions"] = [""]*len(years)
                msg["formats"] = df["Format"].tolist()
            else:
                msg["error"].append("csv doesn't have the expected format")
        except Exception as e:
            print e
            msg["error"].append("csv doesn't have the expected format")
    else:
        try:
            filename = named.split(".")[0]
            df_xls = pd.read_excel(path)
            df_xls.to_csv(pos+filename+".csv",encoding="utf-8")
            df_csv = pd.read_csv(pos+filename+".csv")

            try:
                df_csv.columns = ["appellation","produit","classement","millesime","PV_mini","dispo",
                                  "centil","parker","w"]
                csv_format = "Balande" 
            except Exception as e:
                print e
                df_csv.columns = ["Commune","ranking","Year","wine","Size","parker","price","Notes",
                                  "Year 2","wine (second / white)","Bottle","price 2","empty","parker 2"]
                csv_format = "Twins"
            if csv_format == "Balande":
                rate = eurhkd.objects.latest("value").value
                names = df_csv["produit"].tolist()
                prices = []
                for price in df_csv["PV_mini"].tolist():
                    try:
                        #hkdprice = "{0:.2f}".format(float(price)*float(rate))
                        hkdprice = round(float(price)*float(rate))
                        prices.append(hkdprice)
                    except Exception as e:
                        prices.append(price)  
                #prices = [float(price)*float(rate) for price in prices]
                years = df_csv["millesime"].tolist()
                regions = df_csv["appellation"].tolist()
                regions = [cleaner(region) for region in regions]
                formats = []
                for content in df_csv["centil"].tolist():
                    try:
                        formats.append(wines_dictionary[str(content).lower()])
                    except Exception as e:
                        formats.append(content)
            elif csv_format == "Twins":
                rate = eurhkd.objects.latest("value").value
                names = df_csv["wine"].tolist()
                prices = []
                for price in df_csv["price"].tolist():
                    try:
                        #hkdprice = "{0:.2f}".format(float(price)*float(rate))
                        hkdprice = round(float(price)*float(rate))
                        prices.append(hkdprice)
                    except Exception as e:
                        prices.append(price)
                #prices = [float(price)*float(rate) for price in prices]
                years = df_csv["Year"].tolist()
                regions = df_csv["Commune"].tolist()
                formats = df_csv["Size"].tolist()
            all_years = []
            all_names = []
            all_prices = []
            all_regions = []
            all_formats = []
            for name,price,year,region,a_format in zip(names,prices,years,regions,formats):
                try:
                    match = re.search('\d{4}',year)
                    year = match.group(0)
                except Exception as e:
                    year = None
                if year:
                    all_names.append(name)
                    all_prices.append(price)
                    all_years.append(year)
                    all_regions.append(region)
                    all_formats.append(a_format)
            msg["prices"] = all_prices
            msg["wines"] = all_names
            msg["years"] = all_years
            msg["regions"] = all_regions
            msg["formats"] = all_formats
            if csv_format == "Balande":
                msg["negoces"] = ["Balande"] * len(all_prices)
            elif csv_format == "Twins":
                msg["negoces"] = ["Twins"] * len(all_prices)

        except Exception as e:
            print e
            msg["error"].append("File uploaded doesn't have the expected format: {0}".format(e))
    try:
        prices_after_markup = []
        percentiles = []
        for price in msg["prices"]:
            #check(value,prices_list,rates_list)
            rate,percentile = check(price,markup_prices,markups)
            price_after_markup = float(price) * (1 + rate)
            #price_after_markup = "{0:.2f}".format(price_after_markup)
            price_after_markup = round(price_after_markup)
            prices_after_markup.append(price_after_markup)
            percentiles.append(percentile)
        msg["markup prices"] = prices_after_markup
        msg["percentiles"] = percentiles
    except Exception as e:
        print e
    return msg

def access_api():
    return "code"

def chuncks(l,n):
    avg = len(l)/float(n)
    out = []
    last = 0.0
    
    while last < len(l):
        out.append(l[int(last):int(last+avg)])
        last += avg
    return out

class UploadFileForm(forms.Form):
    file = forms.FileField(max_length=150)

