import json
import pandas as pd
import lxml
import urllib
from xml.etree import ElementTree as ET
from .forms import chuncks
from threading import Thread

class openAPI:
    def __init__(self,year,mode,wine):
        self.password = "cuvees"
        self.year = year
        self.mode = mode
        self.wine = wine
        self.url = self.getUrl()
    def getUrl(self):
        url_main = r"http://api.wine-searcher.com/wine-select-api.lml?Xkey="
        url_main = url_main + self.password + "&Xkeyword_mode=" + str(self.mode)
        url_main = url_main + "&Xwinename=" + str(self.wine) + "&Xvintage=" + str(self.year)
        return url_main + "&Xlocation=hong+kong&Xcurrencycode=hkd"
    def apiData(self):
        root = ET.parse(urllib.urlopen(self.url)).getroot()
        print self.url
        merchants = []
        prices = []
        bottles = []
        links = []
        for name in root.findall("./wines/wine"):
            for i in name:
                if i.tag == "link":
                    links.append(i.text)
                if i.tag == "merchant":
                    merchants.append(i.text)
                if i.tag == "bottle-size":
                    bottles.append(i.text)
                if i.tag == "price":
                    prices.append(i.text)
        return merchants, prices, bottles, links
    def getData(self):
        root = ET.parse(urllib.urlopen(self.url)).getroot()
        merchants = []
        prices = []
        bottles = []
        links = []
        for name in root.findall("./wines/wine"):
            for i in name:
                if i.tag == "link":
                    links.append(i.text)
                if i.tag == "merchant":
                    merchants.append(i.text)
                if i.tag == "bottle-size":
                    bottles.append(i.text)
                if i.tag == "price":
                    prices.append(i.text)
        tmp_links = []
        tmp_merchants = []
        tmp_bottles = []
        tmp_prices = []
        for link,merchant,bottle,price in zip(links,merchants,bottles,prices):
            if bottle == "Bottle":
                if "Cuvees.com" not in merchant and "Aberdeen Fine Wine" not in merchant:
                    tmp_links.append(link)
                    tmp_merchants.append(merchant)
                    tmp_bottles.append(bottle)
                    tmp_prices.append(price)
        
        links = tmp_links
        merchantes = tmp_merchants
        bottles = tmp_bottles
        prices = tmp_prices
        try:
            prices = [float(price.replace(",","")) for price in prices]
            min_price = min(prices)
            indexes = [idx for idx,val in enumerate(prices) if val == min_price]
            merchants_min = [merchants[idx] for idx in indexes]
            prices_min = [prices[idx] for idx in indexes]
            bottles_min = [bottles[idx] for idx in indexes]
            links_min = [links[idx] for idx in indexes]
        except Exception as e:
            merchants_min = None 
            prices_min = None
            bottles_min = None 
            links_min = None                 
        return merchants_min, prices_min, bottles_min, links_min

class APIThread:
    def __init__(self):
        self.wine_dictionary = {}
    def getDictionary(self):
        return self.wine_dictionary
    def getRecommendedPrice(self,markup_price,ws_price):
        ws_price = float(ws_price)
        es_price_2_percent = ws_price * 0.98
        markup_price = float(markup_price)
        if ws_price < markup_price:
            #price = es_price_2_percent
            price = markup_price
        else:
            if es_price_2_percent > markup_price:
                price = es_price_2_percent
            else:
                price = markup_price
        #return "{0:.2f}".format(price)
        return round(price)
    def getMarginHKD(self,recommended_price,cost):
        #return "{0:.2f}".format(float(recommended_price) - float(cost))
        return round(float(recommended_price) - float(cost))
    def getSell(self,lowest_ws_price,recommended_price):
        if float(lowest_ws_price) > float(recommended_price):
            return "Yes"
        else:
            return "No"
    def getThread(self,wines,years,prices,regions,formats,markups,percentiles,negoces,quantities,vendors,types):
        try:
            print wines,years
            for wine,year,price,region,a_format,markup,percentile,negoce,quantity,vendor,a_type \
            in zip(wines,years,prices,regions,formats,markups,percentiles,negoces,quantities,vendors,types):
                obj_wine = openAPI(year,"A",wine)
                merchants_min, prices_min, bottles_min, links_min = obj_wine.getData()
                string = str(year) + " " + str(wine)
                if merchants_min and prices_min and bottles_min and links_min:
                    self.wine_dictionary[string] = {}
                    self.wine_dictionary[string]["merchants"] = merchants_min
                    self.wine_dictionary[string]["pricesmin"] = prices_min
                    self.wine_dictionary[string]["bottles"] = bottles_min
                    self.wine_dictionary[string]["links"] = links_min
                    self.wine_dictionary[string]["wine"] = wine
                    self.wine_dictionary[string]["year"] = year
                    self.wine_dictionary[string]["price"] = price
                    self.wine_dictionary[string]["region"] = region
                    self.wine_dictionary[string]["format"] = a_format
                    self.wine_dictionary[string]["markup"] = markup
                    self.wine_dictionary[string]["percentile"] = percentile
                    self.wine_dictionary[string]["negoce"] = negoce
                    self.wine_dictionary[string]["quantity"] = quantity
                    self.wine_dictionary[string]["vendor"] = vendor
                    self.wine_dictionary[string]["type"] = a_type
                 
                    recommendedPrice = self.getRecommendedPrice(markup,prices_min[0])
                    marginHKD = self.getMarginHKD(recommendedPrice,price)
                    sell = self.getSell(prices_min[0],recommendedPrice)

                    self.wine_dictionary[string]["recommended"] = recommendedPrice
                    self.wine_dictionary[string]["margin"] = marginHKD
                    self.wine_dictionary[string]["sell"] = sell
        except Exception as e:
            print e

def Main(msg):
    
    wines = msg["wines"]
    years = msg["years"]
    prices = msg["prices"]
    regions = msg["regions"]
    formats = msg["formats"]
    markups = msg["markups"]
    percentiles = msg["percentiles"]
    negoces = msg["negoces"]
    quantities = msg["quantities"]
    vendors = msg["vendors"]
    types = msg["types"]

    tmp_wines = []
    tmp_years = []
    tmp_prices = []
    tmp_regions = []
    tmp_formats = []
    tmp_markups = []
    tmp_percentiles = []
    tmp_negoces = []
    tmp_quantities = []
    tmp_vendors = []
    tmp_types = []

    for wine,year,price,region,a_format,markup,percentile,negoce,quantity,vendor,a_type \
    in zip(wines,years,prices,regions,formats,markups,percentiles,negoces,quantities,vendors,types):
        if a_format == "75cl" or a_format == "750ML" or a_format == "750ml":
            tmp_wines.append(wine)
            tmp_years.append(year)
            tmp_prices.append(price)
            tmp_regions.append(region)
            tmp_formats.append(a_format)
            tmp_markups.append(markup)
            tmp_percentiles.append(percentile)
            tmp_negoces.append(negoce)
            tmp_quantities.append(quantity)
            tmp_vendors.append(vendor)
            tmp_types.append(a_type)
    wines = tmp_wines
    years = tmp_years
    prices = tmp_prices
    regions = tmp_regions
    formats = tmp_formats
    markups = tmp_markups
    percentiles = tmp_percentiles
    negoces = tmp_negoces
    quantities = tmp_quantities
    vendors = tmp_vendors
    types = tmp_types
    if len(wines) < 50:
        n = 1
    else:    
        n = 10        

    wines_list = chuncks(wines,n)
    years_list = chuncks(years,n)
    prices_list = chuncks(prices,n)    
    regions_list = chuncks(regions,n)
    formats_list = chuncks(formats,n)
    markups_list = chuncks(markups,n)
    percentiles_list = chuncks(percentiles,n)
    negoces_list = chuncks(negoces,n)
    quantities_list = chuncks(quantities,n)
    vendors_list = chuncks(vendors,n)
    types_list = chuncks(types,n)

    threads_running = []

    apiThread_obj = APIThread()
    for each_wine_list,each_year_list,each_price_list,each_region_list,each_format_list,each_markup_list,each_percentile_list,each_negoce_list, \
    each_quantity_list,each_vendor_list,each_type_list \
    in zip(wines_list,years_list,prices_list,regions_list,formats_list,markups_list,percentiles_list,negoces_list,
           quantities_list,vendors_list,types_list):
        t = Thread(target=apiThread_obj.getThread,
                   args=(each_wine_list,each_year_list,each_price_list,each_region_list,each_format_list,
                         each_markup_list,each_percentile_list,each_negoce_list,each_quantity_list,each_vendor_list,each_type_list))
        threads_running.append(t)
    for t in threads_running:
        t.start()
    for t in threads_running:
        t.join()
    return apiThread_obj.getDictionary()
